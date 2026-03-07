import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Influencer Discovery Engine',
  description: 'Discover and analyze influencers across multiple platforms',
  keywords: 'influencer, discovery, marketing, social media, analytics',
  authors: [{ name: 'Influencer Discovery Team' }],
  openGraph: {
    title: 'Influencer Discovery Engine',
    description: 'Discover and analyze influencers across multiple platforms',
    type: 'website',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  themeColor: '#0f0f0f',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
