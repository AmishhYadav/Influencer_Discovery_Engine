# Architecture

This reflects the structure of a raw new project managed by the AI GSD framework.

## System Design
*   **Pattern**: Currently, the structure operates merely as a configuration holder for agentic workflows and AI tools.
*   **Layers**: There is no business logic tier, data layer, or presentation layer yet.

## Key Components
*   **.claude/get-shit-done**: Workflow management system script runner, and templates that act as the orchestrator for project planning and codebase management.
*   **.planning**: Holds system state, task metadata, and codebase discovery docs written by these agents.

## Data Flow
*   The data mainly flows from the User's prompts -> AI Agent -> GSD tools -> Markdown/JSON output (`.planning/`).
