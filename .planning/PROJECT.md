# Influencer Discovery Engine

## What This Is

An AI-powered discovery engine to help advocacy organizations identify credible, non-activist influencers whose content naturally aligns with animal advocacy values. It analyzes public content (initially focused on YouTube) to score and rank candidates based on thematic alignment, generating concrete outreach briefing kits for human coordinators.

## Core Value

Identify highly credible, naturally aligned creative voices (like doctors and scientists) using existing content signals without selecting for polarizing activism.

## Requirements

### Validated

*   ✓ [Codebase mapped] — Initial empty state mapped.

### Active

*   [ ] Build a YouTube data collection pipeline (transcripts, descriptions, tags, engagement, subscribers).
*   [ ] Create an NLP analysis engine for topic and semantic alignment (detecting themes like plant-based health or sustainability).
*   [ ] Implement a scoring and ranking algorithm (scoring credibility, audience size, engagement, value alignment).
*   [ ] Build an API backend for querying candidates.
*   [ ] Create a React dashboard for searching and exploring influencers.
*   [ ] Develop an AI module to generate outreach briefing kits (bulleted cheat sheets for coordinators).

### Out of Scope

*   Written content sources (blogs, academic papers) — Deferred to post-MVP to focus efforts on validating the YouTube pipeline.
*   Fully automated email sending — Out of scope for MVP; the goal is to equip human coordinators, not replace them.
*   Explicit activist identification — Anti-goal. The system actively deprioritizes polarizing or explicitly activist messaging in favor of soft activism / natural alignment.

## Context

*   **Target Users**: Advocacy outreach teams and coordinators.
*   **Key Profile**: Credible professionals (doctors, chefs, environmental scientists, nutrition experts) whose primary identity is not activism.
*   **Current State**: Greenfield execution within the GSD framework. Existing directory is merely system tooling.

## Constraints

*   **Data Limit**: MVP constrained to YouTube as the single source of truth for rich signals.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| YouTube-first MVP | Provides the richest multi-modal signals (transcripts + metrics) for initial validation. | — Pending |
| Bulleted Briefing Output | Outreach needs precise, actionable context, not long prose or automated templates. | — Pending |

---
*Last updated: 2026-03-06 after initialization*
