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

export async function generateBriefing(channelId: string): Promise<BriefingAcceptedResponse> {
    const res = await fetch(`${API_URL}/api/briefings/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ channel_id: channelId }),
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}

export async function fetchBriefing(briefingId: string): Promise<BriefingResponse> {
    const res = await fetch(`${API_URL}/api/briefings/${briefingId}`)
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
}
