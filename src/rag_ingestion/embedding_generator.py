"""
Embedding Generator Module

This module handles generating vector embeddings using Cohere Embed v3
for text chunks in the RAG system.
"""

import cohere
from typing import List, Dict, Any
import logging
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self, api_key: str = None, model: str = "embed-multilingual-v3.0"):
        """
        Initialize the EmbeddingGenerator.

        Args:
            api_key: Cohere API key (if not provided, will try to read from environment)
            model: Cohere embedding model to use
        """
        self.model = model
        self.api_key = api_key or os.getenv('COHERE_API_KEY')

        if not self.api_key:
            raise ValueError("Cohere API key is required. Set COHERE_API_KEY environment variable.")

        self.client = cohere.Client(self.api_key)

    def generate_embeddings(self, texts: List[str], request_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            texts: List of text chunks to generate embeddings for
            request_type: Type of request (search_document, search_query, classification, etc.)

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        if not texts:
            return []

        try:
            logger.info(f"Generating embeddings for {len(texts)} text chunks using model: {self.model}")

            # Cohere API has limits on the number of texts per request
            # Process in batches to avoid hitting limits
            batch_size = 96  # Cohere's typical limit is 100, using 96 to be safe
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                response = self.client.embed(
                    texts=batch,
                    model=self.model,
                    input_type=request_type
                )

                batch_embeddings = [embedding for embedding in response.embeddings]
                all_embeddings.extend(batch_embeddings)

                logger.info(f"Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

                # Add a small delay to respect rate limits
                time.sleep(0.1)

            logger.info(f"Successfully generated {len(all_embeddings)} embeddings")
            return all_embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def generate_embedding(self, text: str, request_type: str = "search_document") -> List[float]:
        """
        Generate a single embedding for a text chunk.

        Args:
            text: Text to generate embedding for
            request_type: Type of request (search_document, search_query, classification, etc.)

        Returns:
            Embedding as a list of floats
        """
        embeddings = self.generate_embeddings([text], request_type)
        return embeddings[0] if embeddings else []


def generate_embeddings_for_chunks(chunks: List[Dict[str, str]],
                                 api_key: str = None,
                                 model: str = "embed-multilingual-v3.0") -> List[Dict[str, Any]]:
    """
    Generate embeddings for a list of text chunks with metadata.

    Args:
        chunks: List of chunk dictionaries (with 'content', 'title', etc.)
        api_key: Cohere API key (if not provided, will try to read from environment)
        model: Cohere embedding model to use

    Returns:
        List of dictionaries containing chunks with their embeddings
    """
    if not chunks:
        return []

    # Extract just the content for embedding generation
    texts = [chunk['content'] for chunk in chunks]

    generator = EmbeddingGenerator(api_key=api_key, model=model)
    embeddings = generator.generate_embeddings(texts)

    # Combine the chunks with their embeddings
    result = []
    for i, chunk in enumerate(chunks):
        chunk_with_embedding = chunk.copy()
        chunk_with_embedding['embedding'] = embeddings[i]
        chunk_with_embedding['embedding_model'] = model
        result.append(chunk_with_embedding)

    logger.info(f"Attached embeddings to {len(result)} chunks")
    return result


def generate_single_embedding(text: str,
                            title: str = "",
                            api_key: str = None,
                            model: str = "embed-multilingual-v3.0") -> Dict[str, Any]:
    """
    Generate a single embedding with metadata.

    Args:
        text: Text to generate embedding for
        title: Title of the document
        api_key: Cohere API key (if not provided, will try to read from environment)
        model: Cohere embedding model to use

    Returns:
        Dictionary containing the text, metadata, and embedding
    """
    generator = EmbeddingGenerator(api_key=api_key, model=model)
    embedding = generator.generate_embedding(text)

    return {
        'content': text,
        'title': title,
        'embedding': embedding,
        'embedding_model': model
    }


def validate_embedding_dimensions(embeddings: List[List[float]], expected_dimension: int = None) -> bool:
    """
    Validate that all embeddings have the expected dimension.

    Args:
        embeddings: List of embeddings to validate
        expected_dimension: Expected dimension for embeddings (if None, check consistency)

    Returns:
        True if all embeddings have the expected/correct dimensions
    """
    if not embeddings:
        return True

    dimension = len(embeddings[0])

    if expected_dimension and dimension != expected_dimension:
        logger.error(f"Embedding dimension mismatch: expected {expected_dimension}, got {dimension}")
        return False

    # Check that all embeddings have the same dimension
    for i, emb in enumerate(embeddings):
        if len(emb) != dimension:
            logger.error(f"Embedding {i} has inconsistent dimension: {len(emb)}, expected: {dimension}")
            return False

    logger.info(f"All embeddings have consistent dimension: {dimension}")
    return True