"""
Week 7-8の18記事を個別ファイルに分割するスクリプト

Usage:
    python tools/split_articles_to_files.py
"""

import re
import os
import json
from datetime import datetime, timedelta
from pathlib import Path


def extract_articles_from_markdown(md_path):
    """Markdownファイルから18記事を抽出"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 記事を分割（"# 1. "から"# 2. "までが1記事）
    pattern = r'^# (\d+)\. (.+?)$'
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    
    articles = []
    for i, match in enumerate(matches):
        article_num = int(match.group(1))
        title = match.group(2).strip()
        
        # 記事の開始位置
        start_pos = match.start()
        
        # 次の記事の開始位置（最後の記事なら末尾まで）
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # 記事本文を抽出
        article_content = content[start_pos:end_pos].strip()
        
        articles.append({
            'number': article_num,
            'title': title,
            'content': article_content
        })
    
    return articles


def create_safe_dirname(title):
    """タイトルから安全なディレクトリ名を生成"""
    # 記号を削除してスペースをアンダースコアに
    safe = re.sub(r'[『』「」！？\!\?]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    # 長すぎる場合は短縮
    if len(safe) > 50:
        safe = safe[:50]
    return safe


def create_metadata_json(article_num, title, publish_date):
    """metadata.jsonを生成"""
    return {
        "title": title,
        "article_number": article_num,
        "published_date": publish_date.strftime("%Y-%m-%d"),
        "note_url": "",
        "tags": ["夫婦", "関係修復", "レス"],
        "views": 0,
        "likes": 0,
        "category": "relationship",
        "status": "draft",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def main():
    # パス設定
    base_dir = Path("c:/Repos/note-articles")
    source_file = base_dir / "research_ideas/relationship/weeks_7_8_article_plan.md"
    articles_dir = base_dir / "articles"
    
    # 記事を抽出
    print("📖 記事を抽出中...")
    articles = extract_articles_from_markdown(source_file)
    print(f"✅ {len(articles)}記事を抽出しました")
    
    # 開始日（Week 7の初日 = 2025-12-07）
    # Week 5: 2025-11-23～11-29
    # Week 6: 2025-11-30～12-06
    # Week 7: 2025-12-07～12-13
    start_date = datetime(2025, 12, 7)
    
    created_count = 0
    
    for article in articles:
        # 記事ごとの公開日（Day 43から始まるが、記事は2-3日ごとに公開する想定）
        # 18記事を32日（Day 43-60）に分散させる
        # 簡易的に: 記事番号 × 1.7日 ≈ 30日でカバー
        days_offset = int((article['number'] - 1) * 1.7)
        publish_date = start_date + timedelta(days=days_offset)
        
        # ディレクトリ名生成
        safe_title = create_safe_dirname(article['title'])
        dir_name = f"{publish_date.strftime('%Y-%m-%d')}_{safe_title}"
        article_dir = articles_dir / dir_name
        
        # ディレクトリ作成
        article_dir.mkdir(parents=True, exist_ok=True)
        (article_dir / "images").mkdir(exist_ok=True)
        
        # article.md作成
        article_path = article_dir / "article.md"
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article['content'])
        
        # metadata.json作成
        metadata = create_metadata_json(article['number'], article['title'], publish_date)
        metadata_path = article_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # prompts.txt作成（空ファイル）
        prompts_path = article_dir / "prompts.txt"
        with open(prompts_path, 'w', encoding='utf-8') as f:
            f.write("# 使用したプロンプト\n\n")
            f.write("## 記事リライト\n")
            f.write("- weeks_7_8_article_plan.mdから自動分割\n")
            f.write("- PASONA構造：Problem → Affinity → Solution → Offer → Narrow down → Action\n")
        
        created_count += 1
        print(f"✅ [{article['number']:2d}/18] {dir_name}")
    
    print(f"\n🎉 {created_count}記事を個別ファイル化しました！")
    print(f"📁 保存先: {articles_dir}")
    print("\n📋 次のステップ:")
    print("1. 各記事の article.md を確認")
    print("2. metadata.json の tags を必要に応じて調整")
    print("3. images/ フォルダに画像を配置")
    print("4. noteに投稿後、metadata.json に note_url を記入")


if __name__ == "__main__":
    main()
