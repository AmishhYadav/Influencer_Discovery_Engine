import { useState } from 'react'
import { useCreators } from '@/hooks/useCreators'
import CreatorTable from '@/components/CreatorTable'
import CreatorDetailSheet from '@/components/CreatorDetailSheet'

export default function Dashboard() {
    const [minScore, setMinScore] = useState<number | null>(null)
    const [page, setPage] = useState(0)
    const [selectedId, setSelectedId] = useState<string | null>(null)
    const limit = 20

    const { data, isLoading, error } = useCreators({
        limit,
        offset: page * limit,
        minScore,
    })

    return (
        <div>
            {/* ── Filters Bar ── */}
            <div
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 16,
                    marginBottom: 24,
                    flexWrap: 'wrap',
                }}
            >
                <h2 style={{ fontSize: 22, fontWeight: 700, letterSpacing: '-0.02em' }}>
                    🎯 Creator Discovery
                </h2>
                <div style={{ flex: 1 }} />
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <label
                        htmlFor="min-score"
                        style={{ fontSize: 13, color: 'hsl(217.9 10.6% 64.9%)', fontWeight: 500 }}
                    >
                        Min Score
                    </label>
                    <input
                        id="min-score"
                        type="number"
                        min={0}
                        max={100}
                        placeholder="0"
                        value={minScore ?? ''}
                        onChange={(e) => {
                            const val = e.target.value ? Number(e.target.value) : null
                            setMinScore(val)
                            setPage(0)
                        }}
                        style={{
                            width: 72,
                            padding: '6px 10px',
                            borderRadius: 6,
                            border: '1px solid hsl(215 27.9% 16.9%)',
                            background: 'hsl(224 71.4% 6%)',
                            color: 'hsl(210 20% 98%)',
                            fontSize: 13,
                            outline: 'none',
                        }}
                    />
                </div>
                {data && (
                    <span style={{ fontSize: 13, color: 'hsl(217.9 10.6% 64.9%)' }}>
                        {data.total} creator{data.total !== 1 ? 's' : ''} found
                    </span>
                )}
            </div>

            {/* ── Content ── */}
            {error && (
                <div
                    style={{
                        padding: 16,
                        borderRadius: 8,
                        background: 'hsl(0 62.8% 30.6% / 0.15)',
                        color: 'hsl(0 84% 70%)',
                        marginBottom: 16,
                    }}
                >
                    ⚠️ Failed to load creators. Is the API server running on port 8000?
                </div>
            )}

            {isLoading && (
                <div style={{ textAlign: 'center', padding: 48, color: 'hsl(217.9 10.6% 64.9%)' }}>
                    <div className="loading-spinner" style={{ marginBottom: 12 }}>⏳</div>
                    Loading creators...
                </div>
            )}

            {data && (
                <>
                    <CreatorTable creators={data.creators} onSelect={(id) => setSelectedId(id)} />

                    {/* ── Pagination ── */}
                    {data.total > limit && (
                        <div
                            style={{
                                display: 'flex',
                                justifyContent: 'center',
                                gap: 12,
                                marginTop: 20,
                            }}
                        >
                            <button
                                disabled={page === 0}
                                onClick={() => setPage((p) => Math.max(0, p - 1))}
                                style={{
                                    padding: '6px 16px',
                                    borderRadius: 6,
                                    border: '1px solid hsl(215 27.9% 16.9%)',
                                    background: page === 0 ? 'transparent' : 'hsl(263.4 70% 50.4% / 0.15)',
                                    color: page === 0 ? 'hsl(217.9 10.6% 40%)' : 'hsl(263.4 70% 70%)',
                                    cursor: page === 0 ? 'not-allowed' : 'pointer',
                                    fontSize: 13,
                                    fontWeight: 500,
                                }}
                            >
                                ← Previous
                            </button>
                            <span
                                style={{
                                    fontSize: 13,
                                    color: 'hsl(217.9 10.6% 64.9%)',
                                    lineHeight: '32px',
                                }}
                            >
                                Page {page + 1} of {Math.ceil(data.total / limit)}
                            </span>
                            <button
                                disabled={(page + 1) * limit >= data.total}
                                onClick={() => setPage((p) => p + 1)}
                                style={{
                                    padding: '6px 16px',
                                    borderRadius: 6,
                                    border: '1px solid hsl(215 27.9% 16.9%)',
                                    background:
                                        (page + 1) * limit >= data.total
                                            ? 'transparent'
                                            : 'hsl(263.4 70% 50.4% / 0.15)',
                                    color:
                                        (page + 1) * limit >= data.total
                                            ? 'hsl(217.9 10.6% 40%)'
                                            : 'hsl(263.4 70% 70%)',
                                    cursor: (page + 1) * limit >= data.total ? 'not-allowed' : 'pointer',
                                    fontSize: 13,
                                    fontWeight: 500,
                                }}
                            >
                                Next →
                            </button>
                        </div>
                    )}
                </>
            )}

            {/* ── Detail Sheet ── */}
            <CreatorDetailSheet
                channelId={selectedId}
                onClose={() => setSelectedId(null)}
            />
        </div>
    )
}
