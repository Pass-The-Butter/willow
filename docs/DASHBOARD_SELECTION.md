# 📊 Dashboard Selection: Mission Control Interface

## The Requirement

A minimalist, high-accessibility dashboard with a left-hand vertical taxonomy, optimized for chronological reporting and high-fidelity JS visualizations (D3.js).

## Selection: **Astro Starlight**

### Why Starlight?

1. **Open Source & Extensible**: Built on Astro, allowing for complete control and self-hosting on `bunny`.
2. **Accessible by Design**: Astro prioritizes light-weight, semantic HTML, which is critical for "looking after the human's ability to visualise" without sensory overload.
3. **MDX Native**: Seamlessly mixes Markdown with React/Javascript. We can drop our D3 Organograms directly into report pages.
4. **Taxonomy & Search**: Out-of-the-box support for deep nested navigation and local/AI-powered search.
5. **Silicon Valley Aesthetic**: Provides a "Mintlify-like" premium developer experience but within a fully open-source framework.

## How it supports Accessibility

- **High Contrast**: Dark mode support with clear typography (Inter/Roboto).
- **Performance**: Instant page transitions reduce cognitive lag.
- **Clarity**: The vertical sidebar provides a persistent map of the "Brain," reducing the mental effort needed to navigate complex system states.

## Implementation Path

- **Phase 1**: Initialize Starlight on `bunny` (Port 80 via Nginx).
- **Phase 2**: Create `core/skills/report_to_docs.py` to automate chronological postings.
- **Phase 3**: Embed the "Organogram" and "Memory Audit" as interactive MDX components.
