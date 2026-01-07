# SEED.WEB STYLE GUIDE

**LLM-Optimized Frontend Style and Pattern Reference**

This document describes the styling patterns, best practices, and conventions used in the Seed.Web Next.js frontend application.

## Table of Contents

- [Technology Stack](#technology-stack)
- [Styling Architecture](#styling-architecture)
- [Color System](#color-system)
- [Typography System](#typography-system)
- [Spacing System](#spacing-system)
- [Component Structure Patterns](#component-structure-patterns)
- [Responsive Design Patterns](#responsive-design-patterns)
- [Layout Patterns](#layout-patterns)
- [Button Patterns](#button-patterns)
- [Image Handling](#image-handling)
- [Animation Patterns](#animation-patterns)
- [Accessibility Patterns](#accessibility-patterns)
- [Utility Classes](#utility-classes)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Common Tasks Decision Trees](#common-tasks-decision-trees)

---

## Technology Stack

### Core Technologies
- **Framework:** Next.js 15 with React 19
- **Styling:** SCSS Modules (component-scoped)
- **Grid System:** Foundation Sites XY Grid
- **UI Components:** Material-UI (MUI) v6
- **Animations:** GSAP, Framer Motion, react-spring
- **Icons:** Custom icon font (Krd) + MUI icons
- **Type System:** TypeScript 5.4+

### No Tailwind
This project **does not use Tailwind CSS**. All styling is done through:
- SCSS modules (`*.module.scss` files)
- Global SCSS files in `src/Seed.Web/styles/`
- Foundation Sites utility classes
- Custom utility classes defined in `util.scss`

---

## Styling Architecture

### File Organization Pattern

**Every component follows this structure:**

```
ComponentName/
├── componentName.tsx          # React component
├── componentName.module.scss  # Scoped styles
└── componentName.stories.tsx  # Storybook (optional)
```

**Example:**
```
ctaBasic/
├── ctaBasic.tsx
├── ctaBasic.module.scss
├── ctaBasic.test.tsx
└── ctaBasic.stories.tsx
```

### SCSS Module Pattern

**Standard module structure:**

```scss
// ALWAYS import variables and foundation at the top
@import "@styles/variables.scss";
@import "foundation-sites/scss/foundation.scss";

.componentName {
  // Component root styles
  padding: 56px 35px;
  position: relative;

  .childElement {
    // Nested child styles
    max-width: 700px;
    margin: 0 auto;
  }
}

// Responsive breakpoints AFTER base styles
@include breakpoint(medium down) {
  .componentName {
    padding: 20px 15px;
  }
}

@include breakpoint(large) {
  .componentName {
    padding: 80px 60px;
  }
}
```

### Import Pattern in TSX Files

```typescript
import styles from "./componentName.module.scss";
import variables from "@styles/variables.module.scss"; // For accessing SCSS variables in JS

export default function ComponentName() {
  return (
    <div className={styles.componentName}>
      {/* Content */}
    </div>
  );
}
```

### Global vs Module Styles

**Use SCSS Modules for:**
- Component-specific styles
- Block Grid blocks
- Common components
- Any scoped styling

**Use Global Styles for:**
- Typography (`typography.scss`)
- Utility classes (`util.scss`)
- Grid extensions (`grid.scss`)
- Buttons (`button.scss`)
- CSS variables (`variables.scss`)

---

## Color System

### Primary Colors (Current Palette)

Defined in `src/Seed.Web/styles/variables.scss`:

```scss
$white: #FFF;
$black: #000;
$blueDark: #003E52;    // Primary brand dark blue
$blue: #007299;        // Primary brand blue
$greyBlue: #E5EBEE;    // Light backgrounds
$greyHalf: #636B7480;  // 50% opacity grey for dividers
$grey: #D9D9D9;        // Border/divider grey
```

### Semantic Color Usage

```scss
// Text colors
$textColor: #2D2926;           // Primary body text
$darkTextColor: $white;        // Text on dark backgrounds

// Link colors
$linkColor: $blue;             // #007299
$linkHoverColor: $blueDark;    // #003E52
$linkActiveColor: $blue;       // #007299

// Button colors
$buttonColor: $black;
$buttonBackgroundColor: $white;
$buttonHoverColor: $white;
$buttonBackgroundHoverColor: $black;
$buttonActiveColor: $white;
$buttonBackgroundActiveColor: $blue;
```

### Using Colors in Components

**TypeScript approach (accessing from JS):**

```typescript
import variables from "@styles/variables.module.scss";
import isLowContrast from "common/util/isLowContrast";

const isDark = backgroundColor && isLowContrast(
  variables.textColor.substring(1),
  backgroundColor
);

return (
  <div className={isDark ? 'darkBackground' : ''}>
    {/* Content */}
  </div>
);
```

**SCSS approach:**

```scss
@import "@styles/variables.scss";

.component {
  color: $blueDark;
  background-color: $white;

  &:hover {
    color: $blue;
  }
}
```

### Dark Background Pattern

**Global class applied when content is on dark backgrounds:**

```scss
// In typography.scss
.darkBackground {
  color: $white;
  h1, h2, h3, h4, h5, h6, p {
    color: $white;
  }
}
```

**Usage:**

```typescript
<div className={styles.ctaBasic + (isDark ? ' darkBackground' : '')}>
  {/* All text automatically becomes white */}
</div>
```

---

## Typography System

### Font Stack

```scss
// Primary font (used throughout)
$districtProFont: "district-pro", sans-serif;
$defaultFont: $districtProFont;

// Icon font
$iconFont: Krd;  // Custom icon font
```

### Type Scale

**Mobile-first responsive typography:**

```scss
// Mobile (default)
body {
  font-family: $defaultFont;
  font-size: 18px;        // 1.125rem on medium+
  line-height: 28px;
  font-weight: 300;
}

h1 {
  font-size: 1.875rem;    // 30px mobile
  line-height: 2.5rem;    // 40px
  font-weight: 300;
  color: $blueDark;
}

h2 {
  font-size: 1.5rem;      // 24px mobile
  line-height: 2.125rem;  // 34px
  font-weight: 100;
  color: $blueDark;
}

h3 {
  font-size: 1.25rem;     // 20px mobile
  line-height: 1.875rem;  // 30px
  font-weight: 100;
  margin-bottom: 2.5rem;
}

h4 {
  font-size: 1.125rem;    // 18px
  line-height: 1.5rem;    // 24px
  font-weight: 300;
  color: $blueDark;
}

h5 {
  font-size: 0.875rem;    // 14px
  line-height: 1.5rem;    // 24px
  font-weight: 300;
}

h6 {
  font-size: 0.625rem;    // 10px
  line-height: 1rem;      // 16px
  text-transform: uppercase;
  letter-spacing: 2px;
  color: $blue;
}

// Desktop (medium breakpoint and up)
@include breakpoint(medium) {
  body {
    font-size: 1.125rem;  // 18px
    line-height: 1.75rem; // 28px
  }

  h1 {
    font-size: 3.125rem;  // 50px
    line-height: 3.75rem; // 60px
  }

  h2 {
    font-size: 2.5rem;    // 40px
    line-height: 3.125rem;// 50px
    margin-bottom: 1.5rem;
  }

  h3 {
    font-size: 1.875rem;  // 30px
    line-height: 2.5rem;  // 40px
  }

  h4 {
    font-size: 1.25rem;   // 20px → actually 24px per file
    line-height: 2.125rem;// 34px
  }

  h5 {
    font-size: 1.25rem;   // 20px
    line-height: 1.875rem;// 30px
  }

  h6 {
    font-size: 0.875rem;  // 14px
    line-height: 1.125rem;// 18px
  }
}
```

### Font Weight Utility Classes

```scss
.fontWeight100 { font-weight: 100; }
.fontWeight200 { font-weight: 200; }
.fontWeight300 { font-weight: 300; }
.fontWeight400 { font-weight: 400; }
.fontWeight500 { font-weight: 500; }
.fontWeight600 { font-weight: 600; }
.fontWeight700 { font-weight: 700; }
.fontWeight800 { font-weight: 800; }
.fontWeight900 { font-weight: 900; }
```

### Color Utility Classes

```scss
.blackText { color: $black; }
.darkBlueText { color: $blueDark; }
.blueText { color: $blue; }
.whiteText { color: $white; }
```

### Text Decoration Utilities

```scss
.underline {
  padding-bottom: .25em;
  border-bottom: 2px solid $greyHalf;
}

.whiteUnderline {
  width: 100%;
  &::after {
    content: '';
    display: block;
    width: 100%;
    height: 1px;
    background-color: $white;
    margin-top: 1em;
    margin-bottom: 1em;
  }
}

.blueUnderline {
  width: 100%;
  &::after {
    content: '';
    display: block;
    width: 100%;
    height: 1px;
    background-color: $blue;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
  }
}
```

### RTE (Rich Text Editor) Pattern

**Always use the `Rte` component for HTML content from Umbraco:**

```typescript
import Rte from "@components/rte/rte";

export default function Component({ content }: BlockGridItem) {
  const { text } = content as ComponentModel;

  return (
    <Rte
      text={text}
      className={styles.customClass}
    />
  );
}
```

**RTE component features:**
- Automatically converts local URLs to Next.js `<Link>`
- Handles images with proper lazy loading
- Supports modal triggers via `modal` attribute
- Supports quote builder triggers via `data-quotebuilder` attribute
- Wraps tables in scrollable containers

---

## Spacing System

### Spacing Variables

```scss
$margins: (
  0: 0rem,
  1: 1rem,      // 16px
  2: 2.5rem,    // 40px
  3: 7rem       // 112px
);

$paddings: (
  0: 0rem,
  1: 1rem,      // 16px
  2: 2.5rem,    // 40px
  3: 7rem       // 112px
);
```

### Header Heights

```scss
$mobileHeaderHeight: rem-calc(85);      // 85px
$desktopHeaderHeight: rem-calc(90);     // 90px
$desktopHeaderInitHeight: rem-calc(120);// 120px (initial state)
```

### Utility Classes for Spacing

**Margin utilities (generated for all sides):**

```scss
// Usage: .margin-{side}-{size}
.margin-top-0    { margin-top: 0rem; }
.margin-top-1    { margin-top: 1rem; }
.margin-top-2    { margin-top: 2.5rem; }
.margin-top-3    { margin-top: 7rem; }
// Same for right, bottom, left
```

**Responsive spacing utilities:**

```scss
// Usage: .{breakpoint}-margin-{side}-{size}
.medium-margin-top-2  { margin-top: 2.5rem; }
.large-padding-left-3 { padding-left: 7rem; }
```

### Common Spacing Patterns

**Centered content with max-width:**

```scss
.text {
  max-width: 700px;  // Common content width
  margin: 0 auto;    // Center horizontally
  text-align: center;
}
```

**Component padding:**

```scss
// Typical component padding pattern
.component {
  padding: 56px 35px;  // Desktop

  @include breakpoint(medium down) {
    padding: 20px 15px;  // Mobile
  }
}
```

**Gap spacing (Flexbox/Grid):**

```scss
.container {
  display: flex;
  gap: 93px;        // Desktop gap

  @include breakpoint(medium down) {
    gap: 30px;      // Mobile gap
  }
}
```

---

## Component Structure Patterns

### Standard Block Grid Component Pattern

**File: `common/components/blockGrid/blocks/componentName/componentName.tsx`**

```typescript
import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";
import styles from "./componentName.module.scss";
import Rte from "@components/rte/rte";
import ResponsiveImage from "@components/images/responsiveImage";
import { ImageModel } from "@lib/umbraco/types/imageModel.type";

// 1. Define the model interface
export type ComponentModel = {
  title: string;
  text: string;
  image: ImageModel;
  backgroundColor?: string;
};

// 2. Export the component
export default function ComponentName({ content }: BlockGridItem) {
  // 3. Destructure content with type assertion
  const { title, text, image, backgroundColor } = content as ComponentModel;

  // 4. Render with scoped styles
  return (
    <div
      className={styles.component}
      style={backgroundColor ? { backgroundColor: '#' + backgroundColor } : undefined}
    >
      <h2 className={styles.title}>{title}</h2>
      <Rte text={text} className={styles.text} />
      <ResponsiveImage
        image={image}
        sizes={[
          { size: 'small', crop: 'mobile' },
          { size: 'medium', crop: 'desktop' }
        ]}
      />
    </div>
  );
}
```

### Component Import Pattern

```typescript
// Path aliases (configured in tsconfig.json)
import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";
import { ImageModel } from "@lib/umbraco/types/imageModel.type";
import Rte from "@components/rte/rte";
import ResponsiveImage from "@components/images/responsiveImage";
import FlexibleLink from "@components/links/flexibleLink";
import variables from "@styles/variables.module.scss";

// Relative imports for local files
import styles from "./componentName.module.scss";
import SubComponent from "./subComponents/subComponent";
```

### Conditional Class Names Pattern

**Method 1: String concatenation (most common)**

```typescript
<div className={styles.ctaBasic + (isDark ? ' darkBackground' : '')}>
```

**Method 2: Ternary with different classes**

```typescript
<Rte
  text={text}
  className={contentSize == "Narrow" ? styles.textNarrow : "none"}
/>
```

**Method 3: Multiple conditions**

```typescript
const className = [
  styles.component,
  isDark && 'darkBackground',
  isActive && styles.active
].filter(Boolean).join(' ');

<div className={className}>
```

### Common Component Subfolders

```
componentName/
├── componentName.tsx
├── componentName.module.scss
├── componentName.stories.tsx
└── subComponents/           # For related helper components
    ├── subComponent.tsx
    └── subComponent.module.scss
```

**Example: feedProducts/**
```
feedProducts/
├── feedProducts.tsx
├── feedProducts.module.scss
└── subComponents/
    ├── gradientTile.tsx
    ├── imageBackgroundTile.tsx
    ├── outlineTile.tsx
    └── stackedTile.tsx
```

---

## Responsive Design Patterns

### Breakpoint System

**Foundation Sites breakpoints (from `variables.scss`):**

```scss
$breakpoints: (
  small: 0,           // 0px - 639px
  medium: 640px,      // 640px - 1023px
  large: 1024px,      // 1024px - 1199px
  xlarge: 1200px,     // 1200px - 1439px
  xxlarge: 1440px,    // 1440px - 1773px
  xxxlarge: 1774px    // 1774px+
);
```

**Available in TypeScript:**

```typescript
import variables from "@styles/variables.module.scss";

// Access breakpoint values
const mediumBreakpoint = parseInt(variables.breakpointMedium);  // 640
const largeBreakpoint = parseInt(variables.breakpointLarge);    // 1024
```

### Mobile-First Approach

**ALWAYS write mobile styles first, then use `@include breakpoint()` for larger screens:**

```scss
.component {
  // Mobile styles (default, 0-639px)
  padding: 20px 15px;
  font-size: 1rem;

  // Tablet and up (640px+)
  @include breakpoint(medium) {
    padding: 40px 30px;
    font-size: 1.125rem;
  }

  // Desktop and up (1024px+)
  @include breakpoint(large) {
    padding: 56px 35px;
    font-size: 1.25rem;
  }
}
```

### Breakpoint Direction Modifiers

```scss
// "up" is default (min-width)
@include breakpoint(medium) {
  // 640px and up
}

// "down" is max-width
@include breakpoint(medium down) {
  // 0px to 639px
}

// "only" is between breakpoints
@include breakpoint(medium only) {
  // 640px to 1023px only
}
```

### Common Responsive Patterns

**Pattern 1: Flex to Stack**

```scss
.container {
  display: flex;
  flex-direction: column;  // Mobile: stack vertically
  gap: 20px;

  @include breakpoint(large) {
    flex-direction: row;   // Desktop: horizontal
    gap: 93px;
  }
}
```

**Pattern 2: Width Adjustments**

```scss
.headerBox {
  width: 90%;              // Mobile: wider margins
  padding: 36px 23px;

  @include breakpoint(large down) {
    width: 81.77%;         // Tablet
  }

  @include breakpoint(large) {
    width: 56%;            // Desktop: narrower
    padding: 83px 8.27vw;
  }
}
```

**Pattern 3: Reordering**

```scss
.container {
  display: flex;
  flex-wrap: wrap;

  @include breakpoint(medium down) {
    .videoContainer {
      order: -1;           // Move video to top on mobile
    }
  }
}
```

**Pattern 4: Hide/Show**

```scss
.mobileOnly {
  display: block;

  @include breakpoint(large) {
    display: none;
  }
}

.desktopOnly {
  display: none;

  @include breakpoint(large) {
    display: block;
  }
}
```

**Pattern 5: Foundation Visibility Classes (use these)**

```html
<div className="show-for-small-only">Mobile only</div>
<div className="show-for-medium">Tablet and up</div>
<div className="show-for-large">Desktop and up</div>
<div className="hide-for-small-only">Hide on mobile</div>
```

### Max-Width Containers

```scss
// Global max-widths
$global-width: rem-calc(1594);        // 1594px (Foundation default)
$wideMaxWidth: rem-calc(1600);        // 1600px
$desktopMaxWidth: 1774px;

// Common component max-widths
.container {
  max-width: 1416px;  // Common content width
  margin: 0 auto;

  &.wide {
    max-width: rem-calc(1516);
  }
}
```

---

## Layout Patterns

### Foundation XY Grid Usage

**Basic grid structure:**

```jsx
<div className="grid-container">
  <div className="grid-x grid-margin-x">
    <div className="cell small-12 medium-6 large-4">
      {/* Column content */}
    </div>
    <div className="cell small-12 medium-6 large-4">
      {/* Column content */}
    </div>
  </div>
</div>
```

**Grid container variants:**

```jsx
// Standard width (1594px max)
<div className="grid-container">

// Wide width (1600px max)
<div className="grid-container wide">

// Full width
<div className="grid-container full">
```

### Grid Margins

```scss
$grid-margin-gutters: (
  small: 20px,   // Mobile gutter
  medium: 40px,  // Desktop gutter
);
```

### Custom Grid Extensions

**Wide gutters pattern:**

```scss
@include breakpoint(large) {
  .wideGutters {
    > .grid-container > .grid-x {
      margin: 0 -3rem;
      > .cell {
        margin-left: 3rem;
        margin-right: 3rem;
      }
    }
  }
}
```

### Standard Page Layout

```typescript
import Layout from "@components/layout/layout";
import { CommonData } from "@lib/umbraco/types/commonData.type";

export default function Page({ page, commonData }: {
  page: any;
  commonData: CommonData;
}) {
  return (
    <Layout
      page={page}
      commonData={commonData}
      hideNavigation={false}
    >
      {/* Page content */}
    </Layout>
  );
}
```

**Layout component structure:**

```
<Layout>
  <main id="content" className={styles.main}>
    <Header />          // Sticky header
    <div className={styles.content}>
      {children}        // Page content
    </div>
    <Footer />
  </main>
</Layout>
```

### Full Height Sections

```scss
.fullHeight {
  min-height: calc(100vh - #{$mobileHeaderHeight});

  @include breakpoint(large) {
    min-height: calc(100vh - #{$desktopHeaderHeight});
  }
}
```

### Scroll Margin for Anchors

**Global pattern (in `globals.scss`):**

```scss
[id] {
  scroll-margin-top: $mobileHeaderHeight;
}

@include breakpoint(xlarge) {
  [id] {
    scroll-margin-top: $desktopHeaderHeight;
  }
}
```

This ensures anchor links scroll to the correct position accounting for fixed header height.

---

## Button Patterns

### Button Types

**1. Standard Button (black background, white text)**

```jsx
<a href="/path" className="button">
  Click Me
</a>
```

```scss
.button {
  padding: 1.375rem 1.5rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  font-size: 1rem;
  line-height: .875rem;
  background-color: $black;
  color: $white;
  transition: .3s all;

  &:hover {
    color: $white;
    background-color: $black;
  }

  &:focus,
  &:active,
  &.active {
    color: $white;
    background-color: $blue;
  }
}
```

**2. Outline Button**

```jsx
<a href="/path" className="button buttonOutline">
  Click Me
</a>
```

```scss
.buttonOutline {
  border: 1px solid $black;
}
```

**3. Blue Button**

```jsx
<a href="/path" className="button buttonBlue">
  Click Me
</a>
```

```scss
.buttonBlue {
  background-color: $blueDark;
  color: $white;

  &:hover {
    background-color: $black;
  }
}
```

**4. Primary Button**

```jsx
<button className="primaryButton">
  Submit
</button>
```

```scss
.primaryButton {
  display: flex;
  min-height: 40px;
  padding: 4px 16px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  letter-spacing: 0.05em;
  font-weight: 300;
  background: $white;
  color: $black;
  border: none;
  cursor: pointer;
  transition: all 2s;

  &:hover {
    background: $black;
    color: $white;
  }

  &:focus {
    outline: 2px solid $blue;
    outline-offset: 2px;
    background: $blue;
    color: $white;
  }
}
```

**5. Footer Button (with icon)**

```jsx
<a href="/path" className="buttonFooter">
  Learn More
</a>
```

```scss
.buttonFooter {
  display: flex;
  width: 100%;
  align-items: center;
  border-top: 1px solid $greyHalf;
  color: $blueDark;
  font-size: 1.125rem;

  // Icon before (left side)
  &::before {
    content: '';
    width: 43px;
    border-right: 1px solid $greyHalf;
    min-height: 43px;
  }

  // Arrow icon after
  &::after {
    font-family: $iconFont;
    content: '\f00e';  // Arrow icon
    transform: translateX(15px);
    transition: .3s all;
  }

  &:hover::after {
    transform: translateX(13px);
  }
}
```

**6. Small Button Variant**

```jsx
<a href="/path" className="button smallButton">
  Click Me
</a>
```

```scss
.button.smallButton {
  font-size: .875rem;
  padding: 12px 15px;
}
```

### Button Modifiers

```scss
// Fixed width button
.button.buttonFixedWidth {
  width: 140px;
}

// Dark blue text variant
.button.darkBlueText {
  color: $blueDark;
}
```

### CTA Button Component

**Use the reusable `CtaButton` component:**

```typescript
import CtaButton from "@components/buttons/ctaButton";

<CtaButton
  text="<p>Click Here</p>"
  onClick={() => console.log('clicked')}
  className={styles.customClass}
/>
```

**Renders as:**

```jsx
<div className={styles.buttonContainer + (className || '')}>
  <Rte className={styles.button} text={text} />
  <ArrowRight />  {/* MUI icon */}
</div>
```

### FlexibleLink for Buttons

**Use `FlexibleLink` component for CMS-driven buttons:**

```typescript
import FlexibleLink from "@components/links/flexibleLink";
import { FlexibleLinkModel } from "@lib/umbraco/types/flexibleLinkModel.type";

const link: FlexibleLinkModel = {
  label: "Click Me",
  url: "/path",
  newTab: false,
  attributes: {}
};

<FlexibleLink link={link} className="button" />
```

**FlexibleLink features:**
- Automatically uses Next.js `<Link>` for internal links
- Handles external links with `target="_blank"`
- Supports modal triggers via `attributes.modalid`
- Supports quote builder triggers via `attributes.quotebuilder`

---

## Image Handling

### ResponsiveImage Component

**Primary component for all Umbraco images:**

```typescript
import ResponsiveImage from "@components/images/responsiveImage";
import { ImageModel } from "@lib/umbraco/types/imageModel.type";

export default function Component({ image }: { image: ImageModel }) {
  return (
    <ResponsiveImage
      image={image}
      sizes={[
        { size: 'small', crop: 'mobile' },
        { size: 'medium', crop: 'desktop' }
      ]}
      loading="lazy"
    />
  );
}
```

### ResponsiveImage Props

```typescript
type ResponsiveImageModel = {
  image: ImageModel;
  sizes: ResponsiveImageSize[];      // Required: breakpoint mappings
  asBackground?: boolean;             // Use as background image
  loading?: "eager" | "lazy";         // Default: "lazy"
  objectFit?: "contain" | "cover";    // Default: "cover"
  disableWebP?: boolean;              // Default: false
  className?: string;
  role?: string;
  'aria-label'?: string;
};

type ResponsiveImageSize = {
  size: "small" | "medium" | "large" | "xlarge" | "xxlarge" | number;
  crop: string | { width: number; height: number };
};
```

### Image Sizing Patterns

**Pattern 1: Named crops from Umbraco**

```typescript
<ResponsiveImage
  image={image}
  sizes={[
    { size: 'small', crop: 'tileMobile' },      // Named crop from UDA
    { size: 'medium', crop: 'tileDesktop' }     // Named crop from UDA
  ]}
/>
```

**Pattern 2: Custom dimensions**

```typescript
<ResponsiveImage
  image={image}
  sizes={[
    { size: 'large', crop: { width: 852, height: 479 } }
  ]}
/>
```

**Pattern 3: Multiple breakpoints**

```typescript
<ResponsiveImage
  image={image}
  sizes={[
    { size: 640, crop: 'mobile' },
    { size: 1024, crop: 'tablet' },
    { size: 1440, crop: 'desktop' }
  ]}
/>
```

### Background Images

```typescript
<ResponsiveImage
  image={background}
  asBackground={true}
  sizes={[
    { size: 'small', crop: 'mobile' },
    { size: 'medium', crop: 'desktop' }
  ]}
  className={styles.bgImage}
/>
```

**Generates:**

```html
<picture class="asBackground bgImage">
  <source media="(min-width: 1024px)" srcset="..." />
  <source media="(min-width: 640px)" srcset="..." />
  <img loading="lazy" src="..." alt="..." />
</picture>
```

**SCSS for background images:**

```scss
@import "@styles/variables.scss";

.asBackground {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
```

### Object-Fit Options

```typescript
// Cover (default): fills container, may crop
<ResponsiveImage
  image={image}
  sizes={...}
  objectFit="cover"
/>

// Contain: fits entire image, may letterbox
<ResponsiveImage
  image={image}
  sizes={...}
  objectFit="contain"
/>
```

### Loading Priority

```typescript
// Above fold images: eager loading
<ResponsiveImage
  image={heroImage}
  sizes={...}
  loading="eager"
/>

// Below fold images: lazy loading (default)
<ResponsiveImage
  image={contentImage}
  sizes={...}
  loading="lazy"
/>
```

### Accessibility for Images

```typescript
<ResponsiveImage
  image={background}
  asBackground={true}
  sizes={...}
  role="img"
  aria-label={background.name || "Banner image"}
/>
```

---

## Animation Patterns

### Accessibility: Reduced Motion

**ALWAYS respect `prefers-reduced-motion`:**

```typescript
const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

useEffect(() => {
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  setPrefersReducedMotion(mediaQuery.matches);

  const handleChange = (e: MediaQueryListEvent) => {
    setPrefersReducedMotion(e.matches);
  };

  mediaQuery.addEventListener('change', handleChange);
  return () => mediaQuery.removeEventListener('change', handleChange);
}, []);

// Then conditionally apply animations
useEffect(() => {
  if (prefersReducedMotion) return;

  // Animation code here
}, [prefersReducedMotion]);
```

**SCSS fallback:**

```scss
@media (prefers-reduced-motion: reduce) {
  .parallaxBg {
    transform: none !important;
    transition: none !important;
  }

  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Parallax Scroll Pattern

**Optimized with `requestAnimationFrame`:**

```typescript
const parallaxRef = useRef<HTMLDivElement | null>(null);
const rafId = useRef<number | undefined>(undefined);

useEffect(() => {
  if (prefersReducedMotion) return;

  const handleScroll = () => {
    if (rafId.current) {
      cancelAnimationFrame(rafId.current);
    }

    rafId.current = requestAnimationFrame(() => {
      const scrolled = window.scrollY;

      if (parallaxRef.current) {
        const rect = parallaxRef.current.getBoundingClientRect();
        const inView = rect.top < window.innerHeight && rect.bottom > 0;

        if (inView) {
          const speedFactor = 0.3;
          const parallaxOffset = scrolled * speedFactor;
          parallaxRef.current.style.transform = `translateY(${parallaxOffset}px)`;
        }
      }
    });
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  return () => {
    window.removeEventListener('scroll', handleScroll);
    if (rafId.current) {
      cancelAnimationFrame(rafId.current);
    }
  };
}, [prefersReducedMotion]);
```

**SCSS for parallax elements:**

```scss
.parallaxBg {
  position: absolute;
  width: 100%;
  height: 100%;
  transform: translateZ(0);       // Force GPU acceleration
  will-change: transform;         // Optimize for transform changes
  transition: transform 0.1s linear;
}
```

### Smooth Scroll

**Global smooth scrolling (in `globals.scss`):**

```scss
@media (prefers-reduced-motion: no-preference) {
  html,
  body {
    scroll-behavior: smooth;
  }
}
```

### Transition Pattern

```scss
.component {
  transition: .3s all;  // Common: 300ms all properties

  &:hover {
    // Hover state
  }
}

// Specific properties
.button {
  transition:
    background-color .3s ease,
    color .3s ease,
    transform .3s ease;
}
```

### GSAP Usage

**Project includes GSAP for complex animations:**

```typescript
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

export default function Component() {
  useGSAP(() => {
    gsap.from(".animate-in", {
      opacity: 0,
      y: 50,
      duration: 1,
      stagger: 0.2
    });
  });

  return <div className="animate-in">Content</div>;
}
```

### Framer Motion Usage

**Project includes Framer Motion:**

```typescript
import { motion } from "framer-motion";

export default function Component() {
  return (
    <motion.div
      initial={{ opacity: 0, x: -100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 100 }}
      transition={{ duration: 0.6 }}
    >
      Content
    </motion.div>
  );
}
```

---

## Accessibility Patterns

### Semantic HTML

**ALWAYS use semantic elements:**

```jsx
// Good
<section role="banner" aria-label="Product catalog banner">
  <h1>Title</h1>
  <nav aria-label="Main navigation">...</nav>
  <article>...</article>
  <footer>...</footer>
</section>

// Bad
<div className="banner">
  <div className="title">Title</div>
  <div className="nav">...</div>
  <div className="article">...</div>
  <div className="footer">...</div>
</div>
```

### Focus Management

**Visible focus states:**

```scss
.component {
  &:focus-visible {
    outline: 2px solid $blue;  // #007299
    outline-offset: 2px;
  }
}

// Remove default outline, add custom
a, button {
  &:focus {
    outline: none;
  }

  &:focus-visible {
    outline: 2px solid $blue;
    outline-offset: 2px;
  }
}
```

### High Contrast Mode

**Support Windows High Contrast Mode:**

```scss
@media (forced-colors: active) {
  .component {
    background-color: Canvas;
    border: 1px solid CanvasText;

    h1, p {
      color: CanvasText;
    }
  }
}
```

### ARIA Labels

**Meaningful labels for screen readers:**

```jsx
<section
  role="contentinfo"
  aria-label="Product catalog introduction"
>
  <div
    className={styles.headerBox}
    tabIndex={0}
    role="region"
    aria-label="Product catalog header"
  >
    {/* Content */}
  </div>
</section>
```

### Icon Accessibility

**Always provide text alternatives:**

```jsx
// Custom icon font
<i className="bmg-icon bmg-icon-arrow-right" aria-hidden="true"></i>
<span className="visually-hidden">Next</span>

// MUI icons
<ArrowRight aria-hidden="true" />
<span className="visually-hidden">Next</span>
```

### Skip to Content

**Include skip links (in Layout):**

```jsx
<a href="#content" className="skip-to-content">
  Skip to main content
</a>
<main id="content">
  {/* Content */}
</main>
```

```scss
.skip-to-content {
  position: absolute;
  left: -9999px;
  top: 0;

  &:focus {
    left: 0;
    z-index: 9999;
    padding: 1rem;
    background: $white;
    color: $black;
  }
}
```

---

## Utility Classes

### Margin and Padding Utilities

**Generated utilities (from `util.scss`):**

```scss
// Margins
.margin-top-0 { margin-top: 0rem; }
.margin-top-1 { margin-top: 1rem; }
.margin-top-2 { margin-top: 2.5rem; }
.margin-top-3 { margin-top: 7rem; }
// Same for: margin-right-*, margin-bottom-*, margin-left-*

// Responsive margins
.medium-margin-top-2 { margin-top: 2.5rem; }  // @media (min-width: 640px)
.large-padding-left-3 { padding-left: 7rem; }  // @media (min-width: 1024px)

// No margin
.noMargin { margin: 0; }
```

### Full Height Utility

```scss
.fullHeight {
  min-height: calc(100vh - #{$mobileHeaderHeight});

  @include breakpoint(large) {
    min-height: calc(100vh - #{$desktopHeaderHeight});
  }
}
```

### Print Utilities

```scss
@media print {
  .hideForPrint {
    display: none !important;
  }
}
```

### Foundation Visibility Classes

**Use Foundation's built-in classes:**

```html
<!-- Show/hide by breakpoint -->
<div className="show-for-small-only">Mobile only (0-639px)</div>
<div className="show-for-medium">Tablet and up (640px+)</div>
<div className="show-for-medium-only">Tablet only (640-1023px)</div>
<div className="show-for-large">Desktop and up (1024px+)</div>
<div className="show-for-large-only">Desktop only (1024-1199px)</div>

<!-- Hide at breakpoints -->
<div className="hide-for-small-only">Hidden on mobile</div>
<div className="hide-for-medium">Hidden on tablet and up</div>
<div className="hide-for-large">Hidden on desktop and up</div>
```

### Global Utility Classes

**From `globals.scss`:**

```scss
// Fill parent (absolute positioning)
.fill {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

// RTE last child no margin
.rte *:last-child {
  margin-bottom: 0;
}

// Push content down for header
.pushDownContent {
  @include breakpoint(xlarge) {
    padding-top: #{$desktopHeaderInitHeight + 2rem};
  }
}
```

---

## Anti-Patterns to Avoid

### 1. Don't Use Inline Styles for Static Values

**Bad:**

```typescript
<div style={{ padding: "56px 35px", color: "#003E52" }}>
```

**Good:**

```typescript
// In SCSS module
.component {
  padding: 56px 35px;
  color: $blueDark;
}

// In TSX
<div className={styles.component}>
```

**Exception: Dynamic values are fine:**

```typescript
<div style={backgroundColor ? { backgroundColor: '#' + backgroundColor } : undefined}>
```

### 2. Don't Mix px and rem Inconsistently

**Bad:**

```scss
.component {
  padding: 20px;          // px
  margin: 1rem;           // rem
  font-size: 16px;        // px
}
```

**Good:**

```scss
.component {
  padding: 20px;          // Consistent px for spacing
  margin: 20px;
  font-size: 1rem;        // rem for typography
}

// Or use rem consistently
.component {
  padding: 1.25rem;
  margin: 1.25rem;
  font-size: 1rem;
}
```

### 3. Don't Ignore Mobile Styles

**Bad:**

```scss
.component {
  @include breakpoint(large) {
    padding: 80px 60px;
  }
  // No mobile styles!
}
```

**Good:**

```scss
.component {
  padding: 20px 15px;  // Mobile first

  @include breakpoint(large) {
    padding: 80px 60px;
  }
}
```

### 4. Don't Hardcode Colors

**Bad:**

```scss
.component {
  color: #003E52;
  background-color: #FFF;
}
```

**Good:**

```scss
@import "@styles/variables.scss";

.component {
  color: $blueDark;
  background-color: $white;
}
```

### 5. Don't Use !important Unless Necessary

**Bad:**

```scss
.component {
  color: $blue !important;
  padding: 20px !important;
}
```

**Good:**

```scss
.component {
  color: $blue;
  padding: 20px;
}

// Only use !important for overrides or utilities
.forceHide {
  display: none !important;  // Acceptable for utility class
}
```

### 6. Don't Nest Selectors Too Deeply

**Bad:**

```scss
.component {
  .container {
    .wrapper {
      .item {
        .title {
          color: $blue;  // 5 levels deep!
        }
      }
    }
  }
}
```

**Good:**

```scss
.component {
  .title {
    color: $blue;
  }
}
```

### 7. Don't Forget Accessibility

**Bad:**

```jsx
<div onClick={handleClick}>
  Click me
</div>
```

**Good:**

```jsx
<button onClick={handleClick} aria-label="Submit form">
  Click me
</button>
```

### 8. Don't Use Raw HTML Strings

**Bad:**

```typescript
<div dangerouslySetInnerHTML={{ __html: content }} />
```

**Good:**

```typescript
import Rte from "@components/rte/rte";

<Rte text={content} />
```

### 9. Don't Skip Type Definitions

**Bad:**

```typescript
export default function Component({ content }) {  // No types
  const { title, text } = content;
```

**Good:**

```typescript
import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";

export type ComponentModel = {
  title: string;
  text: string;
};

export default function Component({ content }: BlockGridItem) {
  const { title, text } = content as ComponentModel;
```

### 10. Don't Forget Responsive Images

**Bad:**

```jsx
<img src={image.url} alt={image.name} />
```

**Good:**

```typescript
<ResponsiveImage
  image={image}
  sizes={[
    { size: 'small', crop: 'mobile' },
    { size: 'medium', crop: 'desktop' }
  ]}
  loading="lazy"
/>
```

---

## Common Tasks Decision Trees

### When to Create a New Component?

```
Is this content reused in multiple places?
├─ YES → Create in common/components/
├─ NO → Is it a Block Grid block?
    ├─ YES → Create in common/components/blockGrid/blocks/
    └─ NO → Is it a helper for a specific component?
        ├─ YES → Create in that component's subComponents/
        └─ NO → Inline the JSX in the parent component
```

### What Breakpoint Should I Use?

```
What device should this change apply to?
├─ Mobile only (0-639px) → Don't use breakpoint, write base styles
├─ Tablet and up (640px+) → @include breakpoint(medium)
├─ Desktop and up (1024px+) → @include breakpoint(large)
├─ Large desktop (1200px+) → @include breakpoint(xlarge)
├─ Max-width mobile (0-639px) → @include breakpoint(small down)
└─ Between tablet and desktop → @include breakpoint(medium only)
```

### How Should I Handle This Image?

```
Where is the image coming from?
├─ Umbraco (ImageModel) → Use ResponsiveImage component
│   ├─ Has named crops in UDA? → Use crop: 'cropName'
│   └─ Custom size? → Use crop: { width: X, height: Y }
├─ Static asset (public/) → Use Next.js <Image> component
└─ External URL → Use regular <img> tag
```

### What Color Variable Should I Use?

```
What type of element am I styling?
├─ Primary brand element → $blueDark (#003E52)
├─ Interactive element (link, button) → $blue (#007299)
├─ Background → $white or $greyBlue
├─ Text on light background → $textColor (#2D2926) or $blueDark
├─ Text on dark background → $white
├─ Border/divider → $grey or $greyHalf
└─ Pure black/white → $black / $white
```

### Should I Use a Utility Class or Custom SCSS?

```
Is this a one-off style specific to this component?
├─ YES → Use SCSS module
│   .component {
│     margin-top: 2.5rem;
│   }
└─ NO → Is it spacing that might change at breakpoints?
    ├─ YES → Use utility class
    │   <div className="medium-margin-top-2">
    └─ NO → Is it a common pattern (colors, typography)?
        ├─ YES → Use global utility class
        │   <div className="darkBlueText">
        └─ NO → Use SCSS module
```

### How Should I Handle Responsive Layout?

```
What needs to change at different screen sizes?
├─ Layout direction (stack vs row)
│   → display: flex + flex-direction + @include breakpoint
├─ Number of columns
│   → Foundation grid classes (small-12 medium-6 large-4)
├─ Element order
│   → flex + order property + @include breakpoint
├─ Show/hide elements
│   → Foundation visibility classes (show-for-*, hide-for-*)
├─ Spacing values
│   → Define mobile base + @include breakpoint for larger
└─ Element sizes (width, height, font-size)
    → Define mobile base + @include breakpoint for larger
```

### What Animation Library Should I Use?

```
What type of animation do I need?
├─ Simple transitions (color, opacity, transform)
│   → CSS transitions in SCSS
├─ Scroll-based effects (parallax, fade-in on scroll)
│   → requestAnimationFrame + useEffect (see patterns above)
├─ Complex sequenced animations
│   → GSAP with useGSAP hook
├─ Page transitions, simple component animations
│   → Framer Motion
└─ Carousel/slider
    → Swiper library (already installed)

⚠️ ALWAYS check for prefers-reduced-motion!
```

### Should I Create a TypeScript Type or Interface?

```
What am I defining?
├─ Component props from Umbraco
│   → type ComponentModel = { ... }
│   → Export it for reuse
├─ Component props (React)
│   → type ComponentProps = { ... }
│   → Use with function Component({ }: ComponentProps)
├─ Reusable Umbraco data structure
│   → Already exists in @lib/umbraco/types/
│   → Import: ImageModel, UmbracoNode, FlexibleLinkModel, etc.
└─ Should extend BlockGridItem?
    → NO, use: content as ComponentModel inside function
```

---

## Quick Reference

### Import Paths (tsconfig.json aliases)

```typescript
// Types
import BlockGridItem from "@lib/umbraco/types/blockGridItem.type";
import { ImageModel } from "@lib/umbraco/types/imageModel.type";
import { UmbracoNode } from "@lib/umbraco/types/umbracoNode.type";
import { FlexibleLinkModel } from "@lib/umbraco/types/flexibleLinkModel.type";
import { VideoModel } from "@lib/umbraco/types/videoModel.type";
import { CommonData } from "@lib/umbraco/types/commonData.type";

// Components
import Rte from "@components/rte/rte";
import ResponsiveImage from "@components/images/responsiveImage";
import FlexibleLink from "@components/links/flexibleLink";
import Layout from "@components/layout/layout";

// Styles
import styles from "./component.module.scss";
import variables from "@styles/variables.module.scss";

// Utils
import isLowContrast from "common/util/isLowContrast";
import { getCropUrl } from "@lib/umbraco/util/helpers";
```

### Foundation Grid Classes

```html
<!-- Container -->
<div className="grid-container">
<div className="grid-container wide">
<div className="grid-container full">

<!-- Row -->
<div className="grid-x">
<div className="grid-x grid-margin-x">

<!-- Columns -->
<div className="cell small-12">                      <!-- 100% on all -->
<div className="cell small-12 medium-6">             <!-- 100%, then 50% -->
<div className="cell small-12 medium-6 large-4">     <!-- 100%, 50%, 33.33% -->

<!-- Offsets -->
<div className="cell small-12 large-offset-2 large-8">
```

### Common SCSS Patterns

```scss
// Import block (top of every .module.scss)
@import "@styles/variables.scss";
@import "foundation-sites/scss/foundation.scss";

// Breakpoints
@include breakpoint(medium) { }      // 640px+
@include breakpoint(large) { }       // 1024px+
@include breakpoint(medium down) { } // 0-639px
@include breakpoint(medium only) { } // 640-1023px

// Nesting
.parent {
  .child { }
  &:hover { }
  &.modifier { }
  &::before { }
}

// Variables
color: $blueDark;
padding: map-get($paddings, 2);  // 2.5rem
```

### Color Variables Quick Reference

```scss
$white: #FFF
$black: #000
$blueDark: #003E52
$blue: #007299
$greyBlue: #E5EBEE
$greyHalf: #636B7480
$grey: #D9D9D9
$textColor: #2D2926
```

### Spacing Variables Quick Reference

```scss
$margins: (0: 0rem, 1: 1rem, 2: 2.5rem, 3: 7rem)
$paddings: (0: 0rem, 1: 1rem, 2: 2.5rem, 3: 7rem)
$mobileHeaderHeight: 85px
$desktopHeaderHeight: 90px
```

### Breakpoint Values Quick Reference

```scss
small: 0px
medium: 640px
large: 1024px
xlarge: 1200px
xxlarge: 1440px
xxxlarge: 1774px
```

---

## File Locations Reference

```
src/Seed.Web/
├── styles/
│   ├── globals.scss         # Global styles, box-sizing, smooth scroll
│   ├── variables.scss       # Colors, fonts, spacing, breakpoints
│   ├── typography.scss      # Headings, body, text utilities
│   ├── button.scss          # Button styles
│   ├── grid.scss            # Grid extensions
│   ├── util.scss            # Utility classes (margins, padding, etc.)
│   └── variables.module.scss# SCSS variables accessible in TypeScript
├── common/
│   ├── components/
│   │   ├── blockGrid/blocks/  # Block Grid components
│   │   ├── buttons/           # Button components
│   │   ├── images/            # Image components (ResponsiveImage)
│   │   ├── links/             # Link components (FlexibleLink)
│   │   ├── rte/               # RTE component
│   │   ├── layout/            # Layout component
│   │   ├── header/            # Header component
│   │   └── footer/            # Footer component
│   ├── types/                 # Shared TypeScript types
│   └── util/                  # Utility functions
├── lib/
│   └── umbraco/
│       ├── types/             # Umbraco TypeScript types
│       └── util/              # Umbraco utility functions
├── modules/                   # Feature modules
└── app/                       # Next.js app router
    └── [[...slug]]/           # Dynamic catch-all route
```

---

## End of Style Guide

**Last Updated:** 2026-01-06

**For questions or additions to this guide, consult:**
- Existing component implementations in `common/components/blockGrid/blocks/`
- Global styles in `src/Seed.Web/styles/`
- Foundation Sites documentation: https://get.foundation/sites/docs/
- Next.js documentation: https://nextjs.org/docs
