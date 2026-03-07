'use client';

import React from 'react';
import { ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface InteractiveHoverButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  text?: string;
  size?: 'sm' | 'md' | 'lg';
}

const InteractiveHoverButton = React.forwardRef<
  HTMLButtonElement,
  InteractiveHoverButtonProps
>(({ text = 'Button', className, size = 'md', ...props }, ref) => {
  const sizeClasses = {
    sm: 'w-24 p-1.5 text-xs',
    md: 'w-32 p-2 text-sm',
    lg: 'w-40 p-3 text-base',
  };

  return (
    <button
      ref={ref}
      className={cn(
        'group relative cursor-pointer overflow-hidden rounded-full border border-primary bg-background font-semibold transition-all duration-300',
        'hover:shadow-lg hover:shadow-primary/50',
        sizeClasses[size],
        className
      )}
      {...props}
    >
      <span className="inline-block translate-x-1 transition-all duration-300 group-hover:translate-x-12 group-hover:opacity-0">
        {text}
      </span>
      <div className="absolute top-0 z-10 flex h-full w-full translate-x-12 items-center justify-center gap-2 text-background opacity-0 transition-all duration-300 group-hover:-translate-x-1 group-hover:opacity-100">
        <span>{text}</span>
        <ArrowRight className="w-4 h-4" />
      </div>
      <div className="absolute left-[20%] top-[40%] h-2 w-2 scale-[1] rounded-lg bg-primary transition-all duration-300 group-hover:left-[0%] group-hover:top-[0%] group-hover:h-full group-hover:w-full group-hover:scale-[1.8] group-hover:bg-primary"></div>
    </button>
  );
});

InteractiveHoverButton.displayName = 'InteractiveHoverButton';

export { InteractiveHoverButton };
