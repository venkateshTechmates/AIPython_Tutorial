import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "rgb(var(--brand-500) / <alpha-value>)",
          dark:    "rgb(var(--brand-600) / <alpha-value>)",
          50:      "rgb(var(--brand-50)  / <alpha-value>)",
          100:     "rgb(var(--brand-100) / <alpha-value>)",
          200:     "rgb(var(--brand-200) / <alpha-value>)",
          300:     "rgb(var(--brand-300) / <alpha-value>)",
          400:     "rgb(var(--brand-400) / <alpha-value>)",
          500:     "rgb(var(--brand-500) / <alpha-value>)",
          600:     "rgb(var(--brand-600) / <alpha-value>)",
          700:     "rgb(var(--brand-700) / <alpha-value>)",
          800:     "rgb(var(--brand-800) / <alpha-value>)",
          900:     "rgb(var(--brand-900) / <alpha-value>)",
        },
        agent: {
          DEFAULT: "#8b5cf6",
          300: "#c4b5fd",
          400: "#a78bfa",
          500: "#8b5cf6",
          600: "#7c3aed",
        },
        success: {
          DEFAULT: "#10b981",
          300: "#6ee7b7",
          400: "#34d399",
          500: "#10b981",
          600: "#059669",
        },
        warn: {
          DEFAULT: "#f59e0b",
          300: "#fcd34d",
          400: "#fbbf24",
          500: "#f59e0b",
          600: "#d97706",
        },
        danger: {
          DEFAULT: "#ef4444",
          300: "#fca5a5",
          400: "#f87171",
          500: "#ef4444",
          600: "#dc2626",
        },
        surface: { 1: "#0f172a", 2: "#1e293b", 3: "#334155" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      animation: {
        "fade-in": "fadeIn 0.2s ease-in-out",
        "slide-in": "slideIn 0.2s ease-out",
        pulse2: "pulse2 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideIn: {
          "0%": { transform: "translateX(-8px)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        pulse2: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.4" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
