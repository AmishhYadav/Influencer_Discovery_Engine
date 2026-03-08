import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Influencer Discovery Engine',
  description: 'Discover and connect with the perfect influencers for your brand',
  keywords: ['influencer', 'discovery', 'marketing', 'social media'],
  openGraph: {
    title: 'Influencer Discovery Engine',
    description: 'Discover and connect with the perfect influencers for your brand',
    type: 'website',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: '#1a0f1a',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
