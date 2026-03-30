import React from "react";
import { Link, NavLink } from "react-router-dom";
import {
  Activity,
  BookOpen,
  FlaskConical,
  BarChart2,
  Settings,
  Cpu,
  Menu,
  X,
  Moon,
  Sun,
} from "lucide-react";
import { useAppStore } from "../../store/appStore";
import type { ColorTheme } from "../../store/appStore";
import { useTheme } from "../../hooks/useTheme";
import { BackendStatusDot } from "./BackendStatusDot";
import { clsx } from "clsx";

const NAV_ITEMS = [
  { to: "/", label: "Overview", icon: Activity, end: true },
  { to: "/setup", label: "Setup", icon: Settings },
  { to: "/playground", label: "Playground", icon: FlaskConical },
  { to: "/progress", label: "Progress", icon: BarChart2 },
  { to: "/glossary", label: "Glossary", icon: BookOpen },
];

const COLOR_SWATCHES: { id: ColorTheme; hex: string; label: string }[] = [
  { id: "indigo", hex: "#6366f1", label: "Indigo" },
  { id: "violet", hex: "#8b5cf6", label: "Violet" },
  { id: "teal",   hex: "#14b8a6", label: "Teal"   },
  { id: "rose",   hex: "#f43f5e", label: "Rose"   },
  { id: "amber",  hex: "#f59e0b", label: "Amber"  },
  { id: "sky",    hex: "#0ea5e9", label: "Sky"    },
];

export const Topbar: React.FC = () => {
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed);
  const toggleSidebar = useAppStore((s) => s.toggleSidebar);
  const { theme, toggleTheme, colorTheme, setColorTheme } = useTheme();

  return (
    <header className="fixed top-0 left-0 right-0 z-40 h-14 bg-surface-1/95 backdrop-blur border-b border-surface-3 flex items-center px-4 gap-3">
      {/* Toggle sidebar */}
      <button
        onClick={() => toggleSidebar()}
        className="p-1.5 rounded-lg hover:bg-surface-3 text-slate-400 hover:text-white transition-colors"
        aria-label="Toggle sidebar"
      >
        {sidebarCollapsed ? <Menu size={18} /> : <X size={18} />}
      </button>

      {/* Logo */}
      <Link to="/" className="flex items-center gap-2 mr-4">
        <div className="w-7 h-7 rounded-lg bg-brand-600 flex items-center justify-center flex-shrink-0">
          <Cpu size={14} className="text-white" />
        </div>
        <span className="font-bold text-sm text-white hidden sm:block">
          Hospital AI <span className="text-brand-400">Platform</span>
        </span>
      </Link>

      {/* Top nav (md+) */}
      <nav className="hidden md:flex items-center gap-1 flex-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-brand-600/20 text-brand-300"
                  : "text-slate-400 hover:text-slate-200 hover:bg-surface-3"
              )
            }
          >
            <Icon size={15} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="ml-auto flex items-center gap-2">
        <BackendStatusDot />

        {/* Color theme swatches */}
        <div className="hidden sm:flex items-center gap-1 px-1" role="group" aria-label="Color theme">
          {COLOR_SWATCHES.map(({ id, hex, label }) => (
            <button
              key={id}
              onClick={() => setColorTheme(id)}
              title={label}
              aria-label={`${label} theme`}
              className={clsx(
                "w-4 h-4 rounded-full transition-all duration-150",
                colorTheme === id
                  ? "ring-2 ring-white ring-offset-1 ring-offset-surface-1 scale-110"
                  : "opacity-50 hover:opacity-90 hover:scale-105"
              )}
              style={{ backgroundColor: hex }}
            />
          ))}
        </div>

        <button
          onClick={toggleTheme}
          className="p-1.5 rounded-lg hover:bg-surface-3 text-slate-400 hover:text-white transition-colors"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun size={16} /> : <Moon size={16} />}
        </button>
      </div>
    </header>
  );
};
