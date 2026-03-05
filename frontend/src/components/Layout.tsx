import type { ReactNode } from 'react'

export default function Layout({ children }: { children: ReactNode }) {
    return (
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* ── Navbar ── */}
            <header
                style={{
                    padding: '16px 32px',
                    borderBottom: '1px solid hsl(215 27.9% 16.9%)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    background: 'linear-gradient(135deg, hsl(224 71.4% 4.1%) 0%, hsl(263.4 70% 10%) 100%)',
                }}
            >
                <div
                    style={{
                        width: 32,
                        height: 32,
                        borderRadius: 8,
                        background: 'linear-gradient(135deg, hsl(263.4 70% 50.4%), hsl(280 70% 60%))',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 16,
                    }}
                >
                    🔍
                </div>
                <h1 style={{ fontSize: 18, fontWeight: 700, letterSpacing: '-0.02em' }}>
                    Influencer Discovery Engine
                </h1>
                <span
                    style={{
                        marginLeft: 8,
                        fontSize: 11,
                        padding: '2px 8px',
                        borderRadius: 9999,
                        background: 'hsl(263.4 70% 50.4% / 0.2)',
                        color: 'hsl(263.4 70% 70%)',
                        fontWeight: 600,
                    }}
                >
                    MVP
                </span>
            </header>

            {/* ── Main Content ── */}
            <main style={{ flex: 1, padding: '24px 32px' }}>{children}</main>
        </div>
    )
}
