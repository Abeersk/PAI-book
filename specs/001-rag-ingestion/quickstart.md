# Quickstart Guide: RAG Knowledge Ingestion Pipeline

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (for version control)
- Qdrant Cloud account with API key
- Cohere API key

## Setup

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd humanoid-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests beautifulsoup4 cohere qdrant-client lxml html2text pytest python-dotenv
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url
   BOOK_SITEMAP_URL=https://your-book-site.com/sitemap.xml
   ```

## Running the Ingestion Pipeline

1. **Execute the main pipeline script**
   ```bash
   python scripts/run_ingestion_pipeline.py
   ```

2. **Or run individual components for testing**
   ```bash
   # Test sitemap fetching
   python -c "from src.rag_ingestion.sitemap_fetcher import fetch_sitemap; print(fetch_sitemap())"

   # Test content extraction
   python -c "from src.rag_ingestion.content_extractor import extract_content; print(extract_content('https://example.com'))"
   ```

## Configuration

The pipeline can be configured via environment variables in the `.env` file:

- `BOOK_SITEMAP_URL`: URL to the sitemap.xml of the target book
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: URL to your Qdrant Cloud instance
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_COLLECTION_NAME`: Name of the collection to store vectors (default: "book_embeddings")
- `CHUNK_SIZE`: Maximum size of text chunks in characters (default: 2000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `BATCH_SIZE`: Number of items to process in each batch (default: 10)

## Verification

After running the pipeline, verify the results:

1. Check the Qdrant Cloud dashboard to confirm vectors were stored
2. Run test queries to verify retrieval functionality
3. Check logs for any errors or warnings during processing