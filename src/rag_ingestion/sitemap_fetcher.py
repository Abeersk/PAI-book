"""
Sitemap Fetcher Module

This module handles fetching and parsing sitemap.xml files from Docusaurus websites
to extract all content URLs for the RAG ingestion pipeline.
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

def fetch_sitemap(sitemap_url: str) -> List[str]:
    """
    Fetch and parse a sitemap.xml file to extract all valid content URLs.

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of content URLs extracted from the sitemap
    """
    try:
        logger.info(f"Fetching sitemap from: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()

        # Parse the XML content
        root = ET.fromstring(response.content)

        # Handle both regular sitemaps and sitemap indexes
        urls = []
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Check if this is a sitemap index (contains sitemap elements)
        sitemap_elements = root.findall('sitemap:sitemap', namespace)
        if sitemap_elements:
            # This is a sitemap index, need to fetch individual sitemaps
            for sitemap_elem in sitemap_elements:
                loc_elem = sitemap_elem.find('sitemap:loc', namespace)
                if loc_elem is not None:
                    individual_sitemap_url = loc_elem.text
                    urls.extend(fetch_individual_sitemap(individual_sitemap_url))
        else:
            # This is a regular sitemap with URL entries
            urls = extract_urls_from_sitemap(root, namespace)

        logger.info(f"Successfully extracted {len(urls)} URLs from sitemap")
        return urls

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching sitemap from {sitemap_url}: {str(e)}")
        raise
    except ET.ParseError as e:
        logger.error(f"Error parsing sitemap XML from {sitemap_url}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching sitemap from {sitemap_url}: {str(e)}")
        raise


def fetch_individual_sitemap(sitemap_url: str) -> List[str]:
    """
    Fetch and parse an individual sitemap (not a sitemap index).

    Args:
        sitemap_url: URL to the individual sitemap.xml file

    Returns:
        List of content URLs extracted from the sitemap
    """
    try:
        logger.info(f"Fetching individual sitemap from: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        urls = extract_urls_from_sitemap(root, namespace)
        logger.info(f"Successfully extracted {len(urls)} URLs from individual sitemap")
        return urls

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching individual sitemap from {sitemap_url}: {str(e)}")
        raise
    except ET.ParseError as e:
        logger.error(f"Error parsing individual sitemap XML from {sitemap_url}: {str(e)}")
        raise


def extract_urls_from_sitemap(root: ET.Element, namespace: Dict[str, str]) -> List[str]:
    """
    Extract URLs from a sitemap XML root element.

    Args:
        root: XML root element of the sitemap
        namespace: XML namespace mapping

    Returns:
        List of content URLs
    """
    urls = []

    # Find all URL elements in the sitemap
    url_elements = root.findall('sitemap:url', namespace)

    for url_elem in url_elements:
        loc_elem = url_elem.find('sitemap:loc', namespace)
        if loc_elem is not None:
            url = loc_elem.text.strip()
            # Filter out non-content URLs like homepage, index pages, etc.
            if is_valid_content_url(url):
                urls.append(url)

    return urls


def is_valid_content_url(url: str) -> bool:
    """
    Determine if a URL represents valid content for the RAG system.

    Args:
        url: URL to check

    Returns:
        True if the URL represents valid content, False otherwise
    """
    # Parse the URL to get components
    parsed = urlparse(url)

    # Exclude common non-content URLs
    path = parsed.path.lower()

    # Skip homepage/index URLs
    if path in ['/', '/index.html', '']:
        return False

    # Skip common non-content paths
    non_content_patterns = [
        '/tag/', '/category/', '/author/', '/feed', '/rss',
        '/sitemap', '/robots', '/api/', '/admin/', '/login'
    ]

    for pattern in non_content_patterns:
        if pattern in path:
            return False

    # Skip URLs that look like static assets
    static_extensions = ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.pdf']
    for ext in static_extensions:
        if url.lower().endswith(ext):
            return False

    # Otherwise, consider it valid content
    return True


def filter_urls_by_domain(urls: List[str], base_domain: str) -> List[str]:
    """
    Filter URLs to only include those from a specific domain.

    Args:
        urls: List of URLs to filter
        base_domain: Domain to filter by

    Returns:
        List of URLs that belong to the specified domain
    """
    filtered_urls = []
    for url in urls:
        parsed = urlparse(url)
        if base_domain in parsed.netloc:
            filtered_urls.append(url)

    return filtered_urls