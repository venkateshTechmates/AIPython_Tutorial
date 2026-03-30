import React from "react";
import { Outlet } from "react-router-dom";
import { Topbar } from "./Topbar";
import { Sidebar } from "./Sidebar";
import { useAppStore } from "../../store/appStore";
import { clsx } from "clsx";

export const AppShell: React.FC = () => {
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed);

  return (
    <div className="min-h-screen bg-surface-1 text-slate-100 flex flex-col">
      <Topbar />
      <div className="flex flex-1 pt-14">
        {/* Sidebar */}
        <aside
          className={clsx(
            "fixed left-0 top-14 bottom-0 z-30 flex flex-col transition-all duration-200 ease-in-out",
            "bg-surface-1 border-r border-surface-3",
            sidebarCollapsed ? "w-14" : "w-64"
          )}
        >
          <Sidebar />
        </aside>
        {/* Main content */}
        <main
          className={clsx(
            "flex-1 min-h-0 transition-all duration-200 ease-in-out overflow-auto",
            sidebarCollapsed ? "ml-14" : "ml-64"
          )}
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};
