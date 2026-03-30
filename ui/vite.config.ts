import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/AIPython_Tutorial/",
  plugins: [react()],
  build: {
    outDir: "dist",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "react-router-dom"],
          charts: ["recharts"],
          code: ["shiki"],
          motion: ["framer-motion"],
          diagrams: ["mermaid"],
        },
      },
    },
  },
  optimizeDeps: {
    exclude: ["mermaid"],
  },
});
