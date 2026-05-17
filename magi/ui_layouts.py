from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

def make_magi_layout() -> Layout:
    """Generates the structural grid for the MAGI visual terminal."""
    layout = Layout()

    # Split into Header, Core Debate Area, and Verdict Footer
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=5)
    )

    # Split the main body into three horizontal tracks for the 3 MAGI cores
    layout["body"].split_row(
        Layout(name="MELCHIOR"),
        Layout(name="BALTHASAR"),
        Layout(name="CASPER")
    )
    
    return layout

def update_magi_screen(layout, query, core_data, final_verdict=None):
    """Pipes text data dynamically into the Rich panels."""
    
    # 1. Header Display
    layout["header"].update(
        Panel(f"🔮 [bold orange3]MAGI SYSTEM ACTIVE[/bold orange3] | Query: [white]\"{query}\"[/white]", border_style="orange3")
    )
    
    # Core mappings for styling
    core_styles = {
        "MELCHIOR": {"title": "🤖 MAGI-1: MELCHIOR (Logic)", "color": "cyan"},
        "BALTHASAR": {"title": "💖 MAGI-2: BALTHASAR (Mother)", "color": "magenta"},
        "CASPER": {"title": "🔥 MAGI-3: CASPER (Individual)", "color": "orange3"}
    }
    
    for core_id, style in core_styles.items():
        data = core_data[core_id]
        vote = data["vote"]
        text = data["text"]
        
        # Determine border color based on vote
        border = style["color"]
        if vote == "APPROVE": border = "green"
        elif vote == "REJECT": border = "red"
        elif vote == "PENDING": border = "orange3"
        
        # Format the display
        display_text = Text()
        display_text.append(text + "\n\n", style="white")
        
        vote_style = "bold yellow"
        if vote == "APPROVE": vote_style = "bold green"
        elif vote == "REJECT": vote_style = "bold red"
        
        display_text.append("🗳️ STATUS: ", style="bold orange3")
        display_text.append(vote, style=vote_style)
        
        layout[core_id].update(
            Panel(display_text, title=style["title"], border_style=border)
        )
    
    # 5. Final Verdict Footer Display
    if final_verdict:
        verdict_panel = Panel(
            f"[bold white]📊 FINAL SYSTEM VERDICT:[/bold white] {final_verdict}", 
            title="🤖 CONSENSUS ENGINE", 
            border_style="bold orange3"
        )
    else:
        verdict_panel = Panel(
            "[bold yellow]📊 FINAL SYSTEM VERDICT:[/bold yellow] [blink]AWAITING CONSENSUS...[/blink]", 
            title="🤖 CONSENSUS ENGINE", 
            border_style="orange3"
        )
        
    layout["footer"].update(verdict_panel)
