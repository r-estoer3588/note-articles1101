#!/usr/bin/env python3
"""
Gesuinu Prompt Manager - げすいぬ化記事改善ツール

既存の記事をげすいぬスタイル（月収30万円層向け）に変換します。
4つの成功指標（Trust/Empathy/Values/Encouragement）すべて4.0以上を目指します。
"""

import argparse
import sys
from pathlib import Path

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


def read_prompt_template():
    """げすいぬ化プロンプトテンプレートを読み込む"""
    prompt_path = Path(__file__).parent.parent / "prompt" / "article_quality_evaluation_prompt_v3_gesuinu.txt"
    
    if not prompt_path.exists():
        print(f"❌ プロンプトファイルが見つかりません: {prompt_path}")
        sys.exit(1)
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def read_article(file_path):
    """記事ファイルを読み込む"""
    article_path = Path(file_path)
    
    if not article_path.exists():
        print(f"❌ 記事ファイルが見つかりません: {file_path}")
        sys.exit(1)
    
    with open(article_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_improvement_prompt(article_content, evaluate_only=False):
    """記事改善用のプロンプトを生成"""
    template = read_prompt_template()
    
    if evaluate_only:
        mode_text = "評価のみ"
        instruction = """
以下の記事を「げすいぬらしさを保ちながら」4つの成功指標で評価してください。
改善案は不要です。評価テンプレートに従って採点してください。
"""
    else:
        mode_text = "評価 + 改善"
        instruction = """
以下の記事を「げすいぬらしさを保ちながら」4つの成功指標で評価し、すべて4点以上になるまで改善してください。

【げすいぬ版の評価基準】
1. 信頼構築: 4.0以上（データ出典、前提条件、自分の損失額開示）
2. 共感構築: 4.0以上（「俺」OK、「あなた」統一、読者攻撃NG、業界への毒OK）
3. 価値観共有: 4.0以上（執筆理念、構造+感情の業界批判）
4. 励まし: 4.0以上（所要時間、効果、「やらないと損」）

【改善方針】
- ✅ 「俺」はそのまま維持
- ✅ 「カモられた」も維持（自分の失敗談で）
- ✅ 業界への毒は維持（ただし根拠必須）
- ❌ 「お前ら」→「あなた」に変更
- ❌ 「バカ」「情弱」など読者攻撃は削除

【目標】
げすいぬらしい毒と生々しさを残しながら、読者を敵に回さない記事にする。
"""
    
    prompt = f"""@workspace 

{instruction}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【対象記事】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{article_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【評価基準の詳細】

{template}
"""
    
    return prompt, mode_text


def show_prompt_only():
    """プロンプトテンプレートのみを表示してコピー"""
    template = read_prompt_template()
    
    print("=" * 70)
    print("🐕 げすいぬ化プロンプト（評価基準）")
    print("=" * 70)
    print()
    print("以下の内容をクリップボードにコピーしました。")
    print("GitHub Copilot Chat に貼り付けて、記事を添付してください。")
    print()
    
    usage_prompt = f"""@workspace 

以下の記事を「げすいぬらしさを保ちながら」4つの成功指標で評価し、すべて4点以上になるまで改善してください。

【げすいぬ版の評価基準】
1. 信頼構築: 4.0以上（データ出典、前提条件、自分の損失額開示）
2. 共感構築: 4.0以上（「俺」OK、「あなた」統一、読者攻撃NG、業界への毒OK）
3. 価値観共有: 4.0以上（執筆理念、構造+感情の業界批判）
4. 励まし: 4.0以上（所要時間、効果、「やらないと損」）

【改善方針】
- ✅ 「俺」はそのまま維持
- ✅ 「カモられた」も維持（自分の失敗談で）
- ✅ 業界への毒は維持（ただし根拠必須）
- ❌ 「お前ら」→「あなた」に変更
- ❌ 「バカ」「情弱」など読者攻撃は削除

【目標】
げすいぬらしい毒と生々しさを残しながら、読者を敵に回さない記事にする。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【対象記事】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ここに記事を貼り付けてください]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【評価基準の詳細】

{template}
"""
    
    if HAS_PYPERCLIP:
        pyperclip.copy(usage_prompt)
        print("✅ クリップボードにコピーしました")
    else:
        print("⚠️  pyperclip がインストールされていないため、クリップボードにコピーできません")
        print("   以下をコピーしてください:")
        print()
        print(usage_prompt)
    
    print()
    print("💡 使い方:")
    print("   1. GitHub Copilot Chat を開く")
    print("   2. コピーしたプロンプトを貼り付け")
    print("   3. [ここに記事を貼り付けてください] の部分に記事を追加")
    print("   4. 送信して改善案を取得")
    print()


def interactive_mode():
    """対話モードで記事ファイルを選択"""
    print("=" * 70)
    print("🐕 Gesuinu - げすいぬ化記事改善ツール（対話モード）")
    print("=" * 70)
    print()
    print("【選択肢】")
    print("  1. 記事ファイルを指定してげすいぬ化（改善プロンプト生成）")
    print("  2. 記事ファイルを指定して評価のみ実行")
    print("  3. げすいぬ化プロンプトをクリップボードにコピー")
    print("  4. 終了")
    print()
    
    choice = input("選択してください (1-4): ").strip()
    
    if choice == "1":
        file_path = input("\n記事ファイルのパスを入力してください: ").strip()
        if file_path:
            process_article(file_path, evaluate_only=False)
    elif choice == "2":
        file_path = input("\n記事ファイルのパスを入力してください: ").strip()
        if file_path:
            process_article(file_path, evaluate_only=True)
    elif choice == "3":
        show_prompt_only()
    elif choice == "4":
        print("\n👋 終了します")
        sys.exit(0)
    else:
        print("\n❌ 無効な選択です")
        sys.exit(1)


def process_article(file_path, evaluate_only=False):
    """記事を処理してプロンプトを生成"""
    print()
    print("=" * 70)
    print(f"🐕 記事を処理中: {file_path}")
    print("=" * 70)
    print()
    
    # 記事を読み込み
    article_content = read_article(file_path)
    print(f"✅ 記事を読み込みました（{len(article_content)} 文字）")
    
    # プロンプト生成
    prompt, mode_text = generate_improvement_prompt(article_content, evaluate_only)
    print(f"✅ げすいぬ化プロンプトを生成しました（モード: {mode_text}）")
    print()
    
    # クリップボードにコピー
    if HAS_PYPERCLIP:
        pyperclip.copy(prompt)
        print("✅ プロンプトをクリップボードにコピーしました")
    else:
        print("⚠️  pyperclip がインストールされていないため、クリップボードにコピーできません")
        print("   以下をコピーしてください:")
        print()
        print(prompt)
    
    print()
    print("💡 次のステップ:")
    print("   1. GitHub Copilot Chat を開く")
    print("   2. クリップボードの内容を貼り付け（Ctrl+V）")
    print("   3. 送信して改善案を取得")
    print()
    print(f"📊 評価指標: 信頼/共感/価値観/励まし すべて 4.0以上 が目標")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="げすいぬ化記事改善ツール - 月収30万円層向けに記事を最適化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python gesuinu_prompt_manager.py                    # 対話モード
  python gesuinu_prompt_manager.py --show             # プロンプトをコピー
  python gesuinu_prompt_manager.py --file article.md  # 記事を改善
  python gesuinu_prompt_manager.py --file article.md --evaluate  # 評価のみ
        """
    )
    
    parser.add_argument("--show", action="store_true", help="げすいぬ化プロンプトを表示してコピー")
    parser.add_argument("--file", type=str, help="変換対象の記事ファイルパス")
    parser.add_argument("--evaluate", action="store_true", help="評価のみ実行（改善案なし）")
    
    args = parser.parse_args()
    
    if args.show:
        show_prompt_only()
    elif args.file:
        process_article(args.file, evaluate_only=args.evaluate)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
