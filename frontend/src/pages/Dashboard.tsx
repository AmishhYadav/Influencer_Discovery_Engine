import { useState } from 'react'
import { useCreators, useMultiCreators } from '@/hooks/useCreators'
import FiltersToolbar from '@/components/FiltersToolbar'
import CreatorTable from '@/components/CreatorTable'
import CreatorPreviewPanel from '@/components/CreatorPreviewPanel'
import { ChevronLeft, ChevronRight, Layers } from 'lucide-react'
import type { Platform } from '@/api/client'

export default function Dashboard() {
    const [minScore, setMinScore] = useState<number | null>(null)
    const [searchQuery, setSearchQuery] = useState('')
    const [page, setPage] = useState(0)
    const [previewId, setPreviewId] = useState<string | null>(null)
    const [platform, setPlatform] = useState<Platform | null>(null)
    const [viewMode, setViewMode] = useState<'youtube' | 'multi'>('youtube')
    const limit = 20

    // YouTube-only creators (original)
    const youtubeQuery = useCreators({
        limit,
        offset: page * limit,
        minScore,
    })

    // Multi-source creators (new)
    const multiQuery = useMultiCreators({
        limit,
        offset: page * limit,
        platform,
        minScore,
    })

    const isMulti = viewMode === 'multi'
    const data = isMulti ? multiQuery.data : youtubeQuery.data
    const isLoading = isMulti ? multiQuery.isLoading : youtubeQuery.isLoading
    const error = isMulti ? multiQuery.error : youtubeQuery.error
    const totalPages = data ? Math.ceil(data.total / limit) : 0

    // Transform multi-source creators to match the CreatorTable's expected format
    const tableCreators = isMulti && multiQuery.data
        ? multiQuery.data.creators.map((c) => ({
            id: c.id,
            title: c.name,
            description: `${c.platform} • ${c.profile_url || ''}`,
            subscriber_count: c.follower_count,
            video_count: 0,
            alignment_score: c.composite_score,
            platform: c.platform,
        }))
        : youtubeQuery.data?.creators ?? []

    return (
        <div className="flex gap-0 -mr-8">
            {/* ── Main Content ── */}
            <div className="flex-1 min-w-0">
                {/* Page Header */}
                <div className="mb-6 flex items-center justify-between">
                    <div>
                        <h1 className="text-xl font-bold tracking-tight text-text-primary">
                            Creator Discovery
                        </h1>
                        <p className="text-sm text-text-tertiary mt-1">
                            Explore and identify high-alignment creators for your campaigns.
                        </p>
                    </div>

                    {/* View Mode Toggle */}
                    <div className="flex items-center gap-1 bg-surface-2 rounded-lg p-1 border border-border-subtle">
                        <button
                            onClick={() => { setViewMode('youtube'); setPlatform(null); setPage(0) }}
                            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${viewMode === 'youtube'
                                    ? 'bg-accent/15 text-accent'
                                    : 'text-text-tertiary hover:text-text-secondary'
                                }`}
                        >
                            YouTube
                        </button>
                        <button
                            onClick={() => { setViewMode('multi'); setPage(0) }}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${viewMode === 'multi'
                                    ? 'bg-accent/15 text-accent'
                                    : 'text-text-tertiary hover:text-text-secondary'
                                }`}
                        >
                            <Layers className="w-3.5 h-3.5" />
                            All Sources
                        </button>
                    </div>
                </div>

                {/* Filters */}
                <FiltersToolbar
                    minScore={minScore}
                    onMinScoreChange={(val) => { setMinScore(val); setPage(0) }}
                    searchQuery={searchQuery}
                    onSearchChange={setSearchQuery}
                    totalCount={data?.total}
                    platform={isMulti ? platform : undefined}
                    onPlatformChange={isMulti ? ((val) => { setPlatform(val); setPage(0) }) : undefined}
                />

                {/* Error */}
                {error && (
                    <div className="rounded-lg bg-rose-soft border border-rose/20 px-4 py-3 text-sm text-rose mb-4 animate-fade-in">
                        ⚠ Failed to load creators. Is the API server running on port 8000?
                    </div>
                )}

                {/* Table */}
                <CreatorTable
                    creators={tableCreators}
                    isLoading={isLoading}
                    onHover={setPreviewId}
                    showPlatform={isMulti}
                />

                {/* Pagination */}
                {totalPages > 1 && (
                    <div className="flex items-center justify-center gap-3 mt-5">
                        <button
                            disabled={page === 0}
                            onClick={() => setPage((p) => Math.max(0, p - 1))}
                            className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-surface-2 border border-border-subtle text-text-secondary hover:bg-surface-3 hover:text-text-primary"
                        >
                            <ChevronLeft className="w-3.5 h-3.5" />
                            Previous
                        </button>
                        <span className="text-xs text-text-tertiary tabular-nums">
                            {page + 1} / {totalPages}
                        </span>
                        <button
                            disabled={(page + 1) * limit >= (data?.total ?? 0)}
                            onClick={() => setPage((p) => p + 1)}
                            className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-surface-2 border border-border-subtle text-text-secondary hover:bg-surface-3 hover:text-text-primary"
                        >
                            Next
                            <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                    </div>
                )}
            </div>

            {/* ── Preview Panel ── */}
            {previewId && (
                <CreatorPreviewPanel
                    channelId={previewId}
                    onClose={() => setPreviewId(null)}
                />
            )}
        </div>
    )
}
