#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SNSマネタイズプラン生成ツール

STEP1: 対話型で現状を深掘り
STEP2: カスタマイズされた包括的マネタイズプランを生成
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


# カラー出力
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text):
    """ヘッダー出力"""
    print(f"\n{Color.HEADER}{Color.BOLD}{'=' * 60}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{text}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{'=' * 60}{Color.END}\n")


def print_question(number, text):
    """質問出力"""
    print(f"\n{Color.CYAN}{Color.BOLD}【質問 {number}】{Color.END}")
    print(f"{Color.CYAN}{text}{Color.END}")


def print_success(text):
    """成功メッセージ"""
    print(f"{Color.GREEN}✓ {text}{Color.END}")


def print_info(text):
    """情報メッセージ"""
    print(f"{Color.BLUE}ℹ {text}{Color.END}")


def print_warning(text):
    """警告メッセージ"""
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")


def print_error(text):
    """エラーメッセージ"""
    print(f"{Color.RED}✗ {text}{Color.END}")


# STEP1: 質問リスト
STEP1_QUESTIONS = {
    "1": {
        "title": "現在の状況",
        "questions": [
            "職業・年齢・居住地を教えてください",
            "現在の月収はいくらですか？",
            "理想の月収はいくらですか？",
            "SNS運用歴を教えてください（どのプラットフォームで、どれくらいの期間）",
            "現在のフォロワー数を教えてください（各SNS）"
        ]
    },
    "2": {
        "title": "スキル・経験の棚卸し",
        "questions": [
            "仕事で培ったスキルを具体的に教えてください",
            "趣味や特技は何ですか？",
            "「これなら3時間語れる」というテーマは何ですか？",
            "過去に成功した経験や実績を教えてください",
            "人から相談されることが多いことは何ですか？"
        ]
    },
    "3": {
        "title": "リソース確認",
        "questions": [
            "SNSに使える時間は1日何時間ですか？",
            "初期投資可能額はいくらですか？（0円〜10万円程度）",
            "協力者はいますか？（家族、友人、ビジネスパートナー）",
            "すでに持っているコンテンツ資産はありますか？（ブログ、note、動画など）"
        ]
    },
    "4": {
        "title": "目標とマインド",
        "questions": [
            "3ヶ月後にどうなっていたいですか？",
            "1年後に月何万円稼ぎたいですか？",
            "やりたくないことは何ですか？（顔出しNG、DM営業NGなど）",
            "譲れない価値観は何ですか？"
        ]
    },
    "5": {
        "title": "過去の失敗・課題",
        "questions": [
            "これまでSNSで挫折した経験はありますか？",
            "続かなかった理由は何ですか？",
            "「これがネックで動けない」という障害は何ですか？"
        ]
    }
}


def collect_step1_data():
    """STEP1: 対話型で情報収集"""
    print_header("🎯 STEP1: 現状の深掘り分析")
    print_info("あなたの状況を深く理解するため、5つのカテゴリに分けて質問します")
    print_info("質問は一つずつ進めますので、じっくり考えて回答してください\n")
    
    all_answers = {}
    
    for category_num, category_data in STEP1_QUESTIONS.items():
        print_header(f"📋 カテゴリ {category_num}: {category_data['title']}")
        
        category_answers = []
        for i, question in enumerate(category_data['questions'], 1):
            print_question(f"{category_num}-{i}", question)
            answer = input(f"{Color.BOLD}回答 > {Color.END}").strip()
            
            if not answer:
                print_warning("空の回答です。スキップしますか？ (y/n)")
                skip = input("> ").strip().lower()
                if skip == 'y':
                    answer = "[未回答]"
                else:
                    answer = input(f"{Color.BOLD}回答 > {Color.END}").strip()
            
            category_answers.append({
                "question": question,
                "answer": answer
            })
            print_success("回答を記録しました")
        
        all_answers[category_num] = {
            "title": category_data['title'],
            "answers": category_answers
        }
        
        print_success(f"✓ カテゴリ {category_num} 完了")
    
    return all_answers


def save_answers(answers, output_dir="outputs/monetize"):
    """回答をJSONファイルに保存"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_path / f"step1_answers_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)
    
    return filename


def generate_prompt_from_answers(answers):
    """回答からSTEP2用のプロンプトを生成"""
    prompt = """あなたは10年以上のSNSマーケティング経験を持つ戦略コンサルタントです。
私の人生を変える、本気のSNSマネタイズプランを設計してください。

