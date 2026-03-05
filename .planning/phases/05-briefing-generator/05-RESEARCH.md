# Phase 5: Briefing Generator — Research & Technical Strategy

## Objective
Finalize and polish the AI-powered outreach briefing generator to strictly comply with requirement AI-02 and enhance the user experience with custom context and export capabilities.

## Technical Strategy

### 1. Prompt Refinement (Backend)
- **Location:** `src/api/tasks.py`
- **Change:** Update `BRIEFING_PROMPT_TEMPLATE` to include the following sections specifically mentioned in AI-02:
    - **Creator Profile:** Summary of the creator.
    - **Mission Relevance:** Detailed alignment with the campaign goal.
    - **Key Topics:** Main themes identified in their content.
    - **Metrics:** Subscriber and engagement highlights.
    - **Example Content:** Specific excerpts or quotes (already included but will be better labeled).
    - **Suggested Talking Points:** 3-5 specific hooks for outreach.
- **Context Handling:** Ensure `campaign_context` is properly integrated into the prompt if provided.

### 2. UI Enhancements (Frontend)
- **Location:** `frontend/src/components/CreatorDetailSheet.tsx`
- **Additions:**
    - **Textarea for Campaign Context:** A simple input field allowing the user to provide additional context before clicking "Generate Briefing".
    - **Copy to Clipboard Button:** A button that appears once the briefing is generated. It will use `navigator.clipboard.writeText()` to copy the raw markdown.
- **State Management:** Track the `campaignContext` in the `CreatorDetailSheet` component and pass it to the `useGenerateBriefing` mutation.

### 3. API Review
- **Endpoint:** `POST /api/briefings/generate`
- **Schema:** 
    - `BriefingRequest`: already includes `channel_id` and `campaign_context: Optional[str]`. No changes needed.

## Design Considerations
- **Markdown Rendering:** Ensure the `react-markdown` styling remains readable for the new sections.
- **User Feedback:** Show a clear "Copied!" state when the clipboard action is successful.
- **Placeholder Text:** The campaign context textarea should have a helpful placeholder like "e.g., Sustainability campaign for Oatly..."
