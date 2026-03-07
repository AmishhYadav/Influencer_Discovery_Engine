# Visual Guide - Frontend Architecture

## 🎯 Project Overview

```
┌─────────────────────────────────────────────────────────┐
│        INFLUENCER DISCOVERY ENGINE - FRONTEND           │
│                   React + Next.js 15                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │          NEXT.JS FRONTEND APPLICATION             │  │
│  ├───────────────────────────────────────────────────┤  │
│  │                                                   │  │
│  │  ┌──────────────────┐  ┌──────────────────┐     │  │
│  │  │   Pages/Routes   │  │   Components     │     │  │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │     │  │
│  │  │  │ /          │  │  │  │ Navbar     │ │     │  │
│  │  │  │ /explore   │  │  │  │ Hero       │ │     │  │
│  │  │  │ /creators/ │  │  │  │ Cards      │ │     │  │
│  │  │  │    [id]    │  │  │  │ Filters    │ │     │  │
│  │  │  └────────────┘  │  │  └────────────┘ │     │  │
│  │  └──────────────────┘  └──────────────────┘     │  │
│  │                                                   │  │
│  │  ┌──────────────────┐  ┌──────────────────┐     │  │
│  │  │   Hooks/Logic    │  │   Utilities      │     │  │
│  │  │  ┌────────────┐  │  │  ┌────────────┐ │     │  │
│  │  │  │ useApi     │  │  │  │ types.ts   │ │     │  │
│  │  │  │ useSearch  │  │  │  │ utils.ts   │ │     │  │
│  │  │  └────────────┘  │  │  └────────────┘ │     │  │
│  │  └──────────────────┘  └──────────────────┘     │  │
│  │                                                   │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │         STYLING & ANIMATIONS             │   │  │
│  │  │  ┌────────┐ ┌────────┐ ┌──────────────┐ │   │  │
│  │  │  │Tailwind│ │ Framer │ │ CSS Custom   │ │   │  │
│  │  │  │  CSS   │ │Motion  │ │ Properties   │ │   │  │
│  │  │  └────────┘ └────────┘ └──────────────┘ │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                         │                               │
│          ┌──────────────┼──────────────┐               │
│          ▼              ▼              ▼               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │  SWR Hooks   │ │ Local State  │ │ Router State │  │
│  │ (Caching)    │ │              │ │              │  │
│  └──────────────┘ └──────────────┘ └──────────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
          │                              │
          │                              │
          ▼                              ▼
    ┌──────────────┐            ┌──────────────┐
    │   API CALLS  │            │  FILE SYSTEM │
    │ /api/search  │            │ (CSS, assets)│
    │ /api/creators│            └──────────────┘
    └──────────────┘
          │
          ▼
    ┌──────────────┐
    │   Backend    │
    │   Server     │
    │ (Port 8000)  │
    └──────────────┘
```

---

## 🗂️ File Structure Tree

```
frontend/
│
├── 📁 app/                          # Next.js App Router
│   ├── 📄 layout.tsx               # Root layout
│   ├── 📄 page.tsx                 # Home page (hero + search)
│   ├── 📄 globals.css              # Global styles & theme colors
│   ├── 📁 explore/
│   │   └── 📄 page.tsx            # Explore/browse page
│   └── 📁 creators/
│       └── 📁 [id]/
│           └── 📄 page.tsx        # Creator detail page
│
├── 📁 components/                   # React components
│   ├── 📁 ui/                      # UI component library
│   │   ├── 📄 anime-navbar.tsx    # Animated navigation
│   │   ├── 📄 interactive-hover-button.tsx
│   │   └── 📄 shape-landing-hero.tsx
│   ├── 📄 creator-card.tsx        # Creator profile card
│   └── 📄 search-filters.tsx      # Advanced search
│
├── 📁 hooks/                        # Custom React hooks
│   └── 📄 useApi.ts               # SWR data fetching
│
├── 📁 lib/                          # Utilities & helpers
│   ├── 📄 types.ts                # TypeScript interfaces
│   └── 📄 utils.ts                # Utility functions
│
├── 📁 public/                       # Static assets
│   └── (images, fonts, etc.)
│
├── 📄 package.json                 # Dependencies
├── 📄 tsconfig.json                # TypeScript config
├── 📄 tailwind.config.js           # Tailwind CSS config
├── 📄 postcss.config.js            # PostCSS config
├── 📄 next.config.js               # Next.js config
├── 📄 .env.example                 # Env variables template
├── 📄 .gitignore                   # Git ignore
└── 📄 README.md                    # Full documentation
```

