#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
No.100-113の14記事を一括投稿
"""

from pathlib import Path
import time


# 投稿する記事リスト
ARTICLES = [
    {
        "id": 100,
        "title": "NISAで損する銘柄選び",
        "tags": ["NISA", "投資信託", "金融", "資産運用", "初心者向け"],
        "price": 300,
    },
    {
        "id": 101,
        "title": "iDeCoで損する運用方法",
        "tags": ["iDeCo", "年金", "老後資金", "資産運用", "税金"],
        "price": 300,
    },
    {
        "id": 102,
        "title": "投資信託で損する選び方",
        "tags": ["投資信託", "資産運用", "手数料", "インデックス", "アクティブ"],
        "price": 300,
    },
    {
        "id": 103,
        "title": "住宅ローンで損する組み方",
        "tags": ["住宅ローン", "不動産", "金利", "変動金利", "固定金利"],
        "price": 300,
    },
    {
        "id": 104,
        "title": "生命保険で損する入り方",
        "tags": ["生命保険", "保険", "掛け捨て", "貯蓄型", "保険料"],
        "price": 300,
    },
    {
        "id": 105,
        "title": "ふるさと納税で損する選び方",
        "tags": ["ふるさと納税", "節税", "控除", "ワンストップ特例", "確定申告"],
        "price": 300,
    },
    {
        "id": 106,
        "title": "暗号資産で詐欺に遭う買い方",
        "tags": ["暗号資産", "仮想通貨", "詐欺", "投資", "ビットコイン"],
        "price": 300,
    },
    {
        "id": 107,
        "title": "副業で税務調査される申告方法",
        "tags": ["副業", "確定申告", "税務調査", "雑所得", "青色申告"],
        "price": 300,
    },
    {
        "id": 108,
        "title": "フリーランスで損する独立準備",
        "tags": ["フリーランス", "独立", "国民年金", "健康保険", "社会保険"],
        "price": 300,
    },
    {
        "id": 109,
        "title": "金融詐欺に騙される人の特徴",
        "tags": ["詐欺", "投資詐欺", "特殊詐欺", "SNS詐欺", "防犯"],
        "price": 300,
    },
    {
        "id": 110,
        "title": "相続で家族が揉める対策不足",
        "tags": ["相続", "相続税", "遺産分割", "遺言", "家族トラブル"],
        "price": 300,
    },
    {
        "id": 111,
        "title": "法人設立で損する設立方法",
        "tags": ["法人設立", "会社設立", "起業", "登記", "税理士"],
        "price": 300,
    },
    {
        "id": 112,
        "title": "電子マネーで損する使い方",
        "tags": ["電子マネー", "キャッシュレス", "ポイント", "QR決済", "クレカ"],
        "price": 300,
    },
    {
        "id": 113,
        "title": "クレカで損する選び方",
        "tags": ["クレジットカード", "年会費", "ポイント還元", "リボ払い", "審査"],
        "price": 300,
    },
]


def create_batch_post_list():
    """
    一括投稿用のリストを作成
    """
    print("📝 No.100-113 一括投稿リスト\n")
    print("=" * 70)
    
    draft_dir = Path(__file__).parent.parent / 'gethnote' / 'drafts' / '月曜_ギャンブル金'
    
    for article in ARTICLES:
        article_id = article['id']
        title = article['title']
        tags = ', '.join(article['tags'])
        price = article['price']
        
        # ファイルパス
        filename = f"{article_id:03d}_{title}.md"
        filepath = draft_dir / filename
        
        if not filepath.exists():
            print(f"❌ [{article_id:03d}] {title} - ファイルなし")
            continue
        
        # 文字数確認
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        char_count = len(content)
        
        print(f"\n【記事 {article_id}】")
        print(f"タイトル: {title}")
        print(f"タグ: {tags}")
        print(f"価格: ¥{price}")
        print(f"文字数: {char_count}文字")
        print(f"ファイル: {filename}")
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print(f"\n✅ 合計: {len(ARTICLES)}記事")
    print(f"   価格: ¥300 × {len(ARTICLES)} = ¥{300 * len(ARTICLES)}")
    
    # 総文字数計算
    total_chars = 0
    for a in ARTICLES:
        filename = f"{a['id']:03d}_{a['title']}.md"
        filepath = draft_dir / filename
        if filepath.exists():
            total_chars += len(filepath.read_text(encoding='utf-8'))
    
    print(f"   総文字数: 約{total_chars}文字")


def export_for_note():
    """
    note投稿用にエクスポート
    """
    print("\n\n📤 note投稿用データ出力\n")
    
    output_dir = Path(__file__).parent.parent / 'gethnote' / 'ready_to_post'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # メタデータCSV出力
    csv_path = output_dir / 'articles_100-113_metadata.csv'
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("記事ID,タイトル,価格,タグ,ファイル名\n")
        
        for article in ARTICLES:
            article_id = article['id']
            title = article['title']
            tags = '|'.join(article['tags'])
            price = article['price']
            filename = f"{article_id:03d}_{title}.md"
            
            f.write(f"{article_id},{title},{price},{tags},{filename}\n")
    
    print(f"✅ メタデータCSV: {csv_path}")
    
    # 投稿順リスト
    list_path = output_dir / 'post_order_100-113.txt'
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write("# No.100-113 投稿順序\n\n")
        
        for i, article in enumerate(ARTICLES, start=1):
            f.write(f"{i}. [{article['id']:03d}] {article['title']}\n")
    
    print(f"✅ 投稿順リスト: {list_path}")
    
    # 一括投稿用バッチファイル (参考)
    batch_path = output_dir / 'batch_post_note.md'
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write("# No.100-113 一括投稿手順\n\n")
        f.write("## 📋 投稿チェックリスト\n\n")
        
        for article in ARTICLES:
            f.write(f"- [ ] [{article['id']:03d}] {article['title']}\n")
        
        f.write("\n## 📝 共通設定\n\n")
        f.write("- 価格: ¥300\n")
        f.write("- カテゴリ: 月曜_ギャンブル金\n")
        f.write("- 公開設定: 有料部分あり\n")
        f.write("- ハッシュタグ: 各記事のタグ参照\n")
        
        f.write("\n## 🎯 投稿時の注意点\n\n")
        f.write("1. **データ出典を確認**: 全て公的機関データ\n")
        f.write("2. **価格設定**: 必ず¥300に設定\n")
        f.write("3. **有料ライン**: `---` 後の「【有料部分】¥300」から\n")
        f.write("4. **タグ**: 各記事5個のタグを設定\n")
        f.write("5. **プレビュー確認**: 表示崩れチェック\n")
    
    print(f"✅ 投稿手順: {batch_path}")
    
    print(f"\n📁 出力先: {output_dir}")


def main():
    """
    メイン処理
    """
    print("🚀 No.100-113 一括投稿準備ツール")
    print()
    
    # リスト表示
    create_batch_post_list()
    
    # エクスポート
    export_for_note()
    
    print("\n" + "=" * 70)
    print("\n🎉 準備完了!")
    print("\n次のステップ:")
    print("  1. gethnote/ready_to_post/ 内のファイルを確認")
    print("  2. 各記事ファイルをnoteにコピペ")
    print("  3. タグと価格を設定")
    print("  4. プレビュー確認後に公開")
    print("\n💡 Tip: メタデータCSVを参照してタグ設定を効率化")


if __name__ == '__main__':
    main()
