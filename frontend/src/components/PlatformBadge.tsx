import type { Platform } from '@/api/client'
import { Youtube, BookOpen, GraduationCap, Twitter, Instagram } from 'lucide-react'

const PLATFORM_CONFIG: Record<Platform, {
    label: string
    icon: React.ReactNode
    color: string
    bg: string
}> = {
    youtube: {
        label: 'YouTube',
        icon: <Youtube className="w-3 h-3" />,
        color: 'text-red-400',
        bg: 'bg-red-500/10',
    },
    blog: {
        label: 'Blog',
        icon: <BookOpen className="w-3 h-3" />,
        color: 'text-emerald-400',
        bg: 'bg-emerald-500/10',
    },
    academic: {
        label: 'Academic',
        icon: <GraduationCap className="w-3 h-3" />,
        color: 'text-blue-400',
        bg: 'bg-blue-500/10',
    },
    twitter: {
        label: 'Twitter',
        icon: <Twitter className="w-3 h-3" />,
        color: 'text-sky-400',
        bg: 'bg-sky-500/10',
    },
    instagram: {
        label: 'Instagram',
        icon: <Instagram className="w-3 h-3" />,
        color: 'text-pink-400',
        bg: 'bg-pink-500/10',
    },
}

export default function PlatformBadge({ platform }: { platform: Platform }) {
    const config = PLATFORM_CONFIG[platform]
    if (!config) return null

    return (
        <span className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium ${config.color} ${config.bg}`}>
            {config.icon}
            {config.label}
        </span>
    )
}
