import React from "react";
import { Playground } from "../components/playground/Playground";

export const PlaygroundPage: React.FC = () => (
  <div className="flex flex-col gap-4 h-[calc(100vh-8rem)]">
    <div>
      <h1 className="text-2xl font-bold text-white">API Playground</h1>
      <p className="text-sm text-slate-400">
        Explore and test all endpoints from your running FastAPI backends.
      </p>
    </div>
    <div className="flex-1 min-h-0">
      <Playground />
    </div>
  </div>
);
