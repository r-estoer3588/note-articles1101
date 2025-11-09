"""
GETHNOTE記事一括生成スクリプト

master_themes.jsonとgeth_prompt.txtを使って93記事を自動生成。

使い方:
    python generate_articles.py --start 8 --end 100
"""

import json
import re
from pathlib import Path
from typing import Dict, List
import argparse


# 曜日とディレクトリのマッピング
DAY_TO_DIR = {
    "月曜": "月曜_ギャンブル金",
    "火曜": "火曜_ビジネスキャリア",
    "水曜": "水曜_生活節約",
    "木曜": "木曜_社会ネット裏事情",
    "金曜": "金曜_健康美容",
    "土曜": "土曜_恋愛人間関係",
    "日曜": "日曜_趣味遊び"
}

# カテゴリーと曜日のマッピング（14週サイクル）
CATEGORY_TO_DAY_CYCLE = [
    # Week 1 (ID: 1-7) - 既存
    "月曜",  # 1: パチンコ
    "火曜",  # 2: 競馬
    "水曜",  # 3: 節約
    "木曜",  # 4: 詐欺
    "金曜",  # 5: ダイエット
    "土曜",  # 6: 恋愛
    "日曜",  # 7: ゲーム
    
    # Week 2 (ID: 8-14)
    "月曜",  # 8: 年金 (A)
    "火曜",  # 9: 退職 (B)
    "水曜",  # 10: 副業 (B)
    "木曜",  # 11: 税金 (A)
    "金曜",  # 12: 起業 (B)
    "土曜",  # 13: 旅行 (E)
    "日曜",  # 14: FX (A)
]


def load_themes(themes_path: Path) -> Dict:
    """master_themes.jsonを読み込み"""
    with open(themes_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_article_day(article_id: int) -> str:
    """記事IDから曜日を取得（7日サイクル）"""
    day_index = (article_id - 1) % 7
    days = ["月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]
    return days[day_index]


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


def generate_article_content(theme: Dict, article_id: int, next_theme: Dict = None) -> str:
    """記事本文を生成
    
    実際の生成はGitHub Copilotが行うため、ここではテンプレートを返す
    """
    title = f"【{theme['title']}】"
    
    # 次回予告テキスト
    next_preview = ""
    if next_theme:
        next_preview = next_theme['title']
    
    # 記事テンプレート（簡略版 - 実際はgeth_prompt.txtの仕様に従う）
    content = f"""# {title}

これ、マジの話な。

[ここに導入文を追加]

---

## お前、これ知ってた？

[ここにチェックリストを追加]

---

## 続きは有料だけど...

この先は、**さらにヤバい裏話**を晒す。

**この記事で分かること:**

✅ [ポイント1]
✅ [ポイント2]
✅ [ポイント3]

全部読めば**[具体的な金額/効果]**。

---

タバコ1箱分(300円)で読める。

300円ケチって損するバカになるか、300円払って得するか。

お前次第。

---

---

## 【有料部分】¥300

おう、300円払ったな。賢い選択だ。

ここから先は、[テーマ]の裏側を晒す。

---

## [メインコンテンツ1]

[ここに詳細内容を追加]

---

## [メインコンテンツ2]

[ここに詳細内容を追加]

---

## 実際どれくらい得する？

| 項目 | Before | After | 差額 |
|------|--------|-------|------|
| [項目1] | [金額] | [金額] | **+[金額]** |

---

## 最後に

周りのバカどもは、損し続けてる。

でも、**お前は違う**。

この記事読んだだけで「[スキル/知識]を持つ奴」になった。

お前は賢い選択をした。周りのバカどもに差をつけろ。

---

## 次回予告 × フォロー特典

次は「{next_preview}」を公開する。

知らないと[損失額]損するぞ。公開は**[曜日]12時**。見逃すな。

---

### フォロー特典

Twitterフォローしてくれた人には次回記事を**100円引き**で読めるクーポン配布

[@gethinu](https://x.com/gethinu)をフォロー → DMで「クーポン」と送る → GET

---

## 👤 このマガジンについて

**げすいぬ | 底辺脱出マガジン**

底辺から這い上がる情報を晒してる📢

このマガジンでは、タバコ1箱分（300円）で読める有料記事を毎日配信🔥

📅 **月曜**: ギャンブル・金💰  
📅 **火曜**: ビジネス・キャリア💼  
📅 **水曜**: 生活・節約🏠  
📅 **木曜**: 社会・ネット裏事情🌐  
📅 **金曜**: 健康・美容💪  
📅 **土曜**: 恋愛・人間関係💕  
📅 **日曜**: 趣味・遊び🎮

周りのバカどもは損し続けてる。
お前は違う。

🔗 **X(Twitter)**: [@gethinu](https://x.com/gethinu)  
📝 **note**: [げすいぬ | 底辺脱出マガジン](https://note.com/geth_note)

---

*※この記事は一般的な情報提供を目的としています。*

---

#げすいぬ #GETH #底辺脱出
"""
    
    return content


def generate_articles(start_id: int, end_id: int, themes_path: Path, output_dir: Path):
    """記事を一括生成
    
    Args:
        start_id: 開始記事ID
        end_id: 終了記事ID
        themes_path: master_themes.jsonのパス
        output_dir: 出力先ディレクトリ（drafts/）
    """
    themes_data = load_themes(themes_path)
    
    print(f"📚 記事生成開始: ID {start_id} - {end_id}")
    
    for article_id in range(start_id, end_id + 1):
        theme = get_theme_by_id(themes_data, article_id)
        if not theme:
            print(f"⚠️  ID {article_id}: テーマが見つかりません")
            continue
        
        # 次の記事のテーマを取得
        next_theme = get_theme_by_id(themes_data, article_id + 1)
        
        # 曜日を取得
        day = get_article_day(article_id)
        day_dir = DAY_TO_DIR[day]
        
        # ファイル名を生成
        theme_name_clean = re.sub(r'[【】\s]', '', theme['title'])
        theme_name_clean = theme_name_clean[:20]  # 長すぎる場合は短縮
        filename = f"{theme_name_clean}_{article_id:03d}.md"
        
        # 出力パス
        output_path = output_dir / day_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 記事生成
        content = generate_article_content(theme, article_id, next_theme)
        
        # ファイルに書き込み
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ [{article_id:3d}] {day} - {theme['title']}")
    
    print(f"\n🎉 完了！ {end_id - start_id + 1}記事を生成しました")
    print(f"📁 出力先: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="GETHNOTE記事一括生成")
    parser.add_argument("--start", type=int, default=8, help="開始記事ID")
    parser.add_argument("--end", type=int, default=100, help="終了記事ID")
    parser.add_argument(
        "--themes",
        type=str,
        default="../gethnote/themes/master_themes.json",
        help="master_themes.jsonのパス"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../gethnote/drafts",
        help="出力先ディレクトリ"
    )
    
    args = parser.parse_args()
    
    themes_path = Path(args.themes)
    output_dir = Path(args.output)
    
    if not themes_path.exists():
        print(f"❌ エラー: {themes_path} が見つかりません")
        return
    
    generate_articles(args.start, args.end, themes_path, output_dir)


if __name__ == "__main__":
    main()
