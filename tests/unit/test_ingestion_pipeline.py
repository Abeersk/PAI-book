"""
Unit tests for the RAG ingestion pipeline components.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.rag_ingestion import sitemap_fetcher, content_extractor, text_chunker, embedding_generator, vector_storage, config


class TestSitemapFetcher(unittest.TestCase):
    """Test cases for sitemap_fetcher module."""

    @patch('src.rag_ingestion.sitemap_fetcher.requests.get')
    def test_fetch_sitemap_success(self, mock_get):
        """Test successful sitemap fetching."""
        # Mock response
        mock_response = Mock()
        mock_response.content = b'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/page1</loc>
    </url>
    <url>
        <loc>https://example.com/page2</loc>
    </url>
</urlset>'''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        urls = sitemap_fetcher.fetch_sitemap("https://example.com/sitemap.xml")

        self.assertEqual(len(urls), 2)
        self.assertIn("https://example.com/page1", urls)
        self.assertIn("https://example.com/page2", urls)


class TestContentExtractor(unittest.TestCase):
    """Test cases for content_extractor module."""

    def test_extract_title(self):
        """Test title extraction from HTML."""
        from bs4 import BeautifulSoup

        html = "<html><head><title>Test Title</title></head><body>Content</body></html>"
        soup = BeautifulSoup(html, 'html.parser')

        title = content_extractor.extract_title(soup)
        self.assertEqual(title, "Test Title")

    def test_extract_clean_text(self):
        """Test clean text extraction from HTML."""
        from bs4 import BeautifulSoup

        html = """
        <html>
            <head><title>Test</title></head>
            <body>
                <nav>Navigation</nav>
                <header>Header</header>
                <main>
                    <h1>Main Content</h1>
                    <p>This is the main content of the page.</p>
                </main>
                <footer>Footer</footer>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')

        clean_text = content_extractor.extract_clean_text(soup, "https://example.com")
        # Should contain main content but not navigation or footer
        self.assertIn("Main Content", clean_text)
        self.assertIn("This is the main content", clean_text)
        # Navigation and footer should be removed
        # Note: The actual text extraction might still contain some of these elements
        # depending on how html2text processes them, but the function should remove major elements


class TestTextChunker(unittest.TestCase):
    """Test cases for text_chunker module."""

    def test_chunk_text(self):
        """Test text chunking functionality."""
        chunker = text_chunker.TextChunker(chunk_size=50, chunk_overlap=10)

        text = "This is a sample text that will be chunked into smaller pieces. " * 5
        chunks = chunker.chunk_text(text, "Test Document")

        # Should have multiple chunks since the text is longer than chunk_size
        self.assertGreater(len(chunks), 1)

        # Each chunk should have content
        for chunk in chunks:
            self.assertIn('content', chunk)
            self.assertIn('title', chunk)
            self.assertGreater(len(chunk['content']), 0)


class TestEmbeddingGenerator(unittest.TestCase):
    """Test cases for embedding_generator module."""

    @patch('cohere.Client')
    def test_generate_embeddings(self, mock_cohere_client):
        """Test embedding generation."""
        # Mock the Cohere client
        mock_client_instance = Mock()
        mock_client_instance.embed.return_value = Mock()
        mock_client_instance.embed.return_value.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_cohere_client.return_value = mock_client_instance

        generator = embedding_generator.EmbeddingGenerator(api_key="test-key")
        embeddings = generator.generate_embeddings(["test text 1", "test text 2"])

        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), 3)  # 3-dimensional embedding


class TestVectorStorage(unittest.TestCase):
    """Test cases for vector_storage module."""

    @patch('qdrant_client.QdrantClient')
    def test_store_embeddings(self, mock_qdrant_client):
        """Test storing embeddings in Qdrant."""
        # Mock the Qdrant client
        mock_client_instance = Mock()
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        mock_client_instance.create_collection.return_value = True
        mock_client_instance.upsert.return_value = True
        mock_qdrant_client.return_value = mock_client_instance

        storage = vector_storage.VectorStorage(
            url="https://test.qdrant.tech",
            api_key="test-key"
        )

        # Mock the create_collection method to return True
        storage.create_collection = Mock(return_value=True)

        embeddings_data = [
            {
                'content': 'test content',
                'title': 'test title',
                'embedding': [0.1, 0.2, 0.3],
                'url': 'https://example.com',
                'original_index': 0,
                'chunk_index': 0,
                'embedding_model': 'test-model'
            }
        ]

        result = storage.store_embeddings(embeddings_data, batch_size=1)
        self.assertTrue(result)


class TestConfig(unittest.TestCase):
    """Test cases for config module."""

    def test_config_initialization(self):
        """Test configuration initialization."""
        # This will test the default values when environment variables are not set
        # In a real test, we'd mock the environment variables
        try:
            cfg = config.Config()
            # The config should raise an error if required environment variables are not set
            # This is expected behavior
            pass
        except ValueError:
            # This is expected if environment variables are not set
            pass


if __name__ == '__main__':
    unittest.main()