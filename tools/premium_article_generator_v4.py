#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Premium Article Generator V4 - factsを加工せず直接表示
NG/OK抽出ロジックを廃止し、データをそのまま記事に埋め込む
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def find_topic_by_title(title: str, category_data: Dict) -> Dict:
    """
    タイトルから対応するtopicを検索
    """
    # キーワードマッピング (V3と同じ)
    keyword_map = {
        'パチ': ['パチンコ', 'パチスロ'],
        'FX': ['FX(裁量)', 'FX'],
        '節税': ['節税・税金対策'],
        '履歴書': ['履歴書・職務経歴書'],
        '昇進': ['昇進・出世'],
        'ダイエット': ['ダイエット'],
        '美容医療': ['美容医療・整形'],
        'アンチエイジング': ['アンチエイジング'],
        'LINE': ['LINE・SNS'],
        'ご近所': ['ご近所トラブル'],
        '買い物': ['買い物術'],
        '音楽': ['音楽ストリーミング'],
        '趣味グッズ': ['趣味グッズ'],
        'SNS炎上': ['SNS炎上'],
        'ポイント': ['ポイント活用']
    }
    
    # タイトルからキーワード抽出
    for keyword, topics in keyword_map.items():
        if keyword in title:
            # category_dataからtopicを検索
            for item in category_data.get('data', []):
                if item.get('topic') in topics:
                    return item
    
    # デフォルト (最初のtopic)
    if category_data.get('data'):
        return category_data['data'][0]
    
    return {'topic': 'Unknown', 'facts': []}


def extract_loss_amount(facts: List[str]) -> int:
    """
    factsから損失額を抽出 (年間○○万円)
    """
    for fact in facts:
        match = re.search(r'[-年間]+([0-9]+)万', fact)
        if match:
            return int(match.group(1))
    return 100  # デフォルト


def generate_premium_article_v4(
    article_id: int,
    title: str,
    day: str,
    category_data: Dict,
    next_article_title: str = None
) -> str:
    """
    V4: factsをそのまま表示する戦略
    - NG/OK抽出ロジック廃止
    - facts[0-4]を直接箇条書き
    - 比較表もfact文字列そのまま
    """
    
    # トピック検索
    topic_data = find_topic_by_title(title, category_data)
    facts = topic_data.get('facts', [])
    
    if not facts:
        facts = ['データなし'] * 5
    
    # 損失額抽出
    loss_amount = extract_loss_amount(facts)
    
    # facts最低5個確保
    while len(facts) < 5:
        facts.append(facts[0] if facts else 'データ収集中')
    
    # 記事本体生成
    article = f"""# {title}

---

## 【無料部分】タバコ1本吸う間に読める

俺は昔、知らずに年間{loss_amount}万円損してた。

でもある**3つのポイント**に気づいただけで、今は損しなくなった。

その3つのうち、**1つだけ無料で公開する**。

---

## ポイント① あなたの知らない損失

**理由:** 知識がないと確実に損する

実際のデータを見てくれ↓

### あなたが気づいていない損失

"""
    
    # facts を箇条書きで全部表示
    for i, fact in enumerate(facts[:5], 1):
        article += f"**{i}.** {fact}\n\n"
    
    article += f"""
つまり、知らないだけで**年間{loss_amount}万円以上損する**可能性がある。

---

俺も昔は知らなくて大損した。

でも「データを知って行動を変える」だけで人生変わった。マジで。

---

### お前も当てはまってないか？

・業者/他人の言いなり  
・比較検討しない  
・最新情報を知らない

全部**カモフラグ**だぞ。

---

## 残り2つも知りたい？

無料で公開したのは**ポイント①だけ**。

残り2つのポイントを知れば、**年間{loss_amount}万円は確実に守れる**。

---

タバコ1箱分(300円)で読める。

300円ケチって今年も{loss_amount}万円損するか、300円払って守るか。

お前次第。

---

---

## 【有料部分】¥300

おう、300円払ったな。賢い選択だ。

ここから先は本当にヤバい裏側を晒す。

---

## なんでこんなに損する奴が多いのか

{title}の裏事情、知ってるか?

### 業界が隠したがる事実

"""
    
    # 業界裏話 (facts[1], facts[2])
    if len(facts) > 1:
        article += f"**{facts[1]}**\n\n"
    if len(facts) > 2:
        article += f"**{facts[2]}**\n\n"
    
    article += """
業者・インフルエンサー・詐欺師は、お前が無知なまま損してくれた方が儲かる。
だから公式には絶対に教えない情報がある。

「お客様第一」とか言いながら、実は手数料ボッタクリ商品を売りつけてる。

ガチでエグい。

---

## じゃあどうすればいいのか

### ステップ1: **損失パターンを避ける**

以下のパターンは確実に損する↓

"""
    
    # 損失パターン (facts[0], facts[3], facts[4])
    article += f"❌ **パターン①:** {facts[0]}\n\n"
    if len(facts) > 3:
        article += f"❌ **パターン②:** {facts[3]}\n\n"
    if len(facts) > 4:
        article += f"❌ **パターン③:** {facts[4]}\n\n"
    
    article += f"""
これらを避けるだけで**年間{loss_amount}万円は守れる**。マジで。

---

### ステップ2: **正しい行動を取る**

逆に損しない行動はここだ↓

⭕ **行動①: データを知る**  
→ 上記の損失パターンを全部頭に入れる

⭕ **行動②: 3社以上比較する**  
→ 面倒くさがらずに比較。それだけで半額になることも

⭕ **行動③: 最新情報を常にチェック**  
→ 制度・トレンドは毎年変わる。古い知識は損する

この3つを守れば**年間{loss_amount}万円は確実に守れる**。
俺も実際に試して損しなくなった。

---

### ステップ3: **プロが使う裏ワザ**

損しない奴・成功してる奴は全員これやってる。

**1. 業者の提案を鵜呑みにしない**  
→ セカンドオピニオン必須。専門家・経験者に相談

**2. キャンペーン・特典・裏技を徹底活用**  
→ 時期・方法によっては数万~数十万円の差がつく

**3. 定期的に見直す(年1回は必須)**  
→ 契約・習慣したら終わりじゃない。毎年最適化しろ

この3つを満たせばさらに年{int(loss_amount * 0.5)}万円浮く。
俺はこれで年間トータル{int(loss_amount * 1.5)}万円守ってる。ガチで。

---

## 実際どれくらい得するのか

| 項目 | 損失額 |
|------|--------|
"""
    
    # 比較表 (facts そのまま表示)
    for i, fact in enumerate(facts[:3], 1):
        article += f"| {fact[:20]}... | 確認推奨 |\n"
    
    article += f"""| **年間合計** | **約{loss_amount}万円の損失リスク** |

つまり、**年間{loss_amount}万円は確実に守れる可能性がある**。

守った金でタバコ買うもよし、次の投資に回すもよし、貯金して少しマシな生活するもよし。お前の自由だ。

---

## 最後に

周りのバカどもは知らずに損し続けてる。

でもこれを読んだお前は違う。

**年間{loss_amount}万円守る知識**を手に入れた。

あとは行動するだけ。

---

300円払ったのはデカい投資だ。

今年は絶対に損するな。

---
"""
    
    # 次回予告
    if next_article_title:
        article += f"""
## 次回予告

次は「{next_article_title}」で、さらにヤバい裏側を暴露する。

また300円で読める。楽しみに待ってろ。

---
"""
    
    return article


