import { useState } from 'react'
import Markdown from 'react-markdown'
import { useCreator, useGenerateBriefing, useBriefingPolling } from '@/hooks/useCreators'

export default function CreatorDetailSheet({
    channelId,
    onClose,
}: {
    channelId: string | null
    onClose: () => void
}) {
    const { data: creator, isLoading } = useCreator(channelId)
    const generateBriefing = useGenerateBriefing()
    const [briefingId, setBriefingId] = useState<string | null>(null)
    const [campaignContext, setCampaignContext] = useState('')
    const [isCopied, setIsCopied] = useState(false)
    const { data: briefing } = useBriefingPolling(briefingId)

    if (!channelId) return null

    const handleGenerate = async () => {
        try {
            const result = await generateBriefing.mutateAsync({
                channel_id: channelId,
                campaign_context: campaignContext || undefined,
            })
            setBriefingId(result.briefing_id)
        } catch {
            // Error is displayed in the UI below
        }
    }

    const handleCopy = async () => {
        if (briefing?.content) {
            await navigator.clipboard.writeText(briefing.content)
            setIsCopied(true)
            setTimeout(() => setIsCopied(false), 2000)
        }
    }

    const handleClose = () => {
        setBriefingId(null)
        setCampaignContext('')
        setIsCopied(false)
        onClose()
    }

    return (
        <>
            {/* ── Backdrop ── */}
            <div
                onClick={handleClose}
                style={{
                    position: 'fixed',
                    inset: 0,
                    background: 'rgba(0,0,0,0.5)',
                    backdropFilter: 'blur(4px)',
                    zIndex: 40,
                    animation: 'fadeIn 200ms ease-out',
                }}
            />

            {/* ── Sheet Panel ── */}
            <div
                style={{
                    position: 'fixed',
                    top: 0,
                    right: 0,
                    bottom: 0,
                    width: 520,
                    maxWidth: '90vw',
                    background: 'hsl(224 71.4% 4.1%)',
                    borderLeft: '1px solid hsl(215 27.9% 16.9%)',
                    zIndex: 50,
                    overflowY: 'auto',
                    animation: 'slideIn 250ms ease-out',
                    display: 'flex',
                    flexDirection: 'column',
                }}
            >
                {/* Header */}
                <div
                    style={{
                        padding: '20px 24px',
                        borderBottom: '1px solid hsl(215 27.9% 16.9%)',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'start',
                    }}
                >
                    <div>
                        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>
                            {isLoading ? 'Loading...' : creator?.title}
                        </h2>
                        {creator && (
                            <span style={{ fontSize: 12, color: 'hsl(217.9 10.6% 54.9%)' }}>
                                {creator.id}
                            </span>
                        )}
                    </div>
                    <button
                        onClick={handleClose}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'hsl(217.9 10.6% 64.9%)',
                            cursor: 'pointer',
                            fontSize: 20,
                            padding: 4,
                        }}
                    >
                        ✕
                    </button>
                </div>

                {/* Body */}
                {creator && (
                    <div style={{ padding: 24, flex: 1 }}>
                        {/* ── Metrics Grid ── */}
                        <div
                            style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(3, 1fr)',
                                gap: 12,
                                marginBottom: 24,
                            }}
                        >
                            <MetricCard label="Subscribers" value={formatNum(creator.subscriber_count)} />
                            <MetricCard label="Videos" value={String(creator.video_count)} />
                            <MetricCard
                                label="Alignment"
                                value={creator.alignment_score != null ? `${creator.alignment_score}/100` : 'N/A'}
                                highlight={creator.alignment_score != null && creator.alignment_score >= 70}
                            />
                        </div>

                        {/* ── Description ── */}
                        {creator.description && (
                            <div style={{ marginBottom: 24 }}>
                                <SectionTitle>About</SectionTitle>
                                <p style={{ fontSize: 13, lineHeight: 1.6, color: 'hsl(217.9 10.6% 74.9%)' }}>
                                    {creator.description}
                                </p>
                            </div>
                        )}

                        {/* ── Alignment Quotes ── */}
                        {creator.alignment_quotes && creator.alignment_quotes.length > 0 && (
                            <div style={{ marginBottom: 24 }}>
                                <SectionTitle>Justifying Quotes</SectionTitle>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                                    {creator.alignment_quotes.map((q, i) => (
                                        <blockquote
                                            key={i}
                                            style={{
                                                padding: '12px 16px',
                                                borderLeft: '3px solid hsl(263.4 70% 50.4%)',
                                                background: 'hsl(263.4 70% 50.4% / 0.06)',
                                                borderRadius: '0 8px 8px 0',
                                                fontSize: 13,
                                                lineHeight: 1.5,
                                                color: 'hsl(210 20% 90%)',
                                            }}
                                        >
                                            "{q.text}"
                                            <div
                                                style={{
                                                    marginTop: 6,
                                                    fontSize: 11,
                                                    color: 'hsl(263.4 70% 70%)',
                                                    fontWeight: 500,
                                                }}
                                            >
                                                ⏱ {q.timestamp}
                                            </div>
                                        </blockquote>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* ── Briefing Section ── */}
                        <div>
                            <SectionTitle>Engagement Briefing</SectionTitle>

                            {!briefingId && !generateBriefing.isPending && (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                                    <textarea
                                        placeholder="Campaign context (optional)… e.g., 'Sustainability campaign for Oatly'"
                                        value={campaignContext}
                                        onChange={(e) => setCampaignContext(e.target.value)}
                                        style={{
                                            width: '100%',
                                            minHeight: 72,
                                            padding: 12,
                                            borderRadius: 8,
                                            border: '1px solid hsl(215 27.9% 16.9%)',
                                            background: 'hsl(215 27.9% 6%)',
                                            color: 'hsl(210 20% 98%)',
                                            fontSize: 13,
                                            lineHeight: '1.5',
                                            outline: 'none',
                                            resize: 'vertical',
                                            fontFamily: 'inherit',
                                        }}
                                    />
                                    <button
                                        onClick={handleGenerate}
                                        style={{
                                            width: '100%',
                                            padding: '12px 20px',
                                            borderRadius: 8,
                                            border: 'none',
                                            background: 'linear-gradient(135deg, hsl(263.4 70% 50.4%), hsl(280 70% 55%))',
                                            color: 'white',
                                            fontWeight: 600,
                                            fontSize: 14,
                                            cursor: 'pointer',
                                            transition: 'transform 100ms, box-shadow 200ms',
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.transform = 'translateY(-1px)'
                                            e.currentTarget.style.boxShadow = '0 4px 20px hsl(263.4 70% 50.4% / 0.3)'
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.transform = 'translateY(0)'
                                            e.currentTarget.style.boxShadow = 'none'
                                        }}
                                    >
                                        ✨ Generate Briefing
                                    </button>
                                </div>
                            )}

                            {generateBriefing.isPending && (
                                <div style={{ textAlign: 'center', padding: 16, color: 'hsl(217.9 10.6% 64.9%)' }}>
                                    Requesting briefing...
                                </div>
                            )}

                            {generateBriefing.isError && (
                                <div
                                    style={{
                                        padding: 12,
                                        borderRadius: 8,
                                        background: 'hsl(0 62.8% 30.6% / 0.15)',
                                        color: 'hsl(0 84% 70%)',
                                        fontSize: 13,
                                        marginTop: 8,
                                    }}
                                >
                                    Failed to request briefing. Is the API running?
                                </div>
                            )}

                            {briefingId && briefing?.status === 'pending' && (
                                <div
                                    style={{
                                        textAlign: 'center',
                                        padding: 24,
                                        color: 'hsl(263.4 70% 70%)',
                                        fontSize: 13,
                                    }}
                                >
                                    <div style={{ fontSize: 24, marginBottom: 8 }}>⏳</div>
                                    Generating briefing via AI... Polling every 3s
                                    <div
                                        style={{
                                            marginTop: 12,
                                            height: 4,
                                            borderRadius: 2,
                                            background: 'hsl(215 27.9% 16.9%)',
                                            overflow: 'hidden',
                                        }}
                                    >
                                        <div
                                            style={{
                                                width: '60%',
                                                height: '100%',
                                                background: 'hsl(263.4 70% 50.4%)',
                                                borderRadius: 2,
                                                animation: 'pulse 1.5s ease-in-out infinite',
                                            }}
                                        />
                                    </div>
                                </div>
                            )}

                            {briefing?.status === 'completed' && briefing.content && (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 8 }}>
                                    <div
                                        style={{
                                            padding: 20,
                                            borderRadius: 8,
                                            background: 'hsl(215 27.9% 8%)',
                                            border: '1px solid hsl(215 27.9% 16.9%)',
                                            fontSize: 13,
                                            lineHeight: 1.7,
                                        }}
                                        className="briefing-markdown"
                                    >
                                        <Markdown>{briefing.content}</Markdown>
                                    </div>
                                    <button
                                        onClick={handleCopy}
                                        style={{
                                            padding: '10px 16px',
                                            borderRadius: 8,
                                            border: `1px solid ${isCopied ? 'hsl(142 76% 36% / 0.3)' : 'hsl(215 27.9% 16.9%)'}`,
                                            background: isCopied
                                                ? 'hsl(142 76% 36% / 0.12)'
                                                : 'hsl(263.4 70% 50.4% / 0.08)',
                                            color: isCopied ? 'hsl(142 76% 56%)' : 'hsl(263.4 70% 70%)',
                                            fontWeight: 600,
                                            fontSize: 13,
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            gap: 8,
                                            transition: 'all 200ms',
                                        }}
                                    >
                                        {isCopied ? '✅ Copied!' : '📋 Copy to Clipboard'}
                                    </button>
                                </div>
                            )}

                            {briefing?.status === 'failed' && (
                                <div
                                    style={{
                                        padding: 12,
                                        borderRadius: 8,
                                        background: 'hsl(0 62.8% 30.6% / 0.15)',
                                        color: 'hsl(0 84% 70%)',
                                        fontSize: 13,
                                        marginTop: 8,
                                    }}
                                >
                                    Briefing generation failed. {briefing.content}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>

            {/* ── Animations ── */}
            <style>{`
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
        @keyframes slideIn { from { transform: translateX(100%) } to { transform: translateX(0) } }
        @keyframes pulse { 0%, 100% { opacity: 0.4 } 50% { opacity: 1 } }
        .briefing-markdown h1, .briefing-markdown h2, .briefing-markdown h3 {
          margin-top: 16px; margin-bottom: 8px; font-weight: 600;
        }
        .briefing-markdown h1 { font-size: 18px; }
        .briefing-markdown h2 { font-size: 16px; }
        .briefing-markdown h3 { font-size: 14px; }
        .briefing-markdown p { margin-bottom: 8px; }
        .briefing-markdown ul, .briefing-markdown ol { padding-left: 20px; margin-bottom: 8px; }
        .briefing-markdown li { margin-bottom: 4px; }
        .briefing-markdown strong { color: hsl(210 20% 98%); }
      `}</style>
        </>
    )
}

// ── Sub-components ──────────────────────────────────────────────

function MetricCard({
    label,
    value,
    highlight = false,
}: {
    label: string
    value: string
    highlight?: boolean
}) {
    return (
        <div
            style={{
                padding: '14px 16px',
                borderRadius: 10,
                background: highlight ? 'hsl(142 76% 36% / 0.08)' : 'hsl(215 27.9% 10%)',
                border: `1px solid ${highlight ? 'hsl(142 76% 36% / 0.2)' : 'hsl(215 27.9% 16.9%)'}`,
            }}
        >
            <div
                style={{
                    fontSize: 11,
                    fontWeight: 500,
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    color: 'hsl(217.9 10.6% 54.9%)',
                    marginBottom: 4,
                }}
            >
                {label}
            </div>
            <div
                style={{
                    fontSize: 18,
                    fontWeight: 700,
                    color: highlight ? 'hsl(142 76% 56%)' : 'hsl(210 20% 98%)',
                }}
            >
                {value}
            </div>
        </div>
    )
}

function SectionTitle({ children }: { children: React.ReactNode }) {
    return (
        <h3
            style={{
                fontSize: 13,
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                color: 'hsl(217.9 10.6% 54.9%)',
                marginBottom: 12,
            }}
        >
            {children}
        </h3>
    )
}

function formatNum(n: number): string {
    if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
    if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
    return String(n)
}
