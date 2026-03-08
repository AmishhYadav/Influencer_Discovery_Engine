'use client'

import { useEffect } from 'react'
import { AnimeNavBar } from '@/components/ui/anime-navbar'
import { useTrendingCreators } from '@/lib/hooks'
import CreatorCard from '@/components/creator-card'
import { Search, Users, TrendingUp, Star } from 'lucide-react'
import Link from 'next/link'

export default function TrendingPage() {
  const { creators, loading, error } = useTrendingCreators(15)

  const navItems = [
    { name: 'Home', url: '/', icon: Search },
    { name: 'Search', url: '/search', icon: Users },
    { name: 'Trending', url: '/trending', icon: TrendingUp },
    { name: 'About', url: '/about', icon: Star },
  ]

  return (
    <main className="min-h-screen bg-background">
      <AnimeNavBar items={navItems} defaultActive="Trending" />

      <div className="pt-24 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">
              Trending Influencers
            </h1>
            <p className="text-lg text-foreground/70 max-w-2xl mx-auto text-balance">
              Discover the most popular creators right now across all platforms
            </p>
          </div>

          {/* Results */}
          {error && (
            <div className="p-6 bg-accent/10 border border-accent/30 rounded-lg text-center">
              <p className="text-accent">{error}</p>
            </div>
          )}

          {loading && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="h-96 bg-muted/30 rounded-lg animate-pulse" />
              ))}
            </div>
          )}

          {!loading && creators.length === 0 && !error && (
            <div className="text-center">
              <p className="text-foreground/70 text-lg">No trending creators found.</p>
            </div>
          )}

          {creators.length > 0 && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 pb-20">
              {creators.map((creator, idx) => (
                <Link key={creator.id} href={`/creators/${creator.id}`}>
                  <div className="relative">
                    {idx < 3 && (
                      <div className="absolute -top-3 -right-3 z-10">
                        <div className="w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-lg">
                          #{idx + 1}
                        </div>
                      </div>
                    )}
                    <CreatorCard creator={creator} />
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