def main():
    """
    メイン処理: 月曜カテゴリ15記事生成
    """
    print("🔥 Premium Article Generator V4 - データ直接表示")
    print()
    print("改善点:")
    print("- NG/OK抽出ロジック廃止")
    print("- factsをそのまま箇条書き表示")
    print("- 比較表もfact文字列そのまま使用")
    print()
    
    # データ読み込み
    data_file = Path(__file__).parent / 'data_collection_output.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    # 月曜カテゴリ (ギャンブル・金)
    category_data = all_data[0]  # 最初のカテゴリ
    
    print(f"📅 カテゴリ: {category_data['category']}")
    print(f"📝 記事数: 15")
    print(f"💾 データ: {len(category_data['data'])} トピック")
    print()
    
    # 記事タイトル (月曜)
    monday_titles = [
        (1, "【パチで負ける台の見分け方】"),
        (8, "【FXで絶対やってはいけないこと】"),
        (15, "【節税で逆に損する方法】"),
        (22, "【履歴書・職務経歴書で損する書き方】"),
        (29, "【昇進で損する働き方】"),
        (36, "【ダイエットで絶対失敗する食事法】"),
        (43, "【美容医療で失敗するクリニック選び】"),
        (50, "【アンチエイジングで損する習慣】"),
        (57, "【LINE・SNSで嫌われるメッセージ】"),
        (64, "【ご近所トラブルで絶対やってはいけないこと】"),
        (71, "【知らないと損する買い物の裏ワザ】"),
        (78, "【音楽ストリーミングで損しない聴き方】"),
        (85, "【趣味グッズ購入で損しないチェックリスト】"),
        (92, "【SNS炎上で絶対やってはいけない返信】"),
        (99, "【誰も教えてくれないポイント活用法】")
    ]
    
    # 出力ディレクトリ
    output_dir = Path(__file__).parent.parent / 'gethnote' / 'drafts' / '月曜_ギャンブル金'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 記事生成
    for i, (article_id, title) in enumerate(monday_titles):
        next_title = monday_titles[i + 1][1] if i + 1 < len(monday_titles) else None
        
        article = generate_premium_article_v4(
            article_id=article_id,
            title=title,
            day='月曜',
            category_data=category_data,
            next_article_title=next_title
        )
        
        # ファイル保存
        filename = f"{article_id:03d}_{title.replace('【', '').replace('】', '')}.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article)
        
        char_count = len(article)
        print(f"✅ [ID {article_id:3d}] {title} ({char_count}文字)")
    
    print()
    print(f"🎉 完了! 生成: {len(monday_titles)}/{len(monday_titles)}")


if __name__ == '__main__':
    main()