---

## 🔄 Data Flow Diagram

```
USER INTERACTION
      │
      ▼
┌─────────────────────────────────────┐
│  User Types Keywords/Selects Filters │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  SearchFilters Component             │
│  - Collects filter data              │
│  - Validates input                   │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  User Clicks Search Button           │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  app/page.tsx calls handleSearch()   │
│  - Creates SearchQuery object        │
│  - Calls setSearchQuery()            │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  useSearch Hook (SWR)                │
│  - Triggers API call                 │
│  - Manages loading state             │
│  - Caches results                    │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  HTTP Request to Backend             │
│  GET /api/search?...                 │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Backend Processes Request           │
│  - Searches database                 │
│  - Applies filters                   │
│  - Returns results                   │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Response Received                   │
│  { creators: [], total: N, ... }     │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  SWR Caches Response                 │
│  - Stores in memory                  │
│  - Available for reuse               │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Component Re-renders                │
│  - results = data                    │
│  - isLoading = false                 │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Display Creator Grid                │
│  - Map creators to cards             │
│  - Render with animations            │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  User Sees Results                   │
│  - Cards with smooth animations      │
│  - Can click to see details          │
└─────────────────────────────────────┘
```

---

## 🎨 Design System Colors

```
┌─────────────────────────────────────────────┐
│            COLOR PALETTE REFERENCE           │
├─────────────────────────────────────────────┤
│                                             │
│  🟫 BACKGROUND                             │
│  #0f0f0f (Almost Black)                    │
│  Used for: Page backgrounds, main theme    │
│                                             │
│  ⬜ FOREGROUND                              │
│  #ffffff (White)                           │
│  Used for: Text, main content              │
│                                             │
│  🔵 PRIMARY                                │
│  #3b82f6 (Blue)                           │
│  Used for: Buttons, highlights, focus      │
│                                             │
│  🟦 SECONDARY                              │
│  #1e293b (Dark Blue)                      │
│  Used for: Cards, containers               │
│                                             │
│  🔷 ACCENT                                 │
│  #06b6d4 (Cyan)                           │
│  Used for: Highlights, interactive         │
│                                             │
│  ⬛ MUTED                                  │
│  #404040 (Gray)                           │
│  Used for: Disabled, secondary buttons     │
│                                             │
│  🟩 BORDER                                 │
│  #262626 (Dark Gray)                      │
│  Used for: Dividers, borders               │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📱 Responsive Breakpoints

```
MOBILE               TABLET               DESKTOP
(< 640px)          (640px - 1024px)     (> 1024px)
┌──────────┐       ┌──────────────┐     ┌────────────────┐
│          │       │              │     │                │
│ 1 Column │       │  2 Columns   │     │  3 Columns     │
│          │       │              │     │                │
│ [Card]   │       │ [Card][Card] │     │ [C][C][C][C]   │
│          │       │              │     │ [C][C][C][C]   │
│ [Card]   │       │ [Card][Card] │     │ [C][C][C]      │
│          │       │              │     │                │
│ Menu ≡   │       │ Menu Items → │     │ Menu Items →   │
└──────────┘       └──────────────┘     └────────────────┘

Full-width        Optimized            Optimal width
touch-friendly    spacing              readability
```

---

## 🎯 Component Hierarchy

```
├─ RootLayout (app/layout.tsx)
│  │
│  └─ Page Routes
│     │
│     ├─ Home (app/page.tsx)
│     │  ├─ AnimeNavBar
│     │  ├─ HeroGeometric
│     │  ├─ SearchFilters
│     │  ├─ CreatorCard (x many)
│     │  └─ Footer
│     │
│     ├─ Explore (app/explore/page.tsx)
│     │  ├─ AnimeNavBar
│     │  ├─ CreatorCard (x many)
│     │  └─ Pagination Controls
│     │
│     └─ Creator Detail (app/creators/[id]/page.tsx)
│        ├─ AnimeNavBar
│        ├─ Back Button
│        ├─ Creator Header
│        ├─ Stats Cards
│        └─ Additional Info

