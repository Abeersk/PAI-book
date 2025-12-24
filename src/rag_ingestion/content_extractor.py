"""
Content Extractor Module

This module handles downloading HTML pages and extracting clean text content
from Docusaurus book pages, removing navigation and other non-content elements.
"""

import requests
from bs4 import BeautifulSoup
import html2text
from typing import Dict, Optional, List
import logging
import time
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

def extract_content(url: str, delay: float = 1.0) -> Dict[str, str]:
    """
    Download HTML content from a URL and extract clean text content.

    Args:
        url: URL of the page to extract content from
        delay: Delay in seconds between requests to be respectful to the server

    Returns:
        Dictionary containing 'title' and 'content' keys
    """
    try:
        logger.info(f"Extracting content from: {url}")

        # Add delay to be respectful to the server
        time.sleep(delay)

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = extract_title(soup)

        # Extract clean text content
        content = extract_clean_text(soup, url)

        result = {
            'title': title,
            'content': content,
            'url': url
        }

        logger.info(f"Successfully extracted content from: {url}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content from {url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error extracting content from {url}: {str(e)}")
        raise


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the page title from the HTML soup.

    Args:
        soup: BeautifulSoup object of the HTML page

    Returns:
        The page title, or an empty string if not found
    """
    # Try to find title in various common locations
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()

    # Some sites might have h1 as the main title
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text().strip()

    return ""


def extract_clean_text(soup: BeautifulSoup, url: str) -> str:
    """
    Extract clean text content from HTML soup, removing navigation and non-content elements.

    Args:
        soup: BeautifulSoup object of the HTML page
        url: URL of the page (for context in case needed)

    Returns:
        Clean text content
    """
    # Remove common navigation and non-content elements
    for element in soup(['nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript']):
        element.decompose()

    # Remove elements with common class names for navigation, sidebars, etc.
    for element in soup.find_all(class_=['nav', 'navigation', 'sidebar', 'toc', 'table-of-contents',
                                        'menu', 'header', 'footer', 'advertisement', 'ad', 'cookie']):
        element.decompose()

    # For Docusaurus sites, remove common Docusaurus-specific elements
    for element in soup.find_all(class_=['navbar', 'theme-doc-sidebar', 'docSidebarContainer',
                                        'doc-page', 'pagination-nav', 'theme-last-updated']):
        element.decompose()

    # Convert to clean text using html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.body_width = 0  # Don't wrap lines

    clean_html = str(soup)
    clean_text = h.handle(clean_html)

    # Clean up extra whitespace
    clean_text = '\n'.join(line.strip() for line in clean_text.splitlines() if line.strip())

    return clean_text


def extract_content_batch(urls: List[str], delay: float = 1.0) -> List[Dict[str, str]]:
    """
    Extract content from a batch of URLs.

    Args:
        urls: List of URLs to extract content from
        delay: Delay in seconds between requests

    Returns:
        List of dictionaries containing 'title' and 'content' for each URL
    """
    results = []
    failed_urls = []

    for i, url in enumerate(urls):
        try:
            # Add a small delay between requests to be respectful to the server
            if i > 0:
                time.sleep(delay)

            content_data = extract_content(url, delay=0)  # No additional delay since we already delayed
            results.append(content_data)
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {str(e)}")
            failed_urls.append({'url': url, 'error': str(e)})

    if failed_urls:
        logger.warning(f"Failed to extract content from {len(failed_urls)} URLs: {failed_urls}")

    return results


def is_content_page(url: str, html_content: str) -> bool:
    """
    Determine if a page contains meaningful content for the RAG system.

    Args:
        url: URL of the page
        html_content: HTML content of the page

    Returns:
        True if the page contains meaningful content, False otherwise
    """
    # Check if the page has substantial content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get text content
    text_content = soup.get_text()

    # Remove extra whitespace
    clean_text = ' '.join(text_content.split())

    # If text is too short, it's likely not a content page
    if len(clean_text) < 50:
        return False

    # Check for common content indicators
    content_indicators = ['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'blockquote', 'pre', 'code']
    for indicator in content_indicators:
        if soup.find(indicator):
            return True

    return False