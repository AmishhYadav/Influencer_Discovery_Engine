import { useState } from 'react'
import { useCreators } from '@/hooks/useCreators'
import FiltersToolbar from '@/components/FiltersToolbar'
import CreatorTable from '@/components/CreatorTable'
import CreatorPreviewPanel from '@/components/CreatorPreviewPanel'
import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function Dashboard() {
    const [minScore, setMinScore] = useState<number | null>(null)
    const [searchQuery, setSearchQuery] = useState('')
    const [page, setPage] = useState(0)
    const [previewId, setPreviewId] = useState<string | null>(null)
    const limit = 20

    const { data, isLoading, error } = useCreators({
        limit,
        offset: page * limit,
        minScore,
    })

    const totalPages = data ? Math.ceil(data.total / limit) : 0

    return (
        <div className="flex gap-0 -mr-8">
            {/* ── Main Content ── */}
            <div className="flex-1 min-w-0">
                {/* Page Header */}
                <div className="mb-6">
                    <h1 className="text-xl font-bold tracking-tight text-text-primary">
                        Creator Discovery
                    </h1>
                    <p className="text-sm text-text-tertiary mt-1">
                        Explore and identify high-alignment creators for your campaigns.
                    </p>
                </div>

                {/* Filters */}
                <FiltersToolbar
                    minScore={minScore}
                    onMinScoreChange={(val) => { setMinScore(val); setPage(0) }}
                    searchQuery={searchQuery}
                    onSearchChange={setSearchQuery}
                    totalCount={data?.total}
                />

                {/* Error */}
                {error && (
                    <div className="rounded-lg bg-rose-soft border border-rose/20 px-4 py-3 text-sm text-rose mb-4 animate-fade-in">
                        ⚠ Failed to load creators. Is the API server running on port 8000?
                    </div>
                )}

                {/* Table */}
                <CreatorTable
                    creators={data?.creators ?? []}
                    isLoading={isLoading}
                    onHover={setPreviewId}
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
