"""
Interactive CLI for Julian Personal Assistant
"""
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from julian_assistant import JulianAssistant


console = Console()


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║         JULIAN PERSONAL ASSISTANT AI AGENT           ║
    ║                                                       ║
    ║         Your intelligent personal assistant          ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_help():
    """Print help information"""
    help_text = """
# Available Commands

## Schedule Management
- `jadwal hari ini` - View today's schedule
- `jadwal minggu ini` - View this week's schedule
- `statistik jadwal` - View schedule statistics

## Finance Management
- `saldo` - Check current balance
- `ringkasan bulan ini` - View monthly summary
- `statistik keuangan` - View finance statistics

## Data & Statistics
- `tips data` - Get random data tip
- `kategori tips` - View available tip categories
- `saran visualisasi` - Get visualization suggestions

## General
- `bantuan` or `help` - Show this help
- `exit` or `quit` - Exit the application
    """
    console.print(Markdown(help_text))


def main():
    """Main interactive CLI"""
    print_banner()
    
    console.print("\n[yellow]Initializing Julian Assistant...[/yellow]\n")
    
    try:
        with JulianAssistant() as assistant:
            # Show greeting
            greeting = assistant.greet()
            console.print(Panel(greeting, title="Julian", border_style="green"))
            
            # Main interaction loop
            while True:
                try:
                    # Get user input
                    user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                    
                    # Check for exit commands
                    if user_input.lower() in ["exit", "quit", "keluar"]:
                        console.print("\n[yellow]Terima kasih! Sampai jumpa! 👋[/yellow]\n")
                        break
                    
                    # Check for help command
                    if user_input.lower() in ["help", "bantuan", "?"]:
                        print_help()
                        continue
                    
                    # Process command
                    if user_input.strip():
                        response = assistant.process_command(user_input)
                        console.print(Panel(response, title="Julian", border_style="green"))
                
                except KeyboardInterrupt:
                    console.print("\n\n[yellow]Terima kasih! Sampai jumpa! 👋[/yellow]\n")
                    break
                except Exception as e:
                    console.print(f"\n[red]Error: {str(e)}[/red]\n")
    
    except Exception as e:
        console.print(f"\n[red]Failed to initialize assistant: {str(e)}[/red]\n")
        console.print("[yellow]Tip: Make sure to copy .env.example to .env and configure your settings[/yellow]\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
