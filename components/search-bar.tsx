'use client'

import { Search } from 'lucide-react'

interface SearchBarProps {
  onSearch: () => void
  searchQuery: string
  setSearchQuery: (query: string) => void
  loading: boolean
}

export default function SearchBar({ 
  onSearch, 
  searchQuery, 
  setSearchQuery, 
  loading 
}: SearchBarProps) {
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !loading) {
      onSearch()
    }
  }

  return (
    <div className="glass rounded-xl p-2 flex gap-2">
      <div className="flex-1 flex items-center gap-3 px-4">
        <Search className="w-5 h-5 text-primary flex-shrink-0" />
        <input
          type="text"
          placeholder="Search by name, niche, or keywords..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          className="w-full bg-transparent text-foreground placeholder:text-foreground/50 focus:outline-none text-lg"
        />
      </div>
      <button
        onClick={onSearch}
        disabled={loading || !searchQuery.trim()}
        className="px-8 py-3 bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 disabled:from-muted disabled:to-muted disabled:opacity-50 text-white rounded-lg font-semibold transition-all duration-300 flex-shrink-0"
      >
        {loading ? (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Searching...
          </div>
        ) : (
          'Search'
        )}
      </button>
    </div>
  )
}
