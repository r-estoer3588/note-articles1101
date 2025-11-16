#!/usr/bin/env python3
"""
記事ファイルパスの自動修復スクリプト
- drafts/配下のファイルを正規位置に移動
- 重複ファイルは最大サイズを採用
- article_master.jsonを更新
"""

import json
import shutil
from pathlib import Path
from collections import defaultdict


def find_best_file_for_id(article_id, base_dir):
    """指定IDの最適な記事ファイルを検索"""
    pattern = f"{article_id:03d}_*.md"
    candidates = list(base_dir.rglob(pattern))
    
    if not candidates:
        return None
    
    # 最大サイズのファイルを選択（最も完成度が高いと仮定）
    best_file = max(candidates, key=lambda f: f.stat().st_size)
    return best_file


def main():
    print("=" * 80)
    print("🔧 げすいぬ記事ファイルパス自動修復")
    print("=" * 80)
    
    base_dir = Path(__file__).parent.parent
    master_path = base_dir / "article_master.json"
    
    # マスターデータ読み込み
    with open(master_path, 'r', encoding='utf-8') as f:
        master = json.load(f)
    
    print(f"\n📚 対象記事: {len(master['articles'])}本")
    
    # 修復対象を収集
    fixes_needed = []
    already_ok = []
    
    for article in master['articles']:
        article_id = article['id']
        expected_path = base_dir / (article['file'] + '.md')
        
        if expected_path.exists():
            already_ok.append(article_id)
        else:
            # 最適なファイルを検索
            best_file = find_best_file_for_id(article_id, base_dir)
            if best_file:
                fixes_needed.append({
                    'article': article,
                    'current_path': best_file,
                    'target_path': expected_path
                })
    
    print(f"✅ 修復不要: {len(already_ok)}本")
    print(f"🔧 修復必要: {len(fixes_needed)}本")
    
    if not fixes_needed:
        print("\n✨ 全ての記事ファイルが正しい位置にあります！")
        return
    
    # 修復プレビュー
    print(f"\n【修復プレビュー】（上位10件）")
    for item in fixes_needed[:10]:
        print(f"  ID{item['article']['id']:03d}:")
        print(f"    FROM: {item['current_path'].relative_to(base_dir)}")
        print(f"    TO:   {item['target_path'].relative_to(base_dir)}")
    
    # 実行確認
    print(f"\n⚠️  {len(fixes_needed)}本のファイルを移動します。")
    response = input("実行しますか？ [y/N]: ").strip().lower()
    
    if response != 'y':
        print("❌ キャンセルしました")
        return
    
    # 移動実行
    print(f"\n🚀 移動開始...")
    success_count = 0
    error_count = 0
    
    for item in fixes_needed:
        try:
            target_path = item['target_path']
            current_path = item['current_path']
            
            # ディレクトリ作成
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイル移動
            shutil.copy2(current_path, target_path)
            success_count += 1
            
            print(f"  ✅ ID{item['article']['id']:03d}: 移動完了")
            
        except Exception as e:
            error_count += 1
            print(f"  ❌ ID{item['article']['id']:03d}: エラー - {e}")
    
    print(f"\n" + "=" * 80)
    print(f"📌 完了:")
    print(f"  - 成功: {success_count}本")
    print(f"  - 失敗: {error_count}本")
    print(f"  - 投稿準備完了: {len(already_ok) + success_count}本")
    print("=" * 80)
    
    if success_count > 0:
        print("\n✨ 次のステップ:")
        print("  1. python tools/check_article_files.py で再確認")
        print("  2. 投稿スケジュールの作成")
        print("  3. マガジン説明文の準備")


if __name__ == "__main__":
    main()
