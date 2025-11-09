"""
meta.json & x-posts.txt 一括生成スクリプト

全記事のメタ情報とX投稿テンプレートを自動生成。

使い方:
    python generate_meta_and_xposts.py --start 8 --end 100
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional
import argparse


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


def load_themes(themes_path: Path) -> Dict:
    """master_themes.jsonを読み込み"""
    with open(themes_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_theme_by_id(themes_data: Dict, theme_id: int) -> Optional[Dict]:
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


def extract_title_from_markdown(md_path: Path) -> str:
    """Markdownファイルからタイトルを抽出"""
    if not md_path.exists():
        return ""
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 最初の#見出しを探す
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    return md_path.stem


def count_words_in_markdown(md_path: Path) -> Dict[str, int]:
    """Markdownファイルの文字数をカウント"""
    if not md_path.exists():
        return {"free": 0, "paid": 0, "total": 0}
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 有料部分の区切りを検出
    paid_match = re.search(
        r'#+\s*【有料部分】',
        content,
        re.IGNORECASE | re.MULTILINE
    )
    
    if paid_match:
        free_part = content[:paid_match.start()]
        paid_part = content[paid_match.start():]
        
        # Markdown記号を除外して文字数カウント
        free_count = len(re.sub(r'[#*\-\[\]()_`]', '', free_part))
        paid_count = len(re.sub(r'[#*\-\[\]()_`]', '', paid_part))
        total_count = free_count + paid_count
    else:
        total_count = len(re.sub(r'[#*\-\[\]()_`]', '', content))
        free_count = total_count
        paid_count = 0
    
    return {
        "free": free_count,
        "paid": paid_count,
        "total": total_count
    }


def generate_meta_json(
    article_id: int,
    theme: Dict,
    next_theme: Optional[Dict],
    md_path: Path
) -> Dict:
    """meta.jsonの内容を生成"""
    
    title = extract_title_from_markdown(md_path)
    if not title:
        title = f"【{theme['title']}】"
    
    day = get_article_day(article_id)
    category = get_category_from_day(day)
    
    # 次回記事情報
    next_article = None
    if next_theme:
        next_day = get_article_day(article_id + 1)
        next_article = {
            "id": article_id + 1,
            "preview_text": next_theme['title'],
            "publish_day": f"{next_day}12時"
        }
    
    # 文字数カウント
    word_count = count_words_in_markdown(md_path)
    
    meta = {
        "id": article_id,
        "title": title,
        "price": 300,
        "category": category,
        "day_of_week": day,
        "status": "draft",
        "word_count": word_count,
        "tags": [
            "げすいぬ",
            "GETH",
            "底辺脱出",
            theme['title'][:10]
        ],
        "note_url": "",
        "published_date": "",
        "next_article": next_article
    }
    
    return meta


def generate_x_post(
    article_id: int,
    theme: Dict,
    title: str
) -> str:
    """X投稿テンプレートを生成"""
    
    # タイトルから【】を除去
    clean_title = re.sub(r'[【】]', '', title)
    
    template = f"""【マジでヤバい😱】

{clean_title}

これ知らないと年間○万円損してるわ…

周りのバカどもは気づいてない

続きは↓
{{NOTE_URL}}

※300円だけど
タバコ1箱ガマンすれば読める

#損回避 #裏ワザ #げすいぬ #{theme['title'][:8]}
"""
    
    return template.strip()


def generate_files(
    start_id: int,
    end_id: int,
    themes_path: Path,
    drafts_dir: Path,
    meta_dir: Path,
    xposts_dir: Path
):
    """meta.jsonとx-posts.txtを一括生成"""
    
    themes_data = load_themes(themes_path)
    
    print(f"📚 メタファイル生成開始: ID {start_id} - {end_id}")
    
    # ディレクトリ作成
    meta_dir.mkdir(parents=True, exist_ok=True)
    xposts_dir.mkdir(parents=True, exist_ok=True)
    
    for article_id in range(start_id, end_id + 1):
        theme = get_theme_by_id(themes_data, article_id)
        if not theme:
            print(f"⚠️  ID {article_id}: テーマが見つかりません")
            continue
        
        next_theme = get_theme_by_id(themes_data, article_id + 1)
        
        # Markdownファイルパスを特定
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
        
        # Markdownファイルを探す
        md_dir = drafts_dir / day_dir
        md_files = list(md_dir.glob(f"*{article_id:03d}.md"))
        
        if not md_files:
            print(f"⚠️  ID {article_id}: Markdownファイルが見つかりません")
            continue
        
        md_path = md_files[0]
        
        # meta.json生成
        meta_content = generate_meta_json(
            article_id,
            theme,
            next_theme,
            md_path
        )
        
        # ファイル名生成（記事名から）
        theme_name_clean = re.sub(r'[【】\s]', '', theme['title'])
        theme_name_clean = theme_name_clean[:20]
        
        meta_filename = f"{day}_{theme_name_clean}_meta.json"
        meta_path = meta_dir / meta_filename
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_content, f, ensure_ascii=False, indent=2)
        
        # x-posts.txt生成
        title = meta_content['title']
        xpost_content = generate_x_post(article_id, theme, title)
        
        xpost_filename = f"{day}_{theme_name_clean}_x投稿.txt"
        xpost_path = xposts_dir / xpost_filename
        
        with open(xpost_path, 'w', encoding='utf-8') as f:
            f.write(xpost_content)
        
        print(f"✅ [{article_id:3d}] {day} - {theme['title']}")
    
    print(f"\n🎉 完了！ {end_id - start_id + 1}件のメタファイルを生成")
    print(f"📁 meta: {meta_dir}")
    print(f"📁 x-posts: {xposts_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="meta.json & x-posts.txt 一括生成"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=8,
        help="開始記事ID"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=100,
        help="終了記事ID"
    )
    parser.add_argument(
        "--themes",
        type=str,
        default="../gethnote/themes/master_themes.json",
        help="master_themes.jsonのパス"
    )
    parser.add_argument(
        "--drafts",
        type=str,
        default="../gethnote/drafts",
        help="draftsディレクトリ"
    )
    parser.add_argument(
        "--meta",
        type=str,
        default="../gethnote/meta",
        help="metaディレクトリ"
    )
    parser.add_argument(
        "--xposts",
        type=str,
        default="../gethnote/x-posts",
        help="x-postsディレクトリ"
    )
    
    args = parser.parse_args()
    
    themes_path = Path(args.themes)
    drafts_dir = Path(args.drafts)
    meta_dir = Path(args.meta)
    xposts_dir = Path(args.xposts)
    
    if not themes_path.exists():
        print(f"❌ エラー: {themes_path} が見つかりません")
        return
    
    if not drafts_dir.exists():
        print(f"❌ エラー: {drafts_dir} が見つかりません")
        return
    
    generate_files(
        args.start,
        args.end,
        themes_path,
        drafts_dir,
        meta_dir,
        xposts_dir
    )


if __name__ == "__main__":
    main()
