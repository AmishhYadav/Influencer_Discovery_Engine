import { useState } from 'react'
import { ChevronDown, ChevronUp, Quote as QuoteIcon } from 'lucide-react'

interface QuoteItem {
    text: string
    timestamp: string
}

export default function QuoteEvidenceList({ quotes }: { quotes: QuoteItem[] }) {
    const [expandedIndex, setExpandedIndex] = useState<number | null>(null)

    if (!quotes || quotes.length === 0) {
        return (
            <p className="text-xs text-text-tertiary italic">No supporting quotes available.</p>
        )
    }

    return (
        <div className="space-y-2">
            {quotes.map((q, i) => {
                const isExpanded = expandedIndex === i
                const isLong = q.text.length > 120

                return (
                    <div
                        key={i}
                        className="group rounded-lg bg-surface-2 border border-border-subtle overflow-hidden transition-colors hover:border-accent/20"
                    >
                        <div className="flex items-start gap-3 p-3.5">
                            <div className="w-6 h-6 rounded-md bg-accent/10 flex items-center justify-center shrink-0 mt-0.5">
                                <QuoteIcon className="w-3 h-3 text-accent" />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-[13px] text-text-secondary leading-relaxed">
                                    "{isLong && !isExpanded ? q.text.slice(0, 120) + '…' : q.text}"
                                </p>
                                <div className="flex items-center gap-2 mt-2">
                                    <span className="text-[10px] font-mono text-accent/70 bg-accent/8 px-1.5 py-0.5 rounded">
                                        ⏱ {q.timestamp}
                                    </span>
                                    {isLong && (
                                        <button
                                            onClick={() => setExpandedIndex(isExpanded ? null : i)}
                                            className="flex items-center gap-0.5 text-[10px] text-text-tertiary hover:text-text-secondary transition-colors font-medium"
                                        >
                                            {isExpanded ? (
                                                <>Less <ChevronUp className="w-3 h-3" /></>
                                            ) : (
                                                <>More <ChevronDown className="w-3 h-3" /></>
                                            )}
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}
