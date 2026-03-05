# Phase 4: Frontend Dashboard — Context & Decisions

## Objective
Build a web-based dashboard for human coordinators to explore, sort, and filter the discovered creators, and view their alignment profiles (Requirements UI-01, UI-02, UI-03).

## User Decisions & Constraints
The user has opted for the recommended modern, lightweight frontend stack:

**1. Framework: Vite + React (SPA)**
- **Decision:** Pure Client-Side SPA (Option A).
- **Details:** Since this is an internal tool, we do not need the complexity of Server-Side Rendering (SSR) or SEO optimization that Next.js provides. React running via Vite will give us a blazing fast development server and a simple static build.

**2. Styling & Component Library: Tailwind CSS + Shadcn UI**
- **Decision:** Tailwind + Shadcn (Option A).
- **Details:** We will use Tailwind for utility-first styling and Shadcn UI for beautiful, accessible, copy-paste components (Tables, Cards, Buttons, Dialogs). This ensures a premium "dashboard" feel without the bloat of a heavy monolithic library like Material UI.

**3. Data Fetching & State: React Query**
- **Decision:** TanStack Query / React Query (Option A).
- **Details:** Instead of writing complex `useEffect` hooks for every API call, we will use React Query. It handles caching, loading states, error states, and background refetching out of the box, drastically reducing boilerplate when interacting with our FastAPI backend.

## Architecture
The application will consist of two primary views:
1. **Creator List View (UI-01):** A paginated data table showing channels, subscriber counts, and alignment scores. Include filters for minimum score.
2. **Creator Detail Sidebar/Dialog (UI-02, UI-03):** Clicking a row opens a detailed view showing the channel's description, the specific quotes that justified the score, and a button to trigger the async Briefing Generator.
