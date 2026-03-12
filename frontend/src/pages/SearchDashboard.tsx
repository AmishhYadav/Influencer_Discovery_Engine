import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../components/DashboardLayout';
import { CreatorCard } from '../components/CreatorCard';
import { apiClient, type CreatorSummary } from '../api/client';
import { Search, Loader2, Filter, Database, Wifi } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ALL_SOURCES = ['youtube', 'twitter', 'blog', 'academic', 'instagram'];

export default function SearchDashboard() {
    const navigate = useNavigate();
    const [query, setQuery] = useState('');
    const [selectedSources, setSelectedSources] = useState<string[]>(['youtube']);
    const [creators, setCreators] = useState<CreatorSummary[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasSearched, setHasSearched] = useState(false);
    const [fromCache, setFromCache] = useState(false);

    const handleSearch = async (e?: React.FormEvent, forceLive: boolean = false) => {
        if (e) e.preventDefault();
        if (!query.trim()) return;

        if (selectedSources.length === 0) {
            setError('Please select at least one source to search.');
            return;
        }

        try {
            setIsLoading(true);
            setError(null);
            setHasSearched(true);
            setFromCache(false);
            const res = await apiClient.searchCreators(query, selectedSources, forceLive);
            setCreators(res.creators);
            setFromCache(res.from_cache);
        } catch (err: any) {
            console.error(err);
            setError(err.message || 'An error occurred during search. Ensure your API is running.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleForceLiveSearch = () => {
        handleSearch(undefined, true);
    };

    const toggleSource = (source: string) => {
        setSelectedSources((prev: string[]) => 
            prev.includes(source) 
                ? prev.filter((s: string) => s !== source)
                : [...prev, source]
        );
    };

    return (
        <DashboardLayout>
            <div className="space-y-8">
                <header>
                    <h1 className="text-3xl font-semibold tracking-tight text-white mb-2">Creator Discovery</h1>
                    <p className="text-slate-400">Find and analyze aligned influencers across all networks.</p>
                </header>

                {/* Search Bar & Filters */}
                <div className="bg-[#0B101E]/80 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-6 shadow-2xl relative z-20">
                    <form onSubmit={(e) => handleSearch(e)} className="flex gap-4 mb-5">
                        <div className="relative flex-1">
                            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <Search className="h-5 w-5 text-slate-400" />
                            </div>
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                className="block w-full pl-11 pr-4 py-3 bg-slate-900/50 border border-slate-700/80 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500 transition-all text-lg shadow-inner"
                                placeholder="Search by topic, keyword, or URL..."
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="bg-cyan-600 hover:bg-cyan-500 text-white px-8 py-3 rounded-xl font-medium transition-colors shadow-[0_0_15px_-3px_rgba(6,182,212,0.4)] disabled:opacity-50 disabled:shadow-none flex items-center gap-2"
                        >
                            {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Search'}
                        </button>
                    </form>

                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 text-sm text-slate-400">
                            <Filter className="w-4 h-4" />
                            <span>Sources:</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {ALL_SOURCES.map(source => (
                                <button
                                    key={source}
                                    type="button"
                                    onClick={() => toggleSource(source)}
                                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                                        selectedSources.includes(source)
                                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-[0_0_10px_-2px_rgba(6,182,212,0.3)]'
                                            : 'bg-slate-800/40 text-slate-400 border border-slate-700/60 hover:border-slate-600'
                                    }`}
                                >
                                    {source.charAt(0).toUpperCase() + source.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Status States */}
                {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-lg flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-red-500"></div>
                        <p className="text-sm font-medium">{error}</p>
                    </div>
                )}

                {/* Cache Indicator Banner */}
                {fromCache && !isLoading && creators.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl px-5 py-3 flex items-center justify-between"
                    >
                        <div className="flex items-center gap-3">
                            <Database className="w-4 h-4 text-emerald-400" />
                            <span className="text-sm text-emerald-300 font-medium">
                                Showing {creators.length} results from your database (instant)
                            </span>
                        </div>
                        <button
                            onClick={handleForceLiveSearch}
                            className="flex items-center gap-2 px-4 py-1.5 bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-300 rounded-lg text-sm font-medium border border-cyan-500/30 hover:border-cyan-500/60 transition-all"
                        >
                            <Wifi className="w-3.5 h-3.5" />
                            Refresh with Live Search
                        </button>
                    </motion.div>
                )}
                
                {isLoading && creators.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-20 text-slate-400">
                        <Loader2 className="w-10 h-10 animate-spin text-cyan-500 mb-4" />
                        <p className="font-medium">Discovering aligned creators...</p>
                        <p className="text-sm opacity-70 mt-1">This might take a moment depending on the sources.</p>
                    </div>
                )}

                {/* Results Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 relative z-10">
                    <AnimatePresence>
                        {creators.map((creator: CreatorSummary, i: number) => (
                            <motion.div
                                key={`${creator.id}-${i}`}
                                initial={{ opacity: 0, scale: 0.9, y: 10 }}
                                animate={{ opacity: 1, scale: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.9, y: -10 }}
                                transition={{ duration: 0.25, delay: i * 0.03, ease: 'easeOut' }}
                                onClick={() => navigate(`/analytics/${creator.id}`, { state: { shortlisted: creators } })}
                                className="cursor-pointer transition-transform hover:-translate-y-1"
                            >
                                <CreatorCard creator={creator} />
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>

                {!isLoading && creators.length === 0 && !error && hasSearched && (
                    <div className="text-center py-20 text-slate-500 bg-slate-900/30 rounded-3xl border border-slate-800/50 border-dashed">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-800/80 mb-4 shadow-inner">
                            <Search className="w-8 h-8 text-slate-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-300 mb-1">No creators found</h3>
                        <p className="text-sm">Try adjusting your search terms or selecting more sources.</p>
                    </div>
                )}
                
                {!isLoading && !hasSearched && !error && (
                    <div className="text-center py-32 text-slate-500 bg-[#0B101E]/80 backdrop-blur-xl rounded-3xl border border-slate-800/80 shadow-2xl relative z-10 transition-all">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-slate-800/80 mb-6 shadow-inner relative overflow-hidden">
                            <div className="absolute inset-0 bg-cyan-500/10" />
                            <Search className="w-10 h-10 text-cyan-400 relative z-10" />
                        </div>
                        <h3 className="text-xl font-medium text-slate-200 mb-2">Search to Discover Creators</h3>
                        <p className="max-w-md mx-auto text-slate-400">
                            Enter an advocacy topic or niche keyword above. The engine will scrape live data and score alignment.
                        </p>
                    </div>
                )}
            </div>
        </DashboardLayout>
    );
}
