import time
import threading
import sys
import re
import argparse

try:
    import ollama
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.console import Console
    from rich.align import Align
    from rich.text import Text
    from rich.table import Table
    from rich import box
    from prompt_toolkit import PromptSession
    from prompt_toolkit.enums import EditingMode
    from prompt_toolkit.styles import Style as PromptStyle
except ImportError:
    print("❌ CRITICAL ERROR: Missing dependencies!")
    print("👉 Please run: pip install ollama rich prompt_toolkit")
    sys.exit(1)

# --- NERV TACTICAL COLOR PALETTE ---
NERV_AMBER = "#ff9900"
NERV_GREEN = "#00ff66"
NERV_RED = "#ff0033"
NERV_WHITE = "#e0e0e0"

# Global state dictionary
core_data = {
    "MELCHIOR": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER},
    "BALTHASAR": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER},
    "CASPER": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER}
}

VOTE_INSTRUCTION = "\n\nCRITICAL INSTRUCTION: At the absolute end of your response, you MUST output exactly either [VOTE: APPROVE] or [VOTE: REJECT]."

SYSTEM_PROMPTS = {
    "MELCHIOR": "You are MAGI-1: MELCHIOR. You are logical, scientific, and practical. Keep your analysis brief (3-4 sentences)." + VOTE_INSTRUCTION,
    "BALTHASAR": "You are MAGI-2: BALTHASAR. You are empathetic, protective, and human-centric. Keep your analysis brief (3-4 sentences)." + VOTE_INSTRUCTION,
    "CASPER": "You are MAGI-3: CASPER. You are bold, risk-taking, and individualistic. Keep your analysis brief (3-4 sentences)." + VOTE_INSTRUCTION
}

def get_command_center_display():
    """Builds the NERV Command Center dashboard UI."""
    header_table = Table.grid(expand=True)
    header_table.add_column(justify="left")
    header_table.add_column(justify="right")
    header_table.add_row(
        f"[bold {NERV_RED}]🔴 [SYS.AUTH: SENPAI_ADMIN][/bold {NERV_RED}]",
        f"[bold {NERV_AMBER}][NET_STATUS: FULL_TELEMETRY][/bold {NERV_AMBER}]"
    )

    magi_logo = f"""
[bold {NERV_RED}]
  ███╗   ███╗ █████╗  ██████╗ ██╗
  ████╗ ████║██╔══██╗██╔════╝ ██║
  ██╔████╔██║███████║██║  ███╗██║
  ██║╚██╔╝██║██╔══██║██║   ██║██║
  ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝
[/bold {NERV_RED}]
"""
    status_text = Text()
    status_text.append("\n[LOCAL NODE: NERV_HQ_GEOFRONT]\n", style=f"bold {NERV_AMBER}")
    status_text.append("──────────────────────────────────────\n", style=f"{NERV_AMBER} dim")
    
    sync_msg = (
        f"[CORE_1: MELCHIOR]  ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n"
        f"[CORE_2: BALTHASAR] ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n"
        f"[CORE_3: CASPER]    ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n\n"
    )
    status_text.append(Text.from_markup(sync_msg))
    status_text.append("DEFENSE: ABSOLUTE TERROR FIELD ACTIVE", style=f"bold {NERV_RED}")

    main_table = Table.grid(expand=True, padding=(0, 2))
    main_table.add_column(ratio=1)
    main_table.add_column(ratio=1)
    main_table.add_row(Align.center(magi_logo), Align.left(status_text))

    dashboard = Table.grid(expand=True)
    dashboard.add_row(header_table)
    dashboard.add_row(Panel(main_table, border_style=NERV_AMBER, box=box.SQUARE))
    dashboard.add_row(f"[bold {NERV_RED}]⚠️  AWAITING DYNAMIC INPUT QUERY...[/bold {NERV_RED}]")

    return Panel(dashboard, border_style=NERV_AMBER, box=box.HEAVY)

def make_magi_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=4)
    )
    layout["body"].split_row(
        Layout(name="melchior"),
        Layout(name="balthasar"),
        Layout(name="casper")
    )
    return layout

def update_magi_screen(layout: Layout, query: str, final_verdict: str = "SYNCHRONIZING CORES..."):
    header_text = Text(f"MAGI SYSTEM ACTIVE | CODE: 00 | DILEMMA: \"{query}\"", style=f"bold {NERV_AMBER}", justify="center")
    layout["header"].update(Panel(header_text, border_style=NERV_AMBER, box=box.SQUARE))
    
    for core_name, core_id, title in [
        ("MELCHIOR", "melchior", "🤖 MAGI-1: MELCHIOR (LOGIC)"),
        ("BALTHASAR", "balthasar", "💖 MAGI-2: BALTHASAR (MOTHER)"),
        ("CASPER", "casper", "🔥 MAGI-3: CASPER (INDIVIDUAL)")
    ]:
        data = core_data[core_name]
        content = Text()
        content.append(data["text"] + "\n\n", style=NERV_WHITE)
        content.append(f"STATUS: {data['vote']}", style=f"bold {data['color']}")
        layout[core_id].update(
            Panel(Align.left(content), title=f"[bold {data['color']}]{title}[/bold {data['color']}]", border_style=data['color'], box=box.SQUARE, padding=(1, 2))
        )
    
    footer_text = Text.from_markup(final_verdict, justify="center")
    layout["footer"].update(Panel(footer_text, title=f"[bold {NERV_AMBER}]🤖 CONSENSUS ENGINE[/bold {NERV_AMBER}]", border_style=NERV_AMBER, box=box.SQUARE))

