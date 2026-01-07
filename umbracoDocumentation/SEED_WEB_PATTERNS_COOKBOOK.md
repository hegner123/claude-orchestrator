# SEED.WEB PATTERNS COOKBOOK

**Practical "How Do I..." Guide with Real Component Examples**

This cookbook answers common styling questions with real, copy-paste examples from the Seed.Web codebase.

## LLM Optimization Features

This document is optimized for LLM consumption with:
- **Pattern Tags** - Searchable keywords for quick pattern matching
- **Usage Guidance** - "When to use" and "When NOT to use" sections
- **Common Mistakes** - Antipatterns to avoid
- **Severity Markers** - CRITICAL, IMPORTANT, OPTIONAL indicators
- **Decision Trees** - Explicit logic for choosing between patterns
- **Real Examples** - All code from actual production components
- **File References** - Direct links to source files (format: `filename.tsx:line`)

## How to Use This Guide

**For LLMs:** Search by pattern tags (e.g., `#card-overlay`, `#centering-flexbox`, `#gradient-bottom-fade`), severity markers, or use case keywords.

**For Developers:** Use table of contents or search for "How do I..." questions.

**Pattern Tag Format:** `#category-variant-modifier`
- Example: `#card-overlay-gradient`, `#text-eyebrow-uppercase`, `#list-inline-dividers`

---

## Table of Contents

