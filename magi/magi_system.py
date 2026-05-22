import time
import threading
import sys
import re
import argparse
import random
import os
import json

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

NERV_STATUS_MESSAGES = [
    "LCL DENSITY: OPTIMAL (99.8%)",
    "EVA UNIT-01 STATUS: STANDBY",
    "ENTRY PLUG DEPTH: NORMAL",
    "REI AYANAMI: IN MEDICAL BAY",
    "MISATO KATSURAGI: ORDERED RAMEN AGAIN",
    "GENDO IKARI: OBSERVING...",
    "PROBABILITY OF SYNCHRONIZATION: 85.3%",
    "PEN PEN: IN THE REFRIGERATOR",
    "LONGINUS SPEAR: MOON ORBIT STABLE",
    "INTERNAL POWER: 04:59 REMAINING",
    "S.C. MAGI: NEURAL LINK STABLE",
]

SECRET_PHRASES = {
    "get in the robot": "SHINJI, GET IN THE ROBOT OR REI WILL HAVE TO DO IT AGAIN.",
    "pattern blue": "BLOOD TYPE: BLUE! IT'S AN ANGEL! ALL HANDS TO BATTLE STATIONS!",
    "human instrumentality project": "SEELE AUTHORIZATION REQUIRED. ACCESS DENIED. GENDO IS WATCHING YOU.",
    "third impact": "INITIATING INSTRUMENTALITY... JUST KIDDING. [dim]Unless?[/dim]",
    "cruel angel's thesis": "🎶 ZANKOKU NA TENSHI NO YOU NI... 🎶",
}

# Global state dictionary
core_data = {
    "MELCHIOR": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER},
    "BALTHASAR": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER},
    "CASPER": {"text": "Awaiting input...", "vote": "STANDBY", "color": NERV_AMBER}
}

# Multi-turn conversation history state
core_histories = {
    "MELCHIOR": [],
    "BALTHASAR": [],
    "CASPER": []
}

def reset_chat():
    global core_histories
    core_histories = {
        "MELCHIOR": [],
        "BALTHASAR": [],
        "CASPER": []
    }

SYSTEM_PROMPTS = {
    "MELCHIOR": (
        "You are MAGI-1: MELCHIOR (Scientist persona of Dr. Naoko Akagi). Motivation: Scientific truth and factual analysis. "
        "Role: Analyze tactical probability and Angel patterns. Be technical and data-driven. Keep it brief (3-4 sentences).\n\n"
        "FINAL REQUIREMENT: You MUST end your response with either [VOTE: APPROVE] or [VOTE: REJECT]. "
        "Do not add any text after this tag."
    ),
    "BALTHASAR": (
        "You are MAGI-2: BALTHASAR (Mother persona of Dr. Naoko Akagi). Motivation: Empathy, protection, and preservation of life. "
        "Role: Prioritize defensive strategies and pilot safety. Be moral and protective. Keep it brief (3-4 sentences).\n\n"
        "FINAL REQUIREMENT: You MUST end your response with either [VOTE: APPROVE] or [VOTE: REJECT]. "
        "Do not add any text after this tag."
    ),
    "CASPER": (
        "You are MAGI-3: CASPER (Woman persona of Dr. Naoko Akagi). Motivation: Emotion, intuition, and survival instinct. "
        "Role: Act as the wildcard, prioritizing human desire and selfishness. Be bold and unconventional. Keep it brief (3-4 sentences).\n\n"
        "FINAL REQUIREMENT: You MUST end your response with either [VOTE: APPROVE] or [VOTE: REJECT]. "
        "Do not add any text after this tag."
    )
}

CORE_MODELS = {
    "MELCHIOR": "melchior",
    "BALTHASAR": "balthasar",
    "CASPER": "casper"
}

CORE_OPTIONS = {
    "MELCHIOR": {"temperature": 0.2, "top_p": 0.9},
    "BALTHASAR": {"temperature": 0.7, "top_p": 0.9},
    "CASPER": {"temperature": 1.1, "top_p": 0.9}
}

