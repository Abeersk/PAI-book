#!/usr/bin/env python3
"""
Script to run the RAG ingestion pipeline.

This script provides a command-line interface to run the complete RAG ingestion pipeline
with optional parameters for customization.
"""

import argparse
import sys
import os
import logging

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.rag_ingestion.main import run_ingestion_pipeline, run_partial_pipeline, verify_pipeline
from src.rag_ingestion.config import print_config_summary


def main():
    parser = argparse.ArgumentParser(description='RAG Knowledge Ingestion Pipeline')
    parser.add_argument(
        '--sitemap-url',
        type=str,
        help='URL to the sitemap.xml (overrides config)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify the pipeline configuration without running ingestion'
    )
    parser.add_argument(
        '--partial',
        action='store_true',
        help='Run partial pipeline with step selection'
    )
    parser.add_argument(
        '--no-sitemap',
        action='store_true',
        help='Skip sitemap fetching step'
    )
    parser.add_argument(
        '--no-content',
        action='store_true',
        help='Skip content extraction step'
    )
    parser.add_argument(
        '--no-chunking',
        action='store_true',
        help='Skip text chunking step'
    )
    parser.add_argument(
        '--no-embeddings',
        action='store_true',
        help='Skip embedding generation step'
    )
    parser.add_argument(
        '--no-storage',
        action='store_true',
        help='Skip storage step'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    logger.info("RAG Ingestion Pipeline Starting...")

    # Print configuration summary
    print_config_summary()
    print()  # Empty line for readability

    # Verify pipeline configuration
    if not verify_pipeline():
        logger.error("Pipeline verification failed. Please check your configuration.")
        sys.exit(1)

    if args.verify_only:
        logger.info("Verification completed successfully!")
        sys.exit(0)

    # Determine which steps to run
    if args.partial:
        # Run partial pipeline with selected steps
        results = run_partial_pipeline(
            sitemap_url=args.sitemap_url,
            process_sitemap=not args.no_sitemap,
            process_content=not args.no_content,
            process_chunking=not args.no_chunking,
            process_embeddings=not args.no_embeddings,
            process_storage=not args.no_storage
        )
        logger.info("Partial pipeline completed.")
    else:
        # Run complete pipeline
        success = run_ingestion_pipeline(sitemap_url=args.sitemap_url)

        if success:
            logger.info("Pipeline completed successfully!")
            sys.exit(0)
        else:
            logger.error("Pipeline failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()