'use client'

import { useParams } from 'next/navigation'
import { AnimeNavBar } from '@/components/ui/anime-navbar'
import { useCreatorDetail } from '@/lib/hooks'
import { Search, Users, TrendingUp, Star, ExternalLink, Mail } from 'lucide-react'
import Link from 'next/link'

export default function CreatorDetailPage() {
  const params = useParams()
  const creatorId = params.id as string
  const { detail, loading, error } = useCreatorDetail(creatorId)

  const navItems = [
    { name: 'Home', url: '/', icon: Search },
    { name: 'Search', url: '/search', icon: Users },
    { name: 'Trending', url: '/trending', icon: TrendingUp },
    { name: 'About', url: '/about', icon: Star },
  ]

  return (
    <main className="min-h-screen bg-background">
      <AnimeNavBar items={navItems} />

      <div className="pt-24 px-4 pb-20">
        <div className="max-w-4xl mx-auto">
          {error && (
            <div className="p-6 bg-accent/10 border border-accent/30 rounded-lg text-center">
              <p className="text-accent">{error}</p>
            </div>
          )}

          {loading && (
            <div className="space-y-6">
              <div className="h-64 bg-muted/30 rounded-lg animate-pulse" />
              <div className="h-32 bg-muted/30 rounded-lg animate-pulse" />
            </div>
          )}

          {detail && (
            <>
              {/* Header */}
              <div className="glass rounded-xl overflow-hidden mb-8">
                <div className="h-64 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">
                  {detail.creator.image_url ? (
                    <img 
                      src={detail.creator.image_url} 
                      alt={detail.creator.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="text-6xl font-bold text-primary/50">
                      {detail.creator.name.charAt(0)}
                    </div>
                  )}
                </div>

                <div className="p-8">
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
                    <div>
                      <h1 className="text-4xl font-bold text-foreground mb-2">
                        {detail.creator.name}
                      </h1>
                      <p className="text-lg text-foreground/70 mb-4">
                        @{detail.creator.username || 'creator'}
                      </p>
                      {detail.creator.platform && (
                        <div className="flex gap-2 mb-4">
                          <span className="px-4 py-2 bg-primary/20 rounded-lg text-primary font-semibold">
                            {detail.creator.platform.toUpperCase()}
                          </span>
                          {detail.creator.niche && (
                            <span className="px-4 py-2 bg-secondary/20 rounded-lg text-secondary font-semibold">
                              {detail.creator.niche}
                            </span>
                          )}
                        </div>
                      )}
                      {detail.creator.bio && (
                        <p className="text-foreground/80 max-w-2xl">
                          {detail.creator.bio}
                        </p>
                      )}
                    </div>

                    <div className="flex flex-col gap-3">
                      {detail.creator.profile_url && (
                        <a
                          href={detail.creator.profile_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-6 py-3 bg-primary/20 hover:bg-primary/30 border border-primary/50 rounded-lg text-primary font-semibold flex items-center justify-center gap-2 transition-colors"
                        >
                          <ExternalLink className="w-4 h-4" />
                          Visit Profile
                        </a>
                      )}
                      <button className="px-6 py-3 bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 text-white rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors">
                        <Mail className="w-4 h-4" />
                        Contact
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Stats */}
              <div className="grid md:grid-cols-4 gap-4 mb-8">
                {[
                  {
                    label: 'Followers',
                    value: detail.stats.followers,
                    format: (v: number) => `${(v / 1000).toFixed(1)}K`
                  },
                  {
                    label: 'Engagement Rate',
                    value: detail.stats.engagement_rate,
                    format: (v: number) => `${(v * 100).toFixed(1)}%`
                  },
                  {
                    label: 'Recent Posts',
                    value: detail.stats.recent_posts,
                    format: (v: number) => v.toString()
                  },
                  {
                    label: 'Avg Views',
                    value: detail.stats.average_views,
                    format: (v: number) => `${(v / 1000).toFixed(1)}K`
                  },
                ].map((stat, idx) => (
                  <div key={idx} className="glass rounded-xl p-6 text-center">
                    <p className="text-foreground/60 text-sm font-medium mb-2">
                      {stat.label}
                    </p>
                    <p className="text-3xl font-bold text-foreground">
                      {stat.format(stat.value)}
                    </p>
                  </div>
                ))}
              </div>

              {/* Top Content */}
              {detail.top_content && detail.top_content.length > 0 && (
                <div className="glass rounded-xl p-8">
                  <h2 className="text-2xl font-bold text-foreground mb-6">
                    Top Performing Content
                  </h2>
                  <div className="space-y-4">
                    {detail.top_content.map((content, idx) => (
                      <div key={idx} className="p-4 bg-white/5 rounded-lg border border-white/10">
                        <div className="flex justify-between items-start gap-4">
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-foreground mb-1">
                              {content.title}
                            </h3>
                            <p className="text-sm text-foreground/60">
                              {new Date(content.posted_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-foreground/60 mb-1">Engagement</p>
                            <p className="text-xl font-bold text-primary">
                              {(content.engagement / 1000).toFixed(1)}K
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  )
}
