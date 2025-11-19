import re
import csv
import random
from datetime import datetime, timedelta

import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "600_posts_schedule.csv")
MASTER_IDEAS_FILE = os.path.join(BASE_DIR, "master_ideas.md")
WEEK1_FILE = os.path.join(BASE_DIR, "week1_posts_draft.md")

# Templates for daily posts (Day 8+)
# Placeholders: {title}, {raw_text}, {insight}, {hook_threads}, {hook_note}, {category}, {phase}
TEMPLATES = {
    1: { # 07:00 本気(共感)
        "type": "本気(共感)",
        "time": "07:00",
        "image_text": "{title}\n{insight_short}",
        "body": "{hook_threads}\n\n（改行）\n\n{raw_text_short}\n{insight}\n私の実体験はプロフの固定投稿へ。\n#{category} #{phase}"
    },
    2: { # 08:00 軽め(挨拶)
        "type": "軽め(挨拶)",
        "time": "08:00",
        "body": "おはようございます。\n{title}について、ふと考えました。\n今日も無理せずいきましょう。"
    },
    3: { # 10:00 軽め(問)
        "type": "軽め(問)",
        "time": "10:00",
        "body": "【質問】\n{title}、感じたことありますか？\n\n（改行）\n\n正直に教えてください🙋‍♀️"
    },
    4: { # 12:00 本気(解決)
        "type": "本気(解決)",
        "time": "12:00",
        "image_text": "{insight_short}\nそれが\n解決の鍵。",
        "body": "{insight}\n\n（改行）\n\n{hook_note}\n具体的な方法はNoteで公開中。\n#{category} #解決策"
    },
    5: { # 15:00 軽め(共感)
        "type": "軽め(共感)",
        "time": "15:00",
        "body": "{raw_text_short}\nこれ、あるあるですよね。\n共感したら「いいね」お願いします。"
    },
    6: { # 17:00 軽め(一言)
        "type": "軽め(一言)",
        "time": "17:00",
        "body": "夕方のこの時間、ふと思います。\n{insight_short}\n小さな変化が大事です。"
    },
    7: { # 20:00 本気(誘導)
        "type": "本気(誘導)",
        "time": "20:00",
        "image_text": "{title}\n諦めないで。\nまだ間に合う。",
        "body": "{title}。\nその悩みを抱えているあなたへ。\n\n（改行）\n\n{hook_note}\n解決のための「3つのステップ」をNoteにまとめました。\n▼記事はプロフのリンクから\n#夜専用レス手前の会話レシピ"
    },
    8: { # 21:00 軽め(夜)
        "type": "軽め(夜)",
        "time": "21:00",
        "body": "夜のリビング。\n{raw_text_short}\n同じ気持ちの人、いますか？"
    },
    9: { # 22:00 軽め(夜)
        "type": "軽め(夜)",
        "time": "22:00",
        "body": "今日もお疲れ様でした。\n{insight_short}\nおやすみなさい。"
    },
    10: { # 23:00 軽め(〆)
        "type": "軽め(〆)",
        "time": "23:00",
        "body": "明日は今日より少しだけ、心が軽くなりますように。\nプロフの固定投稿もぜひ。\nおやすみなさい。"
    }
}