Custom Hooks:
├─ useSearch(query)
├─ useCreator(id)
├─ useCreators(page)
└─ useFilterOptions()
```

---

## 🔐 State Management

```
LOCAL STATE (Component Level)
┌─────────────────────────────────────┐
│ SearchFilters State                 │
├─────────────────────────────────────┤
│ - keywords (string)                 │
│ - selectedPlatforms (string[])      │
│ - selectedCategories (string[])     │
│ - minFollowers (number)             │
│ - maxFollowers (number)             │
│ - minEngagement (number)            │
│ - maxEngagement (number)            │
│ - isExpanded (boolean)              │
└─────────────────────────────────────┘

URL/ROUTER STATE (Page Level)
┌─────────────────────────────────────┐
│ - Current route (/explore)          │
│ - Creator ID ([id])                 │
│ - Page number (query param)         │
└─────────────────────────────────────┘

CACHED DATA (SWR Level)
┌─────────────────────────────────────┐
│ - Search results                    │
│ - Creator list                      │
│ - Creator details                   │
│ - Filter options                    │
│ Automatically refreshed per config  │
└─────────────────────────────────────┘
```

---

## ⚡ Performance Strategy

```
OPTIMIZATION LAYERS
└─ Code Level
   ├─ TypeScript (compile-time safety)
   ├─ Functional components (optimized)
   ├─ Hooks (efficient state)
   └─ memo() where needed
   
└─ App Level
   ├─ SWR (caching)
   ├─ Lazy loading (images)
   ├─ Code splitting (routes)
   └─ CSS optimization (Tailwind)

└─ Build Level
   ├─ Next.js optimization
   ├─ CSS purging
   ├─ JS minification
   └─ Asset compression
```

---

## 🔌 API Integration Points

```
Frontend                              Backend
┌──────────────┐                ┌──────────────┐
│  Search Form │◄──────────────►│ Search Route │
│ (components) │   GET/POST     │  /api/search │
└──────────────┘                └──────────────┘
       │                               │
       └─────────────────────────────┬─┘
                                     │
┌──────────────┐                ┌─────────────────┐
│  Creator     │◄──────────────►│ Creator Routes  │
│  Cards       │   GET/POST     │ /api/creators   │
│  (display)   │                │ /api/creators/:id
└──────────────┘                └─────────────────┘
       │                               │
       └─────────────────────────────┬─┘
                                     │
                            ┌────────────────┐
                            │ Database       │
                            │ (Python API)   │
                            └────────────────┘
```

---

## 🎨 Animation Layers

```
ENTRANCE ANIMATIONS
├─ Page Load
│  └─ Navbar: Spring from top
│  └─ Hero: Shapes fade in with Y translation
│  └─ Cards: Staggered fade-in

INTERACTION ANIMATIONS
├─ Hover States
│  └─ Cards: Lift up (Y -8px)
│  └─ Buttons: Scale 1.05
│  └─ Links: Color change
│
├─ Active States
│  └─ Nav items: Highlight background
│  └─ Cards: Border color change
│
└─ Loading States
   └─ Skeleton: Pulse animation
   └─ Spinner: Rotate animation

CONTINUOUS ANIMATIONS
├─ Hero Shapes
│  └─ Float up-down (12s loop)
│
└─ Scroll Indicator
   └─ Bounce up-down (2s loop)
```

---

## 📊 Component Props Flow

```
RootLayout
  │
  └─► page.tsx
       │
       ├─► AnimeNavBar
       │    props: items[], logo, defaultActive
       │
       ├─► HeroGeometric
       │    props: badge, title1, title2, onCta
       │
       ├─► SearchFilters
       │    props: onSearch, onClear, isLoading
       │
       └─► CreatorCard (within loop)
            props: creator, delay
```

---

This visual guide should help you understand the complete architecture and flow of the frontend application!
