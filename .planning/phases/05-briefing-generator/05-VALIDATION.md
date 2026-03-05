# Phase 5: Briefing Generator — Validation Strategy

## 1. Automated Verification (Backend)
- **Unit Tests:** Update or added tests in `tests/test_api.py` to verify that `campaign_context` is correctly received by the endpoint.
- **Prompt Logic:** Since we don't mock the LLM output in detail, we will verify that the prompt is constructed correctly in `src/api/tasks.py` using a mock for the OpenAI client if possible, or by inspecting the task logic.

## 2. Manual Visual Verification (E2E)

| Step | Action | Expected Result |
| :--- | :--- | :--- |
| 1 | Open Creator Detail Sheet | A new "Campaign Context" textarea is visible above the Generate button. |
| 2 | Enter "Oatly Sustainability" in textarea and click "Generate" | The backend receives the context. The resulting briefing mentions "Oatly" and "Sustainability". |
| 3 | Wait for Briefing Completion | The briefing renders with sections: Profile, Mission Relevance, Key Topics, Metrics, Example Content, and Talking Points. |
| 4 | Click "Copy to Clipboard" | A "Copied!" message appears temporarily. Pasting into a text editor shows the full markdown content. |

## 3. Build & Quality Checks
- `npm run build` in `frontend` must pass.
- `pytest` for all backend tests must pass.
- Verify no regressions in the briefing polling logic.

## 4. Sign-off Criteria
- The generated briefing content strictly follows the AI-02 format.
- The UI features (Textarea, Copy) are intuitive and bug-free.
- Production build is stable.
