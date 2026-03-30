import React, { useState } from "react";
import { clsx } from "clsx";
import { ChevronDown } from "lucide-react";

interface AccordionItemProps {
  title: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
  className?: string;
  headerClassName?: string;
  bodyClassName?: string;
  icon?: React.ReactNode;
  badge?: React.ReactNode;
}

export const AccordionItem: React.FC<AccordionItemProps> = ({
  title,
  children,
  defaultOpen = false,
  className,
  headerClassName,
  bodyClassName,
  icon,
  badge,
}) => {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div
      className={clsx(
        "rounded-xl border border-surface-3 overflow-hidden bg-surface-2 transition-colors",
        open && "border-brand-600/40",
        className
      )}
    >
      <button
        onClick={() => setOpen((o) => !o)}
        className={clsx(
          "w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-surface-3 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-brand-500",
          headerClassName
        )}
        aria-expanded={open}
      >
        {icon && <span className="text-brand-400 flex-shrink-0">{icon}</span>}
        <span className="flex-1 font-medium text-sm text-slate-200">{title}</span>
        {badge && <span className="mr-2">{badge}</span>}
        <ChevronDown
          size={16}
          className={clsx(
            "flex-shrink-0 text-slate-400 transition-transform duration-200",
            open && "rotate-180"
          )}
        />
      </button>
      <div
        className={clsx(
          "overflow-hidden transition-all duration-200",
          open ? "max-h-[9999px]" : "max-h-0"
        )}
      >
        <div className={clsx("px-4 pb-4 pt-1", bodyClassName)}>{children}</div>
      </div>
    </div>
  );
};

interface AccordionProps {
  children: React.ReactNode;
  className?: string;
}

export const Accordion: React.FC<AccordionProps> = ({ children, className }) => (
  <div className={clsx("flex flex-col gap-2", className)}>{children}</div>
);
