#!/usr/bin/env python3
"""
記事ファイル名を「タイトル_XXX.md」→「XXX_タイトル.md」に変更

例:
  暗号資産で失敗する初心者の罠_009.md
  → 009_暗号資産で失敗する初心者の罠.md
"""

import json
import re
from pathlib import Path


def extract_id_from_filename(filename):
    """ファイル名から記事IDを抽出"""
    # 末尾の_XXX.mdパターンを探す
    match = re.search(r'_(\d{3})$', filename.replace('.md', ''))
    if match:
        return match.group(1)
    return None


def rename_files_and_update_master():
    """ファイル名変更 + article_master.json更新"""
    
    # article_master.json読み込み
    master_path = Path(__file__).parent.parent / "gethnote" / "article_master.json"
    with open(master_path, encoding="utf-8") as f:
        master_data = json.load(f)
    
    print("📝 記事ファイル名変更開始\n")
    
    renamed_count = 0
    
    for article in master_data["articles"]:
        article_id = article["id"]
        old_file_path_str = article["file"]
        
        # 旧ファイルパス構築
        old_file_path = Path(__file__).parent.parent / "gethnote" / "drafts" / f"{old_file_path_str}.md"
        
        if not old_file_path.exists():
            print(f"⚠️  [ID {article_id:3d}] ファイルが見つかりません: {old_file_path}")
            continue
        
        # ファイル名から記事IDを抽出
        old_filename = old_file_path.stem  # .md除く
        extracted_id = extract_id_from_filename(old_filename)
        
        if not extracted_id:
            # sample_pachinko_003_final のような特殊ケース
            # IDが末尾にない場合はスキップ or 手動対応
            print(f"⚠️  [ID {article_id:3d}] ID抽出失敗 - スキップ: {old_filename}")
            continue
        
        # 新ファイル名生成: 009_暗号資産で失敗する初心者の罠
        # タイトル部分 = old_filename から _XXX を除去
        title_part = old_filename.replace(f'_{extracted_id}', '')
        new_filename = f"{extracted_id}_{title_part}.md"
        
        # 新ファイルパス
        new_file_path = old_file_path.parent / new_filename
        
        # ファイル名が同じならスキップ
        if old_file_path == new_file_path:
            continue
        
        # ファイル名変更
        old_file_path.rename(new_file_path)
        
        # article_master.json のfile属性を更新
        # 例: "月曜_ギャンブル金/暗号資産で失敗する初心者の罠_009"
        #  → "月曜_ギャンブル金/009_暗号資産で失敗する初心者の罠"
        old_relative_path = article["file"]
        dir_part, old_fname = old_relative_path.rsplit('/', 1) if '/' in old_relative_path else ('', old_relative_path)
        new_relative_path = f"{dir_part}/{extracted_id}_{title_part}" if dir_part else f"{extracted_id}_{title_part}"
        
        article["file"] = new_relative_path
        
        print(f"✅ [ID {article_id:3d}] {old_filename} → {new_filename.replace('.md', '')}")
        renamed_count += 1
    
    # article_master.json保存
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 完了!")
    print(f"変更ファイル数: {renamed_count}")
    print(f"article_master.json更新済み")


if __name__ == "__main__":
    rename_files_and_update_master()
