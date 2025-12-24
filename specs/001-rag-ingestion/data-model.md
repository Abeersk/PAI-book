# Data Model: RAG Knowledge Ingestion Pipeline

## Entities

### ContentURL
- **id**: string (unique identifier)
- **url**: string (the URL to fetch content from)
- **status**: enum (pending, processing, completed, failed)
- **created_at**: datetime
- **updated_at**: datetime
- **error_message**: string (optional, for failed URLs)

### ExtractedText
- **id**: string (unique identifier)
- **content_url_id**: string (foreign key to ContentURL)
- **raw_html**: string (the original HTML content)
- **clean_text**: string (the extracted clean text)
- **title**: string (page title from HTML)
- **created_at**: datetime

### TextChunk
- **id**: string (unique identifier)
- **extracted_text_id**: string (foreign key to ExtractedText)
- **content**: string (the chunked text content)
- **chunk_index**: integer (position of chunk in original document)
- **created_at**: datetime

### VectorEmbedding
- **id**: string (unique identifier)
- **text_chunk_id**: string (foreign key to TextChunk)
- **vector**: array<float> (the embedding vector values)
- **embedding_model**: string (e.g., "cohere/embed-multilingual-v3.0")
- **created_at**: datetime

### Metadata
- **id**: string (unique identifier)
- **vector_embedding_id**: string (foreign key to VectorEmbedding)
- **source_url**: string (original URL of the content)
- **original_text**: string (the original text that was embedded)
- **document_title**: string (title of the original document)
- **chunk_index**: integer (position of the chunk in the original document)
- **created_at**: datetime

## Relationships
- ContentURL → ExtractedText (one-to-many)
- ExtractedText → TextChunk (one-to-many)
- TextChunk → VectorEmbedding (one-to-one)
- VectorEmbedding → Metadata (one-to-one)

## Validation Rules
- ContentURL.url must be a valid URL format
- ExtractedText.clean_text must not be empty when status is completed
- TextChunk.content must be within embedding service limits (typically < 4000 tokens)
- VectorEmbedding.vector must match the expected dimension for the configured Qdrant collection
- Metadata.source_url must match the original ContentURL

## State Transitions
- ContentURL: pending → processing → completed OR failed