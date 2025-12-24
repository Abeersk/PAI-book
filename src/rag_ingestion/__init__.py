"""
RAG Ingestion Package

This package contains modules for the RAG knowledge ingestion pipeline:
- sitemap_fetcher: Fetches and parses sitemap.xml files
- content_extractor: Extracts clean text from HTML pages
- text_chunker: Chunks text into semantically meaningful segments
- embedding_generator: Generates vector embeddings using Cohere
- vector_storage: Stores embeddings in Qdrant Cloud
- config: Configuration management
- main: Main pipeline orchestrator
"""