# Quickstart Guide: AI-Native Textbook – Custom Docusaurus Home Page

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm run start
   # or
   yarn start
   ```

4. **Open your browser**
   Visit `http://localhost:3000` to see the custom homepage in action.

## Key Files to Modify

- `src/pages/index.tsx` - Main homepage component
- `src/components/HomepageHeader/index.tsx` - Hero section component
- `src/components/HomepageFeatures/index.tsx` - Feature highlights component
- `src/css/custom.css` - Global styles and theme variables
- `src/theme/Root/index.tsx` - Theme context provider

## Customization Points

### Adding Content to Feature Cards
1. Open the `HomepageFeatures` component
2. Update the `features` array with your content
3. Each feature object should have `title`, `description`, and `icon` properties

### Theme Customization
1. Modify `src/css/custom.css` to update color variables
2. The theme automatically supports dark/light mode via CSS custom properties
3. Test both themes using the theme switcher in the navbar

### Responsive Design
1. Media queries are already implemented in CSS modules
2. Adjust breakpoints in `src/css/custom.css` if needed
3. Test responsiveness at different screen sizes (320px, 768px, 1024px, 1920px)

## Building for Production

```bash
npm run build
# or
yarn build
```

The built site will be available in the `build/` directory and can be deployed to any static hosting service.

## Development Workflow

1. Make changes to components in `src/components/`
2. Update styles in corresponding CSS module files
3. Test responsiveness and accessibility
4. Run `npm run serve` to test the production build locally