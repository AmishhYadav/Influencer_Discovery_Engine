'use client'

import { Creator } from '@/lib/api'
import { Users, TrendingUp, Heart } from 'lucide-react'

interface CreatorCardProps {
  creator: Creator
}

export default function CreatorCard({ creator }: CreatorCardProps) {
  return (
    <div className="group glass rounded-xl overflow-hidden hover:bg-white/10 transition-all duration-300 hover:scale-105 cursor-pointer">
      {/* Image */}
      <div className="w-full h-48 bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center overflow-hidden relative">
        {creator.image_url ? (
          <img 
            src={creator.image_url} 
            alt={creator.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
          />
        ) : (
          <div className="text-4xl font-bold text-primary/50">
            {creator.name.charAt(0)}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-bold text-foreground mb-1 truncate">
          {creator.name}
        </h3>
        <p className="text-sm text-foreground/60 mb-4 truncate">
          @{creator.username || 'creator'}
        </p>

        {/* Stats */}
        <div className="space-y-3">
          {creator.platform && (
            <div className="flex items-center gap-2 text-sm">
              <span className="px-2 py-1 bg-primary/20 rounded-md text-primary font-medium">
                {creator.platform}
              </span>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3 text-sm">
            {creator.followers && (
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-secondary" />
                <div>
                  <p className="text-foreground/60 text-xs">Followers</p>
                  <p className="text-foreground font-semibold">
                    {(creator.followers / 1000).toFixed(1)}K
                  </p>
                </div>
              </div>
            )}
            {creator.engagement_rate && (
              <div className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-accent" />
                <div>
                  <p className="text-foreground/60 text-xs">Engagement</p>
                  <p className="text-foreground font-semibold">
                    {(creator.engagement_rate * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            )}
          </div>

          {creator.niche && (
            <p className="text-xs text-foreground/60">
              <span className="text-primary font-semibold">Niche:</span> {creator.niche}
            </p>
          )}

          {creator.bio && (
            <p className="text-xs text-foreground/70 line-clamp-2">
              {creator.bio}
            </p>
          )}
        </div>

        {/* View Profile Button */}
        <button className="w-full mt-4 px-4 py-2 bg-primary/20 hover:bg-primary/30 border border-primary/50 rounded-lg text-primary font-semibold transition-colors">
          View Profile
        </button>
      </div>
    </div>
  )
}