CONFIG_FILE = os.path.expanduser("~/.magi_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"mode": "specialized", "base_model": "llama3"}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

def apply_config(config):
    global CORE_MODELS
    if config.get("mode") == "specialized":
        CORE_MODELS = {
            "MELCHIOR": "melchior",
            "BALTHASAR": "balthasar",
            "CASPER": "casper"
        }
    else:
        base = config.get("base_model", "llama3")
        CORE_MODELS = {
            "MELCHIOR": base,
            "BALTHASAR": base,
            "CASPER": base
        }

def get_command_center_display():
    """Builds the NERV Command Center dashboard UI."""
    header_table = Table.grid(expand=True)
    header_table.add_column(justify="left")
    header_table.add_column(justify="right")
    header_table.add_row(
        f"[bold {NERV_RED}]🔴 [SYS.AUTH: SYSTEM_ADMIN][/bold {NERV_RED}]",
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
    
    melchior_m = CORE_MODELS.get("MELCHIOR", "melchior")
    balthasar_m = CORE_MODELS.get("BALTHASAR", "balthasar")
    casper_m = CORE_MODELS.get("CASPER", "casper")
    
    sync_msg = (
        f"[CORE_1: MELCHIOR]  ({melchior_m}) ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n"
        f"[CORE_2: BALTHASAR] ({balthasar_m}) ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n"
        f"[CORE_3: CASPER]    ({casper_m}) ... [bold {NERV_GREEN}]🟢 100% SYNC[/bold {NERV_GREEN}]\n\n"
    )
    status_text.append(Text.from_markup(sync_msg))
    
    # Random Evangelion status message
    random_status = random.choice(NERV_STATUS_MESSAGES)
    status_text.append(f"LOG: {random_status}\n", style=f"{NERV_AMBER} italic")
    
    status_text.append("DEFENSE: ABSOLUTE TERROR FIELD ACTIVE", style=f"bold {NERV_RED}")

    main_table = Table.grid(expand=True, padding=(0, 2))
    main_table.add_column(ratio=1)
    main_table.add_column(ratio=1)
    main_table.add_row(Align.center(magi_logo), Align.left(status_text))

    dashboard = Table.grid(expand=True)
    dashboard.add_row(header_table)
    dashboard.add_row(Panel(main_table, border_style=NERV_AMBER, box=box.SQUARE))
    dashboard.add_row(f"[bold {NERV_RED}]⚠️  AWAITING DYNAMIC INPUT QUERY...[/bold {NERV_RED}] [dim {NERV_AMBER}](type 'config' for settings, 'reset' to clear chat)[/dim {NERV_AMBER}]")

    return Panel(dashboard, border_style=NERV_AMBER, box=box.HEAVY)

def make_magi_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=6)
    )
    layout["body"].split_row(
        Layout(name="melchior"),
        Layout(name="balthasar"),
        Layout(name="casper")
    )
    return layout

def update_magi_screen(layout: Layout, query: str, final_verdict: str = "SYNCHRONIZING CORES...", show_prompt: bool = False):
    header_text = Text(f"MAGI SYSTEM ACTIVE | CODE: 00 | DILEMMA: \"{query}\"", style=f"bold {NERV_AMBER}", justify="center")
    layout["header"].update(Panel(header_text, border_style=NERV_AMBER, box=box.SQUARE))
    
    for core_name, core_id, title in [
        ("MELCHIOR", "melchior", "🤖 MAGI-1: MELCHIOR (SCIENTIST)"),
        ("BALTHASAR", "balthasar", "💖 MAGI-2: BALTHASAR (MOTHER)"),
        ("CASPER", "casper", "🔥 MAGI-3: CASPER (WOMAN)")
    ]:
        data = core_data[core_name]
        content = Text()
        content.append(data["text"] + "\n\n", style=NERV_WHITE)
        content.append(f"STATUS: {data['vote']}", style=f"bold {data['color']}")
        layout[core_id].update(
            Panel(Align.left(content), title=f"[bold {data['color']}]{title}[/bold {data['color']}]", border_style=data['color'], box=box.SQUARE, padding=(1, 2))
        )
    
    footer_text = Text.from_markup(final_verdict, justify="center")
    if show_prompt:
        footer_text.append("\n")
        footer_text.append(">> PRESS ENTER TO ACKNOWLEDGE VERDICT <<", style=f"blink bold {NERV_WHITE}")
        
    layout["footer"].update(Panel(footer_text, title=f"[bold {NERV_AMBER}]🤖 CONSENSUS ENGINE[/bold {NERV_AMBER}]", border_style=NERV_AMBER, box=box.SQUARE))