def query_core(core_name: str, user_query: str):
    core_data[core_name]["text"] = "Calculating neural pathways...\nQuerying local model..."
    core_data[core_name]["vote"] = "PROCESSING..."
    core_data[core_name]["color"] = NERV_AMBER
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'system', 'content': SYSTEM_PROMPTS[core_name]}, {'role': 'user', 'content': user_query}])
        full_text = response['message']['content'].strip()
        if "[VOTE: APPROVE]" in full_text:
            core_data[core_name]["vote"] = "🟢 APPROVED"
            core_data[core_name]["color"] = NERV_GREEN
            core_data[core_name]["text"] = re.sub(r'\[VOTE:.*?\]', '', full_text).strip()
        elif "[VOTE: REJECT]" in full_text:
            core_data[core_name]["vote"] = "🔴 REJECTED"
            core_data[core_name]["color"] = NERV_RED
            core_data[core_name]["text"] = re.sub(r'\[VOTE:.*?\]', '', full_text).strip()
        else:
            core_data[core_name]["vote"] = "🔴 REJECTED (FORMAT ERROR)"
            core_data[core_name]["color"] = NERV_RED
            core_data[core_name]["text"] = full_text
    except Exception as e:
        core_data[core_name]["vote"] = "💥 SYSTEM CRASH"
        core_data[core_name]["color"] = NERV_RED
        core_data[core_name]["text"] = f"Connection failed.\nError: {str(e)}"

def calculate_final_verdict() -> str:
    approves = sum(1 for core in core_data.values() if "🟢" in core["vote"])
    if approves == 3:
        return f"[bold {NERV_GREEN}]🔴 CODE 01: UNANIMOUS CONSENSUS (3-0) - OPERATION APPROVED[/bold {NERV_GREEN}]"
    elif approves == 2:
        return f"[bold {NERV_AMBER}]🟡 CODE 02: MAJORITY DECISION (2-1) - PROCEED WITH CAUTION[/bold {NERV_AMBER}]"
    else:
        return f"[bold {NERV_RED}]❌ CODE 03: OPERATION REJECTED BY MAGI (INSUFFICIENT CONSENSUS)[/bold {NERV_RED}]"

def run_consensus(user_query: str):
    """Executes the consensus engine for a single dilemma."""
    for core in core_data:
        core_data[core] = {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER}
        
    layout = make_magi_layout()
    threads = []
    for core in ["MELCHIOR", "BALTHASAR", "CASPER"]:
        t = threading.Thread(target=query_core, args=(core, user_query))
        threads.append(t)
        t.start()

    with Live(layout, refresh_per_second=10, screen=True) as live:
        while any(t.is_alive() for t in threads):
            update_magi_screen(layout, user_query)
            time.sleep(0.1)
        final_verdict = calculate_final_verdict()
        update_magi_screen(layout, user_query, final_verdict)
        return final_verdict

def main():
    parser = argparse.ArgumentParser(description="MAGI Supercomputer Strategy System")
    parser.add_argument("-p", "--prompt", type=str, help="Dilemma to process directly via command line")
    args = parser.parse_args()

    console = Console()

    if args.prompt:
        final_verdict = run_consensus(args.prompt)
        # Display the result in the scrollback buffer after the TUI closes
        console.print(f"\n[bold {NERV_AMBER}]" + "="*50 + f"[/bold {NERV_AMBER}]")
        console.print(f"[bold {NERV_WHITE}]MAGI FINAL VERDICT:[/bold {NERV_WHITE}] {final_verdict}")
        console.print(f"[bold {NERV_AMBER}]" + "="*50 + f"[/bold {NERV_AMBER}]\n")
        return

    # Initialize prompt_toolkit session for interactive mode
    session = PromptSession(editing_mode=EditingMode.VI)
    prompt_style = PromptStyle.from_dict({
        'prompt': f'bold {NERV_AMBER}',
        'input': NERV_WHITE,
    })

    while True:
        console.clear()
        console.print(get_command_center_display())
        console.print(f"\n[bold {NERV_AMBER}]🔮 Initialize MAGI System Prompt Sequence...[/bold {NERV_AMBER}]")
        console.print(f"[dim {NERV_WHITE}](Vim mode active: Press Esc for command mode)[/dim {NERV_WHITE}]")
        
        try:
            user_query = session.prompt(
                [('class:prompt', 'Enter tactical dilemma '), ('class:prompt', '(or \'exit\'): ')],
                style=prompt_style
            )
        except KeyboardInterrupt:
            console.print(f"\n[bold {NERV_RED}]EMERGENCY SHUTDOWN[/bold {NERV_RED}]")
            break
        except EOFError:
            break
            
        if user_query.lower() in ['exit', 'quit', 'q']:
            console.print(f"[bold {NERV_AMBER}]>> SHUTTING DOWN NEURAL LINK...[/bold {NERV_AMBER}]")
            break
        if not user_query.strip(): continue

        final_verdict = run_consensus(user_query)
        
        # In interactive mode, we wait for input to keep the result on screen
        print(f"\n[bold {NERV_WHITE}]Press Enter to continue...[/bold {NERV_WHITE}]")
        input()

if __name__ == "__main__":
    main()
