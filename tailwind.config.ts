import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: 'hsl(var(--primary))',
        secondary: 'hsl(var(--secondary))',
        accent: 'hsl(var(--accent))',
        muted: 'hsl(var(--muted))',
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '0% 0%' },
          '100%': { backgroundPosition: '100% 100%' },
        },
        glow: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'pulse-slow': {
          '0%, 100%': {
            transform: 'translateX(-100%)',
          },
          '50%': {
            transform: 'translateX(100%)',
          },
        },
      },
      animation: {
        shimmer: 'shimmer 3s ease-in-out infinite',
        glow: 'glow 2s ease-in-out infinite',
        'pulse-slow': 'pulse-slow 3s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}

export default config
