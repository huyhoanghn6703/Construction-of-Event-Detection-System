import os
import json
import time
from tqdm import tqdm
import logging
import argparse
import pyperclip
import sys
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('event_classification.log'),
        logging.StreamHandler()
    ]
)

def extract_event_type(label_text):
    """Extract event type from label text."""
    label_text = label_text.upper()
    if "POLICY" in label_text:
        return "Policy-Announcement"
    elif "LEADER" in label_text:
        return "Leader-Activity"
    elif "EMERGENCY" in label_text:
        return "Emergency-Event"
    return None

def load_json(json_path):
    """Load JSON data from a file."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        logging.error(f"Error loading JSON: {str(e)}")
        return []

def save_json(json_path, data):
    """Save JSON data to a file."""
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error saving JSON: {str(e)}")

def flatten_events(data):
    """
    Flatten all news events into a list of items to classify.
    """
    flattened = []
    counter = 0
    for item in data:
        if isinstance(item, dict) and "content" in item:
            # Only add items that don't have an event_type or have an empty one
            if "event_type" not in item or not item["event_type"]:
                flattened.append({
                    "global_index": counter,
                    "doc_id": item.get("doc_id", ""),
                    "content": item["content"],
                    "date": item.get("date", "")
                })
                counter += 1
    return flattened

def restore_events(data, flattened):
    """
    Write back each labeled event's type into the original data structure.
    """
    for item in flattened:
        doc_id = item["doc_id"]
        event_type = item.get("event_type")
        if event_type:
            # Find matching item in original data
            for original_item in data:
                if original_item.get("doc_id") == doc_id:
                    original_item["event_type"] = event_type
                    break

def get_user_input_immediate(chunk, all_items, auto_copy=True):
    """
    Get user input for event classification.
    """
    prompt = (
        "Classify each news event as one of:\n"
        "- Policy-Announcement (PA)\n"
        "- Leader-Activity (LA)\n"
        "- Emergency-Event (EE)\n"
        "Reply in format: INDEX: <EVENT-TYPE>\n\n"
    )
    
    for item in chunk:
        prompt += f"Event {item['global_index']}: {item['content']}\n"

    print("\n=== PROMPT TO COPY (if needed) ===")
    print(prompt)
    print("===================================")
    
    if auto_copy:
        try:
            pyperclip.copy(prompt)
            print("\nPrompt copied to clipboard!")
        except:
            print("\nFailed to copy to clipboard")

    print("\nEnter classifications as 'INDEX: <EVENT-TYPE>'")
    print("Type 'done' when finished, or 'exit' to abort.\n")
    
    needed_indices = {it["global_index"] for it in chunk}
    new_labels = {}

    while needed_indices:
        user_line = input("Classification > ").strip()
        if user_line.lower() == 'done':
            if needed_indices:
                print(f"Still missing indices: {needed_indices}")
                continue
            else:
                break
        elif user_line.lower() == 'exit':
            print("Aborting this chunk...")
            break
        
        parts = user_line.split(":")
        if len(parts) == 2:
            idx_str, label = parts[0].strip(), parts[1].strip()
            event_type = None
            
            # Handle shorthand and full format
            if "PA" in label.upper():
                event_type = "Policy-Announcement"
            elif "LA" in label.upper():
                event_type = "Leader-Activity"
            elif "EE" in label.upper():
                event_type = "Emergency-Event"
            
            if event_type:
                try:
                    real_idx = int(idx_str.replace('Event', '').strip())
                    if real_idx in needed_indices:
                        new_labels[real_idx] = event_type
                        needed_indices.remove(real_idx)
                    else:
                        print(f"Index {real_idx} not in current chunk.")
                except ValueError:
                    print(f"Could not parse index '{idx_str}', please try again.")
            else:
                print("Invalid event type. Use PA, LA, or EE.")
        else:
            print("Invalid format. Use 'INDEX: <EVENT-TYPE>'")

    # Apply all new labels
    for idx, event_type in new_labels.items():
        for item in chunk:
            if item["global_index"] == idx:
                item["event_type"] = event_type

    return len(new_labels)

def manual_classify(flattened, chunk_size=10, auto_copy=True):
    """Manual classification logic."""
    idx = 0
    with tqdm(total=len(flattened), desc="Processing events") as pbar:
        while idx < len(flattened):
            chunk = flattened[idx:idx+chunk_size]
            processed = get_user_input_immediate(chunk, flattened, auto_copy=auto_copy)
            pbar.update(len(chunk))
            logging.info(f"Processed {processed}/{len(chunk)} events in chunk")
            idx += chunk_size

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=str, help="Path to the JSON file to process")
    parser.add_argument("-c", "--chunk_size", type=int, default=100, help="Chunk size for processing")
    parser.add_argument("--no-auto-copy", action="store_true", help="Disable auto-copy to clipboard")
    args = parser.parse_args()

    # Load data
    json_path = args.json_path
    logging.info(f"Loading JSON from {json_path}")
    data = load_json(json_path)

    # Flatten events
    flattened = flatten_events(data)
    if not flattened:
        logging.info("No unlabeled events found.")
        return

    # Backup original
    backup_path = json_path.replace(".json", "_backup.json")
    logging.info(f"Backing up to {backup_path}")
    save_json(backup_path, data)

    # Classify - always using manual mode
    manual_classify(flattened, chunk_size=args.chunk_size, auto_copy=not args.no_auto_copy)

    # Write back results
    restore_events(data, flattened)
    save_json(json_path, data)
    logging.info("Classification completed and saved.")


if __name__ == "__main__":
    main()