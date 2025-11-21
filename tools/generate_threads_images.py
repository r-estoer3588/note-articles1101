#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads投稿画像自動生成ツール (Nano Banana Pro / Gemini連携)

概要:
  テキストリストを読み込み、各投稿の感情やシーンに合わせた背景画像を
  Gemini (Nano Banana Pro) で生成し、テキストを合成して保存します。

使い方:
  python tools/generate_threads_images.py --input input/threads_image_prompts.txt --out-dir outputs/threads_images
  
  # プロンプト生成のみ（画像生成なし）
  python tools/generate_threads_images.py --dry-run

前提:
  - GOOGLE_API_KEY 環境変数が設定されていること
  - google-generativeai ライブラリがインストールされていること
    (pip install google-generativeai)
  - Pillow ライブラリがインストールされていること
"""

import argparse
import os
import sys
import re
import time
from pathlib import Path
from typing import List, Dict, Optional

# .envファイルから環境変数を読み込む
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenvがなくても動作するようにする

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("❌ Pillowライブラリが必要です: pip install Pillow")
    sys.exit(1)

# Gemini API (google-generativeai) のインポート試行
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


class ThreadsImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key and HAS_GEMINI:
            print("⚠️ GOOGLE_API_KEYが設定されていません。プロンプト生成はスキップされます。")
        
        if HAS_GEMINI and self.api_key:
            genai.configure(api_key=self.api_key)
            # テキスト生成用モデル (プロンプト作成用)
            self.text_model = genai.GenerativeModel('gemini-2.0-flash')
            # 画像生成用モデル (Imagen 3) - 利用可能な場合
            self.image_model_name = 'imagen-3.0-generate-001' 

    def parse_input_file(self, file_path: Path) -> List[Dict]:
        """入力テキストファイルをパースする"""
        content = file_path.read_text(encoding='utf-8')
        # Day X [Time] で分割
        pattern = re.compile(
            r'(Day \d+ \[\d{2}:\d{2}\])\n(.*?)(?=\nDay \d+ \[\d{2}:\d{2}\]|$)',
            re.DOTALL
        )
        
        matches = pattern.findall(content)
        posts = []
        
        for header, body in matches:
            # header: "Day 1 [07:00]"
            day_match = re.search(r'Day (\d+)', header)
            time_match = re.search(r'\[(\d{2}:\d{2})\]', header)
            
            day = int(day_match.group(1)) if day_match else 0
            time_str = time_match.group(1) if time_match else "00:00"
            text = body.strip()
            
            posts.append({
                "day": day,
                "time": time_str,
                "text": text,
                "header": header
            })
            
        return posts

    def generate_image_prompt(self, text: str, time_str: str) -> str:
        """Geminiを使って、テキストに合った画像生成プロンプトを作成する"""
        if not HAS_GEMINI or not self.api_key:
            return (
                "soft focus, abstract background, emotional atmosphere, "
                "muted colors, high quality"
            )

        system_prompt = """
        あなたはプロのフォトグラファー兼アートディレクターです。
        提供された「30代〜40代女性向けのThreads投稿テキスト」から、
        その感情やシーンに合った「アイキャッチ画像」の生成プロンプト（英語）を作成してください。

        条件:
        - **被写体**: 30代〜40代の日本人女性。
        - **表情**: テキストの感情（不安、孤独、希望、安らぎなど）を繊細な表情で表現する。カメラ目線や横顔など、アイキャッチとして惹きつける構図。
        - **構図**: テキストを配置するための「余白」を意識する（顔を左右どちらかに寄せる、など）。
        - **トーン**: エモーショナル、映画のワンシーンのような高品質なフィルム写真風。
        - **光**: 時間帯（朝/昼/夜）を考慮したドラマチックなライティング。
        - 出力は英語のプロンプトのみ。説明不要。
        """

        user_prompt = f"時間帯: {time_str}\nテキスト:\n{text}"

        try:
            response = self.text_model.generate_content(
                [system_prompt, user_prompt]
            )
            return response.text.strip()
        except Exception as e:
            print(f"⚠️ プロンプト生成エラー: {e}")
            return (
                "soft focus, abstract background, emotional atmosphere, "
                "muted colors"
            )

    def generate_image(self, prompt: str, output_path: Path) -> bool:
        """Gemini (Imagen) で画像を生成する (未実装の場合はプレースホルダ)"""
        print(f"🎨 画像生成プロンプト: {prompt}")
        
        # フォールバック: ランダムな落ち着いた色のグラデーション画像を生成
        self._create_placeholder_image(output_path, prompt)
        return True

    def _create_placeholder_image(self, output_path: Path, prompt: str):
        """プロンプトに基づいて雰囲気のあるプレースホルダ画像を生成"""
        width, height = 1080, 1350  # Threads/Instagram縦長サイズ

        # プロンプトから色味を推測（簡易）
        base_color = (240, 240, 235)  # デフォルト: オフホワイト
        if "night" in prompt.lower() or "dim" in prompt.lower():
            base_color = (40, 45, 60)  # 夜: ダークブルーグレー
        elif "morning" in prompt.lower():
            base_color = (230, 240, 250)  # 朝: ペールブルー
        elif "warm" in prompt.lower() or "sun" in prompt.lower():
            base_color = (250, 240, 220)  # 暖色: ベージュ

        img = Image.new('RGB', (width, height), base_color)
        draw = ImageDraw.Draw(img)

        # ノイズやグラデーションを加えて「それっぽく」する
        import random
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(300, 800)
            color = (
                min(255, base_color[0] + random.randint(-20, 20)),
                min(255, base_color[1] + random.randint(-20, 20)),
                min(255, base_color[2] + random.randint(-20, 20)),
            )
            draw.ellipse(
                (x - r, y - r, x + r, y + r),
                fill=color,
                outline=None
            )

        # ぼかし
        img = img.filter(ImageFilter.GaussianBlur(radius=50))

        img.save(output_path)

    def overlay_text(
        self,
        image_path: Path,
        text: str,
        header: str,
        font_path: Optional[str] = None
    ):
        """画像にテキストを合成する"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # フォント設定
        font_candidates = [
            font_path,
            "C:\\Windows\\Fonts\\msmincho.ttc",  # MS明朝
            "C:\\Windows\\Fonts\\yumin.ttf",     # 游明朝
            "C:\\Windows\\Fonts\\meiryo.ttc",    # メイリオ
            "/System/Library/Fonts/Hiragino Mincho ProN.ttc",  # Mac用
        ]

        selected_font = None
        for f in font_candidates:
            if f and os.path.exists(f):
                selected_font = f
                break

        font_size = 60  # デフォルトサイズ

        try:
            if selected_font:
                font = ImageFont.truetype(selected_font, font_size)
                header_font = ImageFont.truetype(selected_font, 40)
            else:
                font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                print(
                    "⚠️ 日本語フォントが見つかりませんでした。"
                    "デフォルトフォントを使用します。"
                )
        except Exception as e:
            print(f"⚠️ フォント読み込みエラー: {e}")
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()

        # テキスト色
        text_color = (50, 50, 50)  # ダークグレー

        # ヘッダー描画 (Day 1 [07:00])
        draw.text(
            (width // 2, 100),
            header,
            font=header_font,
            fill=text_color,
            anchor="mm"
        )

        # 本文描画 (中央揃え)
        lines = text.split('\n')
        line_height = font_size * 1.8
        total_text_height = len(lines) * line_height
        start_y = (height - total_text_height) // 2

        for i, line in enumerate(lines):
            y = start_y + (i * line_height)
            draw.text(
                (width // 2, y),
                line,
                font=font,
                fill=text_color,
                anchor="mm"
            )

        img.save(image_path)

    def run(
        self,
        input_file: str,
        out_dir: str,
        dry_run: bool = False,
        font: Optional[str] = None
    ):
        input_path = Path(input_file)
        output_dir = Path(out_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"📖 入力ファイルを読み込んでいます: {input_path}")
        posts = self.parse_input_file(input_path)
        print(f"✅ {len(posts)}件の投稿が見つかりました")

        for i, post in enumerate(posts):
            print(f"\n[{i + 1}/{len(posts)}] 処理中: {post['header']}")

            # 1. プロンプト生成
            prompt = self.generate_image_prompt(post['text'], post['time'])

            if dry_run:
                print(f"📝 生成されたプロンプト: {prompt}")
                continue

            # 2. 画像生成
            safe_time = post['time'].replace(':', '')
            filename = f"day{post['day']}_{safe_time}.png"
            out_path = output_dir / filename

            self.generate_image(prompt, out_path)

            # 3. テキスト合成
            self.overlay_text(out_path, post['text'], post['header'], font)
            print(f"💾 保存完了: {out_path}")

            # APIレート制限考慮
            if HAS_GEMINI and not dry_run:
                time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Threads画像自動生成ツール")
    parser.add_argument("--input", required=True, help="入力テキストファイル")
    parser.add_argument(
        "--out-dir", default="outputs/threads_images", help="出力ディレクトリ"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="画像生成を行わずプロンプトのみ表示"
    )
    parser.add_argument("--font", help="使用する日本語フォントのパス")
    parser.add_argument(
        "--api-key", help="Google API Key (省略時は環境変数 GOOGLE_API_KEY)"
    )

    args = parser.parse_args()

    if not HAS_GEMINI:
        print("⚠️ google-generativeai がインストールされていません。")
        print(
            "   プロンプト生成機能はスキップされ、"
            "デフォルトの背景が使用されます。"
        )
        print("   インストール: pip install google-generativeai")
        print()

    generator = ThreadsImageGenerator(api_key=args.api_key)
    generator.run(args.input, args.out_dir, args.dry_run, args.font)


if __name__ == "__main__":
    main()
