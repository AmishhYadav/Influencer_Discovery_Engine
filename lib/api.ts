import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Creator {
  id: string
  name: string
  username?: string
  platform?: string
  followers?: number
  engagement_rate?: number
  bio?: string
  profile_url?: string
  image_url?: string
  categories?: string[]
  niche?: string
  average_views?: number
  recent_posts?: number
}

export interface SearchParams {
  query: string
  platform?: string
  min_followers?: number
  max_followers?: number
  niche?: string
  engagement_threshold?: number
  limit?: number
  offset?: number
}

export interface SearchResponse {
  results: Creator[]
  total: number
  query: string
  search_time: number
}

export interface CreatorDetailResponse {
  creator: Creator
  stats: {
    followers: number
    engagement_rate: number
    recent_posts: number
    average_views: number
  }
  top_content?: Array<{
    title: string
    engagement: number
    posted_at: string
  }>
}

// Search endpoints
export const searchCreators = async (params: SearchParams): Promise<SearchResponse> => {
  const response = await apiClient.post('/search', params)
  return response.data
}

export const getCreatorsByNiche = async (
  niche: string,
  limit?: number
): Promise<Creator[]> => {
  const response = await apiClient.get('/creators/by-niche', {
    params: { niche, limit },
  })
  return response.data.creators
}

export const getCreatorDetail = async (creatorId: string): Promise<CreatorDetailResponse> => {
  const response = await apiClient.get(`/creators/${creatorId}`)
  return response.data
}

export const getTrendingCreators = async (limit?: number): Promise<Creator[]> => {
  const response = await apiClient.get('/creators/trending', {
    params: { limit },
  })
  return response.data.creators
}

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/health')
    return response.status === 200
  } catch (error) {
    return false
  }
}

export default apiClient
