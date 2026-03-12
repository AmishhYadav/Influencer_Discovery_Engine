
import type { CreatorSummary } from '../api/client';
import { User, Twitter, Youtube, GraduationCap, PenTool, ExternalLink, Users, BarChart3, BookOpen, TrendingUp } from 'lucide-react';

interface CreatorCardProps {
    creator: CreatorSummary;
    onClick?: (creator: CreatorSummary) => void;
}

const PlatformIcon = ({ platform }: { platform?: string }) => {
    switch ((platform || '').toLowerCase()) {
        case 'twitter': return <Twitter className="w-4 h-4 text-blue-400" />;
        case 'youtube': return <Youtube className="w-4 h-4 text-red-500" />;
        case 'academic': return <GraduationCap className="w-4 h-4 text-indigo-400" />;
        case 'blog': return <PenTool className="w-4 h-4 text-emerald-400" />;
        case 'instagram': return <User className="w-4 h-4 text-pink-400" />;
        default: return <User className="w-4 h-4 text-slate-400" />;
    }
};

const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
};

/** Returns the best metric to display based on the platform */
function getPrimaryMetric(creator: CreatorSummary): { label: string; value: string; icon: React.ReactNode } {
    const platform = (creator.platform || '').toLowerCase();

    // Social platforms with meaningful follower counts
    if (['youtube', 'twitter', 'instagram'].includes(platform) && (creator.follower_count ?? 0) > 0) {
        return {
            label: platform === 'youtube' ? 'Subscribers' : 'Followers',
            value: formatNumber(creator.follower_count ?? 0),
            icon: <Users className="w-3.5 h-3.5 text-cyan-400" />,
        };
    }

    // Academic — show alignment score as "Research Relevance"
    if (platform === 'academic') {
        return {
            label: 'Research Relevance',
            value: `${Math.round(creator.composite_score ?? 0)}%`,
            icon: <BookOpen className="w-3.5 h-3.5 text-indigo-400" />,
        };
    }

    // Blog — show alignment score
    if (platform === 'blog') {
        return {
            label: 'Content Alignment',
            value: `${Math.round(creator.alignment_score ?? creator.composite_score ?? 0)}%`,
            icon: <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />,
        };
    }

    // Fallback — show composite score
    if ((creator.composite_score ?? 0) > 0) {
        return {
            label: 'Relevance Score',
            value: `${Math.round(creator.composite_score ?? 0)}%`,
            icon: <BarChart3 className="w-3.5 h-3.5 text-cyan-400" />,
        };
    }

    // Nothing meaningful to show
    return {
        label: 'Discovered',
        value: '✓',
        icon: <BarChart3 className="w-3.5 h-3.5 text-slate-500" />,
    };
}

export function CreatorCard({ creator, onClick }: CreatorCardProps) {
    const metric = getPrimaryMetric(creator);

    return (
        <div 
            className="group relative bg-[#0B101E]/60 backdrop-blur-md border border-slate-800/60 hover:border-slate-600/60 rounded-2xl p-5 transition-all duration-300 hover:shadow-[0_0_30px_-5px_var(--tw-shadow-color)] hover:shadow-cyan-500/20 cursor-pointer overflow-hidden"
            onClick={() => onClick?.(creator)}
        >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="relative z-10 flex justify-between items-start mb-4">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700/50 shadow-inner">
                        <PlatformIcon platform={creator.platform} />
                    </div>
                    <div>
                        <h3 className="font-semibold text-slate-200 group-hover:text-white transition-colors truncate max-w-[180px]">{creator.name}</h3>
                        <p className="text-xs text-slate-500 capitalize">{creator.platform}</p>
                    </div>
                </div>
                {creator.profile_url && (
                    <a 
                        href={creator.profile_url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="text-slate-500 hover:text-cyan-400 transition-colors p-1"
                        onClick={(e) => e.stopPropagation()}
                        title="Open Profile"
                    >
                        <ExternalLink className="w-4 h-4" />
                    </a>
                )}
            </div>

            <div className="mt-6">
                <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-800/30 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        {metric.icon}
                        <span className="text-sm text-slate-400">{metric.label}</span>
                    </div>
                    <span className="font-semibold text-slate-200">{metric.value}</span>
                </div>
            </div>
        </div>
    );
}
