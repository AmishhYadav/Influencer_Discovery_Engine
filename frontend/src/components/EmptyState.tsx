import type { ReactNode } from 'react'

export default function EmptyState({
    icon,
    title,
    description,
    action,
}: {
    icon?: ReactNode
    title: string
    description?: string
    action?: ReactNode
}) {
    return (
        <div className="flex flex-col items-center justify-center py-20 text-center animate-fade-in">
            {icon && (
                <div className="w-12 h-12 rounded-xl bg-surface-3 flex items-center justify-center mb-4 text-text-tertiary">
                    {icon}
                </div>
            )}
            <h3 className="text-sm font-semibold text-text-secondary mb-1">{title}</h3>
            {description && (
                <p className="text-xs text-text-tertiary max-w-[280px]">{description}</p>
            )}
            {action && <div className="mt-4">{action}</div>}
        </div>
    )
}
