---
name: presentation-workflow
description: Presentation/PPT creation workflow. "PPT", "프레젠테이션", "발표", "슬라이드" triggers this.
tools:
  - Read
  - Write
  - WebSearch
---

# Presentation Workflow Skill

## Triggers
- "PPT", "프레젠테이션", "발표"
- "슬라이드", "발표자료", "피치덱"
- "presentation", "deck"

## Slide Structure

### Title Slide
```yaml
elements:
  - Title (big, bold)
  - Subtitle (optional)
  - Presenter name
  - Date
  - Company logo
```

### Agenda Slide
```yaml
template: |
  # Agenda
  1. [Topic 1]
  2. [Topic 2]
  3. [Topic 3]
  4. Q&A
```

### Content Slide (6x6 Rule)
```yaml
rules:
  - Maximum 6 bullets per slide
  - Maximum 6 words per bullet
  - One idea per slide
  - Use visuals over text
```

### Data Slide
```yaml
guidelines:
  - Highlight key number
  - Simple chart (bar/line/pie)
  - Clear labels
  - Source citation
```

### Quote Slide
```yaml
template: |
  "[Quote text here]"

  — Author Name, Title
```

### Closing Slide
```yaml
elements:
  - Key takeaway
  - Call to action
  - Contact information
  - Thank you message
```

## Presentation Types

### Pitch Deck (Startup)
```yaml
slides:
  1. Title/Hook
  2. Problem
  3. Solution
  4. Market Size (TAM/SAM/SOM)
  5. Product Demo
  6. Business Model
  7. Traction/Metrics
  8. Competition
  9. Team
  10. Financials/Ask
  11. Contact
```

### Sales Presentation
```yaml
slides:
  1. Title
  2. Agenda
  3. Pain Points
  4. Our Solution
  5. Features & Benefits
  6. Case Studies
  7. Pricing
  8. Implementation
  9. Next Steps
```

### Technical Presentation
```yaml
slides:
  1. Title
  2. Problem Statement
  3. Current State
  4. Proposed Solution
  5. Architecture/Design
  6. Implementation Details
  7. Demo
  8. Results/Metrics
  9. Lessons Learned
  10. Q&A
```

### Status Update
```yaml
slides:
  1. Title
  2. Executive Summary
  3. Progress vs Plan
  4. Key Accomplishments
  5. Challenges/Blockers
  6. Next Steps
  7. Timeline
  8. Questions
```

## Design Guidelines

### Colors
```yaml
scheme:
  primary: Brand color (headlines, emphasis)
  secondary: Supporting color
  background: White or light gray
  text: Dark gray (#333) not pure black
  accent: For highlights only
```

### Typography
```yaml
fonts:
  headings: Sans-serif (bold)
  body: Sans-serif (regular)
  sizes:
    title: 44-60pt
    heading: 32-40pt
    body: 24-28pt
    caption: 18-20pt
```

### Layout
```yaml
principles:
  - Consistent margins (50-80px)
  - Align elements to grid
  - White space is good
  - Visual hierarchy clear
```

## Code for Reveal.js Slides
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/reveal.js/dist/reveal.css">
  <link rel="stylesheet" href="https://unpkg.com/reveal.js/dist/theme/white.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section>
        <h1>Title</h1>
        <p>Subtitle</p>
      </section>
      <section>
        <h2>Agenda</h2>
        <ul>
          <li>Point 1</li>
          <li>Point 2</li>
        </ul>
      </section>
    </div>
  </div>
  <script src="https://unpkg.com/reveal.js/dist/reveal.js"></script>
  <script>Reveal.initialize();</script>
</body>
</html>
```

## Checklist
```yaml
before_presenting:
  - [ ] Spell check all slides
  - [ ] Test on presentation screen
  - [ ] Check all links/videos work
  - [ ] Prepare backup (PDF/USB)
  - [ ] Practice timing (1-2 min/slide)
  - [ ] Prepare for Q&A
```
