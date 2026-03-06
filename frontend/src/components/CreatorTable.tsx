import { useNavigate } from 'react-router-dom'
import { ArrowRight, Users, Video } from 'lucide-react'
import type { Creator } from '@/api/client'
import AlignmentScoreBadge from './AlignmentScoreBadge'
import PlatformBadge from './PlatformBadge'
import Skeleton from './Skeleton'
import EmptyState from './EmptyState'

type TableCreator = Creator & { platform?: string }

function formatSubs(count: number): string {
    if (count >= 1_000_000) return `${(count / 1_000_000).toFixed(1)}M`
    if (count >= 1_000) return `${(count / 1_000).toFixed(1)}K`
    return String(count)
}

export default function CreatorTable({
    creators,
    isLoading,
    onHover,
    showPlatform = false,
}: {
    creators: TableCreator[]
    isLoading?: boolean
    onHover?: (id: string | null) => void
    showPlatform?: boolean
}) {
    const navigate = useNavigate()

    if (isLoading) {
        return (
            <div className="rounded-xl border border-border-subtle overflow-hidden">
                <table className="w-full">
                    <thead>
                        <tr className="bg-surface-1 border-b border-border-subtle">
                            <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Creator</th>
                            {showPlatform && <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Source</th>}
                            <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Followers</th>
                            <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Score</th>
                            <th className="px-4 py-3 w-10" />
                        </tr>
                    </thead>
                    <tbody>
                        {Array.from({ length: 6 }).map((_, i) => (
                            <tr key={i} className="border-b border-border-subtle last:border-b-0">
                                <td className="px-4 py-3.5">
                                    <div className="flex flex-col gap-1.5">
                                        <Skeleton className="h-4 w-36" />
                                        <Skeleton className="h-3 w-56" />
                                    </div>
                                </td>
                                {showPlatform && <td className="px-4 py-3.5 text-center"><Skeleton className="h-4 w-16 mx-auto" /></td>}
                                <td className="px-4 py-3.5 text-right"><Skeleton className="h-4 w-12 ml-auto" /></td>
                                <td className="px-4 py-3.5 flex justify-center"><Skeleton className="h-10 w-10 rounded-full" /></td>
                                <td className="px-4 py-3.5" />
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
    }

    if (creators.length === 0) {
        return (
            <div className="rounded-xl border border-border-subtle border-dashed">
                <EmptyState
                    icon={<Users className="w-5 h-5" />}
                    title="No creators found"
                    description="Try lowering the minimum score or broadening your search."
                />
            </div>
        )
    }

    return (
        <div className="rounded-xl border border-border-subtle overflow-hidden">
            <table className="w-full">
                <thead>
                    <tr className="bg-surface-1 border-b border-border-subtle">
                        <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Creator</th>
                        {showPlatform && <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Source</th>}
                        <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Followers</th>
                        {!showPlatform && <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Videos</th>}
                        <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wider text-text-tertiary">Score</th>
                        <th className="px-4 py-3 w-10" />
                    </tr>
                </thead>
                <tbody>
                    {creators.map((c) => (
                        <tr
                            key={c.id}
                            onClick={() => navigate(`/creator/${c.id}`)}
                            onMouseEnter={() => onHover?.(c.id)}
                            onMouseLeave={() => onHover?.(null)}
                            className="border-b border-border-subtle last:border-b-0 cursor-pointer group hover:bg-accent/[0.03] transition-colors duration-150"
                        >
                            <td className="px-4 py-3.5">
                                <div className="flex items-center gap-3">
                                    {/* Avatar placeholder */}
                                    <div className="w-8 h-8 rounded-lg bg-surface-3 flex items-center justify-center text-text-tertiary text-xs font-bold shrink-0">
                                        {c.title.charAt(0).toUpperCase()}
                                    </div>
                                    <div className="min-w-0">
                                        <div className="flex items-center gap-2">
                                            <span className="text-[13px] font-semibold text-text-primary truncate max-w-[250px]">
                                                {c.title}
                                            </span>
                                        </div>
                                        <div className="text-[11px] text-text-tertiary truncate max-w-[350px] mt-0.5">
                                            {c.description || '—'}
                                        </div>
                                    </div>
                                </div>
                            </td>
                            {showPlatform && (
                                <td className="px-4 py-3.5 text-center">
                                    {c.platform && <PlatformBadge platform={c.platform as any} />}
                                </td>
                            )}
                            <td className="px-4 py-3.5 text-right">
                                <div className="flex items-center justify-end gap-1.5 text-[13px] text-text-secondary tabular-nums">
                                    <Users className="w-3 h-3 text-text-tertiary" />
                                    {formatSubs(c.subscriber_count)}
                                </div>
                            </td>
                            {!showPlatform && (
                                <td className="px-4 py-3.5 text-right">
                                    <div className="flex items-center justify-end gap-1.5 text-[13px] text-text-secondary tabular-nums">
                                        <Video className="w-3 h-3 text-text-tertiary" />
                                        {c.video_count}
                                    </div>
                                </td>
                            )}
                            <td className="px-4 py-3.5">
                                <div className="flex justify-center">
                                    <AlignmentScoreBadge score={c.alignment_score} size={36} />
                                </div>
                            </td>
                            <td className="px-4 py-3.5">
                                <ArrowRight className="w-4 h-4 text-text-tertiary opacity-0 group-hover:opacity-100 transition-opacity" />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
