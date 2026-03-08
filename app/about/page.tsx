'use client'

import { AnimeNavBar } from '@/components/ui/anime-navbar'
import { Search, Users, TrendingUp, Star, Zap, Shield, Globe } from 'lucide-react'
import Link from 'next/link'

export default function AboutPage() {
  const navItems = [
    { name: 'Home', url: '/', icon: Search },
    { name: 'Search', url: '/search', icon: Users },
    { name: 'Trending', url: '/trending', icon: TrendingUp },
    { name: 'About', url: '/about', icon: Star },
  ]

  return (
    <main className="min-h-screen bg-background">
      <AnimeNavBar items={navItems} defaultActive="About" />

      <div className="pt-24 px-4">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">
              About Influencer Discovery Engine
            </h1>
            <p className="text-lg text-foreground/70 text-balance">
              Revolutionizing how brands find and connect with influencers
            </p>
          </div>

          {/* Main Content */}
          <div className="space-y-16">
            {/* Mission */}
            <section className="glass rounded-xl p-8">
              <h2 className="text-3xl font-bold text-foreground mb-4">Our Mission</h2>
              <p className="text-foreground/80 text-lg leading-relaxed text-balance">
                We believe in democratizing influencer marketing. Our mission is to make it easy for brands of all sizes to find, analyze, and collaborate with the perfect influencers for their campaigns. By leveraging advanced technology and data analysis, we help create meaningful connections between brands and creators.
              </p>
            </section>

            {/* Features */}
            <section>
              <h2 className="text-3xl font-bold text-foreground mb-8 text-center">Why Choose Us</h2>
              <div className="grid md:grid-cols-3 gap-6">
                {[
                  {
                    icon: Zap,
                    title: 'Lightning Fast',
                    description: 'Search millions of creators in seconds with our optimized search engine'
                  },
                  {
                    icon: Globe,
                    title: 'Multi-Platform',
                    description: 'Access data from Instagram, TikTok, YouTube, Twitter, and more in one place'
                  },
                  {
                    icon: Shield,
                    title: 'Verified Data',
                    description: 'Our algorithms ensure you get accurate, up-to-date creator information'
                  },
                ].map((feature, idx) => (
                  <div key={idx} className="glass rounded-xl p-6">
                    <feature.icon className="w-12 h-12 text-primary mb-4" />
                    <h3 className="text-xl font-bold text-foreground mb-2">{feature.title}</h3>
                    <p className="text-foreground/70">{feature.description}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* Technology */}
            <section className="glass rounded-xl p-8">
              <h2 className="text-3xl font-bold text-foreground mb-4">Our Technology</h2>
              <p className="text-foreground/80 mb-6 text-balance">
                Built with cutting-edge machine learning and real-time data processing, our platform analyzes thousands of data points to help you make informed decisions. We use advanced algorithms to calculate engagement metrics, audience demographics, and growth trends.
              </p>
              <ul className="space-y-3">
                {[
                  'Real-time creator analytics and engagement tracking',
                  'AI-powered recommendation system',
                  'Multi-source data aggregation and validation',
                  'Advanced filtering and search capabilities',
                  'Secure API for integration with your tools'
                ].map((point, idx) => (
                  <li key={idx} className="flex items-center gap-3 text-foreground/80">
                    <div className="w-2 h-2 bg-primary rounded-full" />
                    {point}
                  </li>
                ))}
              </ul>
            </section>

            {/* CTA Section */}
            <section className="glass rounded-xl p-12 text-center">
              <h2 className="text-3xl font-bold text-foreground mb-4">Ready to Get Started?</h2>
              <p className="text-lg text-foreground/70 mb-8 max-w-2xl mx-auto text-balance">
                Join thousands of brands already discovering their perfect influencers with our platform.
              </p>
              <Link 
                href="/search"
                className="inline-block px-8 py-4 bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 text-white rounded-lg font-semibold transition-all duration-300 hover:scale-105"
              >
                Start Your Search Today
              </Link>
            </section>
          </div>
        </div>
      </div>
    </main>
  )
}
