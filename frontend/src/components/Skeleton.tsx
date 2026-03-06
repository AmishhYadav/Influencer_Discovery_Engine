import clsx from 'clsx'

export default function Skeleton({ className }: { className?: string }) {
    return (
        <div
            className={clsx(
                'rounded-md bg-surface-3 animate-skeleton',
                className
            )}
        />
    )
}
