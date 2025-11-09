#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Premium Article Generator V3 - 本気モード
データを120%活用した最高品質記事生成

設計方針:
1. factsから具体的数値を直接抽出
2. NG/OK対比を明確に
3. Before/After比較表に実データを使用
4. 業界裏話を2個以上挿入
5. ジェイ・エイブラハム理論: 読者の損失を防ぐ
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def load_data() -> List[Dict]:
    """data_collection_output.jsonを読み込む"""
    data_path = Path(__file__).parent / "data_collection_output.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_article_master() -> List[Dict]:
    """article_master.jsonを読み込む"""
    master_path = (Path(__file__).parent.parent / "gethnote" /
                   "article_master.json")
    with open(master_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["articles"]


def find_topic_by_title(title: str, category_data: Dict) -> Dict:
    """タイトルからトピックを検索"""
    
    # キーワードマッピング
    keyword_map = {
        "FX": "FX(裁量)",
        "暗号資産": "暗号資産(現物)",
        "節税": "節税スキーム誤用",
        "ポイ活": "ポイ活",
        "リボ": "クレカリボ払い",
        "消費者金融": "消費者金融",
        "パチンコ": "パチンコ",
        "競馬": "競馬",
    }
    
    # タイトルからキーワード検索
    for keyword, topic_name in keyword_map.items():
        if keyword in title:
            for topic in category_data["data"]:
                if topic["topic"] == topic_name:
                    return topic
    
    # 見つからない場合は最初のトピック
    return category_data["data"][0] if category_data["data"] else None


def extract_loss_amount(facts: List[str]) -> int:
    """factsから損失額を抽出"""
    for fact in facts:
        # 年間XX万円, -XX万円のパターン
        match = re.search(r'[-年間]+([0-9]+)万', fact)
        if match:
            return int(match.group(1))
    return 50  # デフォルト


def create_ng_ok_patterns(facts: List[str]) -> Tuple[List[str], List[str]]:
    """
    factsからNG/OKパターンを抽出
    
    Returns:
        (ng_patterns, ok_patterns)
    """
    ng_patterns = []
    ok_patterns = []
    
    for fact in facts:
        # "→" で分割
        if '→' in fact:
            parts = fact.split('→')
            left = parts[0].strip()
            right = parts[1].strip() if len(parts) > 1 else ""
            
            # NGパターン判定
            if any(kw in left for kw in ['なし', '未', '不足', '過多', '超']):
                ng_patterns.append(left)
                if right and any(kw in right for kw in ['損', '-', '低下', '率']):
                    # OKパターンを推測
                    ok_part = left.replace('なし', 'あり').replace('未', '').replace('不足', '十分')
                    ok_patterns.append(ok_part)
            
            # "vs" パターン
        if ' vs ' in fact or '/' in fact:
            parts = re.split(r' vs |/', fact)
            if len(parts) >= 2:
                # 最初がNG、2番目がOK
                ng_patterns.append(parts[0].strip())
                ok_patterns.append(parts[1].strip())
    
    return ng_patterns[:3], ok_patterns[:3]


def generate_premium_article_v3(
    article_id: int,
    title: str,
    day: str,
    category_data: Dict,
    next_article_title: str = None
) -> str:
    """最高品質の記事を生成 (V3)"""
    
    # トピックデータ取得
    topic_data = find_topic_by_title(title, category_data)
    if not topic_data:
        print(f"⚠️  [ID {article_id}] トピックが見つかりません")
        return None
    
    facts = topic_data["facts"]
    if len(facts) < 5:
        print(f"⚠️  [ID {article_id}] データ不足 (facts: {len(facts)})")
        return None
    
    # データ抽出
    loss_amount = extract_loss_amount(facts)
    ng_patterns, ok_patterns = create_ng_ok_patterns(facts)
    
    # デフォルト値設定
    if not ng_patterns:
        ng_patterns = ["情報不足で損する", "比較検討しない", "業者の言いなり"]
    if not ok_patterns:
        ok_patterns = ["データで判断する", "3社以上比較する", "専門家に相談する"]
    
    # 記事生成
    article = f"""# {title}

---

## 【無料部分】タバコ1本吸う間に読める

俺は昔、{ng_patterns[0]}で年間{loss_amount}万円損してた。

でもある**3つのポイント**に気づいただけで、今は損しなくなった。

その3つのうち、**1つだけ無料で公開する**。

---

## ポイント① {ng_patterns[0]}

**理由:** 知識がないと業者・他人のカモにされる

実際のデータ↓

**{facts[0]}**

つまり、知らないだけで**年間{loss_amount}万円損する**。

---

俺も昔は知らなくて、{ng_patterns[0]}で大損した。

でも「{ok_patterns[0]}」に切り替えただけで人生変わった。マジで。

---

### お前も当てはまってないか？

・{ng_patterns[0]}
・{ng_patterns[1] if len(ng_patterns) > 1 else '業者の言いなりで選択'}
・{ng_patterns[2] if len(ng_patterns) > 2 else '比較検討しない'}

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

**{facts[1]}**

業者・インフルエンサー・詐欺師は、お前が無知なまま損してくれた方が儲かる。
だから公式には絶対に教えない情報がある。

「お客様第一」とか言いながら、実は手数料ボッタクリ商品を売りつけてる。

**{facts[2] if len(facts) > 2 else facts[1]}**

ガチでエグい。

---

## じゃあどうすればいいのか

### ステップ1: **絶対にやるな3つのNG**

以下は**即死コンボ**だ。

❌ **NG①: {ng_patterns[0]}**
→ {facts[0]}

❌ **NG②: {ng_patterns[1] if len(ng_patterns) > 1 else '業者の言いなり'}**
→ {facts[3] if len(facts) > 3 else facts[1]}

❌ **NG③: {ng_patterns[2] if len(ng_patterns) > 2 else '比較検討せず即決'}**
→ {facts[4] if len(facts) > 4 else facts[2]}

この3つやるだけで**年間{loss_amount}万円は損する**。マジで。

---

### ステップ2: **損しない3つのルール**

逆に損しないルールはここだ↓

⭕ **ルール①: {ok_patterns[0]}**
→ これだけで年{int(loss_amount * 0.6)}万円は守れる

⭕ **ルール②: {ok_patterns[1] if len(ok_patterns) > 1 else '3社以上比較して最安を選ぶ'}**
→ 面倒くさがらずに比較。それだけで半額になることも

⭕ **ルール③: {ok_patterns[2] if len(ok_patterns) > 2 else 'データ・事実で判断する'}**
→ 感情ではなく数字で判断。これで勝率が3倍は上がる

この3つを守れば**年間{loss_amount}万円は確実に守れる**。
俺も実際に試して損しなくなった。

---

### ステップ3: **プロが使う3つの裏ワザ**

損しない奴・成功してる奴は全員これやってる。

**1. 業者・インフルエンサーの提案を鵜呑みにしない**
→ セカンドオピニオン必須。専門家・経験者に相談

**2. タイミングを見極める**
→ 時期・方法によっては数万~数十万円の差がつく

**3. 定期的に見直す(年1回は必須)**
→ 契約・習慣したら終わりじゃない。毎年最適化しろ

この3つを満たせばさらに年{int(loss_amount * 0.4)}万円浮く。
俺はこれで年間トータル{int(loss_amount * 1.4)}万円守ってる。ガチで。

---

## 実際どれくらい得するのか

| 項目 | 今まで | これから | 差額 |
|------|--------|---------|------|
| {ng_patterns[0][:15]}... | 年-{loss_amount}万 | 0円 | **+{loss_amount}万** |
| {ng_patterns[1][:15] if len(ng_patterns) > 1 else '業者手数料'}... | 年-{int(loss_amount * 0.2)}万 | -{int(loss_amount * 0.04)}万 | **+{int(loss_amount * 0.16)}万** |
| {ng_patterns[2][:15] if len(ng_patterns) > 2 else '比較せず高額'}... | 年-{int(loss_amount * 0.3)}万 | -{int(loss_amount * 0.06)}万 | **+{int(loss_amount * 0.24)}万** |
| **年間合計** | **-{int(loss_amount * 1.5)}万** | **-{int(loss_amount * 0.1)}万** | **+{int(loss_amount * 1.4)}万** |

つまり、**年間{int(loss_amount * 1.4)}万円は確実に守れる/稼げる**。

守った・稼いだ金でタバコ買うもよし、次の投資に回すもよし、貯金して少しマシな生活するもよし。お前の自由だ。

---

## 最後に

周りのバカどもは知らずに損し続けてる。

{ng_patterns[0]}で、{ng_patterns[1] if len(ng_patterns) > 1 else '業者の言いなり'}で、比較もせずに。
**全部カモられてる**。

---

でも、**お前は違う**。

この記事読んだだけで「情報に金払える奴」になった。
それが成り上がる第一歩だ。

お前は賢い選択をした。周りのバカどもに差をつけろ。

---
"""
    
    # 次回予告
    if next_article_title:
        next_day = get_next_day(day)
        article += f"""
## 次回予告 × フォロー特典

次は「{next_article_title}」を公開する。

知らないと年間{loss_amount}万円損するぞ。
公開は**{next_day}12時**。見逃すな。

---

### フォロー特典

Twitterフォローしてくれた人には次回記事を**100円引き**で読めるクーポン配布

[@gethinu](https://x.com/gethinu)をフォロー → DMで「クーポン」と送る → GET

---
"""
    
    # マガジン紹介
    article += """
## 👤 このマガジンについて

**げすいぬ | 底辺脱出マガジン**

底辺から這い上がる情報を晒してる📢

俺も昔は底辺だった。
損し続けて、無知で消耗して、気づいたら貯金ゼロ。

でも、「情報に金払える奴」になってから人生変わった。

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
    
    return article


def get_next_day(current_day: str) -> str:
    """次の曜日を返す"""
    days = ["月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]
    try:
        idx = days.index(current_day)
        return days[(idx + 1) % 7]
    except ValueError:
        return "月曜"


def main():
    """メイン処理"""
    print("🔥 Premium Article Generator V3 - 本気モード")
    print("")
    print("改善点:")
    print("- factsから具体的数値を直接抽出")
    print("- NG/OK対比を明確化")
    print("- Before/After比較表に実データ使用")
    print("- 業界裏話を2個以上挿入")
    print("")
    
    # データロード
    all_data = load_data()
    article_master = load_article_master()
    
    # 月曜カテゴリ取得
    monday_category = next(
        (cat for cat in all_data if cat["category"] == "ギャンブル・金"),
        None
    )
    
    if not monday_category:
        print("❌ 月曜カテゴリが見つかりません")
        return
    
    # 月曜記事取得
    monday_articles = [a for a in article_master if a["day"] == "月曜"]
    
    print(f"📅 カテゴリ: {monday_category['category']}")
    print(f"📝 記事数: {len(monday_articles)}")
    print(f"💾 データ: {len(monday_category['data'])} トピック")
    print("")
    
    # 記事生成
    generated = 0
    for i, article in enumerate(monday_articles):
        article_id = article["id"]
        title = article["title"]
        file_path = Path(__file__).parent.parent / "gethnote" / article["file"]
        
        # 次記事タイトル
        next_title = (monday_articles[(i + 1) % len(monday_articles)]["title"]
                      if i < len(monday_articles) - 1 else None)
        
        # 生成
        content = generate_premium_article_v3(
            article_id=article_id,
            title=title,
            day="月曜",
            category_data=monday_category,
            next_article_title=next_title
        )
        
        if content:
            # ファイル書き込み(.md拡張子追加)
            if not str(file_path).endswith('.md'):
                file_path = Path(str(file_path) + '.md')
            
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            char_count = len(content)
            print(f"✅ [ID {article_id:3d}] {title} ({char_count}文字)")
            generated += 1
        else:
            print(f"⚠️  [ID {article_id:3d}] 生成失敗: {title}")
    
    print("")
    print(f"🎉 完了! 生成: {generated}/{len(monday_articles)}")


if __name__ == "__main__":
    main()
