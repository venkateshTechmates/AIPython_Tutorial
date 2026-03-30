let mermaidLoaded = false;

export async function renderMermaid(
  id: string,
  definition: string
): Promise<string> {
  if (!mermaidLoaded) {
    const { default: mermaid } = await import("mermaid");
    mermaid.initialize({
      startOnLoad: false,
      theme: "dark",
      themeVariables: {
        primaryColor: "#6366f1",
        primaryTextColor: "#e2e8f0",
        primaryBorderColor: "#4f46e5",
        lineColor: "#64748b",
        secondaryColor: "#1e293b",
        tertiaryColor: "#334155",
        background: "#0f172a",
        mainBkg: "#1e293b",
        nodeBorder: "#4f46e5",
        clusterBkg: "#1e293b",
        titleColor: "#e2e8f0",
        edgeLabelBackground: "#334155",
        attributeBackgroundColorEven: "#1e293b",
        attributeBackgroundColorOdd: "#0f172a",
      },
    });
    mermaidLoaded = true;
  }

  const { default: mermaid } = await import("mermaid");
  const { svg } = await mermaid.render(id, definition);
  return svg;
}
