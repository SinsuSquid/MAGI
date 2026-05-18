import threading
import re
import ollama
from config import SYSTEM_PROMPTS, CORE_MODELS

def parse_vote(text):
    """Robustly parse the vote from the text."""
    if "[VOTE: APPROVE]" in text:
        return "APPROVE"
    if "[VOTE: REJECT]" in text:
        return "REJECT"
    match = re.search(r'\[VOTE:\s*(APPROVE|REJECT)\]', text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "REJECT"

def query_core(core_name, prompt, core_data):
    """Worker function to query a single MAGI core and update shared data."""
    try:
        core_data[core_name]["text"] = "Calculating neural pathways..."
        response = ollama.chat(
            model=CORE_MODELS.get(core_name, 'llama3'),
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPTS[core_name]},
                {'role': 'user', 'content': prompt}
            ]
        )
        full_text = response['message']['content']
        vote = parse_vote(full_text)
        
        # Clean the text for display (remove the vote instruction)
        clean_text = re.sub(r'\[VOTE:.*?\]', '', full_text).strip()
        
        core_data[core_name]["text"] = clean_text
        core_data[core_name]["vote"] = vote
    except Exception as e:
        core_data[core_name]["text"] = f"CORE ERROR: {str(e)}"
        core_data[core_name]["vote"] = "REJECT"

def broadcast_dilemma(dilemma, core_data):
    """Spawns parallel threads to query the MAGI cores."""
    threads = []
    for core in SYSTEM_PROMPTS.keys():
        t = threading.Thread(target=query_core, args=(core, dilemma, core_data))
        threads.append(t)
        t.start()
    return threads
