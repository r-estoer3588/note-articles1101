#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVの投稿内容を「レス卒先輩」ペルソナに合わせてリライトするスクリプト

使い方:
  python tools/rewrite_csv_with_persona.py input.csv [output.csv]

機能:
  - 指定されたCSVの "Text" カラムを読み込む
  - prompt/relationship_context.md のペルソナ定義に基づいてリライト
  - OpenAI API (gpt-4o-mini) を使用
  - 結果を新しいCSVに保存
"""

import csv
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict
from openai import OpenAI


# 定数
CONTEXT_FILE = (
    Path(__file__).parent.parent / "prompt" / "relationship_context.md"
)
MODEL_NAME = "gpt-4o-mini"


def load_context() -> str:
    """ペルソナ定義ファイルを読み込む"""
    if not CONTEXT_FILE.exists():
        print(f"❌ エラー: コンテキストファイルが見つかりません: {CONTEXT_FILE}")
        sys.exit(1)

    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def rewrite_text(client: OpenAI, context: str, original_text: str) -> str:
    """OpenAI APIを使ってテキストをリライト"""
    if not original_text.strip():
        return ""

    system_prompt = f"""
{context}

## 指示
上記の「レス卒先輩」のペルソナとトーン＆マナーに従って、以下の投稿をリライトしてください。
- 元の投稿の意図（メッセージ）は維持する
- 「心理学×行動経済学」の要素を自然に盛り込む（無理ならトーンだけ合わせる）
- 140文字以内で、Twitter(X)向けに最適化する
- 引用符（""）で囲まない
- ハッシュタグは含めない
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"以下の投稿をリライトしてください:\n\n{original_text}",
                },
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ APIエラー: {e}")
        return original_text  # エラー時は元テキストを返す


def process_csv(input_path: Path, output_path: Path):
    """CSVを処理してリライト"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ エラー: 環境変数 OPENAI_API_KEY が設定されていません")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    context = load_context()

    print(f"📖 読み込み中: {input_path}")
    print(f"🤖 使用モデル: {MODEL_NAME}")
    print("-" * 50)

    rows = []
    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # バッファ用リスト
        data = list(reader)
        total = len(data)

        for i, row in enumerate(data, 1):
            original = row.get("Text", "")
            if not original:
                rows.append(row)
                continue

            print(f"[{i}/{total}] リライト中...")
            rewritten = rewrite_text(client, context, original)

            # 変更を表示（デバッグ用）
            print(f"  前: {original[:30]}...")
            print(f"  後: {rewritten[:30]}...")

            row["Text"] = rewritten
            rows.append(row)

    # 保存
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        writer.writerows(rows)

    print("-" * 50)
    print(f"✅ 保存完了: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CSV投稿リライトツール")
    parser.add_argument("input_csv", help="入力CSVファイルのパス")
    parser.add_argument(
        "output_csv",
        nargs="?",
        help="出力CSVファイルのパス（省略時は _refined を付与）",
    )

    args = parser.parse_args()

    input_path = Path(args.input_csv)
    if not input_path.exists():
        print(f"❌ エラー: ファイルが見つかりません: {input_path}")
        sys.exit(1)

    if args.output_csv:
        output_path = Path(args.output_csv)
    else:
        output_path = input_path.with_name(
            f"{input_path.stem}_refined{input_path.suffix}"
        )

    process_csv(input_path, output_path)


if __name__ == "__main__":
    main()
