# Influencer Discovery Engine - Frontend

A modern React frontend for discovering and analyzing influencers across multiple platforms.

## 🚀 Quick Start

Get up and running in 5 minutes:

```bash
# Backend (Terminal 1)
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload --port 8000

# Frontend (Terminal 2)
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

**→ [Full Quick Start Guide →](./QUICK_START.md)**

## 📚 Documentation

Choose what you need:

### New to the Project?
- **[QUICK_START.md](./QUICK_START.md)** - Get running in 5 minutes with copy-paste commands
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - What was built and overview

### Setting Up Locally?
- **[SETUP.md](./SETUP.md)** - Detailed setup instructions for both frontend and backend
- **[FRONTEND_README.md](./FRONTEND_README.md)** - Complete frontend documentation

### Integrating with Backend?
- **[API_INTEGRATION.md](./API_INTEGRATION.md)** - API endpoints, hooks, and integration details

## ✨ Features

### 🔍 Search
- Search creators by name, niche, or keywords
- Filter by platform (Instagram, TikTok, YouTube, Twitter)
- Filter by follower count and engagement rate
- Real-time search results

### 📊 Analytics
- View creator statistics
- Track engagement metrics
- See top-performing content
- Analyze audience demographics

### 🌟 Discover
- Browse trending creators
- Explore creators by niche
- View detailed creator profiles
- Compare creators side-by-side

### 🎨 Design
- Modern dark theme
- Smooth animations and transitions
- Responsive on all devices
- Accessible and user-friendly

## 🛠️ Tech Stack

| Category | Technology |
|----------|-------------|
| Framework | Next.js 15 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| HTTP Client | Axios |
| Icons | Lucide React |

## 📁 Project Structure

```
├── app/                           # Next.js pages
│   ├── page.tsx                  # Home page
│   ├── layout.tsx                # Root layout
│   ├── globals.css               # Global styles
│   ├── search/page.tsx           # Search page
│   ├── trending/page.tsx         # Trending page
│   ├── about/page.tsx            # About page
│   └── creators/[id]/page.tsx    # Creator detail
│
├── components/                    # React components
│   ├── ui/                       # Custom UI components
│   │   ├── animated-shader-hero.tsx
│   │   ├── anime-navbar.tsx
│   │   └── interactive-hover-button.tsx
│   ├── creator-card.tsx
│   └── search-bar.tsx
│
├── lib/                          # Utilities
│   ├── api.ts                    # API client
│   ├── hooks.ts                  # Custom hooks
│   └── utils.ts                  # Helper functions
│
├── QUICK_START.md                # 5-min setup
├── SETUP.md                      # Detailed setup
├── FRONTEND_README.md            # Frontend docs
├── API_INTEGRATION.md            # API docs
├── IMPLEMENTATION_SUMMARY.md     # What was built
└── README.md                     # This file
```

## 🎯 Key Features

### 1. Home Page (`/`)
- Animated WebGL hero section
- Feature showcase
- Call-to-action buttons
- Information about the platform

### 2. Search Page (`/search`)
- Real-time search input
- Advanced filtering options
- Creator result cards
- Pagination support

### 3. Trending Page (`/trending`)
- Most popular creators
- Top rankings
- Trending metrics
- Quick filters

### 4. Creator Profile (`/creators/{id}`)
- Detailed creator information
- Engagement statistics
- Top-performing content
- Social media links

### 5. About Page (`/about`)
- Platform information
- Features overview
- Technology stack
- Company values

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- npm, yarn, pnpm, or bun

### Setup Steps

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Open Browser**
   ```
   http://localhost:3000
   ```

### Backend Integration

The frontend requires the FastAPI backend running on port 8000:

```bash
# In a separate terminal
source venv/bin/activate
python -m uvicorn src.api.main:app --reload --port 8000
```

**Backend API Docs**: http://localhost:8000/docs

## 🎨 Design System

### Colors
- **Primary**: Purple (#A855F7)
- **Secondary**: Cyan (#06B6D4)
- **Accent**: Red (#EF4444)
- **Background**: Dark (#0F0A09)
- **Foreground**: Light (#FAFAF8)

### Typography
- **Headings**: System sans-serif with bold weight
- **Body**: System sans-serif with regular weight
- **Code**: Monospace font

### Animations
- Smooth transitions on all interactive elements
- WebGL shader background on hero
- Animated navbar with mascot character
- Hover effects on cards and buttons

## 📱 Responsive Design

The frontend is mobile-first and responsive:
- **Mobile**: Optimized for small screens
- **Tablet**: Adaptive layout for medium screens
- **Desktop**: Full-featured experience

## 🔌 API Integration

The frontend communicates with FastAPI backend through:

```typescript
// Search endpoint
POST /search
{
  query: string
  platform?: string
  min_followers?: number
  niche?: string
  limit?: number
}

// Get trending creators
GET /creators/trending?limit=10

// Get creator by ID
GET /creators/{creatorId}

// Get creators by niche
GET /creators/by-niche?niche=fitness
```

### Custom Hooks

```typescript
// Search creators
const { results, loading, error, search } = useSearch()

// Get trending creators
const { creators, loading } = useTrendingCreators(10)

// Get creators by niche
const { creators, loading } = useCreatorsByNiche('fashion')

// Get creator details
const { detail, loading } = useCreatorDetail('creator-id')
```

## 🧪 Development

### Available Commands

```bash
npm run dev      # Start dev server with HMR
npm run build    # Build for production
npm run start    # Run production build
npm run lint     # Run ESLint
npm test         # Run tests
```

### Hot Module Replacement (HMR)
Changes are reflected instantly without page reload. Component state is preserved.

### TypeScript
Full type safety with strict mode enabled. All components and APIs are fully typed.

## 📦 Building for Production

```bash
# Build optimized bundle
npm run build

# Test production build locally
npm run start

# Deploy (with Vercel)
vercel
```

## 🐛 Troubleshooting

### Frontend won't connect to backend
1. Ensure backend is running: `http://localhost:8000/docs`
2. Check `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Restart frontend: `npm run dev`

### Port already in use
```bash
# Use different port
npm run dev -- -p 3001
```

### Build errors
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

### Module not found
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
npm run dev
```

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)
- [Axios Documentation](https://axios-http.com/)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Commit with clear messages
4. Push and create a pull request

## 📄 License

This project is part of the Influencer Discovery Engine.

## 🆘 Getting Help

1. **Quick answers**: Check [QUICK_START.md](./QUICK_START.md)
2. **Detailed guide**: See [SETUP.md](./SETUP.md)
3. **API questions**: Read [API_INTEGRATION.md](./API_INTEGRATION.md)
4. **Frontend details**: Check [FRONTEND_README.md](./FRONTEND_README.md)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review relevant documentation
3. Check backend API docs at http://localhost:8000/docs
4. Open an issue with details

## 🎉 What's Next?

After getting the frontend running:

1. **Explore the UI** - Try all pages and features
2. **Read the docs** - Understand the architecture
3. **Customize** - Modify colors, fonts, components
4. **Extend** - Add new features and pages
5. **Deploy** - Push to production with Vercel

---

**Ready to start?** → [Quick Start Guide](./QUICK_START.md)

**Want details?** → [Setup Guide](./SETUP.md)

**Building with backend?** → [API Integration](./API_INTEGRATION.md)
