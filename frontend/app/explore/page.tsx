'use client';

import { useState } from 'react';
import { AnimeNavBar } from '@/components/ui/anime-navbar';
import { CreatorCard } from '@/components/creator-card';
import { useCreators } from '@/hooks/useApi';
import { Zap, Sparkles, TrendingUp } from 'lucide-react';

export default function ExplorePage() {
  const [page, setPage] = useState(1);
  const { creators, isLoading, error } = useCreators(page);

  const navItems = [
    { name: 'Home', url: '/', icon: Sparkles },
    { name: 'Search', url: '/#search', icon: Zap },
    { name: 'Explore', url: '/explore', icon: TrendingUp },
  ];

  return (
    <main className="min-h-screen bg-background pt-24">
      {/* Navbar */}
      <AnimeNavBar
        items={navItems}
        defaultActive="Explore"
        logo={
          <div className="text-lg font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            IDE
          </div>
        }
      />

      {/* Header */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 border-b border-border">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-4">
            Explore Creators
          </h1>
          <p className="text-lg text-muted-foreground">
            Browse and discover top influencers from around the world.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className="h-96 bg-secondary/30 rounded-xl animate-pulse"
                />
              ))}
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-500 text-lg">
                Error loading creators. Please try again.
              </p>
            </div>
          ) : creators && creators.creators.length > 0 ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                {creators.creators.map((creator, index) => (
                  <CreatorCard
                    key={creator.id}
                    creator={creator}
                    delay={index * 0.05}
                  />
                ))}
              </div>

              {/* Pagination */}
              <div className="flex justify-center gap-4">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-6 py-2 bg-primary hover:bg-primary/90 disabled:bg-muted disabled:cursor-not-allowed text-background font-semibold rounded-lg transition-colors"
                >
                  Previous
                </button>
                <div className="flex items-center gap-2">
                  <span className="text-muted-foreground">Page</span>
                  <input
                    type="number"
                    value={page}
                    onChange={(e) => setPage(Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-12 px-3 py-2 bg-secondary border border-border rounded-lg text-foreground text-center"
                  />
                  <span className="text-muted-foreground">
                    of {Math.ceil(creators.total / creators.per_page)}
                  </span>
                </div>
                <button
                  onClick={() =>
                    setPage((p) =>
                      Math.min(
                        Math.ceil(creators.total / creators.per_page),
                        p + 1
                      )
                    )
                  }
                  disabled={page >= Math.ceil(creators.total / creators.per_page)}
                  className="px-6 py-2 bg-primary hover:bg-primary/90 disabled:bg-muted disabled:cursor-not-allowed text-background font-semibold rounded-lg transition-colors"
                >
                  Next
                </button>
              </div>
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground text-lg">
                No creators available at the moment.
              </p>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
