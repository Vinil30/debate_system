import logging
import os
from typing import Callable, Any
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress
from dotenv import load_dotenv
from debate.agents import DebateAgent
from debate.memory import DebateMemory
from debate.judge import DebateJudge
from debate.graph import DebateGraph
import time
from winner_extracter import extract_winner_from_log

load_dotenv()

def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(console=Console(stderr=True)),
            logging.FileHandler("debate.log", mode="w", encoding="utf-8")
        ]
    )
    return logging.getLogger("debate")

def validate_groq_api_key() -> None:
    console = Console()
    
    if "GROQ_API_KEY" not in os.environ:
        console.print("[bold red]❌ GROQ_API_KEY not found in environment variables[/bold red]")
        console.print("\n[yellow]To fix this:[/yellow]")
        console.print("1. Create a .env file in your project directory")
        console.print("2. Add: GROQ_API_KEY=your_actual_api_key_here")
        console.print("3. Get your API key from: https://console.groq.com")
        raise ValueError("GROQ_API_KEY not found. Set it in your .env file.")
    
    api_key = os.environ["GROQ_API_KEY"]
    if not api_key or api_key == "your_actual_groq_api_key_here":
        console.print("[bold red]❌ GROQ_API_KEY is not set to a valid value[/bold red]")
        console.print("\n[yellow]Current value appears to be a placeholder.[/yellow]")
        console.print("Please set your actual Groq API key in the .env file")
        raise ValueError("GROQ_API_KEY appears to be invalid or placeholder value.")
    
    console.print("[green]✓ GROQ_API_KEY found[/green]")

def print_welcome_banner() -> None:
    console = Console()
    console.print(Panel.fit(
        "[bold green]Multi-Agent Debate System (Powered by Groq)[/bold green]",
        subtitle="Scientist vs Philosopher • 8 Rounds • Automated Judging",
        border_style="blue"
    ))

def initialize_components() -> tuple[DebateAgent, DebateAgent, DebateJudge, DebateMemory]:
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Initializing components...", total=4)
        
        progress.update(task, advance=1, description="Creating Scientist...")
        agent_a = DebateAgent("Scientist", "a scientist specializing in AI safety", model="llama3-8b-8192")
        
        progress.update(task, advance=1, description="Creating Philosopher...")
        agent_b = DebateAgent("Philosopher", "a philosopher specializing in ethics of technology", model="llama3-8b-8192")
        
        progress.update(task, advance=1, description="Creating Judge...")
        judge = DebateJudge(model="llama3-70b-8192")
        
        progress.update(task, advance=1, description="Setting up memory...")
        memory = DebateMemory()
        
    return agent_a, agent_b, judge, memory

def run_debate(app: Any, memory: DebateMemory, input_func: Callable[[str], str] = input) -> None:
    console = Console()
    
    # Initial state setup
    initial_state = {
        "memory": memory,
        "input": {
            "prompt": "Enter topic for debate: ",
            "input_func": input_func
        },
        "round": 0,
        "last_argument": "",
        "last_speaker": "",
        "next_speaker": "AgentA"
    }

    # Debate configuration display
    console.print("\n[bold]Debate Configuration[/bold]")
    console.print("• [blue]Agent A:[/blue] Scientist (llama3-8b)")
    console.print("• [blue]Agent B:[/blue] Philosopher (llama3-8b)")
    console.print("• [blue]Judge:[/blue] llama3-70b")
    console.print("• [blue]Rounds:[/blue] 8\n")

    # Get debate topic
    topic = input_func("Enter topic for debate: ")
    initial_state["topic"] = topic
    
    console.print(Panel.fit(
        f"[bold]Debate Topic:[/bold] {topic}",
        border_style="yellow"
    ))
    
    console.print("\n[yellow]🚀 Starting debate...[/yellow]\n")
    time.sleep(1)  # Brief pause before starting

    # Run debate rounds
    for output in app.stream(initial_state):
        initial_state.update(output)
        
        # Show round information
        round_num = initial_state.get("round", 0)
        if round_num > 0:
            speaker = initial_state.get("last_speaker", "Unknown")
            argument = initial_state.get("last_argument", "")
            
            if argument:
                color = "blue" if speaker == "Scientist" else "magenta"
                console.print(f"\n[bold cyan][Round {round_num}][/bold cyan]")
                console.print(f"[bold {color}]{speaker}:[/bold {color}]")
                console.print(Panel.fit(argument, border_style=color, padding=(0, 1)))
                logging.info(f"[Round {round_num}] {speaker}: {argument}")
                time.sleep(1)  # Pause between arguments

        # Handle judgment
        if "judgment" in output:
            console.print("\n[bold yellow]⏳ Judge is deliberating...[/bold yellow]")
            time.sleep(10)  # Dramatic pause
            
            judgment = output["judgment"]
            summary = judgment.get("summary", "No summary available")
            winner = judgment.get("winner", "Draw")
            win_color = "blue" if winner == "Scientist" else "magenta" if winner == "Philosopher" else "yellow"

            console.print("\n" + "="*60)
            console.print("[bold yellow]🏛️  JUDGE'S FINAL VERDICT[/bold yellow]")
            console.print("="*60)
            time.sleep(1)  # Small pause before verdict
            
            console.print(Panel.fit(summary, title="Debate Analysis", border_style="green"))
            console.print(f"\n[bold]🏆 Winner: [{win_color}]{winner}[/{win_color}][/bold]", justify="center")
            logging.info(f"\n[Judge] Winner: {winner}\n{summary}")
            
            break  # End after judgment

def main() -> int:
    try:
        validate_groq_api_key()
        logger = setup_logging()
        print_welcome_banner()

        agent_a, agent_b, judge, memory = initialize_components()
        debate_graph = DebateGraph(agent_a, agent_b, judge)
        app = debate_graph.compile()

        # Skip visualization to avoid errors
        try:
            debate_graph.visualize()
        except Exception as e:
            logger.warning(f"Visualization skipped: {e}")

        run_debate(app, memory, input_func=Console().input)

        # Winner extraction happens AFTER the debate completes
        winner = extract_winner_from_log('debate.log')
        console = Console()
        console.print(f"\n[bold]Final winner extracted from log:[/bold] [green]{winner}[/green]")

        console.print("\n[bold green]✓ Debate completed successfully![/bold green]")
        console.print("[dim]Check 'debate.log' for the full transcript.[/dim]")
        return 0

    except Exception as e:
        Console().print(f"\n[bold red]Error:[/bold red] {str(e)}")
        logging.error(f"System error: {str(e)}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())