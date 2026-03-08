'use client'

import { useSearchParams } from 'next/navigation'
import { useState, useEffect } from 'react'
import { AnimeNavBar } from '@/components/ui/anime-navbar'
import { useSearch } from '@/lib/hooks'
import CreatorCard from '@/components/creator-card'
import SearchBar from '@/components/search-bar'
import { Search, Users, TrendingUp, Star } from 'lucide-react'
import Link from 'next/link'

export default function SearchPage() {
  const searchParams = useSearchParams()
  const initialQuery = searchParams.get('q') || ''
  const [searchQuery, setSearchQuery] = useState(initialQuery)
  const [filters, setFilters] = useState({
    niche: '',
    minFollowers: 0,
    maxFollowers: 10000000,
    platform: '',
  })
  const [hasSearched, setHasSearched] = useState(false)

  const { results, loading, error, search, totalResults } = useSearch()

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setHasSearched(true)
    await search({
      query: searchQuery,
      niche: filters.niche || undefined,
      min_followers: filters.minFollowers || undefined,
      max_followers: filters.maxFollowers || undefined,
      platform: filters.platform || undefined,
      limit: 20,
    })
  }

  useEffect(() => {
    if (initialQuery) {
      setHasSearched(true)
      search({ query: initialQuery, limit: 20 })
    }
  }, [])

  const navItems = [
    { name: 'Home', url: '/', icon: Search },
    { name: 'Search', url: '/search', icon: Users },
    { name: 'Trending', url: '/trending', icon: TrendingUp },
    { name: 'About', url: '/about', icon: Star },
  ]

  return (
    <main className="min-h-screen bg-background">
      <AnimeNavBar items={navItems} defaultActive="Search" />

      <div className="pt-24 px-4">
        <div className="max-w-6xl mx-auto">
          {/* Search Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">
              Find Perfect Influencers
            </h1>
            <p className="text-lg text-foreground/70 max-w-2xl mx-auto text-balance">
              Search across multiple platforms to find creators that match your brand
            </p>
          </div>

          {/* Search Bar */}
          <SearchBar 
            onSearch={handleSearch}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            loading={loading}
          />

          {/* Filters */}
          <div className="grid md:grid-cols-4 gap-4 mt-8">
            <input
              type="text"
              placeholder="Niche (e.g., fitness, fashion)"
              value={filters.niche}
              onChange={(e) => setFilters({ ...filters, niche: e.target.value })}
              className="px-4 py-3 bg-muted/50 border border-white/10 rounded-lg text-foreground placeholder:text-foreground/50 focus:outline-none focus:border-primary transition-colors"
            />
            <select
              value={filters.platform}
              onChange={(e) => setFilters({ ...filters, platform: e.target.value })}
              className="px-4 py-3 bg-muted/50 border border-white/10 rounded-lg text-foreground focus:outline-none focus:border-primary transition-colors"
            >
              <option value="">All Platforms</option>
              <option value="instagram">Instagram</option>
              <option value="tiktok">TikTok</option>
              <option value="youtube">YouTube</option>
              <option value="twitter">Twitter</option>
            </select>
            <input
              type="number"
              placeholder="Min Followers"
              value={filters.minFollowers}
              onChange={(e) => setFilters({ ...filters, minFollowers: parseInt(e.target.value) || 0 })}
              className="px-4 py-3 bg-muted/50 border border-white/10 rounded-lg text-foreground placeholder:text-foreground/50 focus:outline-none focus:border-primary transition-colors"
            />
            <input
              type="number"
              placeholder="Max Followers"
              value={filters.maxFollowers}
              onChange={(e) => setFilters({ ...filters, maxFollowers: parseInt(e.target.value) || 10000000 })}
              className="px-4 py-3 bg-muted/50 border border-white/10 rounded-lg text-foreground placeholder:text-foreground/50 focus:outline-none focus:border-primary transition-colors"
            />
          </div>

          {/* Results Section */}
          {error && (
            <div className="mt-12 p-6 bg-accent/10 border border-accent/30 rounded-lg">
              <p className="text-accent text-center">{error}</p>
            </div>
          )}

          {hasSearched && !loading && results.length === 0 && !error && (
            <div className="mt-12 text-center">
              <p className="text-foreground/70 text-lg">No creators found. Try adjusting your search criteria.</p>
            </div>
          )}

          {loading && (
            <div className="mt-12 grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-80 bg-muted/30 rounded-lg animate-pulse" />
              ))}
            </div>
          )}

          {results.length > 0 && (
            <>
              <div className="mt-12 mb-8">
                <p className="text-foreground/70">
                  Found <span className="text-primary font-semibold">{totalResults}</span> creators
                </p>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 pb-20">
                {results.map((creator) => (
                  <Link key={creator.id} href={`/creators/${creator.id}`}>
                    <CreatorCard creator={creator} />
                  </Link>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  )
}
