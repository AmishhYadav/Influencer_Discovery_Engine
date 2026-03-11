import { useLocation, useParams, useNavigate, Navigate } from 'react-router-dom';
import { DashboardLayout } from '../components/DashboardLayout';
import { LineChart, Activity, Target, Shield, Users, ArrowRight, ArrowLeft } from 'lucide-react';
import { type CreatorSummary } from '../api/client';

export default function AnalyticsDashboard() {
    const { creatorId } = useParams<{ creatorId: string }>();
    const location = useLocation();
    const navigate = useNavigate();

    const shortlisted: CreatorSummary[] = location.state?.shortlisted || [];
    const creator = shortlisted.find(c => c.id === creatorId);

    if (!creator) {
        return <Navigate to="/dashboard" replace />;
    }

    const metrics = [
        { label: 'Composite Score', value: creator.composite_score ?? 0, icon: Activity, color: 'text-cyan-400', bg: 'bg-cyan-400' },
        { label: 'Alignment', value: creator.alignment_score ?? 0, icon: Target, color: 'text-emerald-400', bg: 'bg-emerald-400' },
        { label: 'Credibility', value: creator.credibility_score ?? 0, icon: Shield, color: 'text-blue-400', bg: 'bg-blue-400' },
        { label: 'Reach', value: creator.reach_score ?? 0, icon: Users, color: 'text-purple-400', bg: 'bg-purple-400' },
        { label: 'Engagement', value: creator.engagement_score ?? 0, icon: LineChart, color: 'text-pink-400', bg: 'bg-pink-400' },
    ];

    return (
        <DashboardLayout>
            <div className="space-y-8">
                <header className="flex items-center justify-between">
                    <div>
                        <button onClick={() => navigate(-1)} className="text-slate-400 hover:text-white flex items-center gap-2 mb-4 text-sm transition-colors">
                            <ArrowLeft className="w-4 h-4" /> Back to Search
                        </button>
                        <h1 className="text-3xl font-semibold tracking-tight text-white mb-2">Analytics: {creator.name}</h1>
                        <p className="text-slate-400">Deep-dive performance metrics against the matched cohort.</p>
                    </div>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Platform Stats */}
                    <div className="bg-[#0B101E]/80 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-6 shadow-2xl relative z-20">
                        <h3 className="text-lg font-medium text-slate-200 mb-6 flex items-center gap-2">
                            <Activity className="w-5 h-5 text-cyan-500" />
                            Platform Profile
                        </h3>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                                <span className="text-slate-400">Platform</span>
                                <span className="text-slate-200 capitalize font-medium px-3 py-1 bg-slate-800/50 rounded-lg">{creator.platform}</span>
                            </div>
                            <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                                <span className="text-slate-400">Followers</span>
                                <span className="text-slate-200 font-medium">{creator.follower_count.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                                <span className="text-slate-400">Profile URL</span>
                                <a href={creator.profile_url} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:text-cyan-300 font-medium truncate max-w-[150px]">
                                    Open Link
                                </a>
                            </div>
                        </div>
                    </div>

                    {/* Metric Breakdown */}
                    <div className="md:col-span-1 lg:col-span-2 bg-[#0B101E]/80 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-6 shadow-2xl relative z-20">
                        <h3 className="text-lg font-medium text-slate-200 mb-6 flex items-center gap-2">
                            <Target className="w-5 h-5 text-emerald-500" />
                            Dimensional Scoring
                        </h3>
                        <div className="space-y-6">
                            {metrics.map(metric => (
                                <div key={metric.label}>
                                    <div className="flex justify-between text-sm mb-2">
                                        <span className="text-slate-300 flex items-center gap-2 font-medium">
                                            <metric.icon className={`w-4 h-4 ${metric.color}`} />
                                            {metric.label}
                                        </span>
                                        <span className="text-slate-200 font-medium">{metric.value.toFixed(1)} / 100</span>
                                    </div>
                                    <div className="w-full bg-slate-900 rounded-full h-2.5 overflow-hidden border border-slate-800">
                                        <div className={`${metric.bg} h-2.5 rounded-full transition-all duration-1000 ease-out`} style={{ width: `${metric.value}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Call to action */}
                <div className="flex justify-end pt-4">
                    <button
                        onClick={() => navigate(`/briefings/${creator.id}`)}
                        className="bg-cyan-600 hover:bg-cyan-500 text-white px-8 py-4 rounded-xl font-medium transition-all shadow-[0_0_20px_-5px_rgba(6,182,212,0.4)] hover:shadow-[0_0_25px_-5px_rgba(6,182,212,0.6)] flex items-center gap-2"
                    >
                        Draft Engagement Playbook <ArrowRight className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </DashboardLayout>
    );
}
