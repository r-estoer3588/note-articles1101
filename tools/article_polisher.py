#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article Polisher - 感情トーン強化版
既存98記事の推敲: 感情強化、煽り追加、読みやすさ向上
"""

import re
from pathlib import Path
from typing import Dict, List


def polish_article(content: str, title: str) -> str:
    """
    記事を推敲: 感情トーン強化
    """
    
    # 1. 冒頭の感情強化
    content = re.sub(
        r'俺は昔、知らずに年間(\d+)万円損してた。',
        r'**俺は昔、無知でカモられて年間\1万円ドブに捨ててた。金ドブ。ホゲー**',
        content
    )
    
    # 1-b. 既存の「クソが。」を「金ドブ。ホゲー」に置換
    content = re.sub(
        r'(\*\*俺は昔、無知でカモられて年間\d+万円ドブに捨ててた。)クソが。(\*\*)',
        r'\1金ドブ。ホゲー\2',
        content
    )
    
    # 2. データ紹介の強調
    content = content.replace(
        '実際のデータを見てくれ↓',
        '**実際のデータを見てくれ。これが現実だ↓**'
    )
    
    # 3. カモフラグの強調
    content = content.replace(
        '全部**カモフラグ**だぞ。',
        '**全部カモフラグだ。今すぐ気づけ。**'
    )
    
    # 4. 有料部分の冒頭強化
    content = content.replace(
        'おう、300円払ったな。賢い選択だ。',
        '**おう、300円払ったな。賢い選択だ。周りのバカどもと違う。**'
    )
    
    # 5. 業界裏話の攻撃性強化
    content = re.sub(
        r'業者・インフルエンサー・詐欺師は、お前が無知なまま損してくれた方が儲かる。\n' +
        r'だから公式には絶対に教えない情報がある。',
        r'**業者・インフルエンサー・詐欺師、全員グル。お前をカモるのが仕事だ。**\n' +
        r'だから公式には絶対に教えない情報がある。むしろ隠す。',
        content
    )
    
    # 6. ボッタクリの強調
    content = content.replace(
        '「お客様第一」とか言いながら、実は手数料ボッタクリ商品を売りつけてる。',
        '**「お客様第一」とか笑わせる。実態は手数料ボッタクリ、情報隠蔽、カモ量産システムだ。**'
    )
    
    # 7. ガチでエグいの強調
    content = content.replace(
        'ガチでエグい。',
        '**ガチでエグい。でもこれが業界の真実だ。**'
    )
    
    # 8. NG/OK行動の前振り強化
    content = content.replace(
        'これらを避けるだけで',
        '**これらを今すぐやめろ。それだけで'
    )
    
    # 9. 最後の煽り強化
    content = re.sub(
        r'周りのバカどもは知らずに損し続けてる。\n\n' +
        r'でもこれを読んだお前は違う。',
        r'**周りのバカどもは今日もカモられ続けてる。**\n\n' +
        r'**でもこれを読んだお前だけは違う道を選べる。**',
        content
    )
    
    # 10. 行動促進の強化
    content = content.replace(
        'あとは行動するだけ。',
        '**あとは行動するだけ。今すぐ動け。**'
    )
    
    # 11. 最後のメッセージ強化
    content = content.replace(
        '300円払ったのはデカい投資だ。',
        '**300円払ったのはデカい投資だ。この記事で数万〜数十万は守れる。**'
    )
    
    content = content.replace(
        '今年は絶対に損するな。',
        '**今年は絶対に損するな。お前の人生、お前で守れ。**'
    )
    
    # 12. タイトル強調 (冒頭)
    if '# 【' in content:
        content = content.replace('# 【', '# **【', 1)
        content = content.replace('】', '】**', 1)
    
    # 13. ポイント①の強調
    content = content.replace(
        '## ポイント① あなたの知らない損失',
        '## ポイント① **あなたの知らない損失 (これが現実だ)**'
    )
    
    # 14. 理由の強調
    content = content.replace(
        '**理由:** 知識がないと確実に損する',
        '**理由:** 知識がないと確実にカモられる。業者の養分になるだけだ。'
    )
    
    # 15. 損失額の強調
    content = re.sub(
        r'つまり、知らないだけで\*\*年間(\d+)万円以上損する\*\*可能性がある。',
        r'**つまり、知らないだけで年間\1万円以上ドブに捨てる。**\n\n' +
        r'**お前がカモられた金で、業者が飯食ってる。**',
        content
    )
    
    # 16. 無料→有料の煽り強化
    content = content.replace(
        '300円ケチって今年も',
        '**300円ケチって今年も'
    )
    content = re.sub(
        r'\*\*300円ケチって今年も(\d+)万円損するか、300円払って守るか。',
        r'**300円ケチって今年も\1万円損するか、300円払って守るか。**',
        content
    )
    
    # 17. 選択の強調
    content = content.replace(
        'お前次第。',
        '**お前次第だ。選べ。**'
    )
    
    # 18. ステップ1の強調
    content = content.replace(
        '### ステップ1: **損失パターンを避ける**',
        '### ステップ1: **損失パターンを避ける (絶対やるな)**'
    )
    
    content = content.replace(
        '以下のパターンは確実に損する↓',
        '**以下のパターンは即カモ確定だ↓**'
    )
    
    # 19. ステップ2の強調
    content = content.replace(
        '### ステップ2: **正しい行動を取る**',
        '### ステップ2: **正しい行動を取る (これだけで変わる)**'
    )
    
    content = content.replace(
        '逆に損しない行動はここだ↓',
        '**逆に、カモられない行動はここだ↓**'
    )
    
    # 20. ステップ3の強調
    content = content.replace(
        '### ステップ3: **プロが使う裏ワザ**',
        '### ステップ3: **プロが使う裏ワザ (ここで差がつく)**'
    )
    
    content = content.replace(
        '損しない奴・成功してる奴は全員これやってる。',
        '**カモられない奴・賢い奴は全員これやってる。お前もやれ。**'
    )
    
    # 21. 比較表の前振り強化
    content = content.replace(
        '## 実際どれくらい得するのか',
        '## **実際どれくらい得するのか (数字で見ろ)**'
    )
    
    # 22. 比較表後の強調
    content = re.sub(
        r'つまり、\*\*年間(\d+)万円は確実に守れる可能性がある\*\*。',
        r'**つまり、年間\1万円は確実に守れる。**\n\n' +
        r'**これを知らずに損してる奴が9割。お前は残り1割に入れ。**',
        content
    )
    
    # 23. 金の使い道の強調
    content = content.replace(
        '守った金でタバコ買うもよし、次の投資に回すもよし、貯金して少しマシな生活するもよし。お前の自由だ。',
        '**守った金でタバコ買うもよし、次の投資に回すもよし、貯金して少しマシな生活するもよし。**\n\n' +
        '**とにかく、業者にカモられて終わるな。**'
    )
    
    return content


def main():
    """
    メイン処理: 全98記事を推敲
    """
    print("🔥 Article Polisher - 感情トーン強化推敲")
    print()
    
    # 対象ディレクトリ
    base_dir = Path(__file__).parent.parent / 'gethnote' / 'drafts'
    
    # 全カテゴリフォルダ
    categories = [
        '月曜_ギャンブル金',
        '火曜_ビジネスキャリア',
        '水曜_生活節約',
        '木曜_社会ネット裏事情',
        '金曜_健康美容',
        '土曜_恋愛人間関係',
        '日曜_趣味遊び'
    ]
    
    total_polished = 0
    
    for category in categories:
        cat_dir = base_dir / category
        if not cat_dir.exists():
            print(f"⚠️  {category} フォルダが存在しません")
            continue
        
        # 各カテゴリの記事を推敲
        md_files = sorted(cat_dir.glob('*.md'))
        
        # sample_article除外
        md_files = [f for f in md_files if 'sample_article' not in f.name]
        
        for md_file in md_files:
            # 記事読み込み
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # タイトル抽出
            title_match = re.search(r'# (.+)', content)
            title = title_match.group(1) if title_match else md_file.stem
            
            # 推敲
            polished = polish_article(content, title)
            
            # 文字数比較
            before_len = len(content)
            after_len = len(polished)
            diff = after_len - before_len
            
            # 保存
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(polished)
            
            total_polished += 1
            print(f"✅ [{category[:2]}] {md_file.name[:40]:40s} {before_len}→{after_len} (+{diff})")
    
    print()
    print(f"🎉 推敲完了! {total_polished}記事を強化しました")
    print()
    print("改善内容:")
    print("  - 感情トーン強化 (カモられる、ドブに捨てる)")
    print("  - 煽り追加 (業者の養分、お前次第)")
    print("  - 行動促進強化 (今すぐ動け)")
    print("  - 数値の強調")


if __name__ == '__main__':
    main()
