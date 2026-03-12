import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../components/DashboardLayout';
import { Loader2, Bot, ArrowLeft } from 'lucide-react';
import { apiClient, type BriefingResponse } from '../api/client';
import ReactMarkdown from 'react-markdown';

export default function BriefingsDashboard() {
    const { creatorId } = useParams<{ creatorId: string }>();
    const navigate = useNavigate();
    
    const [briefingId, setBriefingId] = useState<string | null>(null);
    const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isGenerating, setIsGenerating] = useState(false);

    // Step 1: Trigger generation on load if we have a creatorId
    useEffect(() => {
        let isMounted = true;
        
        async function startGeneration() {
            if (!creatorId) return;
            try {
                setIsGenerating(true);
                const res = await apiClient.generateBriefing(creatorId, "General Partnership Outreach");
                if (isMounted) {
                    setBriefingId(res.briefing_id);
                }
            } catch (err: any) {
                console.error(err);
                if (isMounted) setError(err.message || 'Failed to trigger briefing generation.');
                if (isMounted) setIsGenerating(false);
            }
        }

        startGeneration();
        return () => { isMounted = false; };
    }, [creatorId]);

    // Step 2: Poll for completion once we have a briefingId
    useEffect(() => {
        if (!briefingId) return;

        let isMounted = true;
        let pinger: any;

        async function pollStatus() {
            try {
                const currentId = briefingId as string;
                const statusRes = await apiClient.getBriefingStatus(currentId);
                
                if (isMounted) {
                    setBriefing(statusRes);
                    
                    if (statusRes.status === 'completed' || statusRes.status === 'failed') {
                        setIsGenerating(false);
                        clearInterval(pinger);
                        if (statusRes.status === 'failed') {
                            setError(`Briefing generation failed. ${statusRes.content ? `Error: ${statusRes.content}` : ''}`);
                        }
                    }
                }
            } catch (err) {
                console.error(err);
            }
        }

        pollStatus();
        pinger = setInterval(pollStatus, 3000);

        return () => {
            isMounted = false;
            clearInterval(pinger);
        };
    }, [briefingId]);

    const renderContent = () => {
        if (error) {
            return (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-6 rounded-xl relative z-10">
                    <h3 className="font-semibold text-lg mb-2">Generation Failed</h3>
                    <p>{error}</p>
                </div>
            );
        }

        if (isGenerating || !briefing || briefing.status === 'pending') {
            return (
                <div className="text-center py-32 text-slate-500 bg-[#0B101E]/80 backdrop-blur-xl rounded-3xl border border-slate-800/80 shadow-2xl relative z-10">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-slate-800/80 mb-6 shadow-inner relative overflow-hidden">
                        <div className="absolute inset-0 bg-blue-500/10 animate-pulse" />
                        <Loader2 className="w-10 h-10 text-cyan-400 relative z-10 animate-spin" />
                    </div>
                    <h3 className="text-xl font-medium text-slate-200 mb-2">Synthesizing Playbook</h3>
                    <p className="max-w-md mx-auto text-slate-400">
                        Our intelligence engine is analyzing the creator's recent content vectors, estimating alignment, and drafting a bespoke engagement strategy. This takes roughly 10-15 seconds.
                    </p>
                </div>
            );
        }

        // Completed! Render the Markdown beautifully.
        return (
            <div className="bg-[#0B101E]/80 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-8 md:p-10 shadow-2xl relative z-10">
                <div className="briefing-content">
                    <ReactMarkdown
                        components={{
                            h1: ({ children }) => (
                                <h1 className="text-2xl font-bold text-white mb-4 pb-3 border-b border-slate-700/50">{children}</h1>
                            ),
                            h2: ({ children }) => (
                                <h2 className="text-xl font-semibold text-white mt-8 mb-3 pb-2 border-b border-slate-800/50">{children}</h2>
                            ),
                            h3: ({ children }) => (
                                <h3 className="text-lg font-semibold text-cyan-300 mt-6 mb-3 flex items-center gap-2">{children}</h3>
                            ),
                            h4: ({ children }) => (
                                <h4 className="text-base font-semibold text-slate-200 mt-4 mb-2">{children}</h4>
                            ),
                            p: ({ children }) => (
                                <p className="text-slate-300 leading-relaxed mb-4 text-[15px]">{children}</p>
                            ),
                            ul: ({ children }) => (
                                <ul className="space-y-2 mb-5 ml-1">{children}</ul>
                            ),
                            ol: ({ children }) => (
                                <ol className="space-y-2 mb-5 ml-1 list-decimal list-inside">{children}</ol>
                            ),
                            li: ({ children }) => (
                                <li className="text-slate-300 text-[15px] leading-relaxed flex items-start gap-2">
                                    <span className="text-cyan-500 mt-1.5 shrink-0">•</span>
                                    <span>{children}</span>
                                </li>
                            ),
                            blockquote: ({ children }) => (
                                <blockquote className="border-l-3 border-cyan-500/50 bg-cyan-500/5 rounded-r-lg pl-4 pr-3 py-3 my-4 italic text-slate-400 text-[14px]">
                                    {children}
                                </blockquote>
                            ),
                            strong: ({ children }) => (
                                <strong className="text-white font-semibold">{children}</strong>
                            ),
                            em: ({ children }) => (
                                <em className="text-slate-300 italic">{children}</em>
                            ),
                            hr: () => (
                                <hr className="border-slate-700/40 my-6" />
                            ),
                            table: ({ children }) => (
                                <div className="overflow-x-auto my-4">
                                    <table className="w-full text-sm text-left text-slate-300 border border-slate-700/40 rounded-lg overflow-hidden">
                                        {children}
                                    </table>
                                </div>
                            ),
                            thead: ({ children }) => (
                                <thead className="bg-slate-800/60 text-slate-200 text-xs uppercase tracking-wider">
                                    {children}
                                </thead>
                            ),
                            tbody: ({ children }) => (
                                <tbody className="divide-y divide-slate-700/30">{children}</tbody>
                            ),
                            tr: ({ children }) => (
                                <tr className="hover:bg-slate-800/30 transition-colors">{children}</tr>
                            ),
                            th: ({ children }) => (
                                <th className="px-4 py-3 font-semibold">{children}</th>
                            ),
                            td: ({ children }) => (
                                <td className="px-4 py-3">{children}</td>
                            ),
                            a: ({ href, children }) => (
                                <a href={href} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300 underline underline-offset-2 transition-colors">
                                    {children}
                                </a>
                            ),
                            code: ({ children }) => (
                                <code className="bg-slate-800 text-cyan-300 px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>
                            ),
                        }}
                    >
                        {briefing.content}
                    </ReactMarkdown>
                </div>
            </div>
        );
    };

    return (
        <DashboardLayout>
            <div className="space-y-8">
                <header>
                    <button onClick={() => navigate(-1)} className="text-slate-400 hover:text-white flex items-center gap-2 mb-4 text-sm transition-colors">
                        <ArrowLeft className="w-4 h-4" /> Back to Analytics
                    </button>
                    <h1 className="text-3xl font-semibold tracking-tight text-white mb-2 flex items-center gap-3">
                        <Bot className="w-8 h-8 text-blue-400" />
                        Strategy Briefing 
                    </h1>
                    <p className="text-slate-400">AI-generated engagement strategies tailored for this creator.</p>
                </header>

                {renderContent()}
            </div>
        </DashboardLayout>
    );
}
