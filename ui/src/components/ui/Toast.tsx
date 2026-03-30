import React, { createContext, useContext, useState, useCallback } from "react";
import { createPortal } from "react-dom";
import { clsx } from "clsx";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

type ToastType = "success" | "error" | "info";

interface ToastItem {
  id: string;
  type: ToastType;
  message: string;
}

interface ToastContextValue {
  toast: (type: ToastType, message: string) => void;
}

const ToastContext = createContext<ToastContextValue>({ toast: () => {} });

export const useToast = () => useContext(ToastContext);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const dismiss = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback((type: ToastType, message: string) => {
    const id = crypto.randomUUID();
    setToasts((prev) => [...prev.slice(-4), { id, type, message }]);
    setTimeout(() => dismiss(id), 3500);
  }, [dismiss]);

  const icons: Record<ToastType, React.ReactNode> = {
    success: <CheckCircle2 size={16} className="text-success-400 flex-shrink-0" />,
    error: <AlertCircle size={16} className="text-danger-400 flex-shrink-0" />,
    info: <Info size={16} className="text-brand-400 flex-shrink-0" />,
  };

  const styles: Record<ToastType, string> = {
    success: "border-success-500/30 bg-success-900/30",
    error: "border-danger-500/30 bg-danger-900/30",
    info: "border-brand-500/30 bg-brand-900/30",
  };

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      {createPortal(
        <div className="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 pointer-events-none">
          {toasts.map((t) => (
            <div
              key={t.id}
              className={clsx(
                "pointer-events-auto flex items-center gap-2.5 px-4 py-3 rounded-xl border shadow-xl text-sm text-slate-200 bg-surface-2 max-w-xs animate-fadeIn",
                styles[t.type]
              )}
            >
              {icons[t.type]}
              <span className="flex-1">{t.message}</span>
              <button
                onClick={() => dismiss(t.id)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <X size={14} />
              </button>
            </div>
          ))}
        </div>,
        document.body
      )}
    </ToastContext.Provider>
  );
};
