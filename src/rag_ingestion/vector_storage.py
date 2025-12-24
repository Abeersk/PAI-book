"""
Vector Storage Module

This module handles storing vector embeddings in Qdrant Cloud with associated metadata
for the RAG system.
"""

import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class VectorStorage:
    def __init__(self,
                 url: str = None,
                 api_key: str = None,
                 collection_name: str = "book_embeddings"):
        """
        Initialize the VectorStorage.

        Args:
            url: Qdrant URL (if not provided, will try to read from environment)
            api_key: Qdrant API key (if not provided, will try to read from environment)
            collection_name: Name of the Qdrant collection to use
        """
        self.collection_name = collection_name
        self.url = url or os.getenv('QDRANT_URL')
        self.api_key = api_key or os.getenv('QDRANT_API_KEY')

        if not self.url:
            raise ValueError("Qdrant URL is required. Set QDRANT_URL environment variable.")
        if not self.api_key:
            raise ValueError("Qdrant API key is required. Set QDRANT_API_KEY environment variable.")

        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
            prefer_grpc=False  # Using REST API
        )

    def create_collection(self, vector_size: int, distance: str = "Cosine") -> bool:
        """
        Create a Qdrant collection for storing embeddings.

        Args:
            vector_size: Size of the embedding vectors
            distance: Distance metric to use (Cosine, Euclid, Dot)

        Returns:
            True if collection was created successfully
        """
        try:
            # Check if collection already exists
            try:
                existing_collection = self.client.get_collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
                return True
            except:
                # Collection doesn't exist, so we'll create it
                pass

            # Define distance metric
            distance_enum = {
                "Cosine": Distance.COSINE,
                "Euclid": Distance.EUCLID,
                "Dot": Distance.DOT
            }.get(distance, Distance.COSINE)

            # Create the collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance_enum),
            )

            logger.info(f"Created collection {self.collection_name} with {distance} distance metric")
            return True

        except Exception as e:
            logger.error(f"Error creating collection {self.collection_name}: {str(e)}")
            raise

    def store_embeddings(self,
                       embeddings_data: List[Dict[str, Any]],
                       batch_size: int = 10) -> bool:
        """
        Store embeddings with metadata in Qdrant.

        Args:
            embeddings_data: List of dictionaries containing embeddings and metadata
            batch_size: Number of points to store in each batch

        Returns:
            True if embeddings were stored successfully
        """
        if not embeddings_data:
            logger.warning("No embeddings to store")
            return True

        try:
            # Check if collection exists, if not create it
            vector_size = len(embeddings_data[0]['embedding'])
            self.create_collection(vector_size=vector_size)

            # Prepare points for insertion
            points = []
            for item in embeddings_data:
                # Generate a unique ID for each point
                point_id = str(uuid.uuid4())

                # Prepare payload with metadata
                payload = {
                    "source_url": item.get('url', ''),
                    "original_text": item.get('content', ''),
                    "document_title": item.get('title', ''),
                    "original_index": item.get('original_index', 0),
                    "chunk_index": item.get('chunk_index', 0),
                    "embedding_model": item.get('embedding_model', ''),
                    "created_at": item.get('created_at', ''),
                }

                # Remove empty values from payload
                payload = {k: v for k, v in payload.items() if v != "" and v is not None}

                # Create point
                point = PointStruct(
                    id=point_id,
                    vector=item['embedding'],
                    payload=payload
                )
                points.append(point)

            # Insert points in batches
            total_points = len(points)
            logger.info(f"Storing {total_points} embeddings in collection {self.collection_name}")

            for i in range(0, total_points, batch_size):
                batch = points[i:i + batch_size]

                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )

                logger.info(f"Stored batch {i//batch_size + 1}/{(total_points-1)//batch_size + 1}")

            logger.info(f"Successfully stored {total_points} embeddings in Qdrant")
            return True

        except Exception as e:
            logger.error(f"Error storing embeddings in Qdrant: {str(e)}")
            raise

    def search_similar(self,
                     query_embedding: List[float],
                     limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings in Qdrant.

        Args:
            query_embedding: The embedding to search for similar ones
            limit: Number of similar results to return

        Returns:
            List of similar embeddings with their metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            search_results = []
            for result in results:
                search_results.append({
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload,
                    'text': result.payload.get('original_text', ''),
                    'source_url': result.payload.get('source_url', ''),
                    'document_title': result.payload.get('document_title', '')
                })

            logger.info(f"Found {len(search_results)} similar embeddings")
            return search_results

        except Exception as e:
            logger.error(f"Error searching for similar embeddings: {str(e)}")
            raise

    def count_points(self) -> int:
        """
        Count the number of points in the collection.

        Returns:
            Number of points in the collection
        """
        try:
            count = self.client.count(
                collection_name=self.collection_name
            )
            return count.count
        except Exception as e:
            logger.error(f"Error counting points in collection: {str(e)}")
            raise

    def verify_storage(self) -> bool:
        """
        Verify that data was stored correctly by retrieving a sample.

        Returns:
            True if verification passes
        """
        try:
            count = self.count_points()
            logger.info(f"Collection contains {count} points")

            if count > 0:
                # Get a sample point to verify structure
                sample = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=1
                )
                if sample[0]:
                    logger.info("Sample point retrieved successfully, storage verified")
                    return True
                else:
                    logger.error("No points found despite count > 0")
                    return False
            else:
                logger.warning("Collection is empty")
                return True  # This might be expected if no data has been stored yet

        except Exception as e:
            logger.error(f"Error verifying storage: {str(e)}")
            return False


def store_embeddings_in_qdrant(embeddings_data: List[Dict[str, Any]],
                              url: str = None,
                              api_key: str = None,
                              collection_name: str = "book_embeddings",
                              batch_size: int = 10) -> bool:
    """
    Convenience function to store embeddings in Qdrant.

    Args:
        embeddings_data: List of dictionaries containing embeddings and metadata
        url: Qdrant URL (if not provided, will try to read from environment)
        api_key: Qdrant API key (if not provided, will try to read from environment)
        collection_name: Name of the Qdrant collection to use
        batch_size: Number of points to store in each batch

    Returns:
        True if embeddings were stored successfully
    """
    storage = VectorStorage(url=url, api_key=api_key, collection_name=collection_name)
    return storage.store_embeddings(embeddings_data, batch_size=batch_size)


def verify_qdrant_storage(url: str = None,
                         api_key: str = None,
                         collection_name: str = "book_embeddings") -> bool:
    """
    Verify that the Qdrant storage is working correctly.

    Args:
        url: Qdrant URL (if not provided, will try to read from environment)
        api_key: Qdrant API key (if not provided, will try to read from environment)
        collection_name: Name of the Qdrant collection to check

    Returns:
        True if verification passes
    """
    storage = VectorStorage(url=url, api_key=api_key, collection_name=collection_name)
    return storage.verify_storage()