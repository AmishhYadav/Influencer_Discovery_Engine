import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { useBriefingPolling } from '@/hooks/useCreators'
import BriefingViewer from '@/components/BriefingViewer'
import Skeleton from '@/components/Skeleton'

export default function BriefingView() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const { data: briefing, isLoading } = useBriefingPolling(id ?? null)

    return (
        <div className="animate-fade-in max-w-[720px]">
            {/* ── Back Button ── */}
            <button
                onClick={() => navigate(-1)}
                className="flex items-center gap-1.5 text-xs text-text-tertiary hover:text-text-secondary transition-colors mb-6 font-medium"
            >
                <ArrowLeft className="w-3.5 h-3.5" />
                Back
            </button>

            <h1 className="text-xl font-bold tracking-tight text-text-primary mb-6">
                Briefing Report
            </h1>

            {isLoading ? (
                <div className="space-y-4">
                    <Skeleton className="h-5 w-48" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-32 w-full rounded-xl" />
                </div>
            ) : briefing?.status === 'completed' && briefing.content ? (
                <BriefingViewer content={briefing.content} />
            ) : briefing?.status === 'pending' ? (
                <div className="text-center py-12 space-y-3">
                    <div className="w-8 h-8 border-2 border-accent/30 border-t-accent rounded-full animate-spin mx-auto" />
                    <p className="text-sm text-text-tertiary">
                        Generating briefing…
                    </p>
                </div>
            ) : briefing?.status === 'failed' ? (
                <div className="rounded-lg bg-rose-soft border border-rose/20 px-4 py-3 text-sm text-rose">
                    Briefing generation failed. {briefing.content}
                </div>
            ) : (
                <p className="text-sm text-text-tertiary">Briefing not found.</p>
            )}
        </div>
    )
}
