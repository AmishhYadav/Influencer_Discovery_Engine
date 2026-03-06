import { NavLink } from 'react-router-dom'
import { Search, FileText, Compass } from 'lucide-react'
import clsx from 'clsx'

const navItems = [
    { to: '/', label: 'Discovery', icon: Search },
    { to: '/briefings', label: 'Briefings', icon: FileText },
]

export default function Sidebar() {
    return (
        <aside className="flex flex-col h-screen w-[220px] border-r border-border-subtle bg-surface-1 fixed left-0 top-0 z-30">
            {/* ── Logo ── */}
            <div className="flex items-center gap-2.5 px-5 h-14 border-b border-border-subtle">
                <div className="w-7 h-7 rounded-lg bg-accent/20 flex items-center justify-center">
                    <Compass className="w-4 h-4 text-accent" />
                </div>
                <span className="text-[13px] font-semibold tracking-tight text-text-primary">
                    Discovery Engine
                </span>
            </div>

            {/* ── Nav Items ── */}
            <nav className="flex-1 px-3 py-4 space-y-0.5">
                {navItems.map(({ to, label, icon: Icon }) => (
                    <NavLink
                        key={to}
                        to={to}
                        end={to === '/'}
                        className={({ isActive }) =>
                            clsx(
                                'flex items-center gap-2.5 px-3 py-2 rounded-lg text-[13px] font-medium transition-colors duration-150',
                                isActive
                                    ? 'bg-accent/10 text-accent'
                                    : 'text-text-secondary hover:text-text-primary hover:bg-surface-3'
                            )
                        }
                    >
                        <Icon className="w-4 h-4" />
                        {label}
                    </NavLink>
                ))}
            </nav>

            {/* ── Footer ── */}
            <div className="px-5 py-4 border-t border-border-subtle">
                <p className="text-[10px] uppercase tracking-widest text-text-tertiary font-medium">
                    Advocacy Platform
                </p>
            </div>
        </aside>
    )
}
