import pandas as pd
import os
import requests
import time
import argparse

# Configuration
SCHEDULE_FILE = (
    r"c:\Repos\note-articles\research_ideas\relationship\600_posts_schedule.csv"
)
ENV_FILE = r"c:\Repos\note-articles\tools\.env"


def load_env():
    """Load environment variables from .env file manually"""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def get_openai_api_key():
    return os.environ.get("openai_API")


def call_llm_rewrite(current_content, post_type, time_slot, day):
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OpenAI API Key not found in .env")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_prompt = """
あなたは「30代後半の既婚男性、レス解消経験者」として、Threads（スレッズ）で発信しています。
以下の「既存の投稿案」を、より読者の感情を揺さぶる、具体的で映像が浮かぶ文章にリライトしてください。

【リライトのルール】
1. **「分析メモ」を「語り」に変える**: 箇条書きや「〜という問題」といった硬い表現は禁止。語りかける口調で。
2. **映像喚起**: 「スマホのブルーライト」「冷めた味噌汁」「背中」など、具体的な情景描写を入れる。
3. **短く、鋭く**: Threadsなので、長すぎないこと（最大500文字程度、改行を効果的に使う）。
4. **タイプに合わせる**:
   - 「本気」系: 深い共感、少し長めでもOK。
   - 「軽め」系: 一言で刺す、または日常のふとした気づき。単なる挨拶（おはよう）で終わらせない。
5. **文脈**: Day {day} の投稿です。この日のテーマに沿った内容にしてください。

【出力形式】
リライトした本文のみを出力してください。余計な解説は不要です。
""".format(day=day)

    user_prompt = f"""
【時間】{time_slot}
【タイプ】{post_type}
【現在の内容】
{current_content}

この投稿を、上記のルールに従って「詰め」てください。
特に「軽め」の投稿でも、単なる挨拶ではなく、読者の心に少し爪痕を残すような内容にしてください。
"""

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 429:
            print("Rate limit hit. Waiting 20 seconds...")
            time.sleep(20)
            # Retry once
            response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return current_content  # Return original if failed


def main():
    load_env()
    parser = argparse.ArgumentParser(
        description="Refine relationship posts using LLM"
    )
    parser.add_argument(
        '--days',
        type=str,
        default="1-7",
        help="Range of days to process (e.g., 1-7)"
    )
    args = parser.parse_args()

    start_day, end_day = map(int, args.days.split('-'))

    print(f"Loading schedule from {SCHEDULE_FILE}...")
    df = pd.read_csv(SCHEDULE_FILE)

    # Filter rows
    mask = (df['Day'] >= start_day) & (df['Day'] <= end_day)
    target_rows = df[mask]

    print(
        f"Found {len(target_rows)} posts to refine "
        f"(Day {start_day} to {end_day})."
    )

    for index, row in target_rows.iterrows():
        print(f"Processing Day {row['Day']} - {row['Time']} ({row['Type']})...")

        original_content = row['Content']
        new_content = call_llm_rewrite(
            original_content, row['Type'], row['Time'], row['Day']
        )

        # Update DataFrame
        df.at[index, 'Content'] = new_content

        # Sleep briefly to avoid rate limits
        time.sleep(1)

    # Save back to CSV
    print("Saving updated schedule...")
    df.to_csv(SCHEDULE_FILE, index=False, encoding='utf-8-sig')
    print("Done!")


if __name__ == "__main__":
    main()