def parse_master_ideas(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    ideas = []
    # Split by "## R" to find idea blocks
    blocks = re.split(r'^## R', content, flags=re.MULTILINE)
    
    for block in blocks:
        if not block.strip():
            continue
        
        # Re-add "R" to the ID
        lines = block.strip().split('\n')
        header = lines[0]
        if ':' not in header:
            continue
            
        idea_id = "R" + header.split(':')[0].strip()
        title = header.split(':', 1)[1].strip()
        
        # Extract fields
        phase = re.search(r'- フェーズ\s*:\s*(.*)', block)
        category = re.search(r'- カテゴリ\s*:\s*(.*)', block)
        raw_text_match = re.search(r'### 悩みの生テキスト\n(.*?)(?=###|$)', block, re.DOTALL)
        insight_match = re.search(r'### インサイトメモ\n(.*?)(?=###|$)', block, re.DOTALL)
        hook_threads_match = re.search(r'- Threads用:\s*(.*)', block)
        hook_note_match = re.search(r'- note用\s*:\s*(.*)', block)
        
        raw_text = raw_text_match.group(1).strip() if raw_text_match else ""
        # Clean up list markers
        raw_text = re.sub(r'^-\s*', '', raw_text, flags=re.MULTILINE).replace('\n', ' ')
        
        insight = insight_match.group(1).strip() if insight_match else ""
        insight = re.sub(r'^-\s*', '', insight, flags=re.MULTILINE).replace('\n', ' ')
        
        idea = {
            "id": idea_id,
            "title": title,
            "phase": phase.group(1).strip() if phase else "",
            "category": category.group(1).strip() if category else "",
            "raw_text": raw_text,
            "raw_text_short": raw_text[:40] + "..." if len(raw_text) > 40 else raw_text,
            "insight": insight,
            "insight_short": insight[:20] + "..." if len(insight) > 20 else insight,
            "hook_threads": hook_threads_match.group(1).strip() if hook_threads_match else title,
            "hook_note": hook_note_match.group(1).strip() if hook_note_match else title
        }
        ideas.append(idea)
        
    return ideas

def parse_week1_draft(file_path):
    posts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by Day
    days = re.split(r'^## Day', content, flags=re.MULTILINE)
    
    for day_block in days:
        if not day_block.strip():
            continue
            
        day_num_match = re.match(r'\s*(\d+):', day_block)
        if not day_num_match:
            continue
        day_num = int(day_num_match.group(1))
        
        # Find table rows
        rows = re.findall(r'\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', day_block)
        
        for row in rows:
            no, p_type, time, content_text = row
            # Clean content text (remove <br>, bold markers)
            clean_content = content_text.replace('<br>', '\n').replace('**', '')
            
            posts.append({
                "Day": day_num,
                "No": no.strip(),
                "Type": p_type.strip(),
                "Time": time.strip(),
                "Content": clean_content.strip()
            })
            
    return posts

def generate_posts(ideas, start_day=8, end_day=60):
    generated_posts = []
    idea_count = len(ideas)
    
    for day in range(start_day, end_day + 1):
        # Cycle through ideas
        idea_index = (day - start_day) % idea_count
        idea = ideas[idea_index]
        
        for slot_num in range(1, 11):
            template = TEMPLATES[slot_num]
            
            # Fill template
            content = template["body"].format(**idea)
            image_text = template.get("image_text", "").format(**idea)
            
            full_content = ""
            if image_text:
                full_content += f"【画像文字案】\n{image_text}\n\n【本文】\n"
            full_content += content
            
            generated_posts.append({
                "Day": day,
                "No": slot_num,
                "Type": template["type"],
                "Time": template["time"],
                "Content": full_content
            })
            
    return generated_posts

def main():
    print("Parsing Master Ideas...")
    ideas = parse_master_ideas(MASTER_IDEAS_FILE)
    print(f"Found {len(ideas)} ideas.")
    
    print("Parsing Week 1 Draft...")
    week1_posts = parse_week1_draft(WEEK1_FILE)
    print(f"Found {len(week1_posts)} posts for Week 1.")
    
    print("Generating remaining posts (Day 8-60)...")
    # Filter out ideas used in Week 1 if possible, or just use all
    # Week 1 used R010-R016. Let's start from R017 for Day 8
    
    # Reorder ideas to start from R017
    start_idea_id = "R017"
    start_index = 0
    for i, idea in enumerate(ideas):
        if idea["id"] == start_idea_id:
            start_index = i
            break
            
    ordered_ideas = ideas[start_index:] + ideas[:start_index]
    
    remaining_posts = generate_posts(ordered_ideas, start_day=8, end_day=60)
    
    all_posts = week1_posts + remaining_posts
    
    print(f"Total posts: {len(all_posts)}")
    
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Day", "No", "Type", "Time", "Content"])
        writer.writeheader()
        writer.writerows(all_posts)
        
    print("Done.")

if __name__ == "__main__":
    main()
