import type { ReactNode } from 'react'
import Sidebar from './Sidebar'

export default function AppShell({ children }: { children: ReactNode }) {
    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 ml-[220px] min-h-screen">
                <div className="max-w-[1200px] mx-auto px-8 py-8">
                    {children}
                </div>
            </main>
        </div>
    )
}
