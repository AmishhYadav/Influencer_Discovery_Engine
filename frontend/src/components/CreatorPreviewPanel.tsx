import { useNavigate } from 'react-router-dom'
import { Sparkles, ExternalLink } from 'lucide-react'
import { useCreator } from '@/hooks/useCreators'
import AlignmentScoreBadge from './AlignmentScoreBadge'
import Skeleton from './Skeleton'

export default function CreatorPreviewPanel({
    channelId,
    onClose,
}: {
    channelId: string | null
    onClose: () => void
}) {
    const { data: creator, isLoading } = useCreator(channelId)
    const navigate = useNavigate()

    if (!channelId) return null

    return (
        <div className="w-[320px] shrink-0 border-l border-border-subtle bg-surface-1 animate-slide-in overflow-y-auto">
            <div className="p-5">
                {/* ── Header ── */}
                <div className="flex items-start justify-between mb-5">
                    <span className="text-[10px] font-semibold uppercase tracking-widest text-text-tertiary">
                        Quick Preview
                    </span>
                    <button
                        onClick={onClose}
                        className="text-text-tertiary hover:text-text-secondary text-sm transition-colors"
                    >
                        ✕
                    </button>
                </div>

                {isLoading ? (
                    <div className="space-y-4">
                        <Skeleton className="h-5 w-40" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-3/4" />
                        <div className="flex justify-center py-4">
                            <Skeleton className="h-16 w-16 rounded-full" />
                        </div>
                        <Skeleton className="h-20 w-full rounded-lg" />
                    </div>
                ) : creator ? (
                    <div className="space-y-5">
                        {/* Name */}
                        <div>
                            <h3 className="text-[15px] font-semibold text-text-primary leading-tight">
                                {creator.title}
                            </h3>
                            <p className="text-[11px] text-text-tertiary mt-1 font-mono">
                                {creator.id}
                            </p>
                        </div>

                        {/* Score Ring */}
                        <div className="flex flex-col items-center py-3">
                            <AlignmentScoreBadge score={creator.alignment_score} size={64} />
                            <span className="text-[11px] text-text-tertiary mt-2 font-medium">
                                Alignment Score
                            </span>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-2 gap-2">
                            <div className="bg-surface-2 rounded-lg px-3 py-2.5">
                                <div className="text-[10px] uppercase tracking-wider text-text-tertiary font-medium">Subs</div>
                                <div className="text-sm font-semibold text-text-primary mt-0.5 tabular-nums">
                                    {formatNum(creator.subscriber_count)}
                                </div>
                            </div>
                            <div className="bg-surface-2 rounded-lg px-3 py-2.5">
                                <div className="text-[10px] uppercase tracking-wider text-text-tertiary font-medium">Videos</div>
                                <div className="text-sm font-semibold text-text-primary mt-0.5 tabular-nums">
                                    {creator.video_count}
                                </div>
                            </div>
                        </div>

                        {/* Top Quote */}
                        {creator.alignment_quotes && creator.alignment_quotes.length > 0 && (
                            <div>
                                <div className="text-[10px] uppercase tracking-wider text-text-tertiary font-medium mb-2">
                                    Top Quote
                                </div>
                                <blockquote className="text-xs text-text-secondary leading-relaxed border-l-2 border-accent/40 pl-3 italic">
                                    "{creator.alignment_quotes[0].text}"
                                    <span className="block text-[10px] text-accent/70 mt-1 not-italic font-medium">
                                        ⏱ {creator.alignment_quotes[0].timestamp}
                                    </span>
                                </blockquote>
                            </div>
                        )}

                        {/* Actions */}
                        <div className="flex flex-col gap-2 pt-2">
                            <button
                                onClick={() => navigate(`/creator/${creator.id}`)}
                                className="flex items-center justify-center gap-2 w-full px-4 py-2.5 rounded-lg bg-accent text-white text-xs font-semibold hover:bg-accent-hover transition-colors"
                            >
                                <ExternalLink className="w-3.5 h-3.5" />
                                View Full Profile
                            </button>
                            <button
                                onClick={() => navigate(`/creator/${creator.id}?generate=true`)}
                                className="flex items-center justify-center gap-2 w-full px-4 py-2.5 rounded-lg bg-surface-2 border border-border-subtle text-text-secondary text-xs font-semibold hover:bg-surface-3 hover:text-text-primary transition-colors"
                            >
                                <Sparkles className="w-3.5 h-3.5" />
                                Generate Briefing
                            </button>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    )
}

function formatNum(n: number): string {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
    return String(n)
}
