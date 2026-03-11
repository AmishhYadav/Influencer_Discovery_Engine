const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export interface CreatorScoreBreakdown {
    credibility_score: number;
    engagement_score: number;
    reach_score: number;
    alignment_score: number;
    composite_score: number;
}

export interface ContentItem {
    id: string;
    source_type: string;
    title: string;
    url?: string;
    published_at?: string;
}

export interface CreatorDetail {
    id: string;
    name: string;
    platform: string;
    platform_id: string;
    profile_url?: string;
    bio?: string;
    follower_count: number;
    scores?: CreatorScoreBreakdown;
    content_items?: ContentItem[];
}

export interface CreatorSummary {
    id: string;
    name: string;
    platform: string;
    profile_url?: string;
    follower_count: number;
    credibility_score?: number;
    engagement_score?: number;
    reach_score?: number;
    alignment_score?: number;
    composite_score?: number;
}

export interface SearchResponse {
    creators: CreatorSummary[];
    total: number;
    query: string;
    sources: string[];
}

export interface CreatorListResponse {
    creators: CreatorSummary[];
    total: number;
    limit: number;
    offset: number;
}

export interface BriefingRequest {
    creator_id: string; 
    campaign_context?: string;
}

export interface BriefingAcceptedResponse {
    briefing_id: string;
}

export interface BriefingResponse {
    id: string;
    creator_id: string;
    content: string;
    status: 'pending' | 'completed' | 'failed';
    created_at: string;
    updated_at: string;
}


export const apiClient = {
    async searchCreators(query: string, sources: string[]): Promise<SearchResponse> {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, sources, max_results: 10 }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    },

    async getCreators(limit: number = 20, offset: number = 0): Promise<CreatorListResponse> {
        const response = await fetch(`${API_BASE_URL}/search/creators?limit=${limit}&offset=${offset}`);
        if (!response.ok) {
             throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    },

    async getCreatorDetail(creatorId: string): Promise<CreatorDetail> {
        // According to our routers, there's /api/search/creators/{id} (multi-source) 
        // and /api/creators/{id} (youtube channels). For simplicity, let's use the multi-source one.
        const response = await fetch(`${API_BASE_URL}/search/creators/${creatorId}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    },

    // ── Briefings ────────────────────────────────────────────────────────

    /**
     * Trigger a briefing generation for a specific creator.
     */
    async generateBriefing(creatorId: string, campaignContext?: string): Promise<BriefingAcceptedResponse> {
        const response = await fetch(`${API_BASE_URL}/briefings/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ creator_id: creatorId, campaign_context: campaignContext }),
        });
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    },

    /**
     * Retrieve the status and content of a briefing by its ID.
     */
    async getBriefingStatus(briefingId: string): Promise<BriefingResponse> {
        const response = await fetch(`${API_BASE_URL}/briefings/${briefingId}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    }
};
