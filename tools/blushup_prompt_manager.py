#!/usr/bin/env python3
"""
BlushUp Prompt Manager - プロンプト品質向上ツール

GitHub Copilot Chatで使う品質向上プロンプトを辞書管理し、
選択したプロンプトを@workspace付きでクリップボードにコピーします。

使い方:
    python blushup_prompt_manager.py
    python blushup_prompt_manager.py --list
    python blushup_prompt_manager.py --show 1
"""

import argparse
import sys

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# 品質向上プロンプト辞書
QUALITY_PROMPTS = {
    "1": {
        "name": "品質担保",
        "description": "細かいことでも全て質問",
        "prompt": """【品質担保】
回答の品質を極限まで上げるために、必要な情報はどんな細かいことでも必ず全て質問してください。"""
    },
    "2": {
        "name": "前提確認",
        "description": "解釈を箇条書きで確認",
        "prompt": """【前提確認】
回答を生成する前に、あなたがこのタスクを遂行するために設定した前提条件や解釈を箇条書きで提示し、私の認識と合っているか確認してください。"""
    },
    "3": {
        "name": "チェックリスト",
        "description": "見落とし指摘",
        "prompt": """【チェックリスト】
このタスクを進める上で、私が提示した情報以外に、通常考慮すべき（しかし言及されていない）重要な論点や必要なデータがあれば、それを指摘し、質問してください。"""
    },
    "4": {
        "name": "自己評価",
        "description": "尋ねるべきだった質問",
        "prompt": """【自己評価】
今の回答の品質を10倍にするために、あなたは私に【尋ねるべきだった】質問を、重要度の高い順に3つ挙げてください。"""
    },
    "5": {
        "name": "全部盛り",
        "description": "品質担保+前提確認+チェックリスト",
        "prompt": """【品質担保】
回答の品質を極限まで上げるために、必要な情報はどんな細かいことでも必ず全て質問してください。

【前提確認】
回答を生成する前に、あなたがこのタスクを遂行するために設定した前提条件や解釈を箇条書きで提示し、私の認識と合っているか確認してください。

【チェックリスト】
このタスクを進める上で、私が提示した情報以外に、通常考慮すべき（しかし言及されていない）重要な論点や必要なデータがあれば、それを指摘し、質問してください。"""
    }
}


def list_prompts():
    """プロンプト一覧を表示"""
    print("\n📋 プロンプト品質向上ツール\n")
    print("利用可能なプロンプト:\n")
    for key in sorted(QUALITY_PROMPTS.keys()):
        item = QUALITY_PROMPTS[key]
        print(f"  {key}. {item['name']:12} - {item['description']}")
    print()


def show_prompt(number: str):
    """指定されたプロンプトを表示"""
    if number not in QUALITY_PROMPTS:
        print(f"❌ プロンプト番号 '{number}' が見つかりません")
        return False
    
    item = QUALITY_PROMPTS[number]
    print(f"\n{'='*60}")
    print(f"📝 {item['name']} - {item['description']}")
    print(f"{'='*60}\n")
    print(item['prompt'])
    print(f"\n{'='*60}\n")
    return True


def copy_to_clipboard(text: str) -> bool:
    """クリップボードにコピー"""
    if not CLIPBOARD_AVAILABLE:
        print("\n⚠️  pyperclip が利用できません")
        print("   pip install pyperclip を実行してください")
        return False
    
    try:
        # @workspace を自動付与
        copilot_ready = f"@workspace\n\n{text}"
        pyperclip.copy(copilot_ready)
        return True
    except Exception as e:
        print(f"\n❌ クリップボードへのコピーに失敗: {e}")
        return False


def interactive_menu():
    """対話モード"""
    print("\n" + "="*60)
    print("📋 プロンプト品質向上ツール")
    print("="*60 + "\n")
    
    print("どのプロンプトを使いますか？\n")
    for key in sorted(QUALITY_PROMPTS.keys()):
        item = QUALITY_PROMPTS[key]
        print(f"  {key}. {item['name']:12} - {item['description']}")
    
    print(f"\n  q. 終了")
    print()
    
    while True:
        choice = input("番号を選択 (1-5, q): ").strip()
        
        if choice.lower() == 'q':
            print("\n👋 終了します")
            return
        
        if choice not in QUALITY_PROMPTS:
            print("❌ 無効な番号です。もう一度入力してください。")
            continue
        
        item = QUALITY_PROMPTS[choice]
        prompt_text = item['prompt']
        
        print(f"\n{'='*60}")
        print(f"📝 {item['name']}")
        print(f"{'='*60}\n")
        print(prompt_text)
        print(f"\n{'='*60}\n")
        
        if copy_to_clipboard(prompt_text):
            print("✅ クリップボードにコピーしました！")
            print("   (@workspace 付きで GitHub Copilot Chat に貼り付けられます)\n")
        else:
            print("\n📋 上記のプロンプトを手動でコピーしてください\n")
        
        # 続けるか確認
        another = input("別のプロンプトを選択しますか？ (y/n): ").strip().lower()
        if another != 'y':
            print("\n👋 終了します")
            return
        
        print()  # 改行


def main():
    parser = argparse.ArgumentParser(
        description="BlushUp Prompt Manager - プロンプト品質向上ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python blushup_prompt_manager.py              # 対話モード
  python blushup_prompt_manager.py --list       # プロンプト一覧
  python blushup_prompt_manager.py --show 1     # プロンプト表示＆コピー
  python blushup_prompt_manager.py --show 5     # 全部盛りをコピー
        """
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='利用可能なプロンプト一覧を表示'
    )
    
    parser.add_argument(
        '--show',
        metavar='NUMBER',
        type=str,
        help='指定されたプロンプトを表示してクリップボードにコピー'
    )
    
    args = parser.parse_args()
    
    # オプション処理
    if args.list:
        list_prompts()
        return 0
    
    if args.show:
        if not show_prompt(args.show):
            return 1
        if copy_to_clipboard(QUALITY_PROMPTS[args.show]['prompt']):
            print("✅ クリップボードにコピーしました！")
            print("   (@workspace 付きで GitHub Copilot Chat に貼り付けられます)\n")
        return 0
    
    # デフォルト: 対話モード
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\n👋 中断されました")
        return 130
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
