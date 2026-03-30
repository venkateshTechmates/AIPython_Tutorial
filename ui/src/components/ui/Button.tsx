import React from "react";
import { clsx } from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger" | "outline";
  size?: "xs" | "sm" | "md" | "lg";
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  loading = false,
  leftIcon,
  rightIcon,
  children,
  className,
  disabled,
  ...props
}) => {
  const base =
    "inline-flex items-center justify-center gap-2 font-medium rounded-lg transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 focus-visible:ring-offset-surface-1 disabled:opacity-50 disabled:cursor-not-allowed select-none";

  const variants: Record<NonNullable<ButtonProps["variant"]>, string> = {
    primary:
      "bg-brand-600 hover:bg-brand-500 active:bg-brand-700 text-white shadow-sm",
    secondary:
      "bg-surface-2 hover:bg-surface-3 active:bg-surface-1 text-slate-200 border border-surface-3",
    ghost:
      "hover:bg-surface-2 active:bg-surface-3 text-slate-300 hover:text-white",
    danger:
      "bg-danger-600 hover:bg-danger-500 active:bg-danger-700 text-white shadow-sm",
    outline:
      "border border-brand-600 hover:bg-brand-600/10 text-brand-400 hover:text-brand-300",
  };

  const sizes: Record<NonNullable<ButtonProps["size"]>, string> = {
    xs: "text-xs px-2 py-1 gap-1",
    sm: "text-sm px-3 py-1.5",
    md: "text-sm px-4 py-2",
    lg: "text-base px-5 py-2.5",
  };

  return (
    <button
      className={clsx(base, variants[variant], sizes[size], className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
      ) : (
        leftIcon
      )}
      {children}
      {!loading && rightIcon}
    </button>
  );
};
