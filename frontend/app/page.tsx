'use client';

import { useState } from 'react';
import { HeroGeometric } from '@/components/ui/shape-landing-hero';
import { AnimeNavBar } from '@/components/ui/anime-navbar';
import { SearchFilters } from '@/components/search-filters';
import { CreatorCard } from '@/components/creator-card';
import { useSearch } from '@/hooks/useApi';
import { SearchQuery } from '@/lib/types';
import { Zap, Sparkles, TrendingUp } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState<SearchQuery | null>(null);
  const { results, isLoading, error } = useSearch(searchQuery);

  const navItems = [
    { name: 'Home', url: '/', icon: Sparkles },
    { name: 'Search', url: '#search', icon: Zap },
    { name: 'Explore', url: '/explore', icon: TrendingUp },
  ];

  const handleSearch = (query: SearchQuery) => {
    setSearchQuery(query);
  };

  const handleClear = () => {
    setSearchQuery(null);
  };

  const handleCtaClick = () => {
    const searchSection = document.getElementById('search');
    searchSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <main className="min-h-screen bg-background">
      {/* Navbar */}
      <AnimeNavBar
        items={navItems}
        defaultActive="Home"
        logo={
          <div className="text-lg font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            IDE
          </div>
        }
      />

      {/* Hero Section */}
      <HeroGeometric
        badge="Influencer Discovery Engine"
        title1="Find Your Perfect"
        title2="Influencer Partners"
        description="Discover and analyze influencers across Instagram, TikTok, YouTube, Twitter, and more. Advanced filtering, real-time metrics, and data-driven insights."
        ctaText="Start Discovering"
        onCta={handleCtaClick}
      />

      {/* Search Section */}
      <section
        id="search"
        className="relative z-20 py-20 px-4 sm:px-6 lg:px-8 bg-background"
      >
        <div className="max-w-6xl mx-auto">
          <div className="mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
              Advanced Creator Discovery
            </h2>
            <p className="text-lg text-muted-foreground">
              Use our powerful filters to find creators that match your brand perfectly.
            </p>
          </div>

          <SearchFilters
            onSearch={handleSearch}
            onClear={handleClear}
            isLoading={isLoading}
          />
        </div>
      </section>

      {/* Results Section */}
      {searchQuery && (
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-background">
          <div className="max-w-6xl mx-auto">
            <div className="mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-2">
                Results
              </h2>
              {isLoading && (
                <p className="text-muted-foreground">Searching for creators...</p>
              )}
              {!isLoading && results && (
                <p className="text-muted-foreground">
                  Found {results.total} creators
                </p>
              )}
              {error && (
                <p className="text-red-500">Error loading results. Please try again.</p>
              )}
            </div>

            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="h-96 bg-secondary/30 rounded-xl animate-pulse"
                  />
                ))}
              </div>
            ) : results && results.creators.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.creators.map((creator, index) => (
                  <CreatorCard
                    key={creator.id}
                    creator={creator}
                    delay={index * 0.1}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-muted-foreground text-lg">
                  No creators found matching your criteria.
                </p>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Featured Creators Section */}
      {!searchQuery && (
        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-secondary/30">
          <div className="max-w-6xl mx-auto">
            <div className="mb-12">
              <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
                Featured Creators
              </h2>
              <p className="text-lg text-muted-foreground">
                Check out some of our top-rated influencers across different platforms.
              </p>
            </div>

            <div className="text-center py-12">
              <p className="text-muted-foreground text-lg mb-6">
                Featured creators will be displayed here
              </p>
              <Link
                href="/explore"
                className="inline-block px-6 py-3 bg-primary hover:bg-primary/90 text-background font-semibold rounded-lg transition-colors"
              >
                Explore All Creators
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="border-t border-border bg-background py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-lg font-bold text-foreground mb-4">IDE</h3>
              <p className="text-muted-foreground">
                Discover and analyze influencers across all platforms.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Product</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Search
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Analytics
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Company</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Contact
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-4">Legal</h4>
              <ul className="space-y-2 text-muted-foreground">
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Privacy
                  </a>
                </li>
                <li>
                  <a href="#" className="hover:text-foreground transition-colors">
                    Terms
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border pt-8 text-center text-muted-foreground">
            <p>&copy; 2024 Influencer Discovery Engine. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
