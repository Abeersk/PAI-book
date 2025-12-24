"""
Main Pipeline Orchestrator

This module orchestrates the entire RAG ingestion pipeline:
1. Fetch sitemap
2. Extract content from URLs
3. Chunk the content
4. Generate embeddings
5. Store in Qdrant
"""

import logging
from typing import List, Dict, Any
import time
from . import sitemap_fetcher
from . import content_extractor
from . import text_chunker
from . import embedding_generator
from . import vector_storage
from . import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_ingestion_pipeline(sitemap_url: str = None) -> bool:
    """
    Run the complete RAG ingestion pipeline.

    Args:
        sitemap_url: URL to the sitemap.xml (if None, uses configured default)

    Returns:
        True if the pipeline completed successfully, False otherwise
    """
    start_time = time.time()
    logger.info("Starting RAG ingestion pipeline")

    try:
        # Get configuration
        cfg = config.get_config()
        target_sitemap_url = sitemap_url or cfg.BOOK_SITEMAP_URL

        # 1. Fetch sitemap
        logger.info("Step 1: Fetching sitemap...")
        urls = sitemap_fetcher.fetch_sitemap(target_sitemap_url)
        logger.info(f"Found {len(urls)} URLs in sitemap")

        # 2. Extract content from URLs
        logger.info("Step 2: Extracting content from URLs...")
        contents = content_extractor.extract_content_batch(
            urls,
            delay=cfg.REQUEST_DELAY
        )
        logger.info(f"Extracted content from {len(contents)} pages")

        # 3. Chunk the content
        logger.info("Step 3: Chunking content...")
        chunks = text_chunker.chunk_multiple_documents(
            contents,
            chunk_size=cfg.CHUNK_SIZE,
            chunk_overlap=cfg.CHUNK_OVERLAP
        )
        logger.info(f"Created {len(chunks)} text chunks")

        # 4. Generate embeddings
        logger.info("Step 4: Generating embeddings...")
        embedding_data = embedding_generator.generate_embeddings_for_chunks(
            chunks,
            api_key=cfg.COHERE_API_KEY,
            model=cfg.COHERE_MODEL
        )
        logger.info(f"Generated embeddings for {len(embedding_data)} chunks")

        # 5. Store in Qdrant
        logger.info("Step 5: Storing embeddings in Qdrant...")
        vector_storage.store_embeddings_in_qdrant(
            embedding_data,
            url=cfg.QDRANT_URL,
            api_key=cfg.QDRANT_API_KEY,
            collection_name=cfg.QDRANT_COLLECTION_NAME,
            batch_size=cfg.BATCH_SIZE
        )
        logger.info("Successfully stored embeddings in Qdrant")

        # Verification
        logger.info("Verifying storage...")
        if vector_storage.verify_qdrant_storage(
            url=cfg.QDRANT_URL,
            api_key=cfg.QDRANT_API_KEY,
            collection_name=cfg.QDRANT_COLLECTION_NAME
        ):
            logger.info("Storage verification passed")
        else:
            logger.warning("Storage verification failed")

        total_time = time.time() - start_time
        logger.info(f"Pipeline completed successfully in {total_time:.2f} seconds")
        logger.info(f"Processed {len(urls)} URLs, {len(contents)} pages, {len(chunks)} chunks")

        return True

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        logger.exception("Full traceback:")
        return False


