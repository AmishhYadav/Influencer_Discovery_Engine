'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { SearchQuery } from '@/lib/types';
import { Search, X, Sliders } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SearchFiltersProps {
  onSearch: (query: SearchQuery) => void;
  onClear: () => void;
  isLoading?: boolean;
}

const PLATFORMS = ['Instagram', 'TikTok', 'YouTube', 'Twitter', 'Twitch'];
const CATEGORIES = ['Fashion', 'Tech', 'Gaming', 'Fitness', 'Beauty', 'Food', 'Travel', 'Music'];

export function SearchFilters({
  onSearch,
  onClear,
  isLoading = false,
}: SearchFiltersProps) {
  const [keywords, setKeywords] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [minFollowers, setMinFollowers] = useState('');
  const [maxFollowers, setMaxFollowers] = useState('');
  const [minEngagement, setMinEngagement] = useState('');
  const [maxEngagement, setMaxEngagement] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSearch = () => {
    const query: SearchQuery = {};

    if (keywords) {
      query.keywords = keywords.split(',').map((k) => k.trim());
    }
    if (selectedPlatforms.length > 0) {
      query.platforms = selectedPlatforms;
    }
    if (selectedCategories.length > 0) {
      query.category = selectedCategories[0];
    }
    if (minFollowers) {
      query.min_followers = parseInt(minFollowers);
    }
    if (maxFollowers) {
      query.max_followers = parseInt(maxFollowers);
    }
    if (minEngagement) {
      query.min_engagement = parseFloat(minEngagement);
    }
    if (maxEngagement) {
      query.max_engagement = parseFloat(maxEngagement);
    }

    onSearch(query);
  };

  const handleClear = () => {
    setKeywords('');
    setSelectedPlatforms([]);
    setSelectedCategories([]);
    setMinFollowers('');
    setMaxFollowers('');
    setMinEngagement('');
    setMaxEngagement('');
    onClear();
  };

  const hasFilters =
    keywords ||
    selectedPlatforms.length > 0 ||
    selectedCategories.length > 0 ||
    minFollowers ||
    maxFollowers ||
    minEngagement ||
    maxEngagement;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.4 }}
      className="w-full bg-secondary/50 rounded-xl border border-border p-6"
    >
      {/* Search Input */}
      <div className="mb-6">
        <label className="block text-sm font-semibold text-foreground mb-3">
          Search by Keywords
        </label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            placeholder="e.g., photography, fashion, tech"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
          />
        </div>
      </div>

      {/* Filters Toggle */}
      <motion.button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-primary font-semibold mb-4 hover:text-primary/80 transition-colors"
      >
        <Sliders className="w-4 h-4" />
        <span>{isExpanded ? 'Hide' : 'Show'} Advanced Filters</span>
      </motion.button>

      {/* Advanced Filters */}
      <motion.div
        initial={{ opacity: 0, height: 0 }}
        animate={{
          opacity: isExpanded ? 1 : 0,
          height: isExpanded ? 'auto' : 0,
        }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="space-y-6">
          {/* Platforms */}
          <div>
            <label className="block text-sm font-semibold text-foreground mb-3">
              Platforms
            </label>
            <div className="flex flex-wrap gap-2">
              {PLATFORMS.map((platform) => (
                <button
                  key={platform}
                  onClick={() =>
                    setSelectedPlatforms((prev) =>
                      prev.includes(platform)
                        ? prev.filter((p) => p !== platform)
                        : [...prev, platform]
                    )
                  }
                  className={cn(
                    'px-4 py-2 rounded-lg font-semibold transition-all duration-200',
                    selectedPlatforms.includes(platform)
                      ? 'bg-primary text-background'
                      : 'bg-muted text-muted-foreground hover:bg-muted/80'
                  )}
                >
                  {platform}
                </button>
              ))}
            </div>
          </div>

          {/* Categories */}
          <div>
            <label className="block text-sm font-semibold text-foreground mb-3">
              Categories
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {CATEGORIES.map((category) => (
                <button
                  key={category}
                  onClick={() =>
                    setSelectedCategories((prev) =>
                      prev.includes(category)
                        ? prev.filter((c) => c !== category)
                        : [...prev, category]
                    )
                  }
                  className={cn(
                    'px-3 py-2 rounded-lg font-semibold text-sm transition-all duration-200',
                    selectedCategories.includes(category)
                      ? 'bg-accent text-background'
                      : 'bg-muted text-muted-foreground hover:bg-muted/80'
                  )}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Follower Range */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-foreground mb-2">
                Min Followers
              </label>
              <input
                type="number"
                placeholder="1000"
                value={minFollowers}
                onChange={(e) => setMinFollowers(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-2">
                Max Followers
              </label>
              <input
                type="number"
                placeholder="1000000"
                value={maxFollowers}
                onChange={(e) => setMaxFollowers(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
              />
            </div>
          </div>

          {/* Engagement Range */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-foreground mb-2">
                Min Engagement %
              </label>
              <input
                type="number"
                placeholder="0.1"
                step="0.1"
                value={minEngagement}
                onChange={(e) => setMinEngagement(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-foreground mb-2">
                Max Engagement %
              </label>
              <input
                type="number"
                placeholder="50"
                step="0.1"
                value={maxEngagement}
                onChange={(e) => setMaxEngagement(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary transition-colors"
              />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <div className="flex gap-3 mt-6">
        <button
          onClick={handleSearch}
          disabled={isLoading}
          className="flex-1 bg-primary hover:bg-primary/90 disabled:bg-muted disabled:cursor-not-allowed text-background font-semibold py-3 rounded-lg transition-colors duration-200"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
        {hasFilters && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleClear}
            className="px-6 bg-muted hover:bg-muted/80 text-foreground font-semibold py-3 rounded-lg transition-colors duration-200 flex items-center gap-2"
          >
            <X className="w-4 h-4" />
            Clear
          </motion.button>
        )}
      </div>
    </motion.div>
  );
}
