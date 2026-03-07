'use client';

import { motion } from 'framer-motion';
import { Creator } from '@/lib/types';
import { ExternalLink, Heart, Users } from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface CreatorCardProps {
  creator: Creator;
  delay?: number;
}

export function CreatorCard({ creator, delay = 0 }: CreatorCardProps) {
  const platformColors: Record<string, string> = {
    instagram: 'from-pink-500 to-rose-500',
    tiktok: 'from-purple-500 to-pink-500',
    youtube: 'from-red-500 to-pink-500',
    twitter: 'from-blue-400 to-blue-600',
    twitch: 'from-purple-600 to-purple-800',
  };

  const bgGradient = platformColors[creator.platform.toLowerCase()] || 'from-primary to-accent';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      whileHover={{ y: -8, transition: { duration: 0.2 } }}
      className="h-full"
    >
      <Link href={`/creators/${creator.id}`}>
        <div className="relative group h-full bg-secondary/50 rounded-xl overflow-hidden border border-border hover:border-primary/50 transition-all duration-300 cursor-pointer">
          {/* Background gradient */}
          <div
            className={cn(
              'absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 bg-gradient-to-br',
              bgGradient
            )}
          />

          {/* Profile Image Background */}
          <div className="relative h-32 bg-gradient-to-br from-primary/20 to-accent/20 overflow-hidden">
            {creator.profile_image_url && (
              <img
                src={creator.profile_image_url}
                alt={creator.username}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
            )}
            {creator.verified && (
              <div className="absolute top-3 right-3 bg-primary px-2 py-1 rounded-full text-xs font-semibold text-background flex items-center gap-1">
                ✓ Verified
              </div>
            )}
          </div>

          {/* Content */}
          <div className="relative z-10 p-4">
            <div className="mb-3">
              <h3 className="text-lg font-bold text-foreground truncate">
                {creator.username}
              </h3>
              <p className="text-sm text-muted-foreground capitalize">
                {creator.platform}
              </p>
            </div>

            {/* Bio */}
            <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
              {creator.bio || 'No bio available'}
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="bg-muted/50 rounded-lg p-3 group-hover:bg-primary/10 transition-colors">
                <div className="flex items-center gap-2 mb-1">
                  <Users className="w-4 h-4 text-primary" />
                  <span className="text-xs text-muted-foreground">Followers</span>
                </div>
                <p className="text-sm font-bold text-foreground">
                  {(creator.followers_count / 1000).toFixed(1)}K
                </p>
              </div>
              <div className="bg-muted/50 rounded-lg p-3 group-hover:bg-accent/10 transition-colors">
                <div className="flex items-center gap-2 mb-1">
                  <Heart className="w-4 h-4 text-accent" />
                  <span className="text-xs text-muted-foreground">Engagement</span>
                </div>
                <p className="text-sm font-bold text-foreground">
                  {(creator.engagement_rate * 100).toFixed(1)}%
                </p>
              </div>
            </div>

            {/* CTA Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-primary/90 text-background font-semibold py-2 rounded-lg transition-colors duration-200"
            >
              <span>View Profile</span>
              <ExternalLink className="w-4 h-4" />
            </motion.button>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
