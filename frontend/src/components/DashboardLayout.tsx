import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Layers, Activity, Search, LineChart, FileText } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: (string | undefined | null | false)[]) {
    return twMerge(clsx(inputs));
}

export function DashboardLayout({ children }: { children: ReactNode }) {
    const location = useLocation();

    const navItems = [
        { name: 'Discovery', path: '/dashboard', icon: Search },
        { name: 'Analytics', path: '/analytics', icon: LineChart },
        { name: 'Briefings', path: '/briefings', icon: FileText },
    ];

    return (
        <div className="min-h-screen bg-[#0f172a] text-slate-50 flex">
            {/* Sidebar */}
            <aside className="fixed left-0 top-0 bottom-0 w-64 bg-slate-900/50 backdrop-blur-xl border-r border-slate-800/50 z-40 flex flex-col">
                <div className="p-6 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
                        <Activity className="w-4 h-4 text-emerald-400" />
                    </div>
                    <span className="font-semibold text-lg tracking-tight">Influent<span className="text-emerald-400">.</span></span>
                </div>

                <nav className="flex-1 px-4 space-y-2 mt-4">
                    {navItems.map((item) => {
                        const isActive = location.pathname === item.path;
                        const Icon = item.icon;
                        return (
                            <Link
                                key={item.name}
                                to={item.path}
                                className={cn(
                                    "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group relative overflow-hidden",
                                    isActive ? "text-white" : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                                )}
                            >
                                {isActive && (
                                    <motion.div
                                        layoutId="active-nav-bg"
                                        className="absolute inset-0 bg-emerald-500/10 border border-emerald-500/20 rounded-xl"
                                    />
                                )}
                                <Icon className={cn("w-4 h-4 relative z-10", isActive ? "text-emerald-400" : "group-hover:text-emerald-400/70")} />
                                <span className="relative z-10">{item.name}</span>
                            </Link>
                        );
                    })}
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-64 min-h-screen relative">
                <div className="absolute inset-x-0 top-0 h-96 bg-gradient-to-b from-indigo-500/5 to-transparent pointer-events-none" />
                <div className="relative z-10 p-8 max-w-7xl mx-auto min-h-screen">
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4 }}
                    >
                        {children}
                    </motion.div>
                </div>
            </main>
        </div>
    );
}
