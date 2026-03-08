'use client'

import { useState } from 'react'
import { AnimeNavBar } from '@/components/ui/anime-navbar'
import Hero from '@/components/ui/animated-shader-hero'
import { InteractiveHoverButton } from '@/components/ui/interactive-hover-button'
import { Search, Star, TrendingUp, Users } from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearchClick = () => {
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`
    }
  }

  const navItems = [
    { name: 'Home', url: '/', icon: Search },
    { name: 'Search', url: '/search', icon: Users },
    { name: 'Trending', url: '/trending', icon: TrendingUp },
    { name: 'About', url: '/about', icon: Star },
  ]

  return (
    <main className="min-h-screen bg-background">
      <AnimeNavBar items={navItems} defaultActive="Home" />
      
      <Hero
        trustBadge={{
          text: 'Trusted by brands worldwide',
          icons: ['✨'],
        }}
        headline={{
          line1: 'Discover',
          line2: 'Influential Creators',
        }}
        subtitle="Connect with the perfect influencers for your brand. Search, analyze, and collaborate with creators across multiple platforms."
        buttons={{
          primary: {
            text: 'Start Discovering',
            onClick: () => (window.location.href = '/search'),
          },
          secondary: {
            text: 'Explore Trending',
            onClick: () => (window.location.href = '/trending'),
          },
        }}
      />

      <section className="relative z-10 bg-gradient-to-b from-background via-muted to-background px-4 py-20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">
              How It Works
            </h2>
            <p className="text-lg text-foreground/70 max-w-2xl mx-auto text-balance">
              Our intelligent discovery engine helps you find the right influencers for your campaign
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Search,
                title: 'Search',
                description: 'Find influencers by niche, platform, or engagement metrics across multiple channels'
              },
              {
                icon: TrendingUp,
                title: 'Analyze',
                description: 'View detailed analytics including audience demographics, engagement rates, and growth trends'
              },
              {
                icon: Users,
                title: 'Connect',
                description: 'Reach out to creators directly and manage your influencer partnerships in one place'
              },
            ].map((feature, idx) => (
              <div
                key={idx}
                className="glass rounded-xl p-8 hover:bg-white/10 transition-all duration-300"
              >
                <feature.icon className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-xl font-bold text-foreground mb-2">{feature.title}</h3>
                <p className="text-foreground/70">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative z-10 bg-background px-4 py-20 border-t border-white/10">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-8 text-balance">
            Ready to Find Your Next Brand Ambassador?
          </h2>
          <p className="text-lg text-foreground/70 mb-8 text-balance">
            Start exploring thousands of verified influencers and grow your brand today.
          </p>
          <Link href="/search" className="inline-block">
            <InteractiveHoverButton text="Start Searching" />
          </Link>
        </div>
      </section>
    </main>
  )
}
