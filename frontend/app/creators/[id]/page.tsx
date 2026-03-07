'use client';

import { useParams, useRouter } from 'next/navigation';
import { AnimeNavBar } from '@/components/ui/anime-navbar';
import { useCreator } from '@/hooks/useApi';
import { Zap, Sparkles, TrendingUp, ArrowLeft, ExternalLink, Heart, Users, BarChart3 } from 'lucide-react';

export default function CreatorDetailPage() {
  const router = useRouter();
  const params = useParams();
  const creatorId = params.id as string;
  const { creator, isLoading, error } = useCreator(creatorId);

  const navItems = [
    { name: 'Home', url: '/', icon: Sparkles },
    { name: 'Search', url: '/#search', icon: Zap },
    { name: 'Explore', url: '/explore', icon: TrendingUp },
  ];

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background pt-24">
        <AnimeNavBar items={navItems} defaultActive="Explore" />
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="h-96 bg-secondary/30 rounded-xl animate-pulse" />
        </div>
      </main>
    );
  }

  if (error || !creator) {
    return (
      <main className="min-h-screen bg-background pt-24">
        <AnimeNavBar items={navItems} defaultActive="Explore" />
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <p className="text-red-500 text-lg mb-6">Error loading creator details</p>
          <button
            onClick={() => router.back()}
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary/90 text-background font-semibold rounded-lg transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Go Back
          </button>
        </div>
      </main>
    );
  }

  const platformColors: Record<string, string> = {
    instagram: 'from-pink-500 to-rose-500',
    tiktok: 'from-purple-500 to-pink-500',
    youtube: 'from-red-500 to-pink-500',
    twitter: 'from-blue-400 to-blue-600',
    twitch: 'from-purple-600 to-purple-800',
  };

  const bgGradient =
    platformColors[creator.platform.toLowerCase()] || 'from-primary to-accent';

  return (
    <main className="min-h-screen bg-background pt-24">
      {/* Navbar */}
      <AnimeNavBar items={navItems} defaultActive="Explore" />

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Back Button */}
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-2 text-primary hover:text-primary/80 font-semibold mb-8 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>

        {/* Creator Header */}
        <div className="bg-secondary/50 rounded-xl border border-border overflow-hidden mb-8">
          {/* Cover Image */}
          <div className={`bg-gradient-to-br ${bgGradient} h-48 relative`}>
            {creator.profile_image_url && (
              <img
                src={creator.profile_image_url}
                alt={creator.username}
                className="w-full h-full object-cover opacity-50"
              />
            )}
          </div>

          {/* Profile Info */}
          <div className="relative px-8 py-8 -mt-20">
            <div className="flex flex-col sm:flex-row sm:items-end gap-6">
              {/* Avatar */}
              <div className="w-40 h-40 rounded-2xl border-4 border-background bg-secondary/50 overflow-hidden flex-shrink-0">
                {creator.profile_image_url && (
                  <img
                    src={creator.profile_image_url}
                    alt={creator.username}
                    className="w-full h-full object-cover"
                  />
                )}
              </div>

              {/* Info */}
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h1 className="text-4xl font-bold text-foreground">
                    {creator.username}
                  </h1>
                  {creator.verified && (
                    <div className="bg-primary text-background px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
                      ✓ Verified
                    </div>
                  )}
                </div>
                <p className="text-lg text-muted-foreground capitalize mb-4">
                  {creator.platform}
                </p>
                <p className="text-foreground mb-6">{creator.bio}</p>

                {/* CTA */}
                <a
                  href={creator.profile_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 bg-primary hover:bg-primary/90 text-background font-semibold rounded-lg transition-colors"
                >
                  <span>Visit Profile</span>
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          {/* Followers */}
          <div className="bg-secondary/50 rounded-xl border border-border p-6">
            <div className="flex items-center gap-3 mb-2">
              <Users className="w-5 h-5 text-primary" />
              <span className="text-sm font-semibold text-muted-foreground">
                Followers
              </span>
            </div>
            <p className="text-3xl font-bold text-foreground">
              {(creator.followers_count / 1000000).toFixed(2)}M
            </p>
          </div>

          {/* Engagement */}
          <div className="bg-secondary/50 rounded-xl border border-border p-6">
            <div className="flex items-center gap-3 mb-2">
              <Heart className="w-5 h-5 text-accent" />
              <span className="text-sm font-semibold text-muted-foreground">
                Engagement Rate
              </span>
            </div>
            <p className="text-3xl font-bold text-foreground">
              {(creator.engagement_rate * 100).toFixed(2)}%
            </p>
          </div>

          {/* Posts */}
          <div className="bg-secondary/50 rounded-xl border border-border p-6">
            <div className="flex items-center gap-3 mb-2">
              <BarChart3 className="w-5 h-5 text-cyan-500" />
              <span className="text-sm font-semibold text-muted-foreground">
                Total Posts
              </span>
            </div>
            <p className="text-3xl font-bold text-foreground">
              {('posts_count' in creator && creator.posts_count) || 'N/A'}
            </p>
          </div>
        </div>

        {/* Additional Info */}
        {'most_used_hashtags' in creator && creator.most_used_hashtags && (
          <div className="bg-secondary/50 rounded-xl border border-border p-6">
            <h2 className="text-xl font-bold text-foreground mb-4">
              Most Used Hashtags
            </h2>
            <div className="flex flex-wrap gap-2">
              {creator.most_used_hashtags.map((tag, index) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-primary/10 text-primary rounded-lg text-sm font-semibold"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
