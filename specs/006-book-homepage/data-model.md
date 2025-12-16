# Data Model: Physical AI & Humanoid Robotics Book – Attractive Home Page

## Entities

### Book
- **name**: string - "Physical AI & Humanoid Robotics"
- **description**: string - Educational content focused on physical AI and humanoid robotics concepts
- **modules**: array[Module] - Collection of 4 main modules

### Module
- **id**: string - Unique identifier (e.g., "module-1-ros2")
- **title**: string - Complete title with technology (e.g., "Module 1: The Robotic Nervous System (ROS 2)")
- **description**: string - Brief description of educational value
- **chapterHighlights**: array[ChapterHighlight] - 3-4 key chapters with visual elements
- **visualElements**: array[VisualElement] - Icons, diagrams, or illustrations

### ChapterHighlight
- **id**: string - Unique identifier
- **title**: string - Chapter title
- **description**: string - Brief description of chapter content
- **visualElement**: VisualElement - Associated icon or diagram

### VisualElement
- **type**: enum - "icon" | "diagram" | "illustration"
- **src**: string - Path to visual resource
- **altText**: string - Accessibility text
- **title**: string - Visual element title

### User
- **type**: enum - "student" | "educator" | "ai-enthusiast"
- **accessLevel**: enum - "public" (all educational content is publicly accessible)

## Relationships
- Book has many Modules (1:M)
- Module has many ChapterHighlights (1:M)
- ChapterHighlight has one VisualElement (1:1)
- Module has many VisualElements (1:M)

## Validation Rules
- Book must have exactly 4 modules
- Each module must have 3-4 chapter highlights
- Each chapter highlight must have a title (required, min length 5)
- Each module must have a title (required, min length 10)
- Visual elements must have alt text for accessibility
- Module descriptions must be between 20-100 characters

## State Transitions
N/A - Static educational content with no state changes required