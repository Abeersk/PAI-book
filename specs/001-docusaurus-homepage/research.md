# Research: AI-Native Textbook – Custom Docusaurus Home Page

## Decision: Component Architecture
**Rationale**: Based on the requirements, a modular component architecture is chosen to ensure reusability, maintainability, and clear separation of concerns. Each section of the homepage (hero, features, content cards, etc.) will be implemented as independent components.

**Alternatives considered**:
- Single monolithic component: Would be harder to maintain and test
- Pre-built Docusaurus templates: Would not meet the requirement for a fully custom implementation

## Decision: Styling Strategy
**Rationale**: CSS Modules combined with global theme variables will provide scoped styling with the flexibility to implement dark/light mode. This approach aligns with Docusaurus conventions while allowing for the custom design requirements.

**Alternatives considered**:
- Styled-components: Would add unnecessary complexity for a static site
- Pure CSS: Would lack scoping and theme management capabilities
- Tailwind CSS: Would conflict with Docusaurus styling conventions

## Decision: Responsive Design Approach
**Rationale**: Mobile-first responsive design using CSS media queries will ensure optimal experience across all device sizes. This follows modern web development best practices and meets the requirement for responsive design.

**Alternatives considered**:
- Separate mobile app: Not needed for a documentation site
- Fixed-width layouts: Would not meet responsive requirements

## Decision: Theme Management
**Rationale**: Using Docusaurus's built-in theme switching capability combined with CSS custom properties will provide seamless dark/light mode switching while maintaining consistency with the framework.

**Alternatives considered**:
- Custom theme switching: Would require more implementation work
- Third-party theme libraries: Would add unnecessary dependencies

## Decision: Accessibility Implementation
**Rationale**: Following WCAG-AA guidelines with semantic HTML, proper ARIA attributes, and keyboard navigation will ensure the homepage is accessible to all users, including those with disabilities.

**Alternatives considered**:
- Minimal accessibility: Would not meet the requirement for WCAG-AA compliance
- Over-engineered accessibility: Would add unnecessary complexity

## Research Findings Summary

1. **Modern Landing Page Patterns**: Research shows successful educational SaaS sites use hero sections with clear CTAs, feature highlights with interactive elements, and clean visual hierarchies - all requirements in the spec.

2. **Docusaurus Customization**: Docusaurus allows complete homepage replacement through src/pages/index.tsx while maintaining other site functionality.

3. **Theme Integration**: Docusaurus supports data-theme attribute for dark/light mode, which can be leveraged with CSS custom properties.

4. **Performance Optimization**: Static site generation with Docusaurus provides excellent performance out of the box, meeting the 3-second load requirement.

5. **Accessibility Best Practices**: Semantic HTML, proper heading structure, ARIA labels, and keyboard navigation are essential for WCAG-AA compliance.