import threading
import re
import time
import ollama
from config import SYSTEM_PROMPTS, CORE_MODELS

def parse_vote(text):
    """Robustly parse the vote from the text."""
    if re.search(r'VOTE:\s*APPROVE', text, re.IGNORECASE):
        return "APPROVE"
    if re.search(r'VOTE:\s*REJECT', text, re.IGNORECASE):
        return "REJECT"
    return "REJECT"

def query_core(core_name, prompt, core_data):
    """Worker function to query a single MAGI core and update shared data."""
    try:
        full_text = ""
        stream = ollama.chat(
            model=CORE_MODELS.get(core_name, 'llama3'),
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPTS[core_name]},
                {'role': 'user', 'content': prompt}
            ],
            stream=True
        )
        
        for chunk in stream:
            content = chunk['message']['content']
            full_text += content
            
            # Clean the text for display (remove the vote instruction)
            clean_text = re.sub(r'\[?VOTE:\s*(APPROVE|REJECT)\]?', '', full_text, flags=re.IGNORECASE).strip()
            
            core_data[core_name]["text"] = clean_text
            time.sleep(0.01) # Anime drama delay
            
        core_data[core_name]["vote"] = parse_vote(full_text)
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