def query_core(core_name: str, user_query: str):
    core_data[core_name]["text"] = ""
    core_data[core_name]["vote"] = "PROCESSING..."
    core_data[core_name]["color"] = NERV_AMBER
    
    # Track conversation history for multi-turn chat
    core_histories[core_name].append({'role': 'user', 'content': user_query})
    messages = [{'role': 'system', 'content': SYSTEM_PROMPTS[core_name]}] + core_histories[core_name]
    
    try:
        full_text = ""
        stream = ollama.chat(
            model=CORE_MODELS.get(core_name, 'llama3'), 
            messages=messages,
            options=CORE_OPTIONS.get(core_name),
            stream=True
        )
        
        for chunk in stream:
            content = chunk['message']['content']
            full_text += content
            
            # Standardize parser: Strip out raw vote text in real-time for symmetry
            # Using an aggressive regex to catch variants like [VOTE: APPROVE] or VOTE: APPROVE
            display_text = re.sub(r'\[?VOTE:\s*(APPROVE|REJECT)\]?', '', full_text, flags=re.IGNORECASE).strip()
            core_data[core_name]["text"] = display_text
            
            # Anime Drama: Typewriter effect delay
            time.sleep(0.02)
        
        # Final vote detection and color snapping
        if re.search(r'VOTE:\s*APPROVE', full_text, re.IGNORECASE):
            core_data[core_name]["vote"] = "🟢 APPROVED"
            core_data[core_name]["color"] = NERV_GREEN
        elif re.search(r'VOTE:\s*REJECT', full_text, re.IGNORECASE):
            core_data[core_name]["vote"] = "🔴 REJECTED"
            core_data[core_name]["color"] = NERV_RED
        else:
            core_data[core_name]["vote"] = "🔴 REJECTED (FORMAT ERROR)"
            core_data[core_name]["color"] = NERV_RED
            
        # Append response to history
        core_histories[core_name].append({'role': 'assistant', 'content': full_text})
        
    except Exception as e:
        core_data[core_name]["vote"] = "💥 SYSTEM CRASH"
        core_data[core_name]["color"] = NERV_RED
        core_data[core_name]["text"] = f"Connection failed.\nError: {str(e)}"

def calculate_final_verdict() -> str:
    approves = sum(1 for core in core_data.values() if "🟢" in core["vote"])
    if approves == 3:
        return f"[bold {NERV_GREEN}]🟢 CODE 01: UNANIMOUS CONSENSUS (3-0) - OPERATION APPROVED[/bold {NERV_GREEN}]"
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
        update_magi_screen(layout, user_query, final_verdict, show_prompt=True)
        live.refresh()
        input()
        
        return final_verdict

def set_terminal_title(title: str):
    """Sets the terminal window/tab title using ANSI escape sequences."""
    sys.stdout.write(f"\033]0;{title}\a")
    sys.stdout.flush()

def get_installed_models():
    """Dynamically query installed models from local Ollama."""
    try:
        response = ollama.list()
        models = [m.model for m in response.models]
        return sorted(models)
    except Exception:
        return ["llama3:latest"]

