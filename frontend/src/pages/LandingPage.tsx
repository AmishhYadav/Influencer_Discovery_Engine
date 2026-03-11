import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Activity, ShieldCheck } from 'lucide-react';
import LightRays from '../components/LightRays';

export default function LandingPage() {
    return (
        <main className="relative w-full h-screen bg-[#0f172a] flex items-center justify-center overflow-hidden">
            {/* Background Effect */}
            <LightRays
                raysOrigin="top-center"
                raysColor="#10b981" // Emerald
                raysSpeed={1.2}
                lightSpread={1.5}
                rayLength={2.0}
                followMouse={true}
                mouseInfluence={0.4}
                noiseAmount={0.04}
                distortion={0.1}
            />

            {/* Hero Content */}
            <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-4xl w-full">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
                    className="space-y-8 flex flex-col items-center"
                >
                    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium backdrop-blur-md">
                        <Sparkles className="w-4 h-4" />
                        <span>Next-Gen Influencer Discovery Engine</span>
                    </div>

                    <h1 className="text-6xl md:text-8xl font-medium tracking-tighter text-white drop-shadow-2xl">
                        Find the perfect <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-indigo-400 to-violet-400">
                            voices for your mission
                        </span>
                    </h1>

                    <p className="text-slate-300 text-lg md:text-xl font-light max-w-2xl mx-auto leading-relaxed">
                        Discover, analyze, and align with creators across YouTube, X, and academia using composite credibility scoring and AI-driven alignment proof.
                    </p>

                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.4, duration: 0.8 }}
                        className="pt-4"
                    >
                        <Link
                            to="/dashboard"
                            className="group relative inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-white text-slate-950 font-medium text-lg overflow-hidden transition-transform hover:scale-105"
                        >
                            <span className="relative z-10 font-semibold tracking-tight">Launch Dashboard</span>
                            <ArrowRight className="w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" />
                            <div className="absolute inset-0 bg-emerald-400 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-in-out" />
                        </Link>
                    </motion.div>
                </motion.div>
            </div>

            {/* Floating features overlay */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: 1 }}
                className="absolute bottom-12 left-12 right-12 hidden md:flex justify-between items-end z-20 pointer-events-none"
            >
                <div className="glass-panel p-4 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-xl flex items-center gap-4 text-left w-64 shadow-2xl">
                    <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center shrink-0">
                        <Activity className="w-5 h-5 text-emerald-400" />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-white">Composite Scores</div>
                        <div className="text-xs text-slate-400">Ranked across 4 dimensions</div>
                    </div>
                </div>

                <div className="glass-panel p-4 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-xl flex items-center gap-4 text-left w-64 shadow-2xl">
                    <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center shrink-0">
                        <ShieldCheck className="w-5 h-5 text-indigo-400" />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-white">Alignment Proof</div>
                        <div className="text-xs text-slate-400">AI-extracted verifiable quotes</div>
                    </div>
                </div>
            </motion.div>

            {/* Shadow Vignette container */}
            <div className="absolute inset-0 pointer-events-none rounded-[40px] shadow-[inset_0_0_120px_rgba(0,0,0,0.8)] border border-white/5 z-30" />
        </main>
    );
}
