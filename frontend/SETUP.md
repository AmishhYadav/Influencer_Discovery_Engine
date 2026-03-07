# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

Navigate to the frontend directory and install all required packages:

```bash
cd frontend
npm install
# or
pnpm install
# or
yarn install
```

### 2. Configure Environment

Create `.env.local` file in the frontend directory:

```bash
cp .env.example .env.local
```

Update the API URL if your backend runs on a different port:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

## Frontend Architecture

### Pages

1. **Home** (`/`) - Landing page with hero section and search interface
2. **Explore** (`/explore`) - Browse all available creators with pagination
3. **Creator Detail** (`/creators/:id`) - Detailed creator profile page

### Key Components

- **AnimeNavBar** - Animated navbar with mobile support
- **HeroGeometric** - Landing page hero with geometric animations
- **SearchFilters** - Advanced search and filtering interface
- **CreatorCard** - Creator profile card in grid layouts
- **Interactive Hover Button** - Custom interactive button component

### Data Flow

1. User interacts with UI (search, filter, navigate)
2. Components use SWR hooks to fetch data from backend
3. Data is cached and automatically revalidated
4. Results are displayed with smooth animations

## Features Implementation

### Search & Filter
- Multi-keyword search
- Platform filtering (Instagram, TikTok, YouTube, Twitter, Twitch)
- Category filtering (Fashion, Tech, Gaming, etc.)
- Follower count range filtering
- Engagement rate range filtering

### Creator Cards
- Display profile image and basic info
- Show follower count and engagement rate
- Platform-specific color coding
- Hover animations and interactions
- Link to detailed creator profile

### Pagination
- Browse creators with page controls
- Display current page and total pages
- Previous/Next navigation buttons

## API Integration

The frontend expects the following API structure:

```
GET /api/search?keywords=...&platforms=...&min_followers=...
Response: {
  creators: Creator[],
  total: number,
  page: number,
  per_page: number
}

GET /api/creators/:id
Response: CreatorDetail

GET /api/creators?page=1&per_page=20
Response: {
  creators: Creator[],
  total: number,
  page: number,
  per_page: number
}
```

## Styling & Customization

### Theme Colors

The app uses CSS custom properties for theming. Edit `app/globals.css`:

```css
:root {
  --background: #0f0f0f;
  --foreground: #ffffff;
  --primary: #3b82f6;
  --secondary: #1e293b;
  --accent: #06b6d4;
  --muted: #404040;
  --muted-foreground: #a1a1a1;
  --border: #262626;
}
```

### Tailwind CSS

All styling uses Tailwind CSS classes. See `tailwind.config.js` for configuration.

## Troubleshooting

### API Connection Issues

If you see "API Error" messages:

1. Check that the backend is running on the configured URL
2. Verify `NEXT_PUBLIC_API_BASE_URL` in `.env.local`
3. Check browser console for CORS errors
4. Ensure backend API endpoints match the expected structure

### Build Issues

If you encounter build errors:

1. Clear `.next` directory: `rm -rf .next`
2. Reinstall dependencies: `npm install`
3. Check for TypeScript errors: `npx tsc --noEmit`

### Performance Issues

1. Check Network tab in DevTools for slow API calls
2. Verify SWR caching is working (check Network tab)
3. Use `next/image` for optimized images
4. Check for unnecessary re-renders using React DevTools

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel dashboard
3. Set environment variables
4. Deploy automatically on git push

### Other Platforms

Build the app and deploy the `.next` directory:

```bash
npm run build
```

Then serve with your hosting provider following their Next.js deployment guide.

## Development Tips

- Use React DevTools browser extension to debug components
- Enable "Slow 3G" in Chrome DevTools to test performance
- Check the Application tab to verify SWR cache
- Use `console.log()` for debugging (removed before production)

## File Naming Conventions

- Components: PascalCase (`CreatorCard.tsx`)
- Hooks: camelCase with `use` prefix (`useApi.ts`)
- Types: Interfaces use PascalCase (`Creator`)
- Utilities: camelCase (`utils.ts`)

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: add your feature"

# Push to remote
git push origin feature/your-feature

# Create pull request
```

## Next Steps

1. Install and run the development server
2. Verify the application loads at `http://localhost:3000`
3. Test search and filtering functionality
4. Check creator detail pages
5. Customize theme colors and branding as needed
6. Deploy to your preferred hosting platform
