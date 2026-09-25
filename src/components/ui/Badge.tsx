// src/components/ui/Badge.tsx

type BadgeVariant = 'ppo' | 'fixed_cycle' | 'tie' | 'default' | 'success' | 'error' | 'warning';

interface BadgeProps {
  variant?: BadgeVariant;
  pill?: boolean;
  children: React.ReactNode;
  className?: string;
}

const variantClasses: Record<BadgeVariant, string> = {
  ppo:         'bg-[rgba(46,204,113,0.12)] text-[#2ecc71] border border-[rgba(46,204,113,0.25)]',
  fixed_cycle: 'bg-[rgba(231,76,60,0.12)]  text-[#e74c3c] border border-[rgba(231,76,60,0.25)]',
  tie:         'bg-[rgba(243,156,18,0.12)]  text-[#f39c12] border border-[rgba(243,156,18,0.25)]',
  success:     'bg-[rgba(46,204,113,0.12)] text-[#2ecc71] border border-[rgba(46,204,113,0.25)]',
  error:       'bg-[rgba(231,76,60,0.12)]  text-[#e74c3c] border border-[rgba(231,76,60,0.25)]',
  warning:     'bg-[rgba(243,156,18,0.12)]  text-[#f39c12] border border-[rgba(243,156,18,0.25)]',
  default:     'bg-[rgba(162,155,254,0.1)] text-[#c5c0ff] border border-[rgba(162,155,254,0.2)]',
};

export function Badge({ variant = 'default', pill = true, children, className = '' }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 text-xs font-medium font-mono ${
        pill ? 'rounded-full' : 'rounded'
      } ${variantClasses[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
