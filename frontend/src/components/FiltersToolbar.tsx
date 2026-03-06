import { Search, X } from 'lucide-react'

export default function FiltersToolbar({
    minScore,
    onMinScoreChange,
    searchQuery,
    onSearchChange,
    totalCount,
}: {
    minScore: number | null
    onMinScoreChange: (val: number | null) => void
    searchQuery: string
    onSearchChange: (val: string) => void
    totalCount?: number
}) {
    return (
        <div className="flex items-center gap-3 mb-6 flex-wrap">
            {/* ── Search ── */}
            <div className="relative flex-1 min-w-[200px] max-w-[360px]">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
                <input
                    type="text"
                    placeholder="Search creators…"
                    value={searchQuery}
                    onChange={(e) => onSearchChange(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 rounded-lg bg-surface-2 border border-border-subtle text-sm text-text-primary placeholder:text-text-tertiary outline-none focus:border-accent/50 transition-colors"
                />
                {searchQuery && (
                    <button
                        onClick={() => onSearchChange('')}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-0.5 hover:bg-surface-3 rounded text-text-tertiary hover:text-text-secondary transition-colors"
                    >
                        <X className="w-3.5 h-3.5" />
                    </button>
                )}
            </div>

            <div className="h-5 w-px bg-border-subtle" />

            {/* ── Score Filter ── */}
            <div className="flex items-center gap-2">
                <label className="text-xs font-medium text-text-tertiary whitespace-nowrap">
                    Min Score
                </label>
                <input
                    type="number"
                    min={0}
                    max={100}
                    placeholder="0"
                    value={minScore ?? ''}
                    onChange={(e) => {
                        const val = e.target.value ? Number(e.target.value) : null
                        onMinScoreChange(val)
                    }}
                    className="w-16 px-2.5 py-1.5 rounded-md bg-surface-2 border border-border-subtle text-sm text-text-primary outline-none focus:border-accent/50 transition-colors tabular-nums"
                />
            </div>

            {/* ── Active Filter Pills ── */}
            {minScore != null && minScore > 0 && (
                <button
                    onClick={() => onMinScoreChange(null)}
                    className="flex items-center gap-1 px-2 py-1 rounded-md bg-accent/10 text-accent text-xs font-medium hover:bg-accent/20 transition-colors"
                >
                    Score ≥ {minScore}
                    <X className="w-3 h-3" />
                </button>
            )}

            {/* ── Results Count ── */}
            <div className="ml-auto">
                {totalCount != null && (
                    <span className="text-xs text-text-tertiary tabular-nums">
                        {totalCount} creator{totalCount !== 1 ? 's' : ''}
                    </span>
                )}
            </div>
        </div>
    )
}
