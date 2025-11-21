import csv
import os
import re

INPUT_FILE = r'c:\Repos\note-articles\research_ideas\relationship\600_posts_schedule.csv'
OUTPUT_FILE = r'c:\Repos\note-articles\outputs\weeks_7_8_image_generation_instruction.md'

def extract_image_text_and_body(content):
    if "【画像文字案】" not in content:
        return None, None
    
    try:
        img_match = re.search(r'【画像文字案】\n(.*?)\n\n【本文】', content, re.DOTALL)
        body_match = re.search(r'【本文】\n(.*?)$', content, re.DOTALL)
        
        img_text = img_match.group(1).strip() if img_match else ""
        body_text = body_match.group(1).strip() if body_match else ""
        
        # Truncate body for context
        body_text = body_text[:200] + "..." if len(body_text) > 200 else body_text
        
        return img_text, body_text
    except:
        return None, None

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Week 7-8 (Day 43-60) 画像生成用プロンプト指示書\n\n")
        f.write("以下のテキストは、Threads/Instagram投稿の「画像内の文字」と「本文の抜粋」です。\n")
        f.write("これらを元に、**Midjourney v6** 用のプロンプトを生成してください。\n\n")
        f.write("## プロンプト生成の条件\n")
        f.write("- **スタイル**: Photorealistic, Cinematic lighting, Emotional, 35mm film photography style\n")
        f.write("- **雰囲気**: 30代夫婦の「静かな危機」「孤独」「微かな希望」を表現\n")
        f.write("- **アスペクト比**: --ar 3:4\n")
        f.write("- **人物**: 日本人（Japanese）, 30s, 顔ははっきり見せない（背中、手元、横顔、シルエットなど）\n\n")
        f.write("--- \n\n")

        for row in rows:
            day = int(row['Day'])
            if 43 <= day <= 60:
                img_text, body_text = extract_image_text_and_body(row['Content'])
                if img_text:
                    f.write(f"### Day {day} {row['Time']}\n")
                    f.write(f"**画像内文字**:\n{img_text}\n\n")
                    f.write(f"**文脈（本文）**:\n{body_text}\n\n")
                    f.write(f"**推奨ビジュアルイメージ**:\n(ここにAIが考えた情景描写を入れる)\n\n")
                    f.write("---\n")

    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
