import time
import threading
import ollama
from rich.live import Live
from rich.console import Console
from rich.prompt import Prompt
from ui_layouts import make_magi_layout, update_magi_screen
from config import MAGI_HEADER, SYSTEM_PROMPTS, CORE_MODELS

console = Console()

# 1. THE GLOBAL STATE DICTIONARY
# This is what the UI reads from 10 times a second!
core_data = {
    "MELCHIOR": {"text": "Initiating logical analysis...", "vote": "PENDING..."},
    "BALTHASAR": {"text": "Evaluating ethical parameters...", "vote": "PENDING..."},
    "CASPER": {"text": "Calculating wild-card variables...", "vote": "PENDING..."}
}

def query_core(core_name, user_query):
    """Worker thread that talks to local Ollama and updates the global state."""
    try:
        response = ollama.chat(
            model=CORE_MODELS.get(core_name, 'llama3'),
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPTS[core_name]},
                {'role': 'user', 'content': user_query}
            ]
        )
        
        full_text = response['message']['content']
        
        # Parse out the vote logic for the UI colors
        if "[VOTE: APPROVE]" in full_text:
            core_data[core_name]["vote"] = "APPROVE" # ui_layouts.py handles the color/icon
            core_data[core_name]["text"] = full_text.replace("[VOTE: APPROVE]", "").strip()
        elif "[VOTE: REJECT]" in full_text:
            core_data[core_name]["vote"] = "REJECT"
            core_data[core_name]["text"] = full_text.replace("[VOTE: REJECT]", "").strip()
        else:
            core_data[core_name]["vote"] = "REJECT" # Default/Error
            core_data[core_name]["text"] = full_text
            
    except Exception as e:
        core_data[core_name]["vote"] = "ERROR"
        core_data[core_name]["text"] = f"Connection failed: {str(e)}"

def calculate_final_verdict():
    """Tally the votes once all cores are finished."""
    approves = sum(1 for data in core_data.values() if data["vote"] == "APPROVE")
    
    if approves == 3:
        return "[bold green]OPERATION APPROVED (3-0 UNANIMOUS)[/bold green]"
    elif approves == 2:
        return "[bold yellow]PROCEED WITH CAUTION (2-1 MAJORITY)[/bold yellow]"
    else:
        return "[bold red]OPERATION REJECTED (INSUFFICIENT CONSENSUS)[/bold red]"

def run_magi():
    while True:
        console.clear()
        console.print(f"[bold red]{MAGI_HEADER}[/bold red]")
        
        try:
            user_query = Prompt.ask("\n[bold white]INPUT DILEMMA[/bold white] (or 'exit')")
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                console.print("[bold orange3]>> SHUTTING DOWN NEURAL LINK...[/bold orange3]")
                break
                
            if not user_query.strip():
                continue

            # Reset core data for the new dilemma
            core_data["MELCHIOR"] = {"text": "Initiating logical analysis...", "vote": "PENDING"}
            core_data["BALTHASAR"] = {"text": "Evaluating ethical parameters...", "vote": "PENDING"}
            core_data["CASPER"] = {"text": "Calculating wild-card variables...", "vote": "PENDING"}
            
            # Generate the initial UI layout
            layout = make_magi_layout()
            
            # Fire off the 3 AI threads in the background
            threads = []
            for core in ["MELCHIOR", "BALTHASAR", "CASPER"]:
                t = threading.Thread(target=query_core, args=(core, user_query))
                threads.append(t)
                t.start()

            # 🚀 START THE LIVE TERMINAL RENDER LOOP
            with Live(layout, refresh_per_second=10, screen=True) as live:
                # Keep updating the screen while the models are generating!
                while any(t.is_alive() for t in threads):
                    update_magi_screen(layout, user_query, core_data)
                    time.sleep(0.1) # Smooth 10 FPS refresh rate
                    
                # Once threads finish, update one last time with the final tally
                final_verdict = calculate_final_verdict()
                update_magi_screen(layout, user_query, core_data, final_verdict)
                
                # Keep the screen up and wait for user input to continue
                live.console.print("\n[bold white]Press Enter to continue...[/bold white]")
                input()

        except KeyboardInterrupt:
            console.print("\n[bold red]EMERGENCY SHUTDOWN[/bold red]")
            break

if __name__ == "__main__":
    run_magi()
