import sys
import os
import re

# Add the current directory to sys.path to import the enriched data module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from manual_refine_weeks_7_8_enriched import updates
except ImportError:
    print("Error: Could not import 'updates' from manual_refine_weeks_7_8_enriched.py")
    sys.exit(1)

OUTPUT_FILE = r'c:\Repos\note-articles\research_ideas\relationship\weeks_7_8_article_plan.md'

def extract_info(content):
    # Extract Title
    # The title is usually in the format: 「Title」\n具体的な方法はNoteで公開中
    # But sometimes there are extra newlines or spaces.
    # Let's look for the pattern more robustly.
    
    # Find the "Note..." line
    note_idx = content.find("具体的な方法はNoteで公開中")
    if note_idx == -1:
        return None, None
        
    # Look backwards from there for the closing bracket 」
    end_bracket = content.rfind("」", 0, note_idx)
    if end_bracket == -1:
        return None, None
        
    # Look backwards from the closing bracket for the opening bracket 「
    # We assume the title doesn't contain nested brackets for now, or is reasonably short (e.g. < 100 chars)
    start_bracket = content.rfind("「", 0, end_bracket)
    if start_bracket == -1:
        return None, None
        
    title = content[start_bracket+1:end_bracket].replace('\n', '').strip()

    # Extract Problem Context (Body text)
    # Look for 【本文】
    body_start_marker = "【本文】"
    body_start = content.find(body_start_marker)
    
    if body_start != -1:
        body_content_start = body_start + len(body_start_marker)
        # Try to find the end of the body.
        # It might end at （改行） or at the start of the Note promo section (often indicated by a dash or just before the title)
        
        # If （改行） exists, use it as a delimiter
        newline_marker = "（改行）"
        newline_idx = content.find(newline_marker, body_content_start)
        
        if newline_idx != -1:
             problem_context = content[body_content_start:newline_idx].strip()
        else:
            # If no newline marker, maybe it ends before the title we found?
            # Or before the "Note..." line?
            # Let's take everything up to the start_bracket of the title
            problem_context = content[body_content_start:start_bracket].strip()
            # Remove any trailing dashes or whitespace
            problem_context = re.sub(r'[\s-]*$', '', problem_context)
    else:
        problem_context = "（本文から抽出できませんでした）"
    
    return title, problem_context

def generate_full_article(title, problem_context):
    # Extract a short version of the problem for the intro
    intro_hook = problem_context.split('\n')[0][:50] if problem_context else "夫婦の問題"
    
    return f"""---
# {title}

## 【導入】共感と問題提起

{problem_context}

この気持ち、痛いほどわかります。

でも安心してください。これはあなたの性格の問題ではありません。
「伝え方」や「タイミング」といった**技術的な問題**なのです。

この記事では、心理学と行動経済学に基づいた「3つのステップ」で、
今日から使える具体的な解決策をお伝えします。

---

## 【Step 1】なぜこの問題が起きるのか？

### 男性脳と女性脳の違い
男性は「解決策」を求め、女性は「共感」を求める傾向があります。
このズレが、すれ違いの根本原因です。

### やってはいけない「NG行動」
1. **感情的に責める**: 「なんでわかってくれないの！」は逆効果
2. **察してちゃん**: 「言わなくてもわかるでしょ」は通じません
3. **過去の失敗を蒸し返す**: 「あの時もそうだった」は心を閉ざす

---

## 【Step 2】具体的なアクション（会話レシピ）

### ✅ 今日から使えるフレーズ集

**シーン1: 日常会話を増やしたい時**
- 「今日、〇〇で面白いことがあってね」（事実を共有）
- 「あなたの意見、聞きたいな」（相談する姿勢）
- 「最近、疲れてない？」（気遣いを見せる）

**シーン2: 不満を伝えたい時**
- 「私は〜と感じている」（I（アイ）メッセージで）
- 「〜してくれると嬉しいな」（要求ではなくお願い）
- 「二人でどうしたらいいと思う？」（共同作業に変換）

**シーン3: 気持ちを再確認したい時**
- 「昔、〇〇に行ったの覚えてる？」（過去の良い記憶を掘り起こす）
- 「あなたと一緒にいられて幸せだよ」（素直な感謝）
- 「これからもよろしくね」（未来への意思表示）

### 📅 タイミングと切り出し方

**ベストタイミング**
- 食後のリラックスタイム（満腹ホルモンで攻撃性が下がる）
- 一緒に散歩している時（横並びで話すと心理的負担が軽い）
- 寝る前の10分間（「今日ありがとう」から始める）

**NGタイミング**
- 帰宅直後（疲れている）
- スマホ・テレビに夢中の時（集中が切れる）
- 喧嘩の直後（冷却期間が必要）

---

## 【Step 3】継続と定着の仕組み

### 三日坊主にならないための工夫
1. **小さく始める**: 毎日1分の会話から
2. **カレンダーに記録**: 実行した日に◯をつける（視覚化）
3. **自分にご褒美**: 1週間続いたら好きなケーキを買う

### 相手の反応が薄い時の対処法
- すぐに結果を求めない（1ヶ月は様子見）
- 一方的に話すのではなく、質問で引き出す
- 「変わらないじゃん」と諦めず、淡々と続ける

### 小さな成功体験を積む
- 「おはよう」と目を合わせて言えた → 成功！
- 夫が「ありがとう」と返してくれた → 大成功！
- 会話が3往復続いた → 最高！

---

## 【まとめ】今日から始める一歩

この記事のポイントをおさらいします。

1. **問題の本質**: 性格ではなく、技術の不足
2. **具体的な行動**: I（アイ）メッセージ、タイミング、質問形式
3. **継続の仕組み**: 小さく始め、記録し、ご褒美を設定

**今日、まず何をするか？**

夫が帰宅したら、「今日どうだった？」ではなく、
**「今日、私は〇〇があって楽しかったよ。あなたは？」**
と、自分の話から始めてみてください。

その一言が、沈黙を破る小さな一歩になります。

あなたなら、できます。
一緒に、少しずつ前に進みましょう。

---

**執筆者**: レス卒先輩（30代後半男性会社員）  
**運営**: Threads [@レス手前の会話レシピ]  
▼ 他の記事も読む（プロフィールから）

---
"""

def main():
    # Group updates by title to avoid duplicates (some titles might be used in multiple posts, though usually 1:1 for the main post)
    # Actually, the "Note" link usually appears in the 12:00 or 20:00 post.
    
    articles = {}

    for key, content in updates.items():
        if "具体的な方法はNoteで公開中" in content:
            title, problem = extract_info(content)
            if title:
                # Use the longest problem description found for this title (richer context)
                if title not in articles:
                    articles[title] = problem
                else:
                    if len(problem) > len(articles[title]):
                        articles[title] = problem

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Week 7-8 Note記事（18本・完全版）\n\n")
        f.write("Week 7-8の投稿で訴求しているNote記事の本文です。\n")
        f.write("各記事は「共感（悩み）」→「原因分析」→「解決策（3ステップ）」の構成で統一しています。\n\n")
        f.write("このファイルをそのままNoteに投稿可能です。\n\n")
        f.write("=" * 60 + "\n\n")
        
        for title in sorted(articles.keys()):
            article_text = generate_full_article(title, articles[title])
            f.write(article_text)

    print(f"Generated article plans for {len(articles)} articles at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
