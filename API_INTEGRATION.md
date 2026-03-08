# API Integration Guide

This document describes how the React frontend integrates with the FastAPI backend.

## Architecture Overview

```
┌─────────────────────────────┐
│   React Frontend (Next.js)  │
│                             │
│  ┌────────────────────────┐ │
│  │  Components & Pages    │ │
│  └────────────┬───────────┘ │
│               │              │
│  ┌────────────▼───────────┐ │
│  │   Custom Hooks         │ │
│  │ (useSearch, etc.)      │ │
│  └────────────┬───────────┘ │
│               │              │
│  ┌────────────▼───────────┐ │
│  │   API Client (axios)   │ │
│  └────────────┬───────────┘ │
└───────────────┼──────────────┘
                │
                │ HTTP/REST
                │
┌───────────────▼──────────────┐
│   FastAPI Backend            │
│                              │
│  /search                    │
│  /creators/trending         │
│  /creators/by-niche         │
│  /creators/{id}             │
└──────────────────────────────┘
```

## API Client Setup

The API client is configured in `lib/api.ts`:

```typescript
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

## Endpoints

### 1. Search Creators
**Endpoint**: `POST /search`

**Request**:
```typescript
interface SearchParams {
  query: string                    // Search query (required)
  platform?: string               // Filter by platform (instagram, tiktok, youtube, etc.)
  min_followers?: number          // Minimum follower count
  max_followers?: number          // Maximum follower count
  niche?: string                  // Creator niche/category
  engagement_threshold?: number   // Minimum engagement rate
  limit?: number                  // Results per page (default: 20)
  offset?: number                 // Pagination offset (default: 0)
}
```

**Response**:
```typescript
interface SearchResponse {
  results: Creator[]              // Array of creator objects
  total: number                   // Total number of results
  query: string                   // The search query used
  search_time: number             // Search execution time in ms
}
```

**Usage**:
```typescript
const { results, loading, error, search } = useSearch()

await search({
  query: 'fitness influencer',
  platform: 'instagram',
  min_followers: 10000,
  limit: 20
})
```

### 2. Get Trending Creators
**Endpoint**: `GET /creators/trending`

**Query Parameters**:
```
?limit=10   // Number of creators to return (default: 10)
```

**Response**:
```typescript
interface CreatorListResponse {
  creators: Creator[]
  total: number
}
```

**Usage**:
```typescript
const { creators, loading, error } = useTrendingCreators(10)
```

### 3. Get Creators by Niche
**Endpoint**: `GET /creators/by-niche`

**Query Parameters**:
```
?niche=fitness    // Required: creator niche
&limit=10         // Optional: number of results
```

**Response**:
```typescript
interface CreatorListResponse {
  creators: Creator[]
  total: number
}
```

**Usage**:
```typescript
const { creators, loading, error } = useCreatorsByNiche('fashion')
```

### 4. Get Creator Details
**Endpoint**: `GET /creators/{creatorId}`

**Response**:
```typescript
interface CreatorDetailResponse {
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
```

**Usage**:
```typescript
const { detail, loading, error } = useCreatorDetail('creator-id-123')
```

## Data Models

### Creator
```typescript
interface Creator {
  id: string
  name: string
  username?: string
  platform?: string              // instagram, tiktok, youtube, twitter
  followers?: number
  engagement_rate?: number       // 0-1 (multiply by 100 for percentage)
  bio?: string
  profile_url?: string
  image_url?: string
  categories?: string[]
  niche?: string
  average_views?: number
  recent_posts?: number
}
```

## Error Handling

The API client handles errors gracefully:

```typescript
try {
  const response = await searchCreators(params)
  // Handle success
} catch (error) {
  if (error instanceof AxiosError) {
    console.error('API Error:', error.response?.data)
  } else {
    console.error('Unexpected error:', error)
  }
}
```

All custom hooks return an `error` property:

```typescript
const { results, loading, error, search } = useSearch()

if (error) {
  // Display error message to user
  console.error('Search failed:', error)
}
```

## Backend Requirements

### CORS Configuration
The FastAPI backend must allow requests from the frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Response Format
All endpoints should return JSON responses matching the interfaces defined above.

### Status Codes
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Timeout Configuration

The API client is configured with a 10-second timeout. Adjust in `lib/api.ts`:

```typescript
const apiClient: AxiosInstance = axios.create({
  timeout: 10000, // milliseconds
  // ...
})
```

## Environment Variables

### Required
- `NEXT_PUBLIC_API_URL` - Base URL of the FastAPI backend

### Example .env.local
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing the Integration

### Using curl
```bash
# Search endpoint
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "fitness"}'

# Trending creators
curl http://localhost:8000/creators/trending?limit=10

# Creator details
curl http://localhost:8000/creators/123
```

### Using the React Frontend
1. Start the backend: `python -m src.api.main` (or your run command)
2. Configure `.env.local` with correct `NEXT_PUBLIC_API_URL`
3. Start the frontend: `npm run dev`
4. Navigate to http://localhost:3000
5. Try searching or browsing trending creators

## Debugging

### Enable Debug Logging
Add this to `lib/api.ts`:

```typescript
// Log all requests
apiClient.interceptors.request.use(config => {
  console.log('[API Request]', config.method?.toUpperCase(), config.url)
  return config
})

// Log all responses
apiClient.interceptors.response.use(
  response => {
    console.log('[API Response]', response.status, response.config.url)
    return response
  },
  error => {
    console.error('[API Error]', error.response?.status, error.config?.url)
    return Promise.reject(error)
  }
)
```

### Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform a search
4. Click on the API request to see:
   - Request headers and body
   - Response headers and body
   - Network timing

### Verify Backend is Running
```bash
curl http://localhost:8000/health
# Should return 200 OK
```

## Performance Considerations

### Caching
The Axios client can be configured with caching middleware for frequently accessed data:

```typescript
// Implement request caching for GET requests
apiClient.interceptors.response.use(response => {
  if (response.config.method === 'get') {
    // Cache implementation here
  }
  return response
})
```

### Request Debouncing
For search inputs, consider debouncing to reduce API calls:

```typescript
import { useCallback } from 'react'

const debouncedSearch = useCallback(
  debounce((query) => search({ query }), 300),
  [search]
)
```

## Security

### API Key Protection
If the backend requires authentication:

```typescript
// In lib/api.ts
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### HTTPS in Production
Always use HTTPS URLs in production:

```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Common Issues

### 1. CORS Errors
**Error**: `Access to XMLHttpRequest at 'http://localhost:8000/search' blocked by CORS policy`

**Solution**: Ensure backend has CORS middleware configured (see Backend Requirements above)

### 2. Connection Refused
**Error**: `Connect ECONNREFUSED 127.0.0.1:8000`

**Solution**: 
1. Verify backend is running
2. Check if port 8000 is correct
3. Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### 3. Timeout Errors
**Error**: `Request timeout after 10000ms`

**Solution**:
1. Check backend performance
2. Increase timeout in `lib/api.ts`
3. Optimize backend queries

## Future Enhancements

- [ ] Add request/response interceptors for logging
- [ ] Implement response caching with SWR
- [ ] Add pagination support
- [ ] Add real-time updates with WebSockets
- [ ] Implement GraphQL instead of REST (optional)
