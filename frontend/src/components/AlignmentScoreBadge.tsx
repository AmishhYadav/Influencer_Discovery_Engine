import { useMemo } from 'react'

export default function AlignmentScoreBadge({
    score,
    size = 40,
}: {
    score: number | null
    size?: number
}) {
    const { color, bgColor, label } = useMemo(() => {
        if (score == null) return { color: '#63636e', bgColor: '#63636e18', label: '—' }
        if (score >= 70) return { color: '#10b981', bgColor: '#10b98118', label: String(score) }
        if (score >= 40) return { color: '#f59e0b', bgColor: '#f59e0b18', label: String(score) }
        return { color: '#ef4444', bgColor: '#ef444418', label: String(score) }
    }, [score])

    const strokeWidth = size >= 48 ? 3 : 2.5
    const radius = (size - strokeWidth * 2) / 2
    const circumference = 2 * Math.PI * radius
    const progress = score != null ? (score / 100) * circumference : 0
    const offset = circumference - progress

    return (
        <div
            className="relative inline-flex items-center justify-center animate-count-up"
            style={{ width: size, height: size }}
        >
            <svg
                width={size}
                height={size}
                viewBox={`0 0 ${size} ${size}`}
                className="rotate-[-90deg]"
            >
                {/* Background ring */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    fill={bgColor}
                    stroke="#27292f"
                    strokeWidth={strokeWidth}
                />
                {/* Progress ring */}
                {score != null && (
                    <circle
                        cx={size / 2}
                        cy={size / 2}
                        r={radius}
                        fill="none"
                        stroke={color}
                        strokeWidth={strokeWidth}
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={offset}
                        style={{ transition: 'stroke-dashoffset 600ms cubic-bezier(0.16, 1, 0.3, 1)' }}
                    />
                )}
            </svg>
            <span
                className="absolute text-xs font-bold"
                style={{ color, fontSize: size >= 48 ? 14 : 11 }}
            >
                {label}
            </span>
        </div>
    )
}
