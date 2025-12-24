"""
Text Chunker Module

This module handles chunking extracted text into semantically meaningful segments
for optimal embedding generation in the RAG system.
"""

import re
from typing import List, Dict, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200, min_chunk_size: int = 100):
        """
        Initialize the TextChunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
            min_chunk_size: Minimum size of a chunk to be included
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk_text(self, text: str, title: str = "") -> List[Dict[str, str]]:
        """
        Chunk the input text into semantically meaningful segments.

        Args:
            text: The text to be chunked
            title: Title of the document (for context in chunks)

        Returns:
            List of dictionaries containing chunk information
        """
        if not text or len(text.strip()) == 0:
            return []

        # Split text by semantic boundaries first (headings, paragraphs, sentences)
        semantic_chunks = self._split_by_semantic_boundaries(text)

        # Further process these chunks to ensure they fit within size limits
        final_chunks = []
        for i, chunk in enumerate(semantic_chunks):
            subchunks = self._chunk_by_size(chunk, title, i)
            final_chunks.extend(subchunks)

        logger.info(f"Split text into {len(final_chunks)} chunks")
        return final_chunks

    def _split_by_semantic_boundaries(self, text: str) -> List[str]:
        """
        Split text by semantic boundaries like headings, paragraphs, and sentences.

        Args:
            text: Text to split

        Returns:
            List of text segments split by semantic boundaries
        """
        # First, try to split by headings (common in documentation)
        heading_pattern = r'(?:^|\n)(#{1,6}\s+.*?)(?=\n#|\n$|\Z)'
        heading_splits = re.split(heading_pattern, text, flags=re.MULTILINE)

        # Combine headings with their content
        combined_parts = []
        i = 0
        while i < len(heading_splits):
            if i + 1 < len(heading_splits) and not heading_splits[i].startswith('#') and heading_splits[i].strip():
                # This is content after a heading
                combined_parts.append(heading_splits[i])
            elif i + 1 < len(heading_splits) and heading_splits[i].startswith('#'):
                # This is a heading, combine with next content part
                heading = heading_splits[i]
                content = heading_splits[i + 1] if i + 1 < len(heading_splits) else ""
                combined_parts.append(heading + "\n" + content)
                i += 1  # Skip the next one as it's already combined
            elif heading_splits[i].strip():
                # This is content without a heading
                combined_parts.append(heading_splits[i])
            i += 1

        # For each part, further split by paragraphs
        final_parts = []
        for part in combined_parts:
            if len(part) <= self.chunk_size:
                final_parts.append(part)
            else:
                # Split long parts by paragraphs
                paragraphs = [p.strip() for p in part.split('\n\n') if p.strip()]
                if len(paragraphs) > 1:
                    for para in paragraphs:
                        if len(para) <= self.chunk_size:
                            final_parts.append(para)
                        else:
                            # If paragraph is still too long, split by sentences
                            sentence_chunks = self._split_by_sentences(para)
                            final_parts.extend(sentence_chunks)
                else:
                    # If it's a single long paragraph, split by sentences
                    sentence_chunks = self._split_by_sentences(part)
                    final_parts.extend(sentence_chunks)

        return [part for part in final_parts if len(part.strip()) >= self.min_chunk_size]

    def _split_by_sentences(self, text: str) -> List[str]:
        """
        Split text by sentences if it's too long.

        Args:
            text: Text to split by sentences

        Returns:
            List of sentence-based chunks
        """
        # Use regex to split by sentence endings
        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, text)

        # Group sentences into chunks that don't exceed the size limit
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Check if adding this sentence would exceed the chunk size
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                # If the current chunk is substantial, add it
                if len(current_chunk.strip()) >= self.min_chunk_size:
                    chunks.append(current_chunk.strip())

                # If the sentence itself is longer than chunk_size, split it
                if len(sentence) > self.chunk_size:
                    # Split the long sentence into smaller pieces
                    subchunks = self._split_long_sentence(sentence)
                    chunks.extend(subchunks)
                else:
                    # Start a new chunk with the current sentence
                    current_chunk = sentence + " "

        # Add the last chunk if it's substantial
        if current_chunk.strip() and len(current_chunk.strip()) >= self.min_chunk_size:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is longer than the chunk size.

        Args:
            sentence: Long sentence to split

        Returns:
            List of chunks from the long sentence
        """
        chunks = []
        start = 0

        while start < len(sentence):
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a word boundary
            if end < len(sentence):
                # Look for the last space within the chunk to avoid breaking words
                while end > start and sentence[end] != ' ' and sentence[end-1] != ' ':
                    end -= 1

                # If we couldn't find a space, just break at the chunk size
                if end == start:
                    end = start + self.chunk_size

            chunk = sentence[start:end].strip()
            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)

            start = end
            # Skip spaces for the next iteration
            while start < len(sentence) and sentence[start] == ' ':
                start += 1

        return chunks

    def _chunk_by_size(self, text: str, title: str, original_index: int) -> List[Dict[str, str]]:
        """
        Further chunk text if it exceeds the maximum size, with overlap.

        Args:
            text: Text to chunk
            title: Title of the document
            original_index: Original index of this text segment

        Returns:
            List of chunk dictionaries with metadata
        """
        if len(text) <= self.chunk_size:
            return [{
                'content': text,
                'title': title,
                'original_index': original_index,
                'chunk_index': 0
            }]

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            # Determine the end position
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a word boundary
            if end < len(text):
                # Look for the last space within the chunk to avoid breaking words
                search_start = max(start, end - 200)  # Look at most 200 chars back
                break_pos = end
                for i in range(end, search_start, -1):
                    if text[i] == ' ':
                        break_pos = i
                        break

                end = break_pos

            # Extract the chunk
            chunk_content = text[start:end].strip()

            if len(chunk_content) >= self.min_chunk_size:
                chunks.append({
                    'content': chunk_content,
                    'title': title,
                    'original_index': original_index,
                    'chunk_index': chunk_index
                })
                chunk_index += 1

            # Move start position forward, accounting for overlap
            start = end - self.chunk_overlap if end < len(text) else end

            # Skip spaces at the beginning of the next chunk
            while start < len(text) and text[start] == ' ':
                start += 1

        return chunks


def chunk_document(text: str, title: str = "", chunk_size: int = 2000, chunk_overlap: int = 200) -> List[Dict[str, str]]:
    """
    Convenience function to chunk a document.

    Args:
        text: The text to be chunked
        title: Title of the document (for context in chunks)
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of overlapping characters between chunks

    Returns:
        List of dictionaries containing chunk information
    """
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunker.chunk_text(text, title)


def chunk_multiple_documents(documents: List[Dict[str, str]], chunk_size: int = 2000, chunk_overlap: int = 200) -> List[Dict[str, str]]:
    """
    Chunk multiple documents.

    Args:
        documents: List of documents (each with 'content' and 'title' keys)
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of overlapping characters between chunks

    Returns:
        List of chunk dictionaries from all documents
    """
    all_chunks = []

    for doc in documents:
        content = doc.get('content', '')
        title = doc.get('title', '')

        chunks = chunk_document(content, title, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)

    logger.info(f"Chunked {len(documents)} documents into {len(all_chunks)} total chunks")
    return all_chunks