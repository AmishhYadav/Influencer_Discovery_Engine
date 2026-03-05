# Phase 4: Frontend Dashboard — Validation Strategy

## 1. Test Infrastructure Setup
While we have a strong backend testing suite (`pytest`), setting up a full frontend testing suite (Jest/Cypress/Playwright) for an early-stage MVP UI can slow down rapid iteration. 

**MVP Strategy:** 
We will rely on **Manual Visual Verification** coupled with automated **Type Checking / Linting** (`tsc` and `eslint`).

If automated tests are strictly required later, we can introduce Vitest.

## 2. API Mocking vs. Live Backend
For manual testing, we will run the React frontend against the actual local FastAPI server (`uvicorn src.api.main:app`), pointing to a pre-populated SQLite database. This ensures end-to-end (E2E) integration is validated.

## 3. Human Verification Map

The human operator should start both servers:
1. `uvicorn src.api.main:app` (Backend)
2. `npm run dev` in the frontend directory (Frontend)

Open `http://localhost:5173` and perform the following:

| Req ID | Task Description | Verification Method | Sign-off Criteria |
| :--- | :--- | :--- | :--- |
| UI-01 | Creator list & filtering | View the main dashboard page. Change the "Min Score" filter. | The list correctly populates with mock DB data. Changing the filter immediately updates the results via React Query. |
| UI-02 | Creator profile | Click a creator row in the table. | A Sheet or Dialog opens showing the full description, metrics, and alignment quotes from the DB. |
| UI-03 | Briefing generation | In the profile view, click "Generate Briefing". | A loading state appears. After several seconds, the polling completes and the rendered markdown briefing is displayed within the UI. |

## 4. Quality & Build Checks
Before signing off on Phase 4, the following must pass:
1. `npm run lint` — No ESLint errors.
2. `npm run build` — `tsc && vite build` completes successfully. The production bundle must compile without type errors.

## 5. Sign-off Criteria
*   The dashboard looks aesthetically pleasing and modern (Tailwind + Shadcn).
*   All three key workflows (List, Detail, Generate Briefing) function seamlessly against the live local FastAPI backend.
*   The project builds successfully for production.
