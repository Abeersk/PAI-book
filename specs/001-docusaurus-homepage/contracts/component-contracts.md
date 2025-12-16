# Component Interface Contracts: AI-Native Textbook – Custom Docusaurus Home Page

## HomepageHeader Component

### Props Interface
```typescript
interface HomepageHeaderProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  secondaryCtaText?: string;
  secondaryCtaLink?: string;
}
```

### Expected Behavior
- Renders a full-screen hero section with gradient background
- Displays title and subtitle with appropriate typography hierarchy
- Shows primary and optional secondary call-to-action buttons
- Responsive layout that adapts to different screen sizes
- Supports both light and dark themes

## HomepageFeatures Component

### Props Interface
```typescript
interface HomepageFeaturesProps {
  features: Array<{
    title: string;
    description: string;
    icon?: React.ReactNode;
    link?: string;
    ctaText?: string;
  }>;
}
```

### Expected Behavior
- Renders features in a responsive grid layout
- Displays icon, title, and description for each feature
- Shows optional CTA button with link
- Hover states with visual feedback
- Responsive layout that adapts from 1 column (mobile) to 3 columns (desktop)

## ChapterCards Component

### Props Interface
```typescript
interface ChapterCardsProps {
  chapters: Array<{
    title: string;
    description: string;
    chapterNumber: number;
    topics: string[];
    duration: string;
    link: string;
  }>;
}
```

### Expected Behavior
- Renders chapter cards in a responsive grid
- Displays chapter number, title, description, topics, and duration
- Hover states with visual feedback and elevation effect
- Clickable cards that navigate to chapter content
- Responsive layout adapting from 1 column (mobile) to 2-3 columns (desktop)

## Common Component Interfaces

### Theme Context
```typescript
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}
```

### Responsive Context
```typescript
interface ResponsiveContextType {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  currentBreakpoint: 'mobile' | 'tablet' | 'desktop';
}
```