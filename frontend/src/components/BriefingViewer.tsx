import { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import Markdown from 'react-markdown'

export default function BriefingViewer({ content }: { content: string }) {
    const [isCopied, setIsCopied] = useState(false)

    const handleCopy = async () => {
        await navigator.clipboard.writeText(content)
        setIsCopied(true)
        setTimeout(() => setIsCopied(false), 2000)
    }

    return (
        <div className="animate-slide-up space-y-3">
            {/* Header */}
            <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase tracking-widest text-text-tertiary font-semibold">
                    Generated Briefing
                </span>
                <button
                    onClick={handleCopy}
                    className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-[11px] font-medium transition-all ${isCopied
                            ? 'bg-emerald-soft border border-emerald/20 text-emerald'
                            : 'bg-surface-3 border border-border-subtle text-text-secondary hover:text-text-primary hover:bg-surface-4'
                        }`}
                >
                    {isCopied ? (
                        <><Check className="w-3 h-3" /> Copied</>
                    ) : (
                        <><Copy className="w-3 h-3" /> Copy</>
                    )}
                </button>
            </div>

            {/* Content */}
            <div className="rounded-xl bg-surface-2 border border-border-subtle p-5 prose-briefing">
                <Markdown>{content}</Markdown>
            </div>
        </div>
    )
}
