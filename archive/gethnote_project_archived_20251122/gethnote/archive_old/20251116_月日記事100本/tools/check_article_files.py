#!/usr/bin/env python3
"""
記事ファイルの存在確認と修復スクリプト
article_master.jsonと実際のファイルを照合して、ギャップを可視化
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def find_all_article_files():
    """全ての記事ファイルを検索"""
    base_dir = Path(__file__).parent.parent
    article_files = []
    
    # 番号付き記事を検索（001_から始まる）
    for md_file in base_dir.rglob("*.md"):
        if md_file.name[0].isdigit():
            # 相対パスを取得
            rel_path = md_file.relative_to(base_dir)
            article_files.append({
                'path': str(rel_path),
                'name': md_file.name,
                'size': md_file.stat().st_size,
                'dir': md_file.parent.name
            })
    
    return sorted(article_files, key=lambda x: x['name'])

def load_article_master():
    """article_master.jsonを読み込み"""
    master_path = Path(__file__).parent.parent / "article_master.json"
    with open(master_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("=" * 80)
    print("📋 げすいぬ記事ファイル一括チェック")
    print("=" * 80)
    
    # 実ファイル検索
    actual_files = find_all_article_files()
    print(f"\n✅ 実際に存在する記事ファイル: {len(actual_files)}本")
    
    # マスターデータ読み込み
    master = load_article_master()
    total_articles = len(master['articles'])
    print(f"📚 article_master.json登録数: {total_articles}本")
    
    # 番号別にグルーピング
    files_by_number = defaultdict(list)
    for f in actual_files:
        # ファイル名から番号を抽出（001_, 002_など）
        try:
            num = int(f['name'][:3])
            files_by_number[num].append(f)
        except ValueError:
            continue
    
    print(f"\n📊 番号別カバレッジ:")
    print(f"  - ID 001-100: {len([n for n in files_by_number if 1 <= n <= 100])}本")
    print(f"  - ID 101以降: {len([n for n in files_by_number if n > 100])}本")
    
    # 重複チェック
    duplicates = {num: files for num, files in files_by_number.items() if len(files) > 1}
    if duplicates:
        print(f"\n⚠️  重複ファイル検出: {len(duplicates)}番号")
        for num, files in sorted(duplicates.items())[:10]:
            print(f"  ID{num:03d}: {len(files)}個")
            for f in files:
                print(f"    - {f['path']} ({f['size']} bytes)")
    
    # 欠番チェック
    existing_numbers = set(files_by_number.keys())
    missing_numbers = set(range(1, 101)) - existing_numbers
    if missing_numbers:
        print(f"\n❌ 欠番: {len(missing_numbers)}本")
        print(f"  範囲: {sorted(list(missing_numbers))[:20]}")
    
    # マスターとの照合
    print(f"\n🔍 article_master.json照合:")
    found_in_master = 0
    missing_in_master = []
    
    for article in master['articles']:
        article_id = article['id']
        expected_file = article['file'] + '.md'
        
        if os.path.exists(Path(__file__).parent.parent / expected_file):
            found_in_master += 1
        else:
            # 番号に該当するファイルが存在するかチェック
            if article_id in files_by_number:
                missing_in_master.append({
                    'id': article_id,
                    'title': article['title'],
                    'expected': expected_file,
                    'actual': [f['path'] for f in files_by_number[article_id]]
                })
    
    print(f"  ✅ マスターと一致: {found_in_master}本")
    print(f"  ⚠️  パス不一致（ファイルは存在）: {len(missing_in_master)}本")
    
    if missing_in_master:
        print(f"\n  【パス不一致の例】（上位10件）")
        for item in missing_in_master[:10]:
            print(f"  ID{item['id']:03d}: {item['title'][:30]}")
            print(f"    期待: {item['expected']}")
            print(f"    実際: {item['actual'][0] if item['actual'] else 'なし'}")
    
    # 結論
    print(f"\n" + "=" * 80)
    print(f"📌 結論:")
    print(f"  - 実ファイル: {len(actual_files)}本")
    print(f"  - マスター登録: {total_articles}本")
    print(f"  - パス一致: {found_in_master}本")
    print(f"  - 即座に投稿可能: {found_in_master}本")
    print(f"  - パス修正必要: {len(missing_in_master)}本")
    print(f"  - 完全欠番: {len(missing_numbers)}本")
    print("=" * 80)

if __name__ == "__main__":
    main()
