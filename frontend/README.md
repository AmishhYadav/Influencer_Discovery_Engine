# Influencer Discovery Engine - Frontend

A modern React/Next.js frontend for discovering and analyzing influencers across multiple social media platforms.

## Features

- **Advanced Search**: Filter creators by keywords, platforms, follower count, and engagement rate
- **Creator Profiles**: Detailed views of creator information with real-time metrics
- **Responsive Design**: Mobile-first design with smooth animations using Framer Motion
- **Dark Theme**: Professional dark interface inspired by modern SaaS dashboards
- **Real-time Analytics**: Engagement rates, follower counts, and performance metrics

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **UI Framework**: React 19
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **HTTP Client**: SWR for data fetching
- **Icons**: Lucide React
- **Type Safety**: TypeScript

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm, yarn, or pnpm

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies
```bash
npm install
# or
pnpm install
```

3. Set up environment variables
```bash
cp .env.example .env.local
```

Edit `.env.local` and set your API base URL:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Development

Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Home page with hero section
│   ├── explore/           # Creator exploration page
│   └── creators/[id]/     # Creator detail page
├── components/            # React components
│   ├── ui/               # UI component library
│   ├── creator-card.tsx  # Creator card component
│   └── search-filters.tsx # Advanced search filters
├── hooks/                # Custom React hooks
│   └── useApi.ts        # API data fetching hooks
├── lib/                 # Utilities and helpers
│   ├── types.ts         # TypeScript type definitions
│   └── utils.ts         # Utility functions
├── public/              # Static assets
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── next.config.js       # Next.js configuration
```

## Component Guide

### Search Filters
Advanced filtering component with platforms, categories, follower ranges, and engagement metrics.

```tsx
<SearchFilters
  onSearch={(query) => handleSearch(query)}
  onClear={() => handleClear()}
  isLoading={isLoading}
/>
```

### Creator Card
Displays creator information with stats and links to profile.

```tsx
<CreatorCard
  creator={creator}
  delay={0}
/>
```

### Navbar
Animated navigation bar with smooth transitions and mobile support.

```tsx
<AnimeNavBar
  items={navItems}
  defaultActive="Home"
  logo={<div>Logo</div>}
/>
```

### Hero Section
Animated hero section with geometric shapes and call-to-action.

```tsx
<HeroGeometric
  title1="Find Your Perfect"
  title2="Influencer Partners"
  onCta={() => handleCta()}
/>
```

## API Integration

The frontend communicates with the backend API at the URL specified in `NEXT_PUBLIC_API_BASE_URL`. 

### Available API Endpoints

- `GET /api/search` - Search creators with filters
- `GET /api/creators` - List creators with pagination
- `GET /api/creators/:id` - Get creator details
- `GET /api/filter-options` - Get available filter options

## Customization

### Colors and Theme

Edit `app/globals.css` to customize the color scheme:

```css
:root {
  --background: #0f0f0f;
  --foreground: #ffffff;
  --primary: #3b82f6;
  --secondary: #1e293b;
  --accent: #06b6d4;
  /* ... more colors */
}
```

### Tailwind Configuration

Modify `tailwind.config.js` to change spacing, fonts, and other Tailwind settings.

## Performance

- **SWR Integration**: Automatic caching and revalidation of API data
- **Code Splitting**: Automatic code splitting by Next.js
- **Image Optimization**: Next.js Image component ready
- **CSS Optimization**: Tailwind CSS purging in production

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

## Support

For issues and questions, please open an issue on the repository.
