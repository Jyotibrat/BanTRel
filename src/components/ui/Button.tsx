// src/components/ui/Button.tsx
import { forwardRef, type ButtonHTMLAttributes } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost' | 'destructive';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  isLoading?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary:
    'bg-[#a29bfe] text-[#2a1f7e] font-semibold hover:bg-[#c5c0ff] shadow-[0_0_16px_rgba(162,155,254,0.3)] hover:shadow-[0_0_24px_rgba(162,155,254,0.5)] active:scale-[0.98] border border-transparent disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none',
  secondary:
    'bg-[rgba(162,155,254,0.08)] border border-[#474552] text-[#e2e0fc] hover:border-[#a29bfe] hover:bg-[rgba(162,155,254,0.15)] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed',
  ghost:
    'bg-transparent border border-[#474552] text-[#c8c4d3] hover:border-[#a29bfe] hover:text-[#e2e0fc] hover:bg-[rgba(162,155,254,0.08)] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed',
  destructive:
    'bg-[rgba(231,76,60,0.08)] border border-[rgba(231,76,60,0.4)] text-[#e74c3c] hover:bg-[rgba(231,76,60,0.18)] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed',
};

const sizeClasses: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
  md: 'px-4 py-2 text-sm rounded-lg gap-2',
  lg: 'px-6 py-3 text-base rounded-xl gap-2',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { variant = 'primary', size = 'md', isLoading, className = '', children, disabled, ...props },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`inline-flex items-center justify-center font-medium transition-all duration-150 ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
        {...props}
      >
        {isLoading && (
          <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
        )}
        {children}
      </button>
    );
  },
);

Button.displayName = 'Button';
