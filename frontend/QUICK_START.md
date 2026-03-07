# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Configure Environment
```bash
cp .env.example .env.local
```

Make sure `.env.local` contains:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Step 3: Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser 🎉

---

## 📋 Checklist

Before going live, make sure you've:

- [ ] Installed all dependencies
- [ ] Created `.env.local` file
- [ ] Set correct API base URL
- [ ] Backend server is running
- [ ] Development server starts without errors
- [ ] Home page loads and displays hero
- [ ] Navigation bar works
- [ ] Search interface loads
- [ ] API calls are working (check browser console)

---

## 🔧 Common Commands

```bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

---

## 📝 File Structure Overview

```
frontend/
├── app/              # Pages and layouts
├── components/       # Reusable UI components
├── hooks/           # Custom React hooks
├── lib/             # Utilities and types
├── public/          # Static assets
└── config files     # Next.js, Tailwind, etc.
```

---

## 🎨 Customization

### Change Theme Colors
Edit `app/globals.css`:
```css
:root {
  --primary: #3b82f6;  /* Change this */
  --accent: #06b6d4;   /* And this */
}
```

### Update Copy
- Home page: `app/page.tsx`
- Explore page: `app/explore/page.tsx`
- Creator detail: `app/creators/[id]/page.tsx`

---

## ⚠️ Troubleshooting

### Port Already in Use
```bash
npm run dev -- -p 3001  # Use different port
```

### API Connection Error
1. Check backend is running on correct port
2. Verify `NEXT_PUBLIC_API_BASE_URL` is correct
3. Check browser console for CORS errors

### Build Failures
```bash
rm -rf .next node_modules
npm install
npm run build
```

---

## 📚 Documentation

- `README.md` - Full project documentation
- `FRONTEND_SETUP.md` - Detailed setup guide
- `FRONTEND_COMPLETE.md` - Implementation details

---

## 🌍 Deployment

### Vercel (Recommended)
1. Push to GitHub
2. Connect in Vercel dashboard
3. Set environment variables
4. Deploy!

### Docker
Create a `Dockerfile`:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
CMD npm start
```

---

## 📞 Support

For issues:
1. Check browser console for errors
2. Review terminal output
3. Check `.env.local` configuration
4. Verify backend API is running

---

## ✨ Features Overview

- 🎨 Modern dark theme design
- 📱 Responsive mobile layout
- 🔍 Advanced search & filtering
- 💫 Smooth animations
- 🚀 Fast performance
- 📊 Creator profiles & metrics
- 🔄 Pagination support
- ✅ Full TypeScript support

---

**Ready to go?** Run `npm run dev` and start building! 🎉
