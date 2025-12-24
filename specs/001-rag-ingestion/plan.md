# Implementation Plan: RAG Knowledge Ingestion Pipeline

**Branch**: `001-rag-ingestion` | **Date**: 2025-12-24 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/001-rag-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an automated ingestion pipeline that extracts content from a deployed Docusaurus book, generates vector embeddings using Cohere Embed v3, and stores them in Qdrant Cloud for RAG chatbot usage. The pipeline will fetch content from sitemap.xml, extract meaningful text from HTML pages, chunk content semantically, generate embeddings, and store with metadata.

## Technical Context

**Language/Version**: Python 3.11 (for web scraping, text processing, and API integration)
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, lxml, html2text
**Storage**: Qdrant Cloud (vector database), local file system for temporary processing
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server environment (for running the ingestion pipeline)
**Project Type**: Single project (CLI-based ingestion pipeline)
**Performance Goals**: Process 1000+ pages within reasonable time, handle rate limiting gracefully
**Constraints**: <2GB memory usage during processing, handle API rate limits, comply with website terms of service
**Scale/Scope**: Process entire AI & Humanoid Robotics book content, handle 1000+ pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Alignment with Core Principles

✅ **Educational Focus and Conceptual Clarity**: The RAG ingestion pipeline supports educational goals by making book content accessible to learners through a chatbot interface. The pipeline focuses on content extraction and processing rather than complex robotics algorithms.

✅ **Accuracy and Verifiability**: The system will maintain content accuracy by directly extracting from the published Docusaurus book, preserving the original educational content for the RAG system.

✅ **No Complex Robotics Code**: The implementation involves web scraping, text processing, and vector database operations rather than complex robotics algorithms or low-level controllers.

✅ **Spec-Driven Development**: The feature follows structured specifications with clear requirements and acceptance criteria defined in the spec document.

✅ **Reproducibility and Clarity**: The pipeline will be designed to be conceptually clear and reproducible, with proper documentation for educational purposes.

✅ **RAG Chatbot Integrity**: The system ensures that chatbot responses are based strictly on book content by ingesting the complete knowledge base into the vector database.

### Technical Stack Compliance

✅ **Framework**: Uses Docusaurus (as specified in constitution) for the source book content
✅ **Vector Database**: Uses Qdrant Cloud (as specified in constitution) for RAG functionality
✅ **Backend**: Will integrate with FastAPI services as specified in the constitution

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── rag_ingestion/
│   ├── __init__.py
│   ├── sitemap_fetcher.py      # Fetch and parse sitemap.xml
│   ├── content_extractor.py    # Extract text from HTML pages
│   ├── text_chunker.py         # Chunk text into semantically meaningful segments
│   ├── embedding_generator.py  # Generate embeddings using Cohere
│   ├── vector_storage.py       # Store vectors in Qdrant Cloud
│   ├── config.py               # Configuration management
│   └── main.py                 # Main pipeline orchestration
├── tests/
│   ├── unit/
│   │   ├── test_sitemap_fetcher.py
│   │   ├── test_content_extractor.py
│   │   ├── test_text_chunker.py
│   │   ├── test_embedding_generator.py
│   │   └── test_vector_storage.py
│   └── integration/
│       └── test_ingestion_pipeline.py
└── scripts/
    └── run_ingestion_pipeline.py
```

**Structure Decision**: Single project structure selected as this is a CLI-based ingestion pipeline. The code is organized into modules that correspond to each step of the ingestion process: sitemap fetching, content extraction, text chunking, embedding generation, and vector storage. The tests are organized by unit and integration levels to ensure proper validation of each component and the overall pipeline.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