def run_partial_pipeline(
    sitemap_url: str = None,
    process_sitemap: bool = True,
    process_content: bool = True,
    process_chunking: bool = True,
    process_embeddings: bool = True,
    process_storage: bool = True
) -> Dict[str, Any]:
    """
    Run a partial pipeline with configurable steps.

    Args:
        sitemap_url: URL to the sitemap.xml (if None, uses configured default)
        process_sitemap: Whether to process sitemap fetching
        process_content: Whether to process content extraction
        process_chunking: Whether to process text chunking
        process_embeddings: Whether to process embedding generation
        process_storage: Whether to process storage

    Returns:
        Dictionary with results from each processed step
    """
    results = {}
    start_time = time.time()

    try:
        # Get configuration
        cfg = config.get_config()
        target_sitemap_url = sitemap_url or cfg.BOOK_SITEMAP_URL

        # Step 1: Fetch sitemap
        if process_sitemap:
            logger.info("Step 1: Fetching sitemap...")
            urls = sitemap_fetcher.fetch_sitemap(target_sitemap_url)
            results['urls'] = urls
            logger.info(f"Found {len(urls)} URLs in sitemap")

        # Step 2: Extract content
        if process_content:
            urls = results.get('urls', [])
            if not urls:
                raise ValueError("No URLs found. Run sitemap step first or provide URLs.")

            logger.info("Step 2: Extracting content from URLs...")
            contents = content_extractor.extract_content_batch(
                urls,
                delay=cfg.REQUEST_DELAY
            )
            results['contents'] = contents
            logger.info(f"Extracted content from {len(contents)} pages")

        # Step 3: Chunk content
        if process_chunking:
            contents = results.get('contents', [])
            if not contents:
                raise ValueError("No content found. Run content extraction step first.")

            logger.info("Step 3: Chunking content...")
            chunks = text_chunker.chunk_multiple_documents(
                contents,
                chunk_size=cfg.CHUNK_SIZE,
                chunk_overlap=cfg.CHUNK_OVERLAP
            )
            results['chunks'] = chunks
            logger.info(f"Created {len(chunks)} text chunks")

        # Step 4: Generate embeddings
        if process_embeddings:
            chunks = results.get('chunks', [])
            if not chunks:
                raise ValueError("No chunks found. Run chunking step first.")

            logger.info("Step 4: Generating embeddings...")
            embedding_data = embedding_generator.generate_embeddings_for_chunks(
                chunks,
                api_key=cfg.COHERE_API_KEY,
                model=cfg.COHERE_MODEL
            )
            results['embedding_data'] = embedding_data
            logger.info(f"Generated embeddings for {len(embedding_data)} chunks")

        # Step 5: Store in Qdrant
        if process_storage:
            embedding_data = results.get('embedding_data', [])
            if not embedding_data:
                raise ValueError("No embedding data found. Run embedding generation step first.")

            logger.info("Step 5: Storing embeddings in Qdrant...")
            success = vector_storage.store_embeddings_in_qdrant(
                embedding_data,
                url=cfg.QDRANT_URL,
                api_key=cfg.QDRANT_API_KEY,
                collection_name=cfg.QDRANT_COLLECTION_NAME,
                batch_size=cfg.BATCH_SIZE
            )
            results['storage_success'] = success
            logger.info("Successfully stored embeddings in Qdrant")

        total_time = time.time() - start_time
        logger.info(f"Partial pipeline completed in {total_time:.2f} seconds")

        return results

    except Exception as e:
        logger.error(f"Partial pipeline failed with error: {str(e)}")
        logger.exception("Full traceback:")
        return results


def verify_pipeline() -> bool:
    """
    Verify that all components of the pipeline are properly configured.

    Returns:
        True if all components are properly configured, False otherwise
    """
    logger.info("Verifying pipeline configuration...")

    try:
        # Test configuration
        cfg = config.get_config()
        logger.info("✓ Configuration loaded successfully")

        # Test Qdrant connection
        if vector_storage.verify_qdrant_storage(
            url=cfg.QDRANT_URL,
            api_key=cfg.QDRANT_API_KEY,
            collection_name=cfg.QDRANT_COLLECTION_NAME
        ):
            logger.info("✓ Qdrant connection verified")
        else:
            logger.error("✗ Qdrant connection failed")
            return False

        # Test Cohere connection by generating a simple embedding
        test_text = "This is a test for Cohere API connection."
        try:
            test_embedding = embedding_generator.generate_single_embedding(
                test_text,
                api_key=cfg.COHERE_API_KEY,
                model=cfg.COHERE_MODEL
            )
            if test_embedding and 'embedding' in test_embedding:
                logger.info("✓ Cohere API connection verified")
            else:
                logger.error("✗ Cohere API connection failed")
                return False
        except Exception as e:
            logger.error(f"✗ Cohere API connection failed: {str(e)}")
            return False

        logger.info("All pipeline components verified successfully")
        return True

    except Exception as e:
        logger.error(f"Pipeline verification failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Print configuration summary
    config.print_config_summary()

    # Verify pipeline configuration
    if not verify_pipeline():
        logger.error("Pipeline verification failed. Please check your configuration.")
        exit(1)

    # Run the complete pipeline
    success = run_ingestion_pipeline()

    if success:
        logger.info("Pipeline completed successfully!")
        exit(0)
    else:
        logger.error("Pipeline failed!")
        exit(1)