import type { Creator } from '@/api/client'

function ScoreBadge({ score }: { score: number | null }) {
    if (score == null)
        return (
            <span
                style={{
                    padding: '2px 8px',
                    borderRadius: 9999,
                    fontSize: 12,
                    fontWeight: 600,
                    background: 'hsl(215 27.9% 16.9%)',
                    color: 'hsl(217.9 10.6% 64.9%)',
                }}
            >
                N/A
            </span>
        )

    const hue = score >= 70 ? 'var(--score-high)' : score >= 40 ? 'var(--score-medium)' : 'var(--score-low)'

    return (
        <span
            style={{
                padding: '2px 10px',
                borderRadius: 9999,
                fontSize: 12,
                fontWeight: 700,
                background: `hsl(${hue} / 0.15)`,
                color: `hsl(${hue})`,
                minWidth: 36,
                textAlign: 'center',
                display: 'inline-block',
            }}
        >
            {score}
        </span>
    )
}

function formatSubs(count: number): string {
    if (count >= 1_000_000) return `${(count / 1_000_000).toFixed(1)}M`
    if (count >= 1_000) return `${(count / 1_000).toFixed(1)}K`
    return String(count)
}

export default function CreatorTable({
    creators,
    onSelect,
}: {
    creators: Creator[]
    onSelect: (id: string) => void
}) {
    if (creators.length === 0) {
        return (
            <div
                style={{
                    textAlign: 'center',
                    padding: 48,
                    color: 'hsl(217.9 10.6% 64.9%)',
                    borderRadius: 12,
                    border: '1px dashed hsl(215 27.9% 16.9%)',
                }}
            >
                No creators found. Try lowering the minimum score filter.
            </div>
        )
    }

    return (
        <div
            style={{
                borderRadius: 12,
                border: '1px solid hsl(215 27.9% 16.9%)',
                overflow: 'hidden',
            }}
        >
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
                <thead>
                    <tr
                        style={{
                            background: 'hsl(215 27.9% 10%)',
                            borderBottom: '1px solid hsl(215 27.9% 16.9%)',
                        }}
                    >
                        <th style={thStyle}>Creator</th>
                        <th style={{ ...thStyle, textAlign: 'right' }}>Subscribers</th>
                        <th style={{ ...thStyle, textAlign: 'right' }}>Videos</th>
                        <th style={{ ...thStyle, textAlign: 'center' }}>Alignment Score</th>
                    </tr>
                </thead>
                <tbody>
                    {creators.map((c) => (
                        <tr
                            key={c.id}
                            onClick={() => onSelect(c.id)}
                            style={{
                                borderBottom: '1px solid hsl(215 27.9% 12%)',
                                cursor: 'pointer',
                                transition: 'background 150ms',
                            }}
                            onMouseEnter={(e) =>
                                (e.currentTarget.style.background = 'hsl(263.4 70% 50.4% / 0.06)')
                            }
                            onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                        >
                            <td style={tdStyle}>
                                <div>
                                    <div style={{ fontWeight: 600 }}>{c.title}</div>
                                    <div
                                        style={{
                                            fontSize: 12,
                                            color: 'hsl(217.9 10.6% 54.9%)',
                                            marginTop: 2,
                                            maxWidth: 400,
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap',
                                        }}
                                    >
                                        {c.description || '—'}
                                    </div>
                                </div>
                            </td>
                            <td style={{ ...tdStyle, textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>
                                {formatSubs(c.subscriber_count)}
                            </td>
                            <td style={{ ...tdStyle, textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>
                                {c.video_count}
                            </td>
                            <td style={{ ...tdStyle, textAlign: 'center' }}>
                                <ScoreBadge score={c.alignment_score} />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

const thStyle: React.CSSProperties = {
    padding: '12px 16px',
    textAlign: 'left',
    fontSize: 12,
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    color: 'hsl(217.9 10.6% 54.9%)',
}

const tdStyle: React.CSSProperties = {
    padding: '12px 16px',
}
