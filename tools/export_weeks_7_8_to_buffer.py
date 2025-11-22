import csv
import re
import sys
import os
from datetime import datetime, timedelta

# Add the current directory to sys.path to allow importing the data file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from manual_refine_weeks_7_8_enriched import updates
except ImportError:
    # Fallback if running from root
    sys.path.append(os.path.join(os.getcwd(), 'tools'))
    from manual_refine_weeks_7_8_enriched import updates

def parse_post_content(raw_text):
    """
    Extracts the body text from the raw post content.
    Removes '【画像文字案】' sections and keeps '【本文】'.
    """
    body_match = re.search(r'【本文】\n(.*)', raw_text, re.DOTALL)
    if body_match:
        content = body_match.group(1).strip()
    else:
        content = raw_text.strip()
    
    # Clean up common markers
    content = content.replace('（改行）', '\n')
    
    return content


def generate_csv(start_date_str="2025-11-15"):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    output_file = os.path.join("outputs", "weeks_7_8_buffer_import.csv")
    
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    
    rows = []
    
    # Sort keys to ensure chronological order
    sorted_keys = sorted(
        updates.keys(),
        key=lambda x: (int(x.split('_')[0][3:]), x.split('_')[1])
    )
    
    print(
        f"Processing {len(sorted_keys)} posts starting from Day 43 "
        f"({start_date_str})..."
    )
    
    for key in sorted_keys:
        # Key format: Day43_07:00
        day_str, time_str = key.split('_')
        day_num = int(day_str[3:])
        
        # Calculate date: Day 43 is the start date
        # So offset is day_num - 43
        offset = day_num - 43
        post_date = start_date + timedelta(days=offset)
        date_str = post_date.strftime("%Y-%m-%d")
        
        # Parse content
        raw_content = updates[key]
        post_text = parse_post_content(raw_content)
        
        # Generate image filename hint
        # Format: day43_0700.png
        image_filename = f"{day_str.lower()}_{time_str.replace(':', '')}.png"
        
        rows.append({
            "Date": date_str,
            "Time": time_str,
            "Text": post_text,
            "Image Filename": image_filename
        })
        
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Date", "Time", "Text", "Image Filename"]
        )
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Successfully exported {len(rows)} posts to {output_file}")


if __name__ == "__main__":
    # Default start date for Day 43
    # You can change this or add arg parsing if needed
    START_DATE = "2025-11-23"
    generate_csv(START_DATE)
