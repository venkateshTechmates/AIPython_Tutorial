import React, { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { clsx } from "clsx";
import { X } from "lucide-react";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg" | "xl" | "full";
  hideCloseButton?: boolean;
  className?: string;
}

export const Modal: React.FC<ModalProps> = ({
  open,
  onClose,
  title,
  children,
  size = "md",
  hideCloseButton = false,
  className,
}) => {
  const overlayRef = useRef<HTMLDivElement>(null);

  // Close on Escape
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [open, onClose]);

  // Lock scroll
  useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [open]);

  if (!open) return null;

  const sizeClasses = {
    sm: "max-w-sm",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-5xl",
    full: "max-w-[95vw] max-h-[95vh]",
  };

  return createPortal(
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      onClick={(e) => {
        if (e.target === overlayRef.current) onClose();
      }}
    >
      <div
        className={clsx(
          "relative w-full bg-surface-1 border border-surface-3 rounded-2xl shadow-2xl flex flex-col",
          sizeClasses[size],
          size === "full" ? "h-[95vh]" : "max-h-[90vh]",
          className
        )}
        role="dialog"
        aria-modal="true"
        aria-label={title}
      >
        {/* Header */}
        {(title || !hideCloseButton) && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-surface-3 flex-shrink-0">
            {title && (
              <h2 className="text-base font-semibold text-slate-100">{title}</h2>
            )}
            {!hideCloseButton && (
              <button
                onClick={onClose}
                className="ml-auto p-1.5 rounded-lg hover:bg-surface-3 text-slate-400 hover:text-white transition-colors"
                aria-label="Close modal"
              >
                <X size={18} />
              </button>
            )}
          </div>
        )}
        {/* Content */}
        <div className="flex-1 overflow-auto">{children}</div>
      </div>
    </div>,
    document.body
  );
};
