import React from "react";
import { HashRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/shell/AppShell";
import { ToastProvider } from "./components/ui/Toast";
import { OverviewPage } from "./pages/OverviewPage";
import { SetupPage } from "./pages/SetupPage";
import { PartDetailPage } from "./pages/PartDetailPage";
import { PlaygroundPage } from "./pages/PlaygroundPage";
import { ProgressPage } from "./pages/ProgressPage";
import { GlossaryPage } from "./pages/GlossaryPage";

function App() {
  return (
    <ToastProvider>
      <HashRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<OverviewPage />} />
            <Route path="setup" element={<SetupPage />} />
            <Route path="part/:partId" element={<PartDetailPage />} />
            <Route path="playground" element={<PlaygroundPage />} />
            <Route path="progress" element={<ProgressPage />} />
            <Route path="glossary" element={<GlossaryPage />} />
          </Route>
        </Routes>
      </HashRouter>
    </ToastProvider>
  );
}

export default App;