【STEP1で収集した私の情報】

"""
    
    for category_num, category_data in answers.items():
        prompt += f"■ {category_data['title']}\n\n"
        for qa in category_data['answers']:
            prompt += f"Q: {qa['question']}\n"
            prompt += f"A: {qa['answer']}\n\n"
    
    prompt += """
【STEP2: 戦略設計】
上記の回答をもとに、以下の形式で包括的なマネタイズプランを作成してください。

■ あなたの最強ポジション分析
- 市場価値が高いスキルTOP3
- 競合が少ない独自の強み
- マネタイズしやすい切り口
- 「この人といえば◯◯」と言われるポジション提案

■ ターゲット顧客の明確化
- 最も刺さる顧客像(ペルソナ)
- その人が抱える悩みTOP5
- その人が月にいくら使えるか(課金余力)
- その人がよく見るSNSプラットフォーム

■ SNS戦略(プラットフォーム別)
各プラットフォームの役割を明確に:

【メインSNS(濃い発信)】
- プラットフォーム名:
- 発信テーマ:
- 投稿頻度:
- フォロワー◯人達成までの期間:

【サブSNS(導線)】
- プラットフォーム名:
- 使い方:
- 導線設計:

【マネタイズ先(最終的な収益化)】
- プラットフォーム名:
- 何を売るか:
- 単価:

■ マネタイズ戦略(複数案提示)
以下の3つのマネタイズ方法を具体的に提案:

【即金型(30日以内に収益)】
- 方法:
- 想定収益:月◯万円
- 必要なアクション:

【積み上げ型(3〜6ヶ月で安定収益)】
- 方法:
- 想定収益:月◯万円
- 必要なアクション:

【資産型(6ヶ月〜1年で不労所得化)】
- 方法:
- 想定収益:月◯万円
- 必要なアクション:

■ 90日実行プラン
【1ヶ月目:土台作り】
Week1:
- やること(具体的なタスク5個)
- 達成目標:

Week2:
- やること
- 達成目標:

Week3:
- やること
- 達成目標:

Week4:
- やること
- 達成目標:
- 1ヶ月目の成果指標:フォロワー◯人、収益◯円

【2ヶ月目:加速】
Week1:
- やること(具体的なタスク5個)
- 達成目標:

Week2:
- やること
- 達成目標:

Week3:
- やること
- 達成目標:

Week4:
- やること
- 達成目標:
- 2ヶ月目の成果指標:フォロワー◯人、収益◯円

【3ヶ月目:収益化本格化】
Week1:
- やること(具体的なタスク5個)
- 達成目標:

Week2:
- やること
- 達成目標:

Week3:
- やること
- 達成目標:

Week4:
- やること
- 達成目標:
- 3ヶ月目の成果指標:フォロワー◯人、収益◯万円

■ コンテンツ戦略
【バズる投稿テンプレート3選】
1. [タイトル]:投稿の型と具体例
2. [タイトル]:投稿の型と具体例
3. [タイトル]:投稿の型と具体例

【ストック型コンテンツ】
- 作るべきコンテンツ10本
- それぞれの役割と使い方

■ 収益目標とKPI
【1ヶ月目】
- フォロワー目標:◯人
- エンゲージメント率:◯%
- 収益目標:◯円
- 達成のための必須アクション:

【3ヶ月目】
- フォロワー目標:◯人
- 収益目標:◯万円
- 達成のための必須アクション:

【6ヶ月目】
- フォロワー目標:◯人
- 収益目標:◯万円
- 達成のための必須アクション:

■ よくある失敗と回避策
1. [失敗パターン]→[回避策]
2. [失敗パターン]→[回避策]
3. [失敗パターン]→[回避策]

■ リスクヘッジ戦略
- プラン通りいかない場合のプランB
- モチベーションが下がった時の対処法
- 炎上リスクの回避方法

■ あなた専用の成功の方程式
「◯◯(あなたの強み)× ◯◯(ターゲットの悩み)× ◯◯(SNS戦略)= 月◯◯万円」

■ 最初の一歩(今日やること)
1. [タスク1]
2. [タスク2]
3. [タスク3]

【出力の条件】
- 抽象論NG。全て具体的な数字と行動レベルで
- 「〜すると良い」ではなく「〜する」と断言
- 再現性重視。誰がやっても結果が出る設計
- 「これなら自分でもできる」と思える難易度
- 1万文字以上の超具体的プラン
- 途中で手を抜かず、最後まで本気で設計
- 「この人、本気で私の人生変えようとしてくれてる」と思える熱量