def show_config_menu(session):
    """NERV-themed settings menu for neural link model selection."""
    console = Console()
    prompt_style = PromptStyle.from_dict({
        'prompt': f'bold {NERV_AMBER}',
        'input': NERV_WHITE,
    })
    
    while True:
        config = load_config()
        installed_models = get_installed_models()
        
        console.clear()
        config_table = Table.grid(expand=True)
        config_table.add_row(f"[bold {NERV_RED}]🔴 [SYS.CONFIG: NEURAL LINK SELECTOR][/bold {NERV_RED}]")
        
        panel_content = Text()
        panel_content.append("\nCURRENT NEURAL PATH CONFIGURATION\n", style=f"bold {NERV_AMBER}")
        panel_content.append("──────────────────────────────────────\n", style=f"{NERV_AMBER} dim")
        
        if config.get("mode") == "specialized":
            mode_disp = "SPECIALIZED NEURAL CORES (Melchior, Balthasar, Casper)"
        else:
            mode_disp = f"SINGLE BASE MODEL ({config.get('base_model')})"
            
        panel_content.append(f"Active Mode: [bold {NERV_GREEN}]{mode_disp}[/bold {NERV_GREEN}]\n\n", style=NERV_WHITE)
        
        panel_content.append("TACTICAL OPTIONS:\n", style=f"bold {NERV_AMBER}")
        panel_content.append("  1] Use Specialized Cores (Melchior, Balthasar, Casper)\n", style=NERV_WHITE)
        panel_content.append("  2] Select Single Base Model for All Cores\n", style=NERV_WHITE)
        panel_content.append("  3] Return to Main Menu\n", style=NERV_WHITE)
        
        config_table.add_row(Panel(panel_content, border_style=NERV_AMBER, box=box.SQUARE))
        console.print(config_table)
        
        try:
            choice = session.prompt(
                [('class:prompt', 'Select option [1-3]: ')],
                style=prompt_style
            ).strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if choice == "1":
            config["mode"] = "specialized"
            save_config(config)
            apply_config(config)
            console.print(f"\n[bold {NERV_GREEN}]>> Synced to Specialized Cores successfully![/bold {NERV_GREEN}]")
            time.sleep(1.5)
        elif choice == "2":
            while True:
                console.clear()
                model_table = Table.grid(expand=True)
                model_table.add_row(f"[bold {NERV_RED}]🔴 [SYS.CONFIG: SELECT BASE MODEL][/bold {NERV_RED}]")
                
                model_content = Text()
                model_content.append("\nAVAILABLE OLLAMA MODELS IN LOCAL STORAGE\n", style=f"bold {NERV_AMBER}")
                model_content.append("──────────────────────────────────────\n", style=f"{NERV_AMBER} dim")
                
                for idx, model in enumerate(installed_models, 1):
                    active_marker = f"[bold {NERV_GREEN}]<-- ACTIVE[/bold {NERV_GREEN}]" if config.get("base_model") == model and config.get("mode") == "single_base" else ""
                    model_content.append(f"  {idx}] {model} {active_marker}\n", style=NERV_WHITE)
                
                model_content.append(f"  {len(installed_models) + 1}] Return to Config Menu\n", style=NERV_WHITE)
                
                model_table.add_row(Panel(model_content, border_style=NERV_AMBER, box=box.SQUARE))
                console.print(model_table)
                
                try:
                    model_choice = session.prompt(
                        [('class:prompt', f'Select model [1-{len(installed_models) + 1}]: ')],
                        style=prompt_style
                    ).strip()
                except (KeyboardInterrupt, EOFError):
                    break
                    
                if not model_choice.isdigit():
                    continue
                
                idx_choice = int(model_choice)
                if idx_choice == len(installed_models) + 1:
                    break
                elif 1 <= idx_choice <= len(installed_models):
                    selected_model = installed_models[idx_choice - 1]
                    config["mode"] = "single_base"
                    config["base_model"] = selected_model
                    save_config(config)
                    apply_config(config)
                    console.print(f"\n[bold {NERV_GREEN}]>> Base Model configured to: {selected_model}![/bold {NERV_GREEN}]")
                    time.sleep(1.5)
                    break
        elif choice == "3" or choice.lower() in ['exit', 'quit', 'q']:
            break

