import React, { createContext, useContext, useState } from "react";
import { clsx } from "clsx";

interface TabsContextValue {
  active: string;
  setActive: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue>({ active: "", setActive: () => {} });

interface TabsProps {
  defaultTab?: string;
  children: React.ReactNode;
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({ defaultTab = "", children, className }) => {
  const [active, setActive] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div className={clsx("flex flex-col", className)}>{children}</div>
    </TabsContext.Provider>
  );
};

interface TabListProps {
  children: React.ReactNode;
  className?: string;
}

export const TabList: React.FC<TabListProps> = ({ children, className }) => (
  <div
    role="tablist"
    className={clsx(
      "flex gap-1 border-b border-surface-3 overflow-x-auto scrollbar-none",
      className
    )}
  >
    {children}
  </div>
);

interface TabProps {
  id: string;
  children: React.ReactNode;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export const Tab: React.FC<TabProps> = ({ id, children, icon, disabled }) => {
  const { active, setActive } = useContext(TabsContext);
  const isActive = active === id;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      disabled={disabled}
      onClick={() => setActive(id)}
      className={clsx(
        "flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium transition-colors whitespace-nowrap focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 rounded-t-lg -mb-px",
        isActive
          ? "text-brand-400 border-b-2 border-brand-500 bg-brand-500/5"
          : "text-slate-400 hover:text-slate-200 border-b-2 border-transparent hover:border-surface-3",
        disabled && "opacity-40 cursor-not-allowed"
      )}
    >
      {icon && <span className="text-current">{icon}</span>}
      {children}
    </button>
  );
};

interface TabPanelProps {
  id: string;
  children: React.ReactNode;
  className?: string;
}

export const TabPanel: React.FC<TabPanelProps> = ({ id, children, className }) => {
  const { active } = useContext(TabsContext);
  if (active !== id) return null;
  return (
    <div role="tabpanel" className={clsx("flex-1 min-h-0", className)}>
      {children}
    </div>
  );
};
