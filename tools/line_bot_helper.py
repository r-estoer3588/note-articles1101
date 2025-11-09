#!/usr/bin/env python3
"""
LINE Bot ヘルパー関数
n8nから呼び出されるユーティリティスクリプト
"""

import json
import sys
import csv
from datetime import datetime
from pathlib import Path

def get_progress_bar(current: int, total: int) -> str:
    """プログレスバーを生成"""
    filled = int((current / total) * 10)
    return '█' * filled + '░' * (10 - filled)

def format_post_message(post: dict, index: int, total: int) -> str:
    """投稿メッセージをフォーマット"""
    progress = get_progress_bar(index + 1, total)
    
    return f"""🐶 投稿{index + 1}/{total}
{progress}

{post['text']}

テーマ: {post.get('theme', '未設定')}
教育: {post.get('education_type', '未設定')}
テンプレ: {post.get('template_type', '未設定')}"""

def create_quick_reply_buttons(button_type: str) -> list:
    """クイックリプライボタンを生成"""
    
    if button_type == 'count':
        return [
            {'type': 'action', 'action': {'type': 'message', 'label': '3件', 'text': '3'}},
            {'type': 'action', 'action': {'type': 'message', 'label': '5件', 'text': '5'}},
            {'type': 'action', 'action': {'type': 'message', 'label': '10件', 'text': '10'}},
            {'type': 'action', 'action': {'type': 'message', 'label': '20件', 'text': '20'}}
        ]
    
    elif button_type == 'theme':
        themes = [
            {'emoji': '💰', 'name': '貧乏脱出'},
            {'emoji': '🎰', 'name': 'ギャンブル依存'},
            {'emoji': '💼', 'name': '副業'},
            {'emoji': '🏢', 'name': 'ブラック企業'},
            {'emoji': '💸', 'name': '無駄遣い'},
            {'emoji': '📱', 'name': 'SNS依存'},
            {'emoji': '😴', 'name': '疲労'},
            {'emoji': '👥', 'name': '人間関係'}
        ]
        return [
            {
                'type': 'action',
                'action': {
                    'type': 'message',
                    'label': f"{t['emoji']} {t['name']}",
                    'text': t['name']
                }
            }
            for t in themes
        ]
    
    elif button_type == 'post_actions':
        return [
            {'type': 'action', 'action': {'type': 'postback', 'label': '🚀 X投稿', 'data': 'action=post&index={index}'}},
            {'type': 'action', 'action': {'type': 'postback', 'label': '💾 保存', 'data': 'action=save&index={index}'}},
            {'type': 'action', 'action': {'type': 'postback', 'label': '➡️ 次へ', 'data': 'action=next&index={index}'}},
            {'type': 'action', 'action': {'type': 'message', 'label': '🗑️ 破棄', 'text': '破棄'}}
        ]
    
    return []

def read_csv_posts(csv_path: str) -> list:
    """CSVファイルから投稿データを読み込む"""
    posts = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append({
                'text': row['text'],
                'theme': row.get('theme', ''),
                'education_type': row.get('education_type', ''),
                'template_type': row.get('template_type', ''),
                'created_at': row.get('created_at', '')
            })
    
    return posts

def get_today_theme() -> str:
    """曜日別の今日のテーマを取得"""
    themes = {
        0: '時間の使い方',    # 月曜
        1: 'ギャンブル依存',  # 火曜
        2: 'ブラック企業',    # 水曜
        3: '無駄遣い',        # 木曜
        4: 'SNS依存',         # 金曜
        5: '疲労',            # 土曜
        6: '人間関係'         # 日曜
    }
    
    today = datetime.now().weekday()
    return themes.get(today, '時間の使い方')

def create_line_message(message_type: str, **kwargs) -> dict:
    """LINEメッセージを生成"""
    
    if message_type == 'count_selection':
        today_theme = kwargs.get('today_theme')
        text = f"📚 今日は「{today_theme}」のテーマです\n何件生成しますか？" if today_theme else "何件生成しますか？"
        
        return {
            'type': 'text',
            'text': text,
            'quickReply': {
                'items': create_quick_reply_buttons('count')
            }
        }
    
    elif message_type == 'theme_selection':
        return {
            'type': 'text',
            'text': 'テーマを選んでください',
            'quickReply': {
                'items': create_quick_reply_buttons('theme')
            }
        }
    
    elif message_type == 'loading':
        return {
            'type': 'text',
            'text': '⏳ 生成中です...\nしばらくお待ちください'
        }
    
    elif message_type == 'post_display':
        post = kwargs.get('post')
        index = kwargs.get('index', 0)
        total = kwargs.get('total', 1)
        
        buttons = create_quick_reply_buttons('post_actions')
        # インデックスを各ボタンに設定
        for btn in buttons:
            if btn['action']['type'] == 'postback':
                btn['action']['data'] = btn['action']['data'].format(index=index)
        
        return {
            'type': 'text',
            'text': format_post_message(post, index, total),
            'quickReply': {
                'items': buttons
            }
        }
    
    elif message_type == 'help':
        return {
            'type': 'text',
            'text': """🐶 ホゲーアルゴリズム使い方

【リッチメニュー】
📝 投稿生成: バズ投稿を作成
📖 3部作: ストーリー投稿作成
📚 今日: 今日のテーマで生成
🎓 学習: CSV学習実行
📊 状態: 現在の状況確認
❓ ヘルプ: このメッセージ

【投稿表示中】
🚀 X投稿: Xに即投稿
💾 保存: Sheetsに保存
➡️ 次へ: 次の投稿を表示
🗑️ 破棄: 破棄して終了

使い方:
1. リッチメニューをタップ
2. 件数/テーマを選択
3. 生成された投稿を確認
4. 投稿 or 保存を選択"""
        }
    
    elif message_type == 'error':
        error_msg = kwargs.get('error', 'エラーが発生しました')
        return {
            'type': 'text',
            'text': f'❌ {error_msg}\n\nメニューから再度選択してください。'
        }
    
    return {'type': 'text', 'text': 'メッセージ生成エラー'}

def main():
    """メインコマンド"""
    if len(sys.argv) < 2:
        print("Usage: python line_bot_helper.py <command> [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'today_theme':
        print(get_today_theme())
    
    elif command == 'format_post':
        if len(sys.argv) < 5:
            print("Usage: python line_bot_helper.py format_post <csv_path> <index> <total>")
            sys.exit(1)
        
        csv_path = sys.argv[2]
        index = int(sys.argv[3])
        total = int(sys.argv[4])
        
        posts = read_csv_posts(csv_path)
        if index < len(posts):
            message = create_line_message('post_display', post=posts[index], index=index, total=total)
            print(json.dumps(message, ensure_ascii=False))
    
    elif command == 'create_message':
        if len(sys.argv) < 3:
            print("Usage: python line_bot_helper.py create_message <message_type> [kwargs_json]")
            sys.exit(1)
        
        message_type = sys.argv[2]
        kwargs = {}
        if len(sys.argv) > 3:
            kwargs = json.loads(sys.argv[3])
        
        message = create_line_message(message_type, **kwargs)
        print(json.dumps(message, ensure_ascii=False))
    
    elif command == 'read_posts':
        if len(sys.argv) < 3:
            print("Usage: python line_bot_helper.py read_posts <csv_path>")
            sys.exit(1)
        
        csv_path = sys.argv[2]
        posts = read_csv_posts(csv_path)
        print(json.dumps(posts, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
