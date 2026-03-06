import { useState, useEffect } from 'react'
import { useParams, useNavigate, useSearchParams } from 'react-router-dom'
import { ArrowLeft, Users, Video, Sparkles, ExternalLink } from 'lucide-react'
import { useCreator, useGenerateBriefing, useBriefingPolling } from '@/hooks/useCreators'
import AlignmentScoreBadge from '@/components/AlignmentScoreBadge'
import QuoteEvidenceList from '@/components/QuoteEvidenceList'
import BriefingViewer from '@/components/BriefingViewer'
import Skeleton from '@/components/Skeleton'

export default function CreatorProfile() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()
    const { data: creator, isLoading } = useCreator(id ?? null)
    const generateBriefing = useGenerateBriefing()
    const [briefingId, setBriefingId] = useState<string | null>(null)
    const [campaignContext, setCampaignContext] = useState('')
    const { data: briefing } = useBriefingPolling(briefingId)

    // Auto-trigger briefing generation if navigated with ?generate=true
    useEffect(() => {
        if (searchParams.get('generate') === 'true' && id && !briefingId && !generateBriefing.isPending) {
            handleGenerate()
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchParams, id])

    const handleGenerate = async () => {
        if (!id) return
        try {
            const result = await generateBriefing.mutateAsync({
                channel_id: id,
                campaign_context: campaignContext || undefined,
            })
            setBriefingId(result.briefing_id)
        } catch {
            // Error shown in UI
        }
    }

    return (
        <div className="animate-fade-in">
            {/* ── Back Button ── */}
            <button
                onClick={() => navigate('/')}
                className="flex items-center gap-1.5 text-xs text-text-tertiary hover:text-text-secondary transition-colors mb-6 font-medium"
            >
                <ArrowLeft className="w-3.5 h-3.5" />
                Back to Discovery
            </button>

            {isLoading ? (
                <div className="space-y-6">
                    <Skeleton className="h-7 w-64" />
                    <Skeleton className="h-4 w-96" />
                    <div className="grid grid-cols-3 gap-3 max-w-[480px]">
                        <Skeleton className="h-20 rounded-xl" />
                        <Skeleton className="h-20 rounded-xl" />
                        <Skeleton className="h-20 rounded-xl" />
                    </div>
                </div>
            ) : creator ? (
                <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
                    {/* ── Left Column ── */}
                    <div className="space-y-8">
                        {/* Header */}
                        <div>
                            <div className="flex items-center gap-3 mb-2">
                                <div className="w-10 h-10 rounded-xl bg-surface-3 flex items-center justify-center text-text-tertiary text-lg font-bold">
                                    {creator.title.charAt(0).toUpperCase()}
                                </div>
                                <div>
                                    <h1 className="text-lg font-bold tracking-tight text-text-primary">
                                        {creator.title}
                                    </h1>
                                    <p className="text-[11px] text-text-tertiary font-mono">{creator.id}</p>
                                </div>
                            </div>
                            {creator.description && (
                                <p className="text-sm text-text-secondary leading-relaxed mt-3 max-w-[560px]">
                                    {creator.description}
                                </p>
                            )}
                        </div>

                        {/* Metrics */}
                        <div className="grid grid-cols-3 gap-3 max-w-[480px]">
                            <MetricCard
                                icon={<Users className="w-3.5 h-3.5" />}
                                label="Subscribers"
                                value={formatNum(creator.subscriber_count)}
                            />
                            <MetricCard
                                icon={<Video className="w-3.5 h-3.5" />}
                                label="Videos"
                                value={String(creator.video_count)}
                            />
                            <div className="bg-surface-2 rounded-xl border border-border-subtle p-4 flex flex-col items-center justify-center">
                                <AlignmentScoreBadge score={creator.alignment_score} size={48} />
                                <span className="text-[10px] text-text-tertiary font-medium mt-1.5 uppercase tracking-wider">
                                    Alignment
                                </span>
                            </div>
                        </div>

                        {/* Quotes */}
                        <div>
                            <SectionHeading>Supporting Evidence</SectionHeading>
                            <QuoteEvidenceList quotes={creator.alignment_quotes ?? []} />
                        </div>
                    </div>

                    {/* ── Right Column: Briefing ── */}
                    <div className="space-y-5">
                        <SectionHeading>Engagement Briefing</SectionHeading>

                        {!briefingId && !generateBriefing.isPending && (
                            <div className="space-y-3">
                                <textarea
                                    placeholder="Campaign context (optional)… e.g., 'Sustainability campaign for Oatly'"
                                    value={campaignContext}
                                    onChange={(e) => setCampaignContext(e.target.value)}
                                    className="w-full min-h-[80px] p-3 rounded-lg bg-surface-2 border border-border-subtle text-sm text-text-primary placeholder:text-text-tertiary outline-none focus:border-accent/50 transition-colors resize-vertical font-sans"
                                />
                                <button
                                    onClick={handleGenerate}
                                    className="flex items-center justify-center gap-2 w-full px-4 py-3 rounded-lg bg-accent text-white text-sm font-semibold hover:bg-accent-hover transition-all hover:shadow-lg hover:shadow-accent/20"
                                >
                                    <Sparkles className="w-4 h-4" />
                                    Generate Briefing
                                </button>
                            </div>
                        )}

                        {generateBriefing.isPending && (
                            <div className="flex items-center justify-center py-6 text-sm text-text-tertiary">
                                <div className="w-4 h-4 border-2 border-accent/30 border-t-accent rounded-full animate-spin mr-2" />
                                Requesting briefing…
                            </div>
                        )}

                        {generateBriefing.isError && (
                            <div className="rounded-lg bg-rose-soft border border-rose/20 px-4 py-3 text-sm text-rose">
                                Failed to request briefing. Is the API running?
                            </div>
                        )}

                        {briefingId && briefing?.status === 'pending' && (
                            <div className="text-center py-8 space-y-3">
                                <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin mx-auto" />
                                <p className="text-xs text-text-tertiary">
                                    Generating briefing via AI…
                                </p>
                                <div className="h-1 rounded bg-surface-3 overflow-hidden max-w-[200px] mx-auto">
                                    <div className="h-full bg-accent rounded animate-skeleton w-3/5" />
                                </div>
                            </div>
                        )}

                        {briefing?.status === 'completed' && briefing.content && (
                            <BriefingViewer content={briefing.content} />
                        )}

                        {briefing?.status === 'failed' && (
                            <div className="rounded-lg bg-rose-soft border border-rose/20 px-4 py-3 text-sm text-rose">
                                Briefing generation failed. {briefing.content}
                            </div>
                        )}
                    </div>
                </div>
            ) : null}
        </div>
    )
}

// ── Sub-components ──────────────────────────────────────────────

function MetricCard({
    icon,
    label,
    value,
}: {
    icon: React.ReactNode
    label: string
    value: string
}) {
    return (
        <div className="bg-surface-2 rounded-xl border border-border-subtle p-4">
            <div className="flex items-center gap-1.5 mb-1.5">
                <span className="text-text-tertiary">{icon}</span>
                <span className="text-[10px] uppercase tracking-wider text-text-tertiary font-medium">
                    {label}
                </span>
            </div>
            <div className="text-lg font-bold text-text-primary tabular-nums">{value}</div>
        </div>
    )
}

function SectionHeading({ children }: { children: React.ReactNode }) {
    return (
        <h2 className="text-[11px] font-semibold uppercase tracking-widest text-text-tertiary mb-3">
            {children}
        </h2>
    )
}

function formatNum(n: number): string {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
    return String(n)
}
