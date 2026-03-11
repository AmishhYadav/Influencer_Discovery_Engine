import { DashboardLayout } from '../components/DashboardLayout';

export default function SearchDashboard() {
    return (
        <DashboardLayout>
            <div className="space-y-8">
                <header>
                    <h1 className="text-3xl font-semibold tracking-tight">Creator Discovery</h1>
                    <p className="text-slate-400 mt-2">Find and analyze aligned influencers across all networks.</p>
                </header>

                {/* Placeholder for the main dashboard content */}
                <div className="glass-panel border border-slate-800 bg-slate-900/40 backdrop-blur-sm rounded-3xl p-8 min-h-[500px] flex items-center justify-center text-slate-500">
                    Search interface and bento grids will be implemented here.
                </div>
            </div>
        </DashboardLayout>
    );
}
