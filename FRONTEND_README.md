# Influencer Discovery Engine - React Frontend

A modern, responsive React frontend for the Influencer Discovery Engine, built with Next.js 15, TypeScript, and Tailwind CSS.

## Features

- **Search Influencers**: Search across multiple platforms with advanced filtering
- **Trending Creators**: Discover trending influencers in real-time
- **Creator Profiles**: Detailed analytics and engagement metrics
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Animated UI**: Smooth animations with Framer Motion
- **Real-time Data**: Integrates with FastAPI backend for live data

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ or higher
- npm, yarn, pnpm, or bun

### Installation

1. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   # or
   bun install
   ```

2. **Configure Environment Variables**
   
   Create a `.env.local` file in the project root:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
   
   **Note**: The API URL must start with `NEXT_PUBLIC_` to be accessible in the browser.

3. **Start Development Server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   # or
   bun dev
   ```

   The application will be available at `http://localhost:3000`

## Project Structure

```
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   ├── globals.css             # Global styles
│   ├── search/
│   │   └── page.tsx            # Search page
│   ├── trending/
│   │   └── page.tsx            # Trending creators page
│   ├── about/
│   │   └── page.tsx            # About page
│   └── creators/
│       └── [id]/
│           └── page.tsx        # Creator detail page
├── components/
│   ├── ui/
│   │   ├── animated-shader-hero.tsx    # Hero component with shader
│   │   ├── interactive-hover-button.tsx # Hover button
│   │   └── anime-navbar.tsx             # Animated navigation
│   ├── creator-card.tsx         # Creator card component
│   └── search-bar.tsx           # Search bar component
├── lib/
│   ├── api.ts                  # API client and endpoints
│   ├── hooks.ts                # Custom React hooks
│   └── utils.ts                # Utility functions
├── package.json
├── next.config.js
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── .env.example
```

## API Integration

The frontend integrates with the FastAPI backend through the following endpoints:

### Search Endpoint
```typescript
POST /search
{
  query: string
  platform?: string
  min_followers?: number
  max_followers?: number
  niche?: string
  engagement_threshold?: number
  limit?: number
  offset?: number
}
```

### Creator Endpoints
```
GET /creators/trending - Get trending creators
GET /creators/by-niche?niche=fitness - Get creators by niche
GET /creators/{creatorId} - Get detailed creator information
```

## Custom Hooks

### `useSearch()`
Search for creators with filters.
```typescript
const { results, loading, error, search, totalResults } = useSearch()
await search({ query: 'fitness influencer', limit: 20 })
```

### `useCreatorsByNiche(niche, enabled)`
Fetch creators by niche.
```typescript
const { creators, loading, error } = useCreatorsByNiche('fashion')
```

### `useCreatorDetail(creatorId)`
Fetch detailed creator information.
```typescript
const { detail, loading, error } = useCreatorDetail('creator-123')
```

### `useTrendingCreators(limit)`
Fetch trending creators.
```typescript
const { creators, loading, error } = useTrendingCreators(10)
```

## Design System

### Color Palette
- **Background**: `hsl(12, 8%, 6%)` - Deep dark gray
- **Foreground**: `hsl(0, 0%, 98%)` - Off-white
- **Primary**: `hsl(259, 94%, 51%)` - Vibrant purple
- **Secondary**: `hsl(189, 100%, 50%)` - Cyan blue
- **Accent**: `hsl(359, 100%, 50%)` - Bright red
- **Muted**: `hsl(240, 10%, 20%)` - Dark gray

### Typography
- **Sans Serif**: System fonts (Roboto fallback)
- **Monospace**: Fira Code

## Building for Production

```bash
npm run build
npm run start
```

## Environment Variables

### Required
- `NEXT_PUBLIC_API_URL` - FastAPI backend URL (e.g., `http://localhost:8000`)

### Optional
- `NODE_ENV` - Environment mode (automatically set by Next.js)

## Troubleshooting

### API Connection Issues
1. Ensure FastAPI backend is running on the configured URL
2. Check CORS settings on the backend
3. Verify `NEXT_PUBLIC_API_URL` is correctly set
4. Check browser console for network errors

### Build Errors
1. Clear `.next` directory: `rm -rf .next`
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Check Node.js version: Should be 18+

### Styling Issues
1. Verify Tailwind CSS is installed
2. Check `tailwind.config.ts` and `globals.css` are in place
3. Clear Next.js cache: `npm run dev -- --clean`

## Components

### Hero Component
Animated shader-based hero section with particle effects.
```tsx
<Hero
  trustBadge={{ text: "Trusted by brands", icons: ["✨"] }}
  headline={{ line1: "Discover", line2: "Influencers" }}
  subtitle="Find perfect creators for your brand"
  buttons={{
    primary: { text: "Search", onClick: () => {} },
    secondary: { text: "Learn More", onClick: () => {} }
  }}
/>
```

### Anime NavBar
Animated navigation with mascot character.
```tsx
<AnimeNavBar 
  items={navItems}
  defaultActive="Home"
/>
```

### Interactive Hover Button
Button with smooth hover animations.
```tsx
<InteractiveHoverButton text="Click Me" onClick={() => {}} />
```

## Performance Optimization

- **Image Optimization**: Uses Next.js Image component when possible
- **Code Splitting**: Automatic with Next.js App Router
- **Lazy Loading**: Components are lazy-loaded by default
- **Caching**: HTTP caching implemented in axios
- **CSS**: Tailwind CSS with PurgeCSS for minimal bundle

## Contributing

1. Follow the existing code structure
2. Use TypeScript for type safety
3. Keep components small and reusable
4. Write meaningful commit messages

## License

This project is part of the Influencer Discovery Engine project.
