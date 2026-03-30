"""Part 5 — CLI demo runner for the triage agent."""

import asyncio
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from part_05_first_agent.agent.graph import build_triage_graph, get_graph_mermaid

console = Console()


async def run_demo():
    console.print(Panel("[bold cyan]Hospital AI Platform — Triage Agent Demo[/bold cyan]"))

    graph = build_triage_graph()
    session_id = "demo-session-001"
    config = {"configurable": {"thread_id": session_id}}

    # Simulate a triage conversation
    conversation = [
        "Hi, I have severe chest pain that started about an hour ago",
        "It's radiating to my left arm and I'm sweating",
        "I'm 58 years old, male, history of high blood pressure",
    ]

    console.print("\n[bold yellow]Simulating triage conversation...[/bold yellow]\n")

    for user_message in conversation:
        console.print(f"[bold green]Patient:[/bold green] {user_message}")

        state = await graph.ainvoke(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
        )

        last_msg = state["messages"][-1]
        console.print(f"[bold blue]Triage Agent:[/bold blue] {last_msg.content}\n")

        if state.get("urgency_level"):
            console.print(
                Panel(
                    f"Urgency: Level {state['urgency_level']}/5 — {state.get('urgency_label', 'Unknown')}",
                    style="bold red" if state["urgency_level"] <= 2 else "yellow",
                )
            )
            break

    console.print("\n[bold cyan]Graph Visualization (Mermaid):[/bold cyan]")
    console.print(get_graph_mermaid())


if __name__ == "__main__":
    asyncio.run(run_demo())
