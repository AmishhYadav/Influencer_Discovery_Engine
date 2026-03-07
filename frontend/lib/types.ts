export interface Creator {
  id: string;
  username: string;
  platform: string;
  profile_url: string;
  followers_count: number;
  engagement_rate: number;
  bio: string;
  profile_image_url?: string;
  verified: boolean;
}

export interface SearchQuery {
  keywords?: string[];
  platforms?: string[];
  min_followers?: number;
  max_followers?: number;
  min_engagement?: number;
  max_engagement?: number;
  category?: string;
}

export interface SearchResponse {
  creators: Creator[];
  total: number;
  page: number;
  per_page: number;
}

export interface CreatorDetail extends Creator {
  posts_count: number;
  average_likes: number;
  average_comments: number;
  most_used_hashtags: string[];
  recent_posts: Post[];
}

export interface Post {
  id: string;
  title?: string;
  content?: string;
  likes_count: number;
  comments_count: number;
  shares_count?: number;
  created_at: string;
  media_url?: string;
}

export interface FilterOptions {
  platforms: string[];
  categories: string[];
  followers_range: [number, number];
  engagement_range: [number, number];
}
