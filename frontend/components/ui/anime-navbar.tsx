'use client';

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LucideIcon, Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  name: string;
  url: string;
  icon: LucideIcon;
}

interface NavBarProps {
  items: NavItem[];
  className?: string;
  defaultActive?: string;
  logo?: React.ReactNode;
}

export function AnimeNavBar({
  items,
  className,
  defaultActive = 'Home',
  logo,
}: NavBarProps) {
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);
  const [hoveredTab, setHoveredTab] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>(defaultActive);
  const [isMobile, setIsMobile] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (!mounted) return null;

  return (
    <div className="fixed top-5 left-0 right-0 z-[9999]">
      <div className="flex justify-center px-4">
        <motion.div
          className={cn(
            'flex items-center gap-3 bg-background/80 border border-border backdrop-blur-lg py-2 px-4 rounded-full shadow-lg relative',
            'md:bg-black/50',
            className
          )}
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{
            type: 'spring',
            stiffness: 260,
            damping: 20,
          }}
        >
          {/* Logo */}
          {logo && <div className="mr-2">{logo}</div>}

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {items.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.name;
              const isHovered = hoveredTab === item.name;

              return (
                <Link
                  key={item.name}
                  href={item.url}
                  onClick={(e) => {
                    e.preventDefault();
                    setActiveTab(item.name);
                  }}
                  onMouseEnter={() => setHoveredTab(item.name)}
                  onMouseLeave={() => setHoveredTab(null)}
                  className={cn(
                    'relative cursor-pointer text-sm font-semibold px-5 py-2 rounded-full transition-all duration-300',
                    'text-muted-foreground hover:text-foreground',
                    isActive && 'text-foreground'
                  )}
                >
                  {isActive && (
                    <motion.div
                      className="absolute inset-0 rounded-full -z-10 bg-gradient-to-r from-primary/20 to-accent/20"
                      layoutId="active-pill"
                      transition={{
                        type: 'spring',
                        stiffness: 380,
                        damping: 30,
                      }}
                    />
                  )}
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden flex items-center justify-center w-10 h-10 rounded-full hover:bg-muted transition-colors"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? (
              <X className="w-5 h-5" />
            ) : (
              <Menu className="w-5 h-5" />
            )}
          </button>
        </motion.div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && isMobile && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="absolute top-full mt-2 left-4 right-4 bg-background/90 border border-border backdrop-blur-lg rounded-lg shadow-lg overflow-hidden"
            >
              {items.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    href={item.url}
                    onClick={() => {
                      setActiveTab(item.name);
                      setIsOpen(false);
                    }}
                    className="flex items-center gap-3 px-4 py-3 text-sm font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors border-b border-border last:border-b-0"
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
