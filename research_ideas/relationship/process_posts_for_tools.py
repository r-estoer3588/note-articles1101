import csv
import re
import os
from datetime import datetime, timedelta

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "600_posts_schedule.csv")
BUFFER_OUTPUT_FILE = os.path.join(BASE_DIR, "buffer_import.csv")
IMAGE_PROMPT_FILE = os.path.join(BASE_DIR, "image_generation_prompt.txt")

START_DATE = datetime(2025, 11, 22) # Starting tomorrow

def clean_text_for_buffer(content):
    # Extract body part
    if "【本文】" in content:
        parts = content.split("【本文】")
        body = parts[1].strip()
    else:
        body = content.strip()
    
    # Replace （改行） with actual newlines for tap inducement
    # Usually 3-5 lines are good for "See more"
    body = body.replace("（改行）", "\n\n\n")
    
    # Remove other internal markers if any
    body = re.sub(r'【.*?】', '', body) # Remove any other bracketed headers left
    
    return body.strip()

def extract_image_text(day, time, content):
    if "【画像文字案】" not in content:
        return None
    
    try:
        # Extract text between markers
        match = re.search(r'【画像文字案】\n(.*?)\n\n【本文】', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    except:
        pass
    return None

def main():
    print(f"Reading from {INPUT_FILE}...")
    
    buffer_rows = []
    image_items = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            day = int(row['Day'])
            time_str = row['Time']
            content = row['Content']
            
            # 1. Prepare Buffer Data
            # Calculate date
            post_date = START_DATE + timedelta(days=day-1)
            date_str = post_date.strftime('%Y-%m-%d')
            
            # Clean body
            clean_body = clean_text_for_buffer(content)
            
            # Buffer CSV format usually: Date, Time, Text
            # Or just Text if bulk importing to queue, but let's provide Date/Time for completeness
            buffer_rows.append({
                "Date": date_str,
                "Time": time_str,
                "Text": clean_body
            })
            
            # 2. Prepare Image Data
            img_text = extract_image_text(day, time_str, content)
            if img_text:
                image_items.append(f"Day {day} [{time_str}]\n{img_text}\n")

    # Write Buffer CSV
    print(f"Writing Buffer CSV to {BUFFER_OUTPUT_FILE}...")
    with open(BUFFER_OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        # Buffer Bulk Import often expects just the text, or specific columns.
        # We will provide a standard format: Date, Time, Text
        writer = csv.DictWriter(f, fieldnames=["Date", "Time", "Text"])
        writer.writeheader()
        writer.writerows(buffer_rows)

    # Write Image Prompt Text
    print(f"Writing Image Prompt to {IMAGE_PROMPT_FILE}...")
    with open(IMAGE_PROMPT_FILE, 'w', encoding='utf-8') as f:
        f.write("以下はThreads投稿用の画像に入れる文字案のリストです。\n")
        f.write("これらを元に、Canva等で画像を作成するための構成案を考えてください。\n\n")
        f.write("-" * 20 + "\n")
        for item in image_items:
            f.write(item + "\n" + "-" * 20 + "\n")

    print("Done.")

if __name__ == "__main__":
    main()