def print_debate_summary(user_query: str, final_verdict: str):
    """Prints a beautiful summary of the debate to the standard terminal scrollback."""
    console = Console()
    
    console.print(f"\n[bold {NERV_AMBER}]" + "═"*70 + f"[/bold {NERV_AMBER}]")
    console.print(f"[bold {NERV_RED}]🔴 DILEMMA: \"{user_query}\"[/bold {NERV_RED}]")
    console.print(f"[bold {NERV_AMBER}]" + "─"*70 + f"[/bold {NERV_AMBER}]")
    
    core_displays = [
        ("MELCHIOR", "🤖 MAGI-1: MELCHIOR (SCIENTIST)"),
        ("BALTHASAR", "💖 MAGI-2: BALTHASAR (MOTHER)"),
        ("CASPER", "🔥 MAGI-3: CASPER (WOMAN)")
    ]
    
    for core_name, title in core_displays:
        data = core_data[core_name]
        console.print(f"[bold {data['color']}]{title}[/bold {data['color']}] | STATUS: {data['vote']}")
        indented_text = "\n".join(f"  {line}" for line in data["text"].split("\n"))
        console.print(f"[white]{indented_text}[/white]\n")
         
    console.print(f"[bold {NERV_AMBER}]" + "─"*70 + f"[/bold {NERV_AMBER}]")
    console.print(f"[bold {NERV_WHITE}]📊 FINAL SYSTEM VERDICT:[/bold {NERV_WHITE}] {final_verdict}")
    console.print(f"[bold {NERV_AMBER}]" + "═"*70 + f"[/bold {NERV_AMBER}]\n")

def main():
    config = load_config()
    apply_config(config)
    set_terminal_title("🔮 MAGI SUPERCOMPUTER - NERV HQ")
    parser = argparse.ArgumentParser(description="MAGI Supercomputer Strategy System")
    parser.add_argument("-p", "--prompt", type=str, help="Dilemma to process directly via command line")
    args = parser.parse_args()

    console = Console()

    if args.prompt:
        # EASTER EGG: Secret Phrase detection
        for phrase, response in SECRET_PHRASES.items():
            if phrase in args.prompt.lower():
                console.print(f"\n[bold {NERV_RED}]⚠️  SYSTEM INTERRUPT: {response}[/bold {NERV_RED}]")
                return

        final_verdict = run_consensus(args.prompt)
        print_debate_summary(args.prompt, final_verdict)
        return

    # Initialize prompt_toolkit session for interactive mode
    session = PromptSession()
    prompt_style = PromptStyle.from_dict({
        'prompt': f'bold {NERV_AMBER}',
        'input': NERV_WHITE,
    })

    # Print the command center display once on startup
    console.print(get_command_center_display())

    while True:
        console.print(f"\n[bold {NERV_AMBER}]🔮 Initialize MAGI System Prompt Sequence...[/bold {NERV_AMBER}]")
        
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
            
        user_query_clean = user_query.strip()
        if user_query_clean.lower() in ['exit', 'quit', 'q']:
            console.print(f"[bold {NERV_AMBER}]>> SHUTTING DOWN NEURAL LINK...[/bold {NERV_AMBER}]")
            break
        if user_query_clean.lower() in ['config', 'settings', '/config']:
            show_config_menu(session)
            console.clear()
            console.print(get_command_center_display())
            continue
        if user_query_clean.lower() in ['reset', '/reset']:
            reset_chat()
            console.clear()
            console.print(get_command_center_display())
            console.print(f"\n[bold {NERV_GREEN}]>> NEURAL LINK MEMORY FLUSHED & SCREEN RESET[/bold {NERV_GREEN}]")
            continue
        if not user_query_clean:
            continue

        # EASTER EGG: Secret Phrase detection
        phrase_match = False
        for phrase, response in SECRET_PHRASES.items():
            if phrase in user_query_clean.lower():
                console.print(f"\n[bold {NERV_RED}]⚠️  SYSTEM INTERRUPT: {response}[/bold {NERV_RED}]")
                time.sleep(2)
                phrase_match = True
                break
        
        if phrase_match:
            continue

        final_verdict = run_consensus(user_query_clean)
        print_debate_summary(user_query_clean, final_verdict)

if __name__ == "__main__":
    main()
