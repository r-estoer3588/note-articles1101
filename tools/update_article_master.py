"""
article_master.json更新スクリプト

全100記事をarticle_master.jsonに登録。

使い方:
    python update_article_master.py
"""

import json
from pathlib import Path
from typing import Dict, List


def load_themes(themes_path: Path) -> Dict:
    """master_themes.jsonを読み込み"""
    with open(themes_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_theme_by_id(themes_data: Dict, theme_id: int) -> Dict:
    """テーマIDからテーマ情報を取得"""
    for category_key, category_data in themes_data["categories"].items():
        if "themes" in category_data:
            for theme in category_data["themes"]:
                if theme["id"] == theme_id:
                    return theme
        elif "sub_categories" in category_data:
            for sub_cat_data in category_data["sub_categories"].values():
                for theme in sub_cat_data["themes"]:
                    if theme["id"] == theme_id:
                        return theme
    return None


def get_article_day(article_id: int) -> str:
    """記事IDから曜日を取得"""
    day_index = (article_id - 1) % 7
    days = ["月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]
    return days[day_index]


def get_category_from_day(day: str) -> str:
    """曜日からカテゴリーを取得"""
    mapping = {
        "月曜": "ギャンブル・金💰",
        "火曜": "ビジネス・キャリア💼",
        "水曜": "生活・節約🏠",
        "木曜": "社会・ネット裏事情🌐",
        "金曜": "健康・美容💪",
        "土曜": "恋愛・人間関係💕",
        "日曜": "趣味・遊び🎮"
    }
    return mapping[day]


def get_file_path_from_id(article_id: int, theme: Dict) -> str:
    """記事IDからファイルパスを生成"""
    day = get_article_day(article_id)
    day_dir_map = {
        "月曜": "月曜_ギャンブル金",
        "火曜": "火曜_ビジネスキャリア",
        "水曜": "水曜_生活節約",
        "木曜": "木曜_社会ネット裏事情",
        "金曜": "金曜_健康美容",
        "土曜": "土曜_恋愛人間関係",
        "日曜": "日曜_趣味遊び"
    }
    
    day_dir = day_dir_map[day]
    theme_name = theme['title'].replace('【', '').replace('】', '').strip()
    theme_name = theme_name[:20]  # 長い場合は短縮
    
    return f"{day_dir}/{theme_name}_{article_id:03d}"


def update_article_master(
    themes_path: Path,
    master_path: Path
):
    """article_master.jsonを更新"""
    
    themes_data = load_themes(themes_path)
    
    # 既存のarticle_master.jsonを読み込み
    if master_path.exists():
        with open(master_path, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
    else:
        master_data = {
            "project": "GETHNOTE",
            "target": "100記事",
            "current_count": 0,
            "articles": [],
            "next_article_id": 1,
            "notes": [
                "next_preview は次回記事の実際のタイトルから一部抜粋",
                "記事作成時は必ずこのリストを参照して next_preview を設定",
                "新記事追加時は最新のidを確認してインクリメント"
            ]
        }
    
    # 既存記事のIDリスト
    existing_ids = {article["id"] for article in master_data["articles"]}
    
    print(f"📚 article_master.json更新開始")
    print(f"既存記事数: {len(existing_ids)}")
    
    new_articles = []
    
    for article_id in range(1, 101):
        if article_id in existing_ids:
            continue  # 既存記事はスキップ
        
        theme = get_theme_by_id(themes_data, article_id)
        if not theme:
            print(f"⚠️  ID {article_id}: テーマが見つかりません")
            continue
        
        # 次の記事のテーマを取得
        next_theme = get_theme_by_id(themes_data, article_id + 1)
        next_preview = next_theme['title'] if next_theme else ""
        
        day = get_article_day(article_id)
        category = get_category_from_day(day)
        file_path = get_file_path_from_id(article_id, theme)
        
        article = {
            "id": article_id,
            "day": day,
            "category": category,
            "title": f"【{theme['title']}】",
            "file": file_path,
            "status": "draft",
            "note_url": "",
            "published_date": "",
            "next_preview": next_preview
        }
        
        new_articles.append(article)
        print(f"✅ [{article_id:3d}] {day} - {theme['title']}")
    
    # 新記事を追加
    master_data["articles"].extend(new_articles)
    
    # IDでソート
    master_data["articles"].sort(key=lambda x: x["id"])
    
    # 統計更新
    master_data["current_count"] = len(master_data["articles"])
    master_data["next_article_id"] = 101
    
    # 保存
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 完了！")
    print(f"総記事数: {master_data['current_count']}")
    print(f"新規追加: {len(new_articles)}記事")
    print(f"📁 保存先: {master_path}")


def main():
    themes_path = Path("../gethnote/themes/master_themes.json")
    master_path = Path("../gethnote/article_master.json")
    
    if not themes_path.exists():
        print(f"❌ エラー: {themes_path} が見つかりません")
        return
    
    update_article_master(themes_path, master_path)


if __name__ == "__main__":
    main()
