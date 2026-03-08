# Phase 4: Frontend Dashboard — Research & Technical Strategy

## Objective
Build a web-based dashboard for human coordinators to explore, sort, and filter the discovered creators, and view their alignment profiles (Requirements UI-01, UI-02, UI-03).

## Tech Stack Overview
1. **Framework:** React 18, scaffolded with Vite (`npm create vite@latest frontend -- --template react-ts`).
2. **Styling:** Tailwind CSS (`tailwindcss`, `postcss`, `autoprefixer`).
3. **Component Library:** Shadcn UI (Radix UI primitives + Tailwind).
4. **Data Fetching:** TanStack Query (React Query) for caching and server state.
5. **Routing:** `react-router-dom` for client-side routing (even if it's just one or two pages, it helps manage state via URL params).
6. **Icons:** `lucide-react` (standard with Shadcn).

## Core Concepts & State Management

**1. Creator Discovery (UI-01)**
- **Route:** `/`
- **State:** `page` (number), `minScore` (number). These should ideally be synced with the URL search params so links are shareable.
- **Data Hook:** `useCreators({ limit, offset, min_score })` -> calls `GET /api/creators`.
- **UI:** A data table or grid of cards showing creator avatars (optional), names, subscriber counts, and alignment scores. 

**2. Creator Profile & Quotes (UI-02)**
- **Route:** `/creator/:id` (or a slide-out sheet/dialog on the main `/` route to keep context). A Sheet (Slide-over) is highly recommended for this "discovery" workflow so the user doesn't lose their place in the list.
- **Data Hook:** `useCreator(id)` -> calls `GET /api/creators/{channel_id}`.
- **UI:** Shows description, metrics, and the `alignment_quotes` array (text + timestamp).

**3. Briefing Generator Trigger (UI-03)**
- **UI:** A prominent "Generate Briefing" button inside the Creator Profile.
- **Action:** Triggers a `useMutation` that calls `POST /api/briefings/generate`.
- **Follow-up:** Since generation is async, the UI needs to poll or show a loading state until the briefing is ready.
  - *MVP approach:* Start polling `GET /api/briefings/{id}` every 3 seconds until `status === "completed"`, then display the markdown content.
  - *UI Component:* Markdown rendered via `react-markdown`.

## FastAPI Integration (CORS)
We already configured `CORSMiddleware` in `src/api/main.py` allowing all origins `["*"]` so the React dev server (e.g., `localhost:5173`) can freely talk to the FastAPI backend (`localhost:8000`).
The Vite app should use an environment variable (e.g., `VITE_API_URL: http://localhost:8000`) for API calls.

## Shadcn UI Tooling Strategy
Instead of installing all of shadcn at once, we will initialize the project (`npx shadcn-ui@latest init`) and then add specific components as needed:
- `button`
- `table`
- `card`
- `sheet` (for the creator detail pull-out)
- `badge` (for alignment scores)
- `input` (for score filtering)
- `skeleton` (for loading states)