- [Cards](#cards)
- [Text Patterns](#text-patterns)
- [Lists](#lists)
- [Spacing & Sizing](#spacing--sizing)
- [Overlays & Gradients](#overlays--gradients)
- [Hover Effects](#hover-effects)
- [Badges & Tags](#badges--tags)
- [Accordions](#accordions)
- [Centering Content](#centering-content)
- [Aspect Ratios](#aspect-ratios)
- [Borders & Shadows](#borders--shadows)

---

## Cards

### How do I create a basic card?

**Pattern Tags:** `#card-basic` `#card-vertical` `#image-hover-zoom` `#flex-column`

**Source Files:** `common/components/cardTile/cardTile.tsx`, `cardTile.module.scss`

**Complexity:** ⭐⭐ Medium

**Use Case:** Product listings, blog posts, resource cards, any vertical card with image + text + optional CTA

```typescript
// cardTile.tsx
import styles from "./cardTile.module.scss";
import Image from "next/image";
import Rte from "@components/rte/rte";

export default function CardTile({ image, tag, summary, url, label, icon, maxWidth, maxHeight }) {
  return (
    <div className={styles.cardContainer} style={{ maxWidth: maxWidth ? `${maxWidth}px` : "auto" }}>
      <div className={styles.imageContainer} style={{ maxWidth: maxWidth ? `${maxWidth}px` : "auto", maxHeight: maxHeight ? `${maxHeight}px` : "auto" }}>
        <Image src={image} alt={tag} width={maxWidth} height={maxHeight} />
      </div>
      <Rte text={tag} className={styles.tag} />
      <Rte text={summary} className={styles.summary} />
      {url && (
        <a href={url} className={`${styles.buttonContainer} eyebrow`}>
          <div className="squareButton">
            <i className={icon ? icon : "bmg-icon bmg-icon-right-arrow"}></i>
          </div>
          {label}
        </a>
      )}
    </div>
  );
}
```

```scss
// cardTile.module.scss
@import "@styles/variables.scss";

.cardContainer {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 30px;
  cursor: pointer !important;

  .imageContainer {
    transition: transform 3s ease;
    margin-bottom: 34px;
    overflow: hidden;
    border-radius: $borderRadius;  // 10px

    img {
      transition: transform 3s ease;
      object-fit: cover;

      &:hover {
        transform: scale(1.1);
      }
    }
  }

  .tag {
    * {
      font-family: $defaultFont;
      text-transform: uppercase;
      font-weight: 700;
    }
    margin-bottom: 20px;
  }

  .summary {
    margin-bottom: 20px;
  }

  .buttonContainer {
    display: flex;
    align-items: center;
    gap: 15px;

    &:hover {
      color: $white;
    }
  }
}

@include breakpoint(small down) {
  .cardContainer {
    margin-bottom: 0px;
  }
}
```

**Key Patterns:**
- `border-radius: $borderRadius` (10px) for rounded corners
- `margin-bottom: 30px` on desktop, `0px` on mobile
- Image hover scale effect: `transform: scale(1.1)`
- Slow transition for smooth effect: `3s ease`

**✅ When to use:**
- Content cards in grid layouts
- Blog post previews
- Product/resource listings
- Any card with clear hierarchy: image → tag → summary → CTA

**❌ When NOT to use:**
- Cards needing text overlay on image (use overlay card instead)
- Horizontal card layouts (this is vertical only)
- Cards without images (use text-only pattern)
- Hero sections (use banner patterns instead)

**⚠️ Common Mistakes:**
- **CRITICAL:** Forgetting `overflow: hidden` on `.imageContainer` - image will overflow on hover
- Using Next.js `<Image>` without width/height props
- Not testing hover effect on touch devices
- Using different transition speeds (stick to `3s` for consistency)

---

### How do I create a card with an image overlay?

**Pattern Tags:** `#card-overlay` `#card-gradient` `#text-over-image` `#aspect-ratio` `#absolute-positioning`

**Source Files:** `common/components/productCard/productCard.tsx`, `productCard.module.scss`

**Complexity:** ⭐⭐⭐ Complex

**Use Case:** Product cards, portfolio items, any card where text overlays the image with gradient background

**Example from: `productCard.tsx` / `productCard.module.scss`**

```typescript
// productCard.tsx
import styles from "./productCard.module.scss";
import ResponsiveImage from "@components/images/responsiveImage";
import Link from "next/link";

export default function ProductCard({ product }) {
  return (
    <Link href={product.url} className={styles.productCard}>
      <div className={styles.imageContainer}>
        <ResponsiveImage
          image={product.properties.image}
          className={styles.productImage}
          sizes={[
            { size: "small", crop: "tileMobile" },
            { size: "medium", crop: "tileDesktop" },
          ]}
        />
        <div className={styles.overlay}></div>
        <div className={styles.text + " darkBackground"}>
          <h4 className={styles.productName}>{product.name}</h4>
          <p className={styles.productCollection}>
            <i className="bmg-icon bmg-icon-grid"></i>
            <span>{product.properties.collection.name}</span>
          </p>
        </div>
      </div>
    </Link>
  );
}
```

```scss
// productCard.module.scss
@import "@styles/variables.scss";

.productCard {
  display: block;
  width: 100%;
  text-decoration: none;
}

.imageContainer {
  position: relative;
  width: 100%;
  aspect-ratio: 6/5;
  overflow: hidden;
  transition: all 0.4s ease-in-out;

  img {
    transition: transform 0.5s ease;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &:hover {
    img {
      transform: scale(1.1);
    }

    .overlay {
      height: 70%;
      background: linear-gradient(to top, rgba(3, 53, 70, 1) 10%, transparent 60%);
    }
  }
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50%;
  background: linear-gradient(to top, rgba(3, 53, 70, 0.9) 10%, transparent 90%);
  transition: all 0.4s ease-in-out;
}

.text {
  position: absolute;
  display: flex;
  flex-direction: column;
  height: 102px;
  left: 0;
  right: 0;
  width: 90%;
  margin: auto;
  border-top: 1px solid white;
  padding: 1rem 0;
  bottom: 0;
  color: white;
  transition: all 0.4s ease-in-out;
}

.productName {
  margin-bottom: 0 !important;
  font-weight: 300;
}

.productCollection {
  display: flex;
  font-size: 18px;
  gap: 0.2rem;
  color: #ffffff;
  align-items: center;
  line-height: 28px;
  margin-bottom: 0 !important;
  font-weight: 300;

  i {
    font-size: 22px;
  }
}

// Responsive adjustments
@include breakpoint(medium down) {
  .imageContainer {
    aspect-ratio: 768/600;
  }

  .text {
    height: 80px;
    padding: 0.5rem 0;

    .productName {
      font-size: 1.25rem;
      margin-bottom: 0.3rem !important;
    }

    .productCollection {
      font-size: 16px;
      line-height: 24px;

      i {
        font-size: 18px;
      }
    }
  }
}

@include breakpoint(small down) {
  .imageContainer {
    aspect-ratio: 323/352;
  }

  .text {
    height: 70px;
    padding: 0.3rem 0;

    .productName {
      font-size: 1.1rem;
    }

    .productCollection {
      font-size: 14px;
      line-height: 20px;

      i {
        font-size: 16px;
      }
    }
  }
}
```

**Key Patterns:**
- `aspect-ratio: 6/5` for consistent card dimensions
- Gradient overlay: `linear-gradient(to top, rgba(3, 53, 70, 0.9) 10%, transparent 90%)`
- Text positioned absolutely at bottom with `bottom: 0`
- Hover increases overlay height: `height: 50%` → `height: 70%`
- Use `.darkBackground` global class for white text
- Responsive aspect ratios: `6/5` → `768/600` → `323/352`

**✅ When to use:**
- Product cards with prominent imagery
- Portfolio/gallery items
- Cards where image is primary focus
- Need text readability over varied images

**❌ When NOT to use:**
- Text-heavy cards (gradient limits space)
- Cards with complex CTAs
- Situations where image shouldn't be obscured
- Accessibility-critical text (contrast may vary)

**⚠️ Common Mistakes:**
- **CRITICAL:** Forgetting `position: relative` on parent `.imageContainer`
- **CRITICAL:** Not using `.darkBackground` class - text won't be white
- Using fixed heights instead of `aspect-ratio` (breaks responsive)
- Overlay gradient too dark - test with light images
- Not accounting for z-index layers (image → overlay → text)
- Forgetting responsive aspect ratio adjustments

**🎯 Pro Tip:** Test overlay with both light and dark images to ensure text readability

---

### How do I center a text box inside a card with a box shadow?

**Pattern Tags:** `#card-centered` `#flexbox-centering` `#box-shadow` `#text-constrained`

**Source Files:** `common/components/blockGrid/blocks/headlines/headlineContent.module.scss`

**Complexity:** ⭐ Simple

**Use Case:** Centered content cards, quote cards, testimonial cards, feature highlights

**Example from: `headlineContent.module.scss`**

```scss
@import '@styles/variables.scss';

.wrapper {
  width: 100%;
  display: flex;
  flex: 1;
  flex-direction: column;
  background-color: $blue;
  border-radius: $borderRadius;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);  // Subtle shadow

  .textContainer {
    display: flex;
    flex: 1;
    flex-direction: column;
    justify-content: center;  // Vertical centering
    align-items: center;      // Horizontal centering
    padding: 2rem 2rem 3rem 2rem;
    color: $white;
  }

  .text {
    text-align: center;       // Center text alignment
    color: $white;
    max-width: 430px;         // Constrain width
    margin: 0 auto;           // Additional horizontal centering
  }
}
```

**Usage:**

```typescript
<div className={styles.wrapper}>
  <div className={styles.textContainer}>
    <Rte text={text} className={styles.text} />
  </div>
</div>
```

**Key Patterns:**
- Flexbox centering: `justify-content: center` + `align-items: center`
- Constrain text width: `max-width: 430px` (or `700px` for wider content)
- `margin: 0 auto` for horizontal centering within max-width
- `text-align: center` for centering text lines
- Subtle shadow: `box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1)`

**✅ When to use:**
- Quote/testimonial cards
- Feature highlights with short text
- Stat displays
- Centered announcements

**❌ When NOT to use:**
- Long-form content (breaks center alignment)
- Left-aligned reading content
- Cards with multiple CTAs

**⚠️ Common Mistakes:**
- Forgetting `flex: 1` on text container (won't expand to fill space)
- Not constraining max-width (text too wide, hard to read)
- Using only `text-align: center` without flexbox (won't vertically center)
- Shadow too strong (keep at `0.1` alpha for subtlety)

---

### How do I create a card with a background image and centered content?

**Pattern Tags:** `#card-background-image` `#fixed-height` `#absolute-overlay` `#bottom-aligned`

**Source Files:** `common/components/blockGrid/blocks/ctaTile/ctaTile.module.scss`

**Complexity:** ⭐⭐⭐ Complex

**Use Case:** Hero cards, CTA tiles, promotional cards with background imagery

**Example from: `ctaTile.module.scss`**

```scss
.ctaTile {
  padding: 40px 0;
  width: 100%;
  position: relative;
  height: 439px;

  .imageContainer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    .backgroundImage {
      width: 100%;
      height: 100%;
      object-fit: cover;
      overflow: hidden;
    }

    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 2;
      background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0) 50%, $blueDark);
      height: 100%;
      width: 100%;
    }
  }

  .content {
    position: relative;
    z-index: 3;
    display: flex;
    flex-flow: column;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
  }
}

@include breakpoint(large up) {
  .ctaTile {
    height: 700px;
  }
}
```

**Key Patterns:**
- Fixed height container: `height: 439px` (mobile) → `700px` (desktop)
- Absolute positioned background image fills container
- Overlay gradient: `linear-gradient(to bottom, rgba(0, 0, 0, 0) 50%, $blueDark)`
- Content layer with `z-index: 3` above overlay
- Flexbox with `justify-content: flex-end` to bottom-align content

**✅ When to use:**
- Hero-style CTA cards
- Promotional tiles in grid
- Large feature cards with short content
- Sections where background image sets the mood

**❌ When NOT to use:**
- Variable height content (uses fixed height)
- Content-heavy cards
- Accessibility-first situations (image dependency)
- Small card sizes (design breaks below 400px)

**⚠️ Common Mistakes:**
- **CRITICAL:** Not setting z-index layers correctly (image: 1, overlay: 2, content: 3)
- Using responsive height (stick to fixed heights for this pattern)
- Overlay too opaque - image becomes invisible
- Not testing with various image contrasts

---

### 🎯 Card Pattern Decision Tree

**Choose your card pattern:**

```
What's your primary goal?
├─ Display content below image
│  └─ Use: Basic Card (#card-basic)
│     Files: cardTile.tsx
│
├─ Text overlays image at bottom
│  └─ Use: Overlay Card (#card-overlay)
│     Files: productCard.tsx
│
├─ Center content in card
│  └─ Use: Centered Card (#card-centered)
│     Files: headlineContent.module.scss
│
└─ Full-screen background with content
   └─ Use: Background Image Card (#card-background-image)
      Files: ctaTile.module.scss
```

**By use case:**
- **Product listing:** Overlay Card (productCard.tsx)
- **Blog posts:** Basic Card (cardTile.tsx)
- **Testimonials:** Centered Card (headlineContent)
- **Hero/CTA:** Background Image Card (ctaTile)

---

## Text Patterns

### How do I create eyebrow text (small uppercase labels)?

**Pattern Tags:** `#text-eyebrow` `#text-uppercase` `#text-label` `#letter-spacing`

**Source Files:** `common/components/blockGrid/blocks/bannerImage/bannerImage.module.scss`

**Complexity:** ⭐ Simple

**Use Case:** Category labels, section tags, "NEW" indicators, pre-headline labels

```scss
.rteContent {
  :global {
    p.eyebrow {
      font-family: $defaultFont;
      font-style: normal;
      font-weight: 700;
      font-size: 14px;
      line-height: 18px;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: #007299;
      margin-bottom: 16px;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
  }
}

@include breakpoint(small down) {
  .rteContent {
    :global {
      p.eyebrow {
        font-size: 10px;
        line-height: 16px;
        margin-bottom: 4px;
      }
    }
  }
}
```

**Usage in RTE:**

```html
<p class="eyebrow">New Arrival</p>
<h1>Product Title</h1>
```

**Key Patterns:**
- `text-transform: uppercase`
- `letter-spacing: 0.2em` for wide tracking
- `font-weight: 700` (bold)
- Small font size: `14px` desktop, `10px` mobile
- Brand blue color: `#007299`
- Optional subtle text shadow

**✅ When to use:**
- Above h1 headings to show category/context
- Product tags ("NEW", "SALE", "FEATURED")
- Section labels in complex layouts
- Metadata labels

**❌ When NOT to use:**
- As primary heading (use h1-h6 instead)
- For body text
- When uppercase conflicts with brand voice
- Screen reader-critical content (uppercase can affect pronunciation)

**⚠️ Common Mistakes:**
- Using `<h6>` instead of `<p class="eyebrow">` (semantic hierarchy)
- Letter spacing too tight (use minimum `0.2em`)
- Font size too large (defeats purpose of label)
- Forgetting responsive size reduction on mobile

**🎯 Pro Tip:** Always pair with a proper heading below. Eyebrows provide context, not hierarchy.

---

### How do I style headings with proper hierarchy?

**Pattern Tags:** `#text-headings` `#typography-scale` `#semantic-html` `#responsive-type`

**Source Files:** `styles/typography.scss` (global)

**Complexity:** ⭐ Simple (use global styles)

**Use Case:** All headings site-wide - global styles, no custom code needed

**From: `typography.scss` (global styles)**

```scss
h1 {
  font-size: 1.875rem;    // 30px mobile
  line-height: 2.5rem;
  font-weight: 300;
  color: $blueDark;
}

h2 {
  font-size: 1.5rem;      // 24px mobile
  line-height: 2.125rem;
  font-weight: 100;
  color: $blueDark;
}

h3 {
  font-size: 1.25rem;     // 20px mobile
  line-height: 1.875rem;
  margin-bottom: 2.5rem;
  font-weight: 100;
}

h4 {
  font-size: 1.125rem;    // 18px
  line-height: 1.5rem;
  font-weight: 300;
  color: $blueDark;
}

h5 {
  font-size: 0.875rem;    // 14px
  line-height: 1.5rem;
  font-weight: 300;
}

h6 {
  font-size: 0.625rem;    // 10px
  line-height: 1rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: $blue;
}

@include breakpoint(medium) {
  h1 {
    font-size: 3.125rem;  // 50px desktop
    line-height: 3.75rem;
  }

  h2 {
    font-size: 2.5rem;    // 40px desktop
    line-height: 3.125rem;
    margin-bottom: 1.5rem;
  }

  h3 {
    font-size: 1.875rem;  // 30px desktop
    line-height: 2.5rem;
  }

  h4 {
    font-size: 1.25rem;   // 20px desktop
    line-height: 2.125rem;
  }

  h5 {
    font-size: 1.25rem;   // 20px desktop
    line-height: 1.875rem;
  }

  h6 {
    font-size: 0.875rem;  // 14px desktop
    line-height: 1.125rem;
  }
}
```

**Key Patterns:**
- Use `h6` for eyebrow-style labels (uppercase, small, brand blue)
- Use `h1` for page/section titles
- Use `h2` for major section headings
- Use `h3`-`h4` for subsections
- Font weights: `100` (thin), `300` (light), `500` (medium), `700` (bold)
- Mobile-first sizing with responsive scale-up

---

### How do I add underlines to text?

**From: `typography.scss` (global utilities)**

```scss
// Simple underline
.underline {
  padding-bottom: .25em;
  border-bottom: 2px solid $greyHalf;
}

// White underline with spacing
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

// Blue underline with spacing
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

**Usage:**

```jsx
<h2 className="blueUnderline">Section Title</h2>
<p className="underline">Highlighted text</p>
```

**Key Patterns:**
- Direct border: `border-bottom: 2px solid $greyHalf`
- Pseudo-element for spacing: `::after` with margins
- Full-width underlines span container width

---

### How do I create captions or meta text?

**Example from: `productCard.module.scss`**

```scss
.productCollection {
  display: flex;
  font-size: 18px;
  gap: 0.2rem;
  color: #ffffff;
  align-items: center;
  line-height: 28px;
  margin-bottom: 0 !important;
  font-weight: 300;

  i {
    font-size: 22px;  // Icon slightly larger
  }
}

@include breakpoint(medium down) {
  .productCollection {
    font-size: 16px;
    line-height: 24px;

    i {
      font-size: 18px;
    }
  }
}

@include breakpoint(small down) {
  .productCollection {
    font-size: 14px;
    line-height: 20px;

    i {
      font-size: 16px;
    }
  }
}
```

**Key Patterns:**
- Smaller font size than body text: `14px`-`18px`
- Light weight: `font-weight: 300`
- Flexbox for icon + text: `display: flex; align-items: center; gap: 0.2rem`
- Icons slightly larger than text for visual balance
- Remove default margins: `margin-bottom: 0 !important`

---

## Lists

### How do I create an inline list with dividers?

**Example from: `inline-list.tsx` / `inline-list.module.scss`**

```typescript
// inline-list.tsx
import styles from './inline-list.module.scss';

export default function InlineList({ items, divider = true, gutterSize = 1 }) {
  return (
    <ul className={`${styles.inlineList} ${styles['size' + gutterSize]}`}>
      {items.map((item, index) => (
        <Fragment key={index}>
          {divider && index > 0 && (
            <li className={styles.divider + ' ' + styles.default}></li>
          )}
          <li>{item}</li>
        </Fragment>
      ))}
    </ul>
  );
}
```

```scss
// inline-list.module.scss
@import '@styles/variables.scss';

$inlineListGutters: (
  1: 1rem,    // Small gap
  2: 2rem,    // Medium gap
  3: 4rem,    // Large gap
  4: 8rem,
  5: 12rem,
);

.inlineList {
  display: inline-flex;
  list-style: none;
  padding-left: 0;
  flex-wrap: wrap;

  &.size1 {
    $size: rem-calc(map-get($inlineListGutters, 1) / 2);
    margin: 0 -#{$size} -1rem;
    > li {
      margin: 0 #{$size} 1rem;
    }
  }

  &.size2 {
    $size: rem-calc(map-get($inlineListGutters, 2) / 2);
    margin: 0 -#{$size} -1rem;
    > li {
      margin: 0 #{$size} 1rem;
    }
  }

  &.size3 {
    $size: rem-calc(map-get($inlineListGutters, 3) / 2);
    margin: 0 -#{$size} -1rem;
    > li {
      margin: 0 #{$size} 1rem;
    }
  }

  .divider.default {
    &::before {
      content: '';
      display: inline-block;
      width: 1px;
      height: 1.5em;
      background-color: $linkColor;
    }
  }

  &.dark {
    .divider::before {
      background-color: $white;
    }
  }
}
```

**Usage:**

```jsx
<InlineList
  items={['Home', 'Products', 'About', 'Contact']}
  divider={true}
  gutterSize={2}
/>
```

**Renders:**
```
Home | Products | About | Contact
```

**Key Patterns:**
- `display: inline-flex` for horizontal layout
- Gutter sizes: `1` (1rem), `2` (2rem), `3` (4rem)
- Divider as pseudo-element `::before` on list items
- Negative margins on container, positive on items for consistent spacing
- Dark variant with white dividers

---

### How do I create a two-column list?

**From: `typography.scss`**

```scss
.twoColumn {
  ul:first-child {
    margin-bottom: 0;
  }

  @include breakpoint(medium) {
    display: flex;
    gap: 30px;

    ul:first-child {
      margin-bottom: 1rem;
    }
  }
}
```

**Usage:**

```html
<div class="twoColumn">
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
  <ul>
    <li>Item 3</li>
    <li>Item 4</li>
  </ul>
</div>
```

**Key Patterns:**
- Stacked on mobile, side-by-side on tablet+
- `gap: 30px` between columns
- Adjust margins to prevent extra spacing

---

## Spacing & Sizing

### What padding should I use for components?

**Common patterns from real components:**

```scss
// Small components (buttons, badges)
padding: 4px 16px;              // primaryButton
padding: 6px 24px;              // badge (mobile)
padding: 15px 40px;             // badge (desktop)

// Medium components (cards, tiles)
padding: 20px 15px;             // card mobile
padding: 35px 50px;             // ctaButton
padding: 56px 35px;             // ctaBasic desktop

// Large components (sections, heroes)
padding: 2rem 2rem 3rem 2rem;  // headlineContent text container
padding: 83px 8.27vw 59px 8.27vw;  // bannerImage header box (desktop)
padding: 36px 23px 20px 23px;   // bannerImage header box (mobile)

// Accordion
padding: 25px 30px;             // accordion summary
padding: 0 30px 25px;           // accordion details
```

**General rules:**
- **Buttons:** `4px-15px` vertical, `16px-40px` horizontal
- **Cards:** `20px-35px` mobile, `35px-56px` desktop
- **Sections:** `2rem-7rem` (use spacing variables)
- **Use vertical padding > horizontal padding** for better mobile UX

---

### What margins should I use between elements?

**From spacing variables and real components:**

```scss
// Tight spacing (within component)
margin-bottom: 4px;             // eyebrow mobile
margin-bottom: 16px;            // eyebrow desktop
margin-bottom: 20px;            // card summary, tag

// Medium spacing (between sections)
margin-bottom: 30px;            // card container
margin-bottom: 34px;            // card image

// Wide spacing (major sections)
margin-bottom: 2.5rem;          // h3 default
margin-top: 2.5rem;             // section spacing

// Use spacing variables
margin-top: map-get($margins, 1);   // 1rem
margin-top: map-get($margins, 2);   // 2.5rem
margin-top: map-get($margins, 3);   // 7rem
```

**General rules:**
- **Within cards:** `16px-20px`
- **Between cards:** `30px`
- **Between sections:** `2.5rem` (40px)
- **Major sections:** `7rem` (112px)

---

### What max-width should I use for content?

**Common max-widths from components:**

```scss
max-width: 430px;    // headlineContent text (narrow)
max-width: 575px;    // ctaTile model image
max-width: 700px;    // ctaBasic text (standard)
max-width: 875px;    // richtext narrow variant
max-width: 1416px;   // ctaWithImage container
max-width: 1516px;   // grid-container.wide
max-width: 1594px;   // $global-width (Foundation)
max-width: 1600px;   // $wideMaxWidth

// Percentage-based
max-width: 90%;      // headlineContent wrapper, productCard text
max-width: 95%;      // mobile width
```

**General rules:**
- **Narrow text:** `430px-700px`
- **Standard content:** `875px-1000px`
- **Wide sections:** `1416px-1600px`
- **Mobile:** `90%-95%` of viewport

---

### What gap should I use in flexbox/grid?

**From real components:**

```scss
gap: 0.2rem;       // Icon + text (tight)
gap: 15px;         // Button container
gap: 25px;         // Social media links
gap: 30px;         // Two-column layout, card elements
gap: 93px;         // ctaWithImage (desktop)

// Responsive gaps
gap: 20px;         // Mobile
gap: 30px;         // Tablet
gap: 93px;         // Desktop
```

**General rules:**
- **Tight (icon + text):** `0.2rem` (3-4px)
- **Standard:** `15px-30px`
- **Wide:** `50px-100px`
- **Increase gap on larger screens**

---

## Overlays & Gradients

### How do I create a gradient overlay on an image?

**Example from: `productCard.module.scss`**

```scss
.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50%;
  background: linear-gradient(
    to top,
    rgba(3, 53, 70, 0.9) 10%,
    transparent 90%
  );
  transition: all 0.4s ease-in-out;
}

// On hover, expand overlay
&:hover .overlay {
  height: 70%;
  background: linear-gradient(
    to top,
    rgba(3, 53, 70, 1) 10%,
    transparent 60%
  );
}
```

**Key Patterns:**
- Position `absolute` with parent `relative`
- Start from `bottom: 0` for bottom-up gradients
- Use `rgba()` for transparency
- Gradient syntax: `linear-gradient(direction, color stop%, color stop%)`
- Common directions: `to top`, `to bottom`, `to right`, `to left`
- Transition overlay changes for smooth hover effects

---

### How do I create a solid color overlay?

**Example from: `ctaBasic.module.scss`**

```scss
.overlay {
  position: absolute;
  z-index: -1;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: .7;
}

// Usage with background color
<div className={styles.overlay} style={{ backgroundColor: '#' + backgroundColor }}></div>
```

**Alternative with mix-blend-mode:**

```scss
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: multiply;
  opacity: .7;
}
```

**Key Patterns:**
- `z-index: -1` to position behind content
- Use `opacity` for transparency control
- `mix-blend-mode: multiply` for color blending effects

---

### What gradient styles are commonly used?

**From real components:**

```scss
// Bottom fade (for image overlays)
background: linear-gradient(
  to top,
  rgba(3, 53, 70, 0.9) 10%,
  transparent 90%
);

// Top fade
background: linear-gradient(
  to bottom,
  rgba(0, 0, 0, 0) 50%,
  $blueDark
);

// Horizontal fade (for text readability)
background: linear-gradient(
  to right,
  rgba($blue, 0) 55%,
  $blue 100%
);

// Button gradient (deprecated in codebase, but exists)
background: linear-gradient(
  121deg,
  rgb(163 177 196) 0%,
  rgb(108 132 165) 100%
);
```

**Key Patterns:**
- Use brand colors with transparency
- Start with `rgba(color, 0)` for transparent
- End with solid color or `rgba(color, 0.9)`
- Position stops at `10%`, `50%`, `55%`, `90%`, `100%`

---

## Hover Effects

### How do I create an image zoom hover effect?

**Pattern Tags:** `#hover-zoom` `#image-scale` `#transform` `#overflow-hidden`

**Source Files:** `cardTile.module.scss`, `productCard.module.scss`

**Complexity:** ⭐⭐ Medium

**Use Case:** Card hovers, gallery items, any image that should zoom on interaction

```scss
.imageContainer {
  overflow: hidden;  // CRITICAL: prevents image overflow
  transition: transform 3s ease;  // Optional: container transition

  img {
    transition: transform 0.5s ease;  // Smooth zoom
    width: 100%;
    height: 100%;
    object-fit: cover;

    &:hover {
      transform: scale(1.1);  // 10% zoom
    }
  }
}
```

**Key Patterns:**
- **Parent must have `overflow: hidden`**
- Image scale: `1.1` (10% zoom) is standard
- Transition duration: `0.5s` (fast), `3s` (slow)
- Always use `ease` or `ease-in-out` for natural motion

**✅ When to use:**
- Product cards
- Portfolio/gallery images
- Blog post featured images
- Any clickable image card

**❌ When NOT to use:**
- Touch-only devices (hover doesn't exist)
- Accessibility mode (may cause motion sickness)
- Background images (use overlay expansion instead)
- Icons or small images (zoom too noticeable)

**⚠️ Common Mistakes:**
- **CRITICAL:** Forgetting `overflow: hidden` - zoomed image leaks outside container
- **CRITICAL:** Hover on `img` instead of parent - inconsistent behavior
- Using scale > 1.15 (too dramatic)
- Not testing with reduced motion preferences
- Transition on parent AND child (choose one)

**🎯 Pro Tip:** Use `3s` for subtle, elegant zoom. Use `0.5s` for quick, responsive feel.

---

### How do I create a hover state for cards?

**Pattern Tags:** `#hover-card` `#hover-multi-effect` `#overlay-expand`

**Source Files:** `productCard.module.scss`, `ctaButton.module.scss`

**Complexity:** ⭐⭐ Medium

**Use Case:** Interactive cards with multiple hover effects (image + overlay + color)

**Example from: `productCard.module.scss`**

```scss
.imageContainer {
  transition: all 0.4s ease-in-out;

  &:hover {
    // Zoom image
    img {
      transform: scale(1.1);
    }

    // Expand overlay
    .overlay {
      height: 70%;
      background: linear-gradient(to top, rgba(3, 53, 70, 1) 10%, transparent 60%);
    }
  }
}
```

**Example from: `ctaButton.module.scss`**

```scss
.buttonContainer {
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: $black;
    color: $white;
  }
}
```

**Key Patterns:**
- Combine multiple effects: image zoom + overlay change
- Standard transition: `0.3s-0.4s ease-in-out`
- Change `background-color`, `color`, `transform`, `opacity`
- Add `cursor: pointer` for clickable elements

---

### How do I create hover effects for buttons?

**From: `button.scss`**

```scss
.button {
  background-color: $black;
  color: $white;
  transition: .3s all;

  &:hover {
    background-color: $black;  // Stays same
    color: $white;
  }

  &:focus,
  &:active,
  &.active {
    background-color: $blue;   // Changes to brand blue
    color: $white;
  }
}

.buttonFooter {
  color: $blueDark;

  &::after {
    transform: translateX(15px);
    transition: .3s all;
  }

  &:hover {
    color: $black;

    &::after {
      width: 18px;
      transform: translateX(13px);  // Slight movement
    }
  }
}
```

**Key Patterns:**
- Always include `:hover`, `:focus`, `:active` states
- Focus state should be distinct for accessibility
- Animate icons with `transform: translateX()`
- Keep transitions short: `0.3s`

---

## Badges & Tags

### How do I create a badge on a card?

**Example from: `productCard.module.scss`**

```scss
.badge {
  position: absolute;
  top: 18px;
  left: 0;  // Or omit for default positioning
  color: #003e52;
  background: #ffffff;
  padding: 15px 40px;
  font-size: 16px;
  line-height: 14px;
  letter-spacing: 0.05em;
  backdrop-filter: blur(2px);  // Frosted glass effect
  z-index: 2;
}

@include breakpoint(medium down) {
  .badge {
    padding: 6px 24px;
    font-size: 12px;
    top: 12px;
  }
}

@include breakpoint(small down) {
  .badge {
    padding: 4px 16px;
    font-size: 10px;
    top: 12px;
  }
}
```

**Usage:**

```typescript
{displayableTags.map(tag => (
  <div key={tag.id} className={styles.badge}>
    {tag.name}
  </div>
))}
```

**Key Patterns:**
- Position `absolute` on top of image container
- Top positioning: `18px` desktop, `12px` mobile
- White background with dark text for contrast
- `backdrop-filter: blur(2px)` for modern frosted effect
- Letter spacing: `0.05em` for readability
- Responsive padding: `4px-15px` vertical, `16px-40px` horizontal

---

### How do I create tags in a text area?

**Example from: `cardTile.module.scss`**

```scss
.tag {
  * {
    font-family: $defaultFont;
    text-transform: uppercase;
    font-weight: 700;
  }
  margin-bottom: 20px;
}
```

**Usage with RTE:**

```typescript
<Rte text={tag} className={styles.tag} />
```

**Key Patterns:**
- `text-transform: uppercase`
- `font-weight: 700` (bold)
- Small font size (inherits from parent or use `12px-14px`)
- Margin below: `20px`
- Use brand colors: `$blue` or `$blueDark`

---

## Accordions

### How do I create a styled accordion?

**Example from: `standardAccordion.tsx`**

```typescript
import { Accordion, AccordionSummary, AccordionDetails, styled } from "@mui/material";
import variables from "@styles/variables.module.scss";

const StyledAccordion = styled(Accordion)({
  boxShadow: 'none',
  marginTop: '17px',
  '&:first-child': {
    marginTop: '0'
  },
  '&:before': {
    display: 'none', // Removes default divider
  }
});

const StyledAccordionSummary = styled(AccordionSummary)({
  margin: 0,
  padding: '25px 30px',
  minHeight: 'auto',
  '& .MuiAccordionSummary-expandIconWrapper i::before': {
    content: "'\\f011'"  // Collapsed icon
  },
  '& .MuiAccordionSummary-content': {
    margin: 0
  },
  '&.Mui-expanded': {
    minHeight: 0
  },
  '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
    backgroundColor: variables.blue,
    color: variables.white,
    transform: 'none'
  },
  '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded i::before': {
    content: "'\\f010'"  // Expanded icon
  }
});

const StyledAccordionDetails = styled(AccordionDetails)({
  padding: '0 30px 25px',
  borderTop: 'none',
});

export function StandardAccordion({children, ...model}) {
  return (
    <StyledAccordion {...model}>
      {children}
    </StyledAccordion>
  );
}

export function StandardAccordionSummary({children, expandIcon, ...model}) {
  return (
    <StyledAccordionSummary {...model} expandIcon={expandIcon || <i className="bmg-icon"></i>}>
      {children}
    </StyledAccordionSummary>
  );
}

export function StandardAccordionDetails({children, ...model}) {
  return (
    <StyledAccordionDetails {...model}>
      {children}
    </StyledAccordionDetails>
  );
}
```

**Usage:**

```typescript
import { StandardAccordion, StandardAccordionSummary, StandardAccordionDetails } from "@components/accordion/standardAccordion";

<StandardAccordion>
  <StandardAccordionSummary>
    <h3>Question</h3>
  </StandardAccordionSummary>
  <StandardAccordionDetails>
    <p>Answer content here</p>
  </StandardAccordionDetails>
</StandardAccordion>
```

**Key Patterns:**
- Remove MUI default shadow: `boxShadow: 'none'`
- Padding: `25px 30px` for summary, `0 30px 25px` for details
- Margin between items: `17px`
- Expand icon changes color when expanded: brand blue background
- Use custom icon font characters for expand/collapse icons

---

## Centering Content

### How do I center content horizontally?

**Pattern Tags:** `#centering-horizontal` `#flexbox-centering` `#margin-auto` `#text-align`

**Complexity:** ⭐ Simple

**Use Case:** Horizontal centering - choose method based on content type

**1. Flexbox (best for containers):**

```scss
.container {
  display: flex;
  justify-content: center;  // Horizontal centering
  align-items: center;      // Vertical centering
}
```

**2. Auto margins (best for max-width elements):**

```scss
.content {
  max-width: 700px;
  margin: 0 auto;  // Centers within parent
}
```

**3. Text alignment (for text only):**

```scss
.text {
  text-align: center;
}
```

**4. Grid (for complex layouts):**

```scss
.container {
  display: grid;
  place-items: center;  // Centers both axes
}
```

---

### How do I center content vertically?

**Methods:**

**1. Flexbox (most common):**

```scss
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;  // Vertical centering in column layout
  min-height: 100vh;        // Or specific height
}
```

**2. Absolute positioning (for overlays):**

```scss
.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

**3. Grid:**

```scss
.container {
  display: grid;
  align-items: center;
  min-height: 100vh;
}
```

---

### How do I center content both horizontally and vertically?

**Best method (flexbox):**

```scss
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;  // Or specific height
}
```

**Example from `headlineContent.module.scss`:**

```scss
.textContainer {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.text {
  text-align: center;
  max-width: 430px;
  margin: 0 auto;
}
```

---

## Aspect Ratios

### How do I maintain aspect ratio for images/cards?

**Modern CSS (preferred):**

```scss
.imageContainer {
  width: 100%;
  aspect-ratio: 6/5;  // Width:Height ratio
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

// Responsive aspect ratios
@include breakpoint(medium down) {
  .imageContainer {
    aspect-ratio: 768/600;
  }
}

@include breakpoint(small down) {
  .imageContainer {
    aspect-ratio: 323/352;
  }
}
```

**Common aspect ratios from the codebase:**
- `6/5` - Product cards (desktop)
- `768/600` - Product cards (tablet)
- `323/352` - Product cards (mobile)
- `16/9` - Video content
- `1/1` - Square tiles

---

### How do I create a responsive video container?

**Padding-top method (for older browser support):**

```scss
.videoContainer {
  position: relative;
  width: 100%;
  padding-top: 56.25%;  // 16:9 aspect ratio (9/16 * 100)

  video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
```

**Dynamic padding from data:**

```typescript
<div className={styles.videoWrapper} style={{ paddingTop: (image.height * 100 / image.width) + '%' }}>
  <video autoPlay muted loop>
    <source src={image?.url} type="video/mp4" />
  </video>
</div>
```

---

## Borders & Shadows

### What border styles are used?

**From real components:**

```scss
// Border radius (from variables.scss)
border-radius: $borderRadius;  // 10px (standard)

// Simple borders
border-top: 1px solid white;           // productCard text
border-top: 1px solid $greyHalf;       // buttonFooter
border: 1px solid $black;              // buttonOutline

// Border with transparency
border-top: 1px solid $buttonFooterBorderColor;  // #636B7480 (50% opacity)
```

**Key Patterns:**
- Standard radius: `$borderRadius` (10px)
- Border width: `1px` (standard), `2px` (emphasized)
- Use `$greyHalf` (#636B7480) for subtle borders
- White borders on dark backgrounds
- Dark borders on light backgrounds

---

### What box-shadow styles are used?

**From real components:**

```scss
// Subtle shadows (cards, elevated content)
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

// Text shadows (for readability on images)
text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

// No shadow (MUI override)
boxShadow: 'none';  // For accordions
```

**Shadow formula:**
```scss
box-shadow: [x-offset] [y-offset] [blur-radius] [color];
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
//          ↑ ↑   ↑    ↑
//          x y   blur alpha (10% black)
```

**Key Patterns:**
- X-offset: `0` (centered)
- Y-offset: `1px-2px` (slight downward)
- Blur: `2px-10px` (larger = softer)
- Color: `rgba(0, 0, 0, 0.1)` (10% black, very subtle)
- Avoid heavy shadows - prefer subtle depth

---

## Quick Reference Tables

### Spacing Values

| Use Case | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Button padding | `4px 16px` | `12px 15px` | `4px 16px` - `15px 40px` |
| Card padding | `20px 15px` | `35px` | `56px 35px` |
| Section padding | `2rem` | `3rem` | `2rem-7rem` |
| Element gaps | `15px` | `25px` | `30px-93px` |
| Margins between cards | `20px` | `30px` | `30px` |
| Margins between sections | `2.5rem` | `2.5rem` | `2.5rem-7rem` |

### Typography Scale

| Element | Mobile | Desktop | Weight | Color |
|---------|--------|---------|--------|-------|
| h1 | `30px / 40px` | `50px / 60px` | `300` | `$blueDark` |
| h2 | `24px / 34px` | `40px / 50px` | `100` | `$blueDark` |
| h3 | `20px / 30px` | `30px / 40px` | `100` | - |
| h4 | `18px / 24px` | `20px / 34px` | `300` | `$blueDark` |
| h5 | `14px / 24px` | `20px / 30px` | `300` | - |
| h6 (eyebrow) | `10px / 16px` | `14px / 18px` | `700` | `$blue` |
| Body | `18px / 28px` | `18px / 28px` | `300` | `$textColor` |

### Color Quick Reference

| Use | Variable | Hex | Usage |
|-----|----------|-----|-------|
| Primary brand | `$blueDark` | `#003E52` | Headings, primary elements |
| Interactive | `$blue` | `#007299` | Links, buttons (active), eyebrows |
| Text (light bg) | `$textColor` | `#2D2926` | Body text |
| Text (dark bg) | `$white` | `#FFF` | Text on overlays |
| Background light | `$greyBlue` | `#E5EBEE` | Light sections |
| Borders | `$greyHalf` | `#636B7480` | Subtle dividers (50% opacity) |
| Borders alt | `$grey` | `#D9D9D9` | Standard dividers |

### Breakpoint Values

| Name | Min Width | Usage |
|------|-----------|-------|
| `small` | `0px` | Default mobile styles |
| `medium` | `640px` | Tablet portrait |
| `large` | `1024px` | Desktop |
| `xlarge` | `1200px` | Large desktop |
| `xxlarge` | `1440px` | Extra large desktop |
| `xxxlarge` | `1774px` | Ultra wide |

### Max-Width Guidelines

| Content Type | Max Width | Use Case |
|-------------|-----------|----------|
| Narrow text | `430px` | Captions, short descriptions |
| Standard text | `700px` | Paragraphs, standard content |
| Wide text | `875px` | Rich text, long-form content |
| Content sections | `1416px` | Standard content container |
| Wide sections | `1516px-1600px` | Full-width layouts |
| Page container | `1594px` | Foundation grid max |

---

## Pattern Comparison Tables

### Card Patterns Comparison

| Pattern | Complexity | Image Position | Text Position | Best For | File |
|---------|------------|----------------|---------------|----------|------|
| Basic Card | ⭐⭐ | Above text | Below image | Blog posts, lists | `cardTile.tsx` |
| Overlay Card | ⭐⭐⭐ | Background | Over image (bottom) | Products, portfolio | `productCard.tsx` |
| Centered Card | ⭐ | Optional | Centered | Quotes, stats | `headlineContent` |
| Background Card | ⭐⭐⭐ | Full background | Bottom aligned | Hero, CTA | `ctaTile` |

### Centering Methods Comparison

| Method | Use For | Horizontal | Vertical | Browser Support | Code Complexity |
|--------|---------|------------|----------|-----------------|-----------------|
| Flexbox | Containers | ✅ | ✅ | Modern | Simple |
| Margin Auto | Max-width elements | ✅ | ❌ | All | Very Simple |
| Text Align | Text only | ✅ | ❌ | All | Very Simple |
| Grid | Complex layouts | ✅ | ✅ | Modern | Medium |
| Absolute + Transform | Overlays | ✅ | ✅ | All | Medium |

### Hover Effect Comparison

| Effect | Target | Transition Speed | Use Case | Critical Requirement |
|--------|--------|------------------|----------|---------------------|
| Image Zoom | `<img>` | 0.5s - 3s | Cards, galleries | `overflow: hidden` on parent |
| Overlay Expand | `.overlay` div | 0.4s | Product cards | Parent `position: relative` |
| Color Change | Background/text | 0.3s | Buttons, links | None |
| Icon Movement | Pseudo-element | 0.3s | Arrows, icons | `transform` property |

### Gradient Overlay Comparison

| Direction | Syntax | Use Case | Typical Stops |
|-----------|--------|----------|---------------|
| Bottom Fade | `to top` | Image overlays (text at bottom) | `10%, 90%` |
| Top Fade | `to bottom` | Hero sections | `50%, 100%` |
| Horizontal | `to right` | Text readability | `55%, 100%` |
| Radial | `radial-gradient()` | Spotlight effects | Center-based |

### Spacing Quick Reference

| Element Type | Mobile | Desktop | Variable |
|--------------|--------|---------|----------|
| Button | `4px 16px` | `15px 40px` | None |
| Card | `20px 15px` | `56px 35px` | None |
| Section | `2rem` | `7rem` | `$margins` map |
| Gap (tight) | `15px` | `30px` | None |
| Gap (wide) | `30px` | `93px` | None |

### Typography Hierarchy Quick Reference

| Element | Purpose | Mobile | Desktop | Weight | Color |
|---------|---------|--------|---------|--------|-------|
| h6 (eyebrow) | Labels, tags | 10px | 14px | 700 | `$blue` |
| h5 | Small headings | 14px | 20px | 300 | Default |
| h4 | Subsection | 18px | 20px | 300 | `$blueDark` |
| h3 | Section heading | 20px | 30px | 100 | Default |
| h2 | Major heading | 24px | 40px | 100 | `$blueDark` |
| h1 | Page title | 30px | 50px | 300 | `$blueDark` |

---

## LLM Quick Search Index

**By Task:**
- **Center a card:** `#card-centered` → headlineContent.module.scss
- **Text over image:** `#card-overlay` → productCard.module.scss
- **Zoom on hover:** `#hover-zoom` → cardTile.module.scss
- **Small label text:** `#text-eyebrow` → bannerImage.module.scss
- **Gradient overlay:** `#gradient-bottom-fade` → productCard.module.scss
- **List with dividers:** `#list-inline-dividers` → inline-list.module.scss
- **Center horizontally:** `#centering-horizontal` → See Centering Content section
- **Center vertically:** `#centering-vertical` → See Centering Content section

**By Component File:**
- `cardTile.tsx` → Basic card, image zoom hover
- `productCard.tsx` → Overlay card, gradient overlay, multi-effect hover
- `headlineContent.module.scss` → Centered card, flexbox centering
- `ctaTile.module.scss` → Background image card, fixed height
- `bannerImage.module.scss` → Eyebrow text, text shadows
- `inline-list.module.scss` → Inline lists with dividers
- `standardAccordion.tsx` → MUI accordion styling

**By Pattern Complexity:**
- ⭐ Simple: Basic card centering, text styles, borders
- ⭐⭐ Medium: Image zoom, basic overlays, inline lists
- ⭐⭐⭐ Complex: Overlay cards, background cards, multi-effect hovers

---

## End of Cookbook

**For architectural patterns and detailed documentation, see:**
- `ai/SEED_WEB_STYLE_GUIDE.md` - Complete style guide
- `ai/DATATYPE_IMPLEMENTATION_GUIDE.md` - UDA and data type workflows

**Document Version:** 2.0 (LLM-Optimized)
**Last Updated:** 2026-01-06
