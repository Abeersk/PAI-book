# Data Model: AI-Native Textbook – Custom Docusaurus Home Page

## Key Entities

### Homepage Layout
- **Description**: Represents the structural organization of content sections on the main page
- **Components**: Hero section, features section, content cards, navigation, footer
- **Relationships**: Contains multiple sections and components that make up the homepage

### Theme Configuration
- **Description**: Represents the settings and preferences for dark/light mode display
- **Attributes**:
  - themeMode: 'light' | 'dark'
  - colorPalette: Object containing color definitions
  - contrastRatio: Number (for accessibility compliance)
- **Validation**: Must meet WCAG-AA contrast requirements (≥ 4.5:1 for normal text)

### Responsive Breakpoints
- **Description**: Represents the screen size thresholds that trigger different layout adaptations
- **Attributes**:
  - mobile: 320px - 767px
  - tablet: 768px - 1023px
  - desktop: 1024px+
- **Validation**: Layout must adapt appropriately without horizontal scrolling in each range

## Component Data Structures

### Homepage Feature Card
- **title**: string (required)
- **description**: string (required)
- **icon**: React component or image path
- **link**: optional URL for more information
- **ctaText**: optional string for call-to-action

### Chapter Card
- **title**: string (required)
- **description**: string (required)
- **chapterNumber**: number (required)
- **topics**: array of strings
- **duration**: string (estimated reading time)
- **link**: URL to chapter content

### Technology Item
- **name**: string (required)
- **description**: string (required)
- **icon**: React component or image path
- **category**: string (e.g., 'framework', 'tool', 'platform')

## UI State Management

### Theme State
- **currentTheme**: 'light' | 'dark'
- **userPreference**: 'light' | 'dark' | 'system'
- **systemTheme**: 'light' | 'dark' (detected from OS)

### Responsive State
- **currentBreakpoint**: 'mobile' | 'tablet' | 'desktop'
- **isMobile**: boolean
- **isTablet**: boolean
- **isDesktop**: boolean