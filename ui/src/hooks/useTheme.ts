import { useEffect } from "react";
import { useAppStore } from "../store/appStore";

export function useTheme() {
  const { theme, setTheme, toggleTheme, colorTheme, setColorTheme } = useAppStore();

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }, [theme]);

  useEffect(() => {
    document.documentElement.setAttribute("data-color", colorTheme);
  }, [colorTheme]);

  return { theme, setTheme, toggleTheme, colorTheme, setColorTheme };
}