【重要】
このプランはテンプレートではなく、私の状況に100%カスタマイズしてください。
私の強み・経験・リソースを最大限活かし、最短距離で結果を出せる戦略を。
人生を変える覚悟で、本気のプランをお願いします。
"""
    
    return prompt


def generate_plan_with_openai(prompt):
    """OpenAI APIでプラン生成"""
    if not OPENAI_AVAILABLE:
        print_error("openaiパッケージがインストールされていません")
        return None
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print_error("OPENAI_API_KEYが設定されていません")
        return None
    
    print_info("OpenAI APIでプラン生成中...")
    print_info("これには数分かかる場合があります...")
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "あなたは10年以上のSNSマーケティング経験を持つ戦略コンサルタントです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        plan = response.choices[0].message.content
        print_success("プラン生成完了！")
        return plan
    
    except Exception as e:
        print_error(f"API呼び出しエラー: {e}")
        return None


def save_plan(plan, output_dir="outputs/monetize"):
    """生成されたプランを保存"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_path / f"monetize_plan_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# SNSマネタイズプラン\n\n")
        f.write(f"生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(plan)
    
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="SNSマネタイズプラン生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python monetize_planner.py              # 対話型で質問に答える
  python monetize_planner.py --api        # OpenAI APIでプラン自動生成
  python monetize_planner.py --load data.json --api  # 保存済み回答からプラン生成

出力:
  outputs/monetize/step1_answers_YYYYMMDD_HHMMSS.json  # 回答データ
  outputs/monetize/monetize_plan_YYYYMMDD_HHMMSS.md   # 生成されたプラン
        """
    )
    
    parser.add_argument(
        '--api',
        action='store_true',
        help='OpenAI APIでプラン自動生成（OPENAI_API_KEY必須）'
    )
    
    parser.add_argument(
        '--load',
        type=str,
        metavar='FILE',
        help='保存済みの回答JSONファイルを読み込む'
    )
    
    parser.add_argument(
        '--prompt-only',
        action='store_true',
        help='プロンプトのみ生成してクリップボードにコピー'
    )
    
    args = parser.parse_args()
    
    # ロゴ表示
    print_header("💰 SNSマネタイズプラン生成ツール")
    print_info("あなたの人生を変える、本気のマネタイズプランを設計します\n")
    
    # 回答の収集または読み込み
    if args.load:
        print_info(f"回答を読み込み中: {args.load}")
        with open(args.load, 'r', encoding='utf-8') as f:
            answers = json.load(f)
        print_success("回答を読み込みました")
    else:
        answers = collect_step1_data()
        
        # 回答を保存
        saved_file = save_answers(answers)
        print_success(f"回答を保存しました: {saved_file}")
    
    # プロンプト生成
    print_header("📝 STEP2: プロンプト生成")
    prompt = generate_prompt_from_answers(answers)
    
    # プロンプトを保存
    output_dir = Path("outputs/monetize")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_file = output_dir / f"prompt_{timestamp}.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print_success(f"プロンプトを保存しました: {prompt_file}")
    
    # クリップボードにコピー
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(prompt)
            print_success("プロンプトをクリップボードにコピーしました")
        except:
            print_warning("クリップボードへのコピーに失敗しました")
    
    if args.prompt_only:
        print_info("\nプロンプトのみモード: このプロンプトをGitHub Copilot Chatに貼り付けてください")
        return
    
    # API生成
    if args.api:
        print_header("🤖 STEP3: AIによるプラン生成")
        plan = generate_plan_with_openai(prompt)
        
        if plan:
            plan_file = save_plan(plan)
            print_success(f"プランを保存しました: {plan_file}")
            
            print_header("✨ 完了")
            print_success("マネタイズプランの生成が完了しました！")
            print_info(f"📄 プラン: {plan_file}")
        else:
            print_warning("\nAPI生成に失敗しました")
            print_info("プロンプトは保存されているので、GitHub Copilot Chatで使用できます")
    else:
        print_header("✨ STEP1完了")
        print_success("質問への回答が完了しました！")
        print_info(f"📄 プロンプト: {prompt_file}")
        print_info("\n次のステップ:")
        print_info("1. GitHub Copilot Chatでプロンプトを使用")
        print_info("2. または --api オプションで自動生成")
        print_info(f"\n   python monetize_planner.py --load {saved_file} --api")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\n中断されました")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
