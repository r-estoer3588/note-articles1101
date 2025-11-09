#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重複記事の自動削除 - 品質の低い方を削除
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


def calculate_quality_score(content: str) -> Dict:
    """
    記事の品質スコアを計算
    """
    # 文字数
    char_count = len(content)
    
    # データポイント数 (**1.**, **2.** など)
    data_points = len(re.findall(r'\*\*\d+\.\*\*', content))
    
    # 「金ドブ。ホゲー」の有無
    has_kindobu = '金ドブ。ホゲー' in content
    
    # 「業者の養分」の有無
    has_youbun = '業者の養分' in content
    
    # 「カモられる」の出現回数
    kamo_count = content.count('カモられ')
    
    # 「今すぐ」「お前次第」などの行動促進
    action_count = content.count('今すぐ') + content.count('お前次第')
    
    # スコア計算
    score = 0
    score += min(char_count / 100, 30)  # 文字数 (最大30点)
    score += data_points * 5  # データポイント (1個5点)
    score += 10 if has_kindobu else 0  # 金ドブ (10点)
    score += 5 if has_youbun else 0  # 養分 (5点)
    score += kamo_count * 2  # カモられる (1回2点)
    score += action_count * 2  # 行動促進 (1回2点)
    
    return {
        'score': score,
        'char_count': char_count,
        'data_points': data_points,
        'has_kindobu': has_kindobu,
        'has_youbun': has_youbun,
        'kamo_count': kamo_count,
        'action_count': action_count
    }


def find_duplicates(base_dir: Path) -> Dict[str, List[Path]]:
    """
    重複ファイルを検出
    """
    files_by_title = {}
    
    for md_file in base_dir.rglob('*.md'):
        # sample除外
        if 'sample' in md_file.name.lower():
            continue
        
        # 番号を除いたタイトル
        title = re.sub(r'^\d+_', '', md_file.name)
        
        if title not in files_by_title:
            files_by_title[title] = []
        
        files_by_title[title].append(md_file)
    
    # 重複のみ
    return {k: v for k, v in files_by_title.items() if len(v) > 1}


def main():
    """
    メイン処理
    """
    print("🔍 重複記事の品質チェック & 自動削除")
    print()
    
    base_dir = Path(__file__).parent.parent / 'gethnote' / 'drafts'
    
    # 重複検出
    duplicates = find_duplicates(base_dir)
    
    if not duplicates:
        print("✅ 重複なし")
        return
    
    print(f"📊 重複タイトル: {len(duplicates)}種類\n")
    
    deleted_count = 0
    kept_count = 0
    
    for title, files in sorted(duplicates.items()):
        print(f"\n{'='*60}")
        print(f"📄 {title}")
        print(f"   {len(files)}個の重複")
        
        # 各ファイルの品質スコア計算
        file_scores = []
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            quality = calculate_quality_score(content)
            file_scores.append((file, quality))
            
            cat_name = file.parent.name
            print(f"\n   [{cat_name}] {file.name}")
            print(f"      スコア: {quality['score']:.1f}点")
            print(f"      文字数: {quality['char_count']}, データ: {quality['data_points']}")
            print(f"      金ドブ: {'✅' if quality['has_kindobu'] else '❌'}, "
                  f"養分: {'✅' if quality['has_youbun'] else '❌'}")
        
        # スコア順にソート
        file_scores.sort(key=lambda x: x[1]['score'], reverse=True)
        
        # 最高スコアを残す
        keep_file, keep_score = file_scores[0]
        print(f"\n   ✅ 残す: {keep_file.parent.name}/{keep_file.name} ({keep_score['score']:.1f}点)")
        kept_count += 1
        
        # 残りを削除
        for file, score in file_scores[1:]:
            print(f"   🗑️  削除: {file.parent.name}/{file.name} ({score['score']:.1f}点)")
            file.unlink()
            deleted_count += 1
    
    print(f"\n{'='*60}")
    print(f"\n🎉 完了!")
    print(f"   残した記事: {kept_count}種類")
    print(f"   削除した記事: {deleted_count}個")


if __name__ == '__main__':
    main()
