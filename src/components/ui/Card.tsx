// src/components/ui/Card.tsx
import { type HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  elevated?: boolean;
  hoverable?: boolean;
}

export function Card({ elevated, hoverable, className = '', children, ...props }: CardProps) {
  const base =
    'rounded-xl border border-[#474552] bg-[#1e1e32] shadow-[0_4px_20px_-2px_rgba(10,10,20,0.45)]';
  const elevatedClass = elevated
    ? 'bg-[#28283d] shadow-[0_8px_24px_-4px_rgba(6,6,15,0.6)]'
    : '';
  const hoverClass = hoverable
    ? 'transition-all duration-200 hover:border-[#a29bfe] hover:bg-[#28283d] hover:shadow-[0_8px_24px_-4px_rgba(6,6,15,0.6)] cursor-pointer'
    : '';

  return (
    <div
      className={`${base} ${elevatedClass} ${hoverClass} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
