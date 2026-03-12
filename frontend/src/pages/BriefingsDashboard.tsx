import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../components/DashboardLayout';
import { Loader2, Bot, ArrowLeft } from 'lucide-react';
import { apiClient, type BriefingResponse } from '../api/client';

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
                // Assert briefingId is not null for TS
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
                // Keep polling on transient errors, don't crash the loop
            }
        }

        // Poll immediately, then every 3s
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

        // Completed! Show the text block.
        return (
            <div className="bg-[#0B101E]/80 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-8 shadow-2xl relative z-10 text-slate-300">
                <div className="prose prose-invert prose-cyan max-w-none">
                    {/* Fallback rendering of raw markdown string logic */}
                    <div className="whitespace-pre-wrap font-mono text-sm leading-relaxed" dangerouslySetInnerHTML={{ __html: briefing.content.replace(/\ng/, '<br/>') }} />
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
