const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface Creator {
    id: string
    title: string
    description: string
    subscriber_count: number
    video_count: number
    alignment_score: number | null
}

export interface CreatorDetail extends Creator {
    alignment_quotes: Array<{ text: string; timestamp: string }> | null
}

export interface CreatorListResponse {
    creators: Creator[]
    total: number
    limit: number
    offset: number
}

export interface BriefingResponse {
    id: string
    channel_id: string
    content: string | null
    status: string
}

export interface BriefingAcceptedResponse {
    status: string
    briefing_id: string
}

// ── Creators ─────────────────────────────────────────────────────

export async function fetchCreators(params: {
    limit?: number
    offset?: number
    minScore?: number | null
}): Promise<CreatorListResponse> {
    const searchParams = new URLSearchParams()
    searchParams.set('limit', String(params.limit ?? 20))
    searchParams.set('offset', String(params.offset ?? 0))
    if (params.minScore != null) {
        searchParams.set('min_score', String(params.minScore))
    }

    const res = await fetch(`${API_URL}/api/creators?${searchParams}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

export async function fetchCreator(id: string): Promise<CreatorDetail> {
    const res = await fetch(`${API_URL}/api/creators/${id}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

// ── Briefings ────────────────────────────────────────────────────

export async function generateBriefing(params: {
    channel_id: string
    campaign_context?: string
}): Promise<BriefingAcceptedResponse> {
    const res = await fetch(`${API_URL}/api/briefings/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

export async function fetchBriefing(briefingId: string): Promise<BriefingResponse> {
    const res = await fetch(`${API_URL}/api/briefings/${briefingId}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

// ── Multi-Source Types ───────────────────────────────────────────

export type Platform = 'youtube' | 'blog' | 'twitter' | 'instagram' | 'academic'

export interface MultiCreator {
    id: string
    name: string
    platform: Platform
    platform_id: string | null
    profile_url: string | null
    follower_count: number
    credibility_score: number | null
    engagement_score: number | null
    reach_score: number | null
    alignment_score: number | null
    composite_score: number | null
}

export interface ContentItem {
    id: string
    source_type: string
    title: string
    text_content: string
    url: string | null
    published_at: string
    engagement_metrics: Record<string, number> | null
}

export interface CompositeScoreBreakdown {
    credibility_score: number
    engagement_score: number
    reach_score: number
    alignment_score: number
    composite_score: number
}

export interface MultiCreatorDetail {
    id: string
    name: string
    platform: Platform
    platform_id: string
    profile_url: string
    bio: string
    follower_count: number
    scores: CompositeScoreBreakdown
    content_items: ContentItem[]
}

export interface MultiCreatorListResponse {
    creators: MultiCreator[]
    total: number
    limit: number
    offset: number
}

export interface SearchRequest {
    query: string
    sources: Platform[]
    max_results: number
}

export interface SearchResponse {
    creators: MultiCreator[]
    total: number
    query: string
    sources: string[]
}

// ── Multi-Source API Calls ────────────────────────────────────────

export async function fetchMultiCreators(params: {
    limit?: number
    offset?: number
    platform?: Platform | null
    minScore?: number | null
}): Promise<MultiCreatorListResponse> {
    const searchParams = new URLSearchParams()
    searchParams.set('limit', String(params.limit ?? 20))
    searchParams.set('offset', String(params.offset ?? 0))
    if (params.platform) {
        searchParams.set('platform', params.platform)
    }
    if (params.minScore != null) {
        searchParams.set('min_score', String(params.minScore))
    }

    const res = await fetch(`${API_URL}/api/search/creators?${searchParams}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

export async function fetchMultiCreator(id: string): Promise<MultiCreatorDetail> {
    const res = await fetch(`${API_URL}/api/search/creators/${id}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

export async function searchCreators(request: SearchRequest): Promise<SearchResponse> {
    const res = await fetch(`${API_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}
