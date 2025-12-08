#!/usr/bin/env python3
"""
Threads API Token Generator - OAuth 2.0 Flow
シンプルなOAuthフローでThreads APIアクセストークンを生成

使用方法:
1. Meta Developersダッシュボードから App ID と App Secret を取得
2. このスクリプトを実行
3. ブラウザで認証
4. トークンが自動で.envに追加されます
"""

import http.server
import socketserver
import urllib.parse
import webbrowser
import requests
from pathlib import Path

# 設定
PORT = 8000
REDIRECT_URI = f"http://localhost:{PORT}/callback"
SCOPES = "threads_basic,threads_manage_insights"

# App IDとApp Secretを入力
print("=" * 60)
print("Threads API Token Generator")
print("=" * 60)
print("\nMeta Developersダッシュボードから以下を取得してください:")
print("https://developers.facebook.com/apps/")
print("→ アプリ「レス卒先輩分析ツール」→ 設定 → ベーシック\n")

APP_ID = input("Threads App ID: ").strip()
APP_SECRET = input("Threads App Secret: ").strip()

if not APP_ID or not APP_SECRET:
    print("❌ App IDとApp Secretが必要です")
    exit(1)

# OAuth認証URL
auth_url = (
    f"https://threads.net/oauth/authorize?"
    f"client_id={APP_ID}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    f"scope={SCOPES}&"
    f"response_type=code"
)

print(f"\n✅ 認証URLを生成しました")
print(
    f"\n📌 重要: Meta Developersダッシュボードで以下のリダイレクトURIを追加してください:"
)
print(f"   {REDIRECT_URI}")
print(f"\nアプリ設定 → Threads API → 設定 → OAuth リダイレクト URI")
print("\n続行するにはEnterキーを押してください...")
input()


# コールバックサーバー
class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        if self.path.startswith("/callback"):
            # 認証コードを取得
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if "code" in params:
                auth_code = params["code"][0]

                # 成功ページを表示
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    b"""
                <html>
                <head><title>Success</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: green;">&#10004; Authentication Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
                """
                )
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: No authorization code received")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # ログを抑制


auth_code = None

# ブラウザで認証URLを開く
print(f"\n🌐 ブラウザで認証ページを開きます...")
print(f"   レス卒先輩のThreadsアカウントでログインしてください\n")
webbrowser.open(auth_url)

# コールバックを待機
print("⏳ 認証完了を待っています...")
with socketserver.TCPServer(("", PORT), CallbackHandler) as httpd:
    httpd.handle_request()

if not auth_code:
    print("❌ 認証コードが取得できませんでした")
    exit(1)

print(f"\n✅ 認証コードを取得しました")

# アクセストークンを取得
print(f"🔄 アクセストークンを取得中...")
token_url = "https://graph.threads.net/oauth/access_token"
token_data = {
    "client_id": APP_ID,
    "client_secret": APP_SECRET,
    "code": auth_code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}

try:
    response = requests.post(token_url, data=token_data)
    response.raise_for_status()
    token_response = response.json()

    access_token = token_response.get("access_token")
    user_id = token_response.get("user_id")

    if not access_token or not user_id:
        print(f"❌ トークン取得失敗: {token_response}")
        exit(1)

    print(f"\n✅ アクセストークンを取得しました!")
    print(f"   User ID: {user_id}")
    print(f"   Token: {access_token[:20]}...")

    # .envファイルに追加
    env_file = Path(__file__).parent / ".env"

    with open(env_file, "a", encoding="utf-8") as f:
        f.write(f"\n\n# Threads API 認証情報\n")
        f.write(f"THREADS_ACCESS_TOKEN={access_token}\n")
        f.write(f"THREADS_USER_ID={user_id}\n")

    print(f"\n✅ .envファイルに追加しました: {env_file}")
    print(f"\n🎉 セットアップ完了! 分析ツールを実行できます:")
    print(f"   python threads_performance_analyzer.py --analyze --learn")

except Exception as e:
    print(f"❌ エラー: {e}")
    exit(1)
