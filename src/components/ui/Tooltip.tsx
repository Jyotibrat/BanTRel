// src/components/ui/Tooltip.tsx
import { useState, type ReactNode } from 'react';

interface TooltipProps {
  content: string;
  children: ReactNode;
}

export function Tooltip({ content, children }: TooltipProps) {
  const [visible, setVisible] = useState(false);

  return (
    <span
      className="relative inline-flex items-center"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      {children}
      {visible && (
        <span
          role="tooltip"
          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 z-50 w-64 rounded-lg border border-[rgba(162,155,254,0.3)] bg-[#2b2b48] p-3 text-xs leading-relaxed text-[#c8c4d3] shadow-[0_16px_36px_-6px_rgba(0,0,0,0.75)] pointer-events-none"
        >
          {content}
          <span className="absolute top-full left-1/2 -translate-x-1/2 -mt-px w-0 h-0 border-x-4 border-x-transparent border-t-4 border-t-[#2b2b48]" />
        </span>
      )}
    </span>
  );
}
