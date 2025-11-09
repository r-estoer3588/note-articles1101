#!/usr/bin/env python3
"""
学習スクリプトのラッパー：進捗をLINE push通知
"""
import subprocess
import sys
import re
import os
import requests
from pathlib import Path

# 環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_USER_ID = os.environ.get('LINE_USER_ID', '')  # 管理者のLINE USER ID

def send_line_push(user_id: str, message: str):
    """LINE push メッセージ送信"""
    if not LINE_CHANNEL_ACCESS_TOKEN or not user_id:
        print(f"[SKIP PUSH] {message}")
        return
    
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[PUSH ERROR] {e}")


def main():
    """学習スクリプト実行 + 進捗通知"""
    # 引数をそのまま渡す（--learn --input ...）
    cmd = [
        sys.executable,
        str(Path(__file__).parent / 'hogey_algorithm.py')
    ] + sys.argv[1:]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    
    # リアルタイム出力で進捗監視
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    last_progress = -1
    total_steps = 0
    
    for line in iter(proc.stdout.readline, ''):
        line = line.rstrip()
        print(line)  # 標準出力にも流す
        
        # PROGRESS:XX:TOTAL 形式を検出
        match = re.match(r'PROGRESS:(\d+):(\d+)', line)
        if match:
            current_pct = int(match.group(1))
            total_steps = int(match.group(2))
            
            # 10%刻みで通知（または重要なマイルストーン）
            if current_pct % 20 == 0 and current_pct != last_progress:
                msg = f"🎓 学習進捗: {current_pct}%\n処理中: {total_steps}件"
                send_line_push(LINE_USER_ID, msg)
                last_progress = current_pct
    
    proc.wait()
    exit_code = proc.returncode
    
    if exit_code == 0:
        send_line_push(LINE_USER_ID, "✅ 学習が完了しました！\n次回の投稿生成から新しいパターンが反映されます。")
    else:
        send_line_push(LINE_USER_ID, f"❌ 学習に失敗しました（終了コード: {exit_code}）")
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
