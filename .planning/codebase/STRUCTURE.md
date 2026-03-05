# Directory Structure

## Overview
*   The project root doesn't contain any application source files at the moment.
*   The only meaningful structure pertains to the GSD CLI tool extensions and Agent state.

## Key Locations
*   `.claude/` - Master folder for project tooling.
    *   `.claude/commands/` - Defines the slash commands like `/gsd:new-project` and `/gsd:map-codebase`.
    *   `.claude/get-shit-done/` - The core logic of the task automation framework.
    *   `.claude/get-shit-done/workflows/` - Concrete workflows that command definitions invoke.
*   `.planning/` - Used during GSD cycles for persistent structured state.
    *   `.planning/codebase/` - Machine-readable documentation summarizing existing code.

## Conventions
*   Using `-` separators for scripts and `.md` extensions for most rules / templates / workflows.
