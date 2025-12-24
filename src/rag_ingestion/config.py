"""
Configuration Module

This module handles configuration for the RAG ingestion pipeline,
loading settings from environment variables and providing default values.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """
    Configuration class for the RAG ingestion pipeline.
    """

    def __init__(self):
        # Load all configuration values
        self.load_config()

    def load_config(self):
        """Load configuration from environment variables with defaults."""
        # Book and sitemap settings
        self.BOOK_SITEMAP_URL = self._get_env_var(
            'BOOK_SITEMAP_URL',
            'https://your-book-site.com/sitemap.xml'
        )

        # Cohere settings
        self.COHERE_API_KEY = self._get_env_var('COHERE_API_KEY')
        self.COHERE_MODEL = self._get_env_var('COHERE_MODEL', 'embed-multilingual-v3.0')

        # Qdrant settings
        self.QDRANT_URL = self._get_env_var('QDRANT_URL')
        self.QDRANT_API_KEY = self._get_env_var('QDRANT_API_KEY')
        self.QDRANT_COLLECTION_NAME = self._get_env_var('QDRANT_COLLECTION_NAME', 'book_embeddings')

        # Processing settings
        self.CHUNK_SIZE = int(self._get_env_var('CHUNK_SIZE', '2000'))
        self.CHUNK_OVERLAP = int(self._get_env_var('CHUNK_OVERLAP', '200'))
        self.BATCH_SIZE = int(self._get_env_var('BATCH_SIZE', '10'))
        self.REQUEST_DELAY = float(self._get_env_var('REQUEST_DELAY', '1.0'))

        # Validation settings
        self.MIN_CHUNK_SIZE = int(self._get_env_var('MIN_CHUNK_SIZE', '100'))

        # Logging settings
        self.LOG_LEVEL = self._get_env_var('LOG_LEVEL', 'INFO')

        # Validation
        self._validate_config()

    def _get_env_var(self, key: str, default: Optional[str] = None) -> str:
        """
        Get environment variable with default fallback.

        Args:
            key: Environment variable key
            default: Default value if key is not found

        Returns:
            Environment variable value or default
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    def _validate_config(self):
        """Validate the loaded configuration."""
        errors = []

        # Validate required keys are set (skip validation for placeholder values during development)
        if not self.COHERE_API_KEY:
            errors.append("COHERE_API_KEY must be set to a valid API key")
        elif self.COHERE_API_KEY.startswith('your-') and self.COHERE_API_KEY.endswith('-here'):
            # Skip validation for placeholder values
            pass
        elif 'your-api-key' in self.COHERE_API_KEY:
            # Skip validation for placeholder values
            pass

        if not self.QDRANT_URL:
            errors.append("QDRANT_URL must be set to a valid Qdrant URL")
        elif self.QDRANT_URL.startswith('https://your-') and self.QDRANT_URL.endswith('-url'):
            # Skip validation for placeholder values
            pass
        elif 'your-qdrant-url' in self.QDRANT_URL:
            # Skip validation for placeholder values
            pass

        if not self.QDRANT_API_KEY:
            errors.append("QDRANT_API_KEY must be set to a valid API key")
        elif self.QDRANT_API_KEY.startswith('your-') and self.QDRANT_API_KEY.endswith('-here'):
            # Skip validation for placeholder values
            pass
        elif 'your-api-key' in self.QDRANT_API_KEY:
            # Skip validation for placeholder values
            pass

        if not self.BOOK_SITEMAP_URL:
            errors.append("BOOK_SITEMAP_URL must be set to a valid sitemap URL")
        elif self.BOOK_SITEMAP_URL.startswith('https://your-') and self.BOOK_SITEMAP_URL.endswith('-site.com'):
            # Skip validation for placeholder values
            pass
        elif 'your-book-site.com' in self.BOOK_SITEMAP_URL:
            # Skip validation for placeholder values
            pass

        # Validate numeric values
        if self.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE must be greater than 0")

        if self.CHUNK_OVERLAP < 0:
            errors.append("CHUNK_OVERLAP must be 0 or greater")

        if self.BATCH_SIZE <= 0:
            errors.append("BATCH_SIZE must be greater than 0")

        if self.REQUEST_DELAY < 0:
            errors.append("REQUEST_DELAY must be 0 or greater")

        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(errors))

    def get_cohere_config(self) -> dict:
        """Get configuration specifically for Cohere client."""
        return {
            'api_key': self.COHERE_API_KEY,
            'model': self.COHERE_MODEL
        }

    def get_qdrant_config(self) -> dict:
        """Get configuration specifically for Qdrant client."""
        return {
            'url': self.QDRANT_URL,
            'api_key': self.QDRANT_API_KEY,
            'collection_name': self.QDRANT_COLLECTION_NAME
        }

    def get_processing_config(self) -> dict:
        """Get configuration for processing settings."""
        return {
            'chunk_size': self.CHUNK_SIZE,
            'chunk_overlap': self.CHUNK_OVERLAP,
            'batch_size': self.BATCH_SIZE,
            'request_delay': self.REQUEST_DELAY,
            'min_chunk_size': self.MIN_CHUNK_SIZE
        }

    def get_book_config(self) -> dict:
        """Get configuration for book/sitemap settings."""
        return {
            'sitemap_url': self.BOOK_SITEMAP_URL
        }

    def get_logging_config(self) -> dict:
        """Get configuration for logging."""
        return {
            'level': self.LOG_LEVEL
        }


# Global configuration instance
config = Config()


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config instance
    """
    return config


def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.

    Returns:
        True if all required variables are set, False otherwise
    """
    try:
        config = Config()
        return True
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False


def print_config_summary():
    """Print a summary of the current configuration (without sensitive data)."""
    print("RAG Ingestion Pipeline Configuration:")
    print(f"  - Book Sitemap URL: {config.BOOK_SITEMAP_URL}")
    print(f"  - Cohere Model: {config.COHERE_MODEL}")
    print(f"  - Qdrant Collection: {config.QDRANT_COLLECTION_NAME}")
    print(f"  - Chunk Size: {config.CHUNK_SIZE}")
    print(f"  - Chunk Overlap: {config.CHUNK_OVERLAP}")
    print(f"  - Batch Size: {config.BATCH_SIZE}")
    print(f"  - Request Delay: {config.REQUEST_DELAY}s")
    print(f"  - Log Level: {config.LOG_LEVEL}")