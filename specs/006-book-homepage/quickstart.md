# Quickstart: Physical AI & Humanoid Robotics Book – Attractive Home Page

## Setup

1. **Prerequisites**
   - Node.js 18+
   - npm or yarn
   - Git

2. **Installation**
   ```bash
   # Clone the repository
   git clone [repository-url]
   cd [repository-name]

   # Install dependencies
   npm install
   ```

3. **Local Development**
   ```bash
   # Start development server
   npm start

   # The site will be available at http://localhost:3000
   ```

## Project Structure

```
docs/
├── index.md                 # Home page with hero section and modules
├── module-*/                # Module directories
│   ├── index.md            # Module overview pages
│   └── chapter-*.md        # Individual chapter pages
├── src/
│   ├── components/         # React components
│   │   ├── HomepageHero.jsx
│   │   ├── ModuleCard.jsx
│   │   ├── ChapterHighlight.jsx
│   │   └── CTASection.jsx
│   └── css/
│       └── custom.css      # Custom styling
└── static/
    └── img/                # Images and diagrams
```

## Key Features

### 1. Homepage Hero Section
- Attractive design with compelling tagline
- Background illustration relevant to robotics
- Primary CTA button linking to full content

### 2. Module Cards
- Interactive cards for 4 main modules
- Icons and visual elements for each module
- Brief descriptions with educational focus
- Links to module overview pages

### 3. Chapter Highlights
- 3-4 key chapters per module
- Visual elements (icons/diagrams) for each chapter
- Concise descriptions focusing on concepts

### 4. Call-to-Action Sections
- Clear links to full book content
- Prominent positioning for easy navigation
- Supporting CTAs for RAG chatbot

## Customization

### Adding New Modules
1. Create new module directory in `docs/`
2. Add `index.md` with module overview
3. Add chapter files as needed
4. Update sidebar configuration

### Adding Visual Elements
1. Place images in `static/img/`
2. Reference in markdown files or React components
3. Ensure accessibility with proper alt text
4. Optimize for fast loading

## Building for Production

```bash
# Build static files
npm run build

# Serve built files locally
npm run serve
```

## Testing

```bash
# Verify build works correctly
npm run build
```

## Deployment

The site is designed for GitHub Pages deployment:
1. Push to main branch
2. Configure GitHub Pages to use `/docs` folder
3. Site will be available at `[username].github.io/[repository-name]`