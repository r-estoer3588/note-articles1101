"""
note自動投稿スクリプト

93記事を自動的にnoteに投稿するPlaywrightベースのスクリプト。

機能:
- noteへの自動ログイン
- 記事の自動作成・投稿
- 有料設定(¥300)の自動適用
- 一括投稿モード

使い方:
    python note_auto_poster.py --email your@email.com --password yourpass --articles-dir ../gethnote/drafts
"""

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
import argparse


class NoteAutoPoster:
    """note自動投稿クラス"""
    
    def __init__(self, email: str, password: str, headless: bool = False):
        self.email = email
        self.password = password
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def start(self):
        """ブラウザを起動"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        self.page = await context.new_page()
        
    async def close(self):
        """ブラウザを閉じる"""
        if self.browser:
            await self.browser.close()
            
    async def login(self):
        """noteにログイン"""
        print("📝 noteにログイン中...")
        
        # ログインページへ移動
        await self.page.goto("https://note.com/login")
        await self.page.wait_for_load_state("networkidle")
        
        # メールアドレス入力
        await self.page.fill('input[name="login"]', self.email)
        await self.page.fill('input[name="password"]', self.password)
        
        # ログインボタンをクリック
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_load_state("networkidle")
        
        # ログイン成功確認
        if "login" in self.page.url:
            raise Exception("❌ ログイン失敗。メールアドレスとパスワードを確認してください。")
        
        print("✅ ログイン成功")
        
    async def create_article(self, title: str, content: str, price: int = 300):
        """記事を作成・投稿
        
        Args:
            title: 記事タイトル
            content: 記事本文(Markdown)
            price: 販売価格(デフォルト: 300円)
        """
        print(f"📄 記事作成中: {title}")
        
        # 新規記事作成ページへ
        await self.page.goto("https://note.com/new")
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        
        # タイトル入力
        title_selector = 'textarea[placeholder*="タイトル"], input[placeholder*="タイトル"]'
        await self.page.wait_for_selector(title_selector, timeout=10000)
        await self.page.fill(title_selector, title)
        
        # 本文入力
        # noteのエディタはcontenteditable要素
        editor_selector = '[contenteditable="true"]'
        await self.page.wait_for_selector(editor_selector, timeout=10000)
        
        # Markdownを段落ごとに入力（改行を保持）
        paragraphs = content.split('\n')
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                await self.page.type(editor_selector, paragraph)
            if i < len(paragraphs) - 1:
                await self.page.keyboard.press('Enter')
            await asyncio.sleep(0.1)  # 入力安定化
        
        await asyncio.sleep(2)
        
        # 有料設定
        await self._set_paid_article(price)
        
        # 公開
        await self._publish_article()
        
        print(f"✅ 投稿完了: {title}")
        
    async def _set_paid_article(self, price: int):
        """有料記事設定
        
        Args:
            price: 販売価格
        """
        print(f"💰 有料設定: ¥{price}")
        
        # 公開設定ボタンをクリック
        settings_button = 'button:has-text("公開設定")'
        try:
            await self.page.click(settings_button, timeout=5000)
        except:
            # 別のセレクタを試す
            await self.page.click('button:has-text("設定")', timeout=5000)
        
        await asyncio.sleep(1)
        
        # 有料記事にチェック
        paid_checkbox = 'input[type="checkbox"][value="paid"], label:has-text("有料")'
        await self.page.click(paid_checkbox)
        await asyncio.sleep(1)
        
        # 価格入力
        price_input = 'input[type="number"], input[placeholder*="価格"]'
        await self.page.fill(price_input, str(price))
        
        await asyncio.sleep(1)
        
    async def _publish_article(self):
        """記事を公開"""
        print("📢 記事を公開中...")
        
        # 公開ボタンをクリック
        publish_button = 'button:has-text("公開する")'
        await self.page.click(publish_button)
        await self.page.wait_for_load_state("networkidle")
        
        await asyncio.sleep(2)
        
    def parse_markdown_article(self, markdown_path: Path) -> Dict[str, str]:
        """Markdownファイルを解析
        
        Args:
            markdown_path: Markdownファイルパス
            
        Returns:
            {"title": タイトル, "content": 本文, "free_part": 無料部分, "paid_part": 有料部分}
        """
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # タイトル抽出（最初の#見出し）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else markdown_path.stem
        
        # 有料部分の区切りを検出
        paid_separator = re.search(r'#+\s*【有料部分】', content, re.IGNORECASE | re.MULTILINE)
        
        if paid_separator:
            free_part = content[:paid_separator.start()].strip()
            paid_part = content[paid_separator.start():].strip()
        else:
            free_part = content
            paid_part = ""
        
        return {
            "title": title,
            "content": content,
            "free_part": free_part,
            "paid_part": paid_part
        }
        
    async def post_articles_from_directory(self, articles_dir: Path, limit: Optional[int] = None):
        """ディレクトリ内の全記事を投稿
        
        Args:
            articles_dir: 記事が格納されたディレクトリ
            limit: 投稿する記事数の上限（Noneの場合は全部）
        """
        # 曜日ごとのサブディレクトリを取得
        subdirs = [d for d in articles_dir.iterdir() if d.is_dir()]
        
        articles = []
        for subdir in sorted(subdirs):
            md_files = list(subdir.glob("*.md"))
            articles.extend(md_files)
        
        if limit:
            articles = articles[:limit]
        
        print(f"📚 投稿予定記事数: {len(articles)}")
        
        for i, article_path in enumerate(articles, 1):
            print(f"\n--- [{i}/{len(articles)}] ---")
            
            try:
                article_data = self.parse_markdown_article(article_path)
                await self.create_article(
                    title=article_data["title"],
                    content=article_data["content"],
                    price=300
                )
                
                # 投稿間隔を空ける（rate limit対策）
                if i < len(articles):
                    wait_time = 60  # 60秒待機
                    print(f"⏱️  次の記事まで{wait_time}秒待機...")
                    await asyncio.sleep(wait_time)
                    
            except Exception as e:
                print(f"❌ エラー: {article_path.name} - {e}")
                continue
        
        print(f"\n🎉 完了！ {len(articles)}記事を投稿しました")


async def main():
    parser = argparse.ArgumentParser(description="note自動投稿スクリプト")
    parser.add_argument("--email", required=True, help="noteのメールアドレス")
    parser.add_argument("--password", required=True, help="noteのパスワード")
    parser.add_argument("--articles-dir", required=True, help="記事が格納されたディレクトリパス")
    parser.add_argument("--limit", type=int, help="投稿する記事数の上限")
    parser.add_argument("--headless", action="store_true", help="ヘッドレスモードで実行")
    
    args = parser.parse_args()
    
    articles_dir = Path(args.articles_dir)
    if not articles_dir.exists():
        print(f"❌ エラー: ディレクトリが見つかりません: {articles_dir}")
        return
    
    poster = NoteAutoPoster(
        email=args.email,
        password=args.password,
        headless=args.headless
    )
    
    try:
        await poster.start()
        await poster.login()
        await poster.post_articles_from_directory(articles_dir, limit=args.limit)
    finally:
        await poster.close()


if __name__ == "__main__":
    asyncio.run(main())
