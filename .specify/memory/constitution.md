<!--
Sync Impact Report:
Version change: 0.1.0 -> 1.0.0 (initial project constitution)
Added sections: All core principles for AI/Spec-Driven Book on Physical AI & Humanoid Robotics
Removed sections: Template placeholders
Templates requiring updates: ✅ plan-template.md, spec-template.md, tasks-template.md
Follow-up TODOs: None
-->
# AI/Spec-Driven Book on Physical AI & Humanoid Robotics Constitution

## Core Principles

### Educational Focus and Conceptual Clarity
All content must prioritize conceptual understanding over implementation details. Technical concepts must be explained with simple flows, diagrams, and summaries. Content must emphasize understanding systems, architectures, and workflows rather than implementing complex robotics algorithms.
**Rationale**: The primary goal of the book is conceptual clarity and learning, not low-level robotics engineering. This ensures accessibility for learners with AI/software backgrounds.

### Accuracy and Verifiability
All technical concepts must align with official documentation and trusted sources. All factual claims must be verifiable. Prefer official docs, whitepapers, and well-known research references.
**Rationale**: Maintaining accuracy builds trust and ensures learners receive reliable information aligned with industry standards.

### No Complex Robotics Code
No complex robotics code, low-level controllers, kinematics math, or advanced motion planning implementations. Code samples (if any) must be minimal, educational, and pseudocode or simplified examples.
**Rationale**: The book must focus on conceptual understanding rather than implementation details. This aligns with the educational mission and avoids overwhelming readers with unnecessary complexity.

### Spec-Driven Development
All content follows structured specifications (Spec-Kit Plus). Every feature/module must have clear requirements and acceptance criteria defined before implementation.
**Rationale**: Ensures systematic development and maintains quality control throughout the project lifecycle.

### Reproducibility and Clarity
Examples must be easy to follow and conceptually reproducible. Written for learners and students with an AI/software background. Each concept explained with simple flow, diagrams, and summaries.
**Rationale**: Enables learners to understand and apply concepts without getting bogged down in implementation specifics.

### RAG Chatbot Integrity
The chatbot must answer questions strictly using book content. Must support Q&A based only on user-selected text. Must prevent hallucinations.
**Rationale**: Maintains the integrity of the educational content and ensures the chatbot serves as a reliable study aid.

## Technical Stack Constraints

**Framework**: Docusaurus for book framework, deployed on GitHub Pages
**Spec Framework**: Spec-Kit Plus for specification management
**Authoring Tool**: Claude Code for content creation
**Robotics Platforms**: ROS 2, Gazebo, Unity, NVIDIA Isaac (conceptual use only)
**AI Focus**: Vision-Language-Action (VLA) pipelines and reasoning systems
**Backend**: FastAPI for API services
**Database**: Neon Serverless Postgres for data storage
**Vector Database**: Qdrant Cloud (Free Tier) for RAG functionality
**Chatbot**: OpenAI Agents / ChatKit SDK for question-answering

## Book Structure Requirements

**Modular Organization**: Clean modular structure aligned with an educational curriculum
**Core Modules**:
1. The Robotic Nervous System (ROS 2) – concepts & architecture
2. The Digital Twin (Gazebo & Unity) – simulation principles
3. The AI-Robot Brain (NVIDIA Isaac) – perception & training concepts
4. Vision-Language-Action (VLA) – LLM-driven planning and reasoning
5. Capstone: Autonomous Humanoid – system-level walkthrough (conceptual)

## Governance

**Amendment Procedure**: Changes to core principles require explicit approval from project stakeholders and must be documented with rationale.
**Versioning Policy**: Follow semantic versioning - MAJOR for backward incompatible changes, MINOR for new principles/features, PATCH for clarifications.
**Compliance Reviews**: All content contributions must be reviewed for adherence to constitutional principles before acceptance.
**Quality Assurance**: Regular audits ensure ongoing compliance with educational focus and technical constraints.

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10
