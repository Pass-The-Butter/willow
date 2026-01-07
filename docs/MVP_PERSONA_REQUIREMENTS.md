# 🎭 Willow Persona Requirements: Operations & Assessment

**Date**: 2026-01-05
**Status**: ACTIVE DRAFT (MVP Focus)
**Vision Reference**: Apollo-1 / AUI.io style Human-in-the-Loop Neurosymbolic AI

---

## 🤵 Persona 1: Robin (Claims Operations Manager)

### The Objective

Robin needs a high-level view of "Stock" (outstanding claims) to optimize resourcing. In the Insurance Factory model, **Claims = Income**, so efficient processing is the primary revenue driver.

### Requirements

- **Stock Reporting**: Ability to request a weekly starting inventory of outstanding claims.
- **Performance Analytics**: Query Willow via chatbot for a bar chart showing **Claims Assessed per FTE per Hour** for the previous week.
- **Visual Aesthetic**: Premium, interactive bar charts (D3.js integration) with smooth GSAP animations for transitions.

### Operational Intent

By understanding the "Stock" level, Robin can dynamicially reassign "Human-in-the-Loop" resources or prioritize specific agent swarms.

---

## 🕵️ Persona 2: The Claims Assessor

### The Objective

A specialized human or agent role that interacts with Willow to make informed, enriched decisions on complex claims.

### Requirements

- **Claim Summarization**: Willow must provide a comprehensive view:
  - **Customer & Policy Details**: Core contract data.
  - **Claim Specifics**: Amount, incident date, Vet details.
  - **Enriched Pet History**: Vet visit logs and diagnosis history parsed from graph nodes.
- **Unstructured Data Ingestion**:
  - **Scenario**: A customer calls about a previous vet or gives more detail on a breed.
  - **Willow's Task**: Summary of the new info and assessment of its **relevance** to the current claim.
- **Human-in-the-Loop (AUI.io / Apollo-1 Pattern)**:
  - Willow follows Standard Operating Procedures (SOPs).
  - The Assessor can override, enrich, or adjust the process steps.
  - **Feedback Loop**: Human adjustments are captured and fed back into the Neurosymbolic system.

---

## 🧠 Neurosymbolic Intelligence & Self-Betterment

### The "Apollo-1" Evolution Pattern

Willow does not just run static code. It operates on a **Neurosymbolic Feedback Loop**:

1.  **Symbolic Execution**: Willow follows strict Graph-based SOPs (The "Logic").
2.  **Neural Enrichment**: Natural language data (phone calls, vet notes) is parsed via LLMs (The "Intuition").
3.  **Heuristic Refactoring**: After analyzing millions of process steps or conversations, the system:
    - Identifies bottlenecks.
    - Suggests new Heuristics.
    - **Self-Refactors**: The AI betters its own internal logic based on success/failure patterns.

### Technical Goal for MVP

- **GSAP UI**: A "beautiful" chat and dashboard interface that feels alive.
- **D3 Graph Visualization**: The "Glass Box" view where the Assessor can see _why_ a decision was proposed.
- **Relevance Scoring**: A specialized skill to determine if a piece of "Pet History" is relevant to a "Current Claim".

---

**Notes Captured By**: Willow Captain (Architect)
**Next Step**: Integrate these personas into the `/factory` GSAP scrollytelling demo.
