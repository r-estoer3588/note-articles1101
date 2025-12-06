#!/usr/bin/env python3
"""
Threads Manual Performance Logger - 手動パフォーマンス記録ツール

Threads APIが未設定の場合でも、アプリで確認した
「いいね」「閲覧数」を手動で記録し、学習データを生成する。

Usage:
    # 対話モードで記録
    python threads_manual_logger.py

    # 記録データからレポート生成
    python threads_manual_logger.py --report

    # CSV一括インポート
    python threads_manual_logger.py --import performance.csv
"""

import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

# Configuration paths
BASE_DIR = Path(__file__).parent.parent
TOOLS_DIR = Path(__file__).parent
LEARNING_DIR = BASE_DIR / "learning"
LOG_FILE = LEARNING_DIR / "threads_performance_log.json"
SCHEDULE_FILE = BASE_DIR / "research_ideas" / "relationship" / "600_posts_schedule.csv"


def ensure_dirs():
    """必要なディレクトリを作成"""
    LEARNING_DIR.mkdir(parents=True, exist_ok=True)


def load_log() -> List[Dict]:
    """パフォーマンスログを読み込み"""
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_log(data: List[Dict]):
    """パフォーマンスログを保存"""
    ensure_dirs()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ ログ保存: {LOG_FILE}")


def load_schedule() -> pd.DataFrame:
    """投稿スケジュールを読み込み"""
    if SCHEDULE_FILE.exists():
        return pd.read_csv(SCHEDULE_FILE)
    return pd.DataFrame()


def interactive_log():
    """対話モードでパフォーマンスを記録"""
    print(
        """
╔══════════════════════════════════════════════════════════════════════════════╗
║            Threads 手動パフォーマンス記録                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Threadsアプリで確認した投稿のパフォーマンスを記録します。
終了するには 'q' を入力してください。
"""
    )

    schedule = load_schedule()
    log = load_log()

    while True:
        print("\n" + "-" * 40)

        # Day番号入力
        day_input = input("📅 Day番号 (例: 1-21, q=終了): ").strip()
        if day_input.lower() == "q":
            break

        try:
            day = int(day_input)
        except ValueError:
            print("❌ 数字を入力してください")
            continue

        # No番号入力
        no_input = input("📝 投稿No (例: 1-10): ").strip()
        try:
            no = int(no_input)
        except ValueError:
            print("❌ 数字を入力してください")
            continue

        # スケジュールから投稿内容を取得して表示
        if not schedule.empty:
            post = schedule[(schedule["Day"] == day) & (schedule["No"] == no)]
            if not post.empty:
                content = post.iloc[0]["Content"]
                post_type = post.iloc[0]["Type"]
                time = post.iloc[0]["Time"]
                print(f"\n【投稿内容プレビュー】")
                print(f"  タイプ: {post_type}")
                print(f"  時間: {time}")
                print(f"  内容: {content[:100]}...")
            else:
                print(f"⚠️ Day{day}_No{no} がスケジュールに見つかりません")

        # パフォーマンス入力
        views_input = input("👁️ 閲覧数: ").strip()
        likes_input = input("❤️ いいね数: ").strip()
        replies_input = input("💬 返信数 (省略可): ").strip() or "0"
        reposts_input = input("🔄 リポスト数 (省略可): ").strip() or "0"

        try:
            views = int(views_input)
            likes = int(likes_input)
            replies = int(replies_input)
            reposts = int(reposts_input)
        except ValueError:
            print("❌ 数字を入力してください")
            continue

        # メモ（任意）
        note = input("📝 メモ (任意): ").strip()

        # 記録追加
        record = {
            "day": day,
            "no": no,
            "post_id": f"Day{day}_No{no}",
            "views": views,
            "likes": likes,
            "replies": replies,
            "reposts": reposts,
            "engagement_total": likes + replies + reposts,
            "engagement_rate": round((likes + replies + reposts) / (views + 1) * 100, 2),
            "note": note,
            "recorded_at": datetime.now().isoformat(),
        }

        # 投稿内容も保存
        if not schedule.empty and not post.empty:
            record["content"] = post.iloc[0]["Content"]
            record["type"] = post.iloc[0]["Type"]
            record["time"] = post.iloc[0]["Time"]

        # 既存レコードをチェック（同じpost_idなら更新）
        existing_idx = next(
            (i for i, r in enumerate(log) if r["post_id"] == record["post_id"]), None
        )
        if existing_idx is not None:
            log[existing_idx] = record
            print(f"🔄 Day{day}_No{no} を更新しました")
        else:
            log.append(record)
            print(f"✅ Day{day}_No{no} を記録しました")

        save_log(log)

    print("\n✅ 記録を終了しました")


def generate_report():
    """記録データからレポートを生成"""
    log = load_log()

    if not log:
        print("❌ 記録データがありません。まず対話モードで記録してください。")
        return

    df = pd.DataFrame(log)

    print(
        """
╔══════════════════════════════════════════════════════════════════════════════╗
║            Threads パフォーマンスレポート                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    )

    # 全体統計
    print("【📊 全体統計】")
    print(f"  記録投稿数: {len(df)}件")
    print(f"  総閲覧数: {df['views'].sum():,}")
    print(f"  総いいね数: {df['likes'].sum():,}")
    print(f"  平均閲覧数: {df['views'].mean():.1f}")
    print(f"  平均いいね数: {df['likes'].mean():.1f}")
    print(f"  平均ER: {df['engagement_rate'].mean():.2f}%")

    # 100閲覧以上
    high_views = df[df["views"] >= 100]
    print(f"\n【🔥 100閲覧以上の投稿】 {len(high_views)}件")
    for _, row in high_views.sort_values("views", ascending=False).iterrows():
        print(f"  {row['post_id']}: 👁️{row['views']} ❤️{row['likes']} - {row.get('type', 'N/A')}")

    # いいね獲得投稿
    liked = df[df["likes"] >= 1]
    print(f"\n【❤️ いいね獲得投稿】 {len(liked)}件")
    for _, row in liked.sort_values("likes", ascending=False).iterrows():
        print(f"  {row['post_id']}: 👁️{row['views']} ❤️{row['likes']} - {row.get('type', 'N/A')}")

    # タイプ別分析
    if "type" in df.columns:
        print(f"\n【📝 タイプ別パフォーマンス】")
        type_stats = df.groupby("type").agg(
            {
                "views": "mean",
                "likes": "mean",
                "engagement_rate": "mean",
                "post_id": "count",
            }
        ).round(2)
        type_stats.columns = ["平均閲覧", "平均いいね", "平均ER%", "投稿数"]
        type_stats = type_stats.sort_values("平均ER%", ascending=False)
        print(type_stats.to_string())

    # 時間帯別分析
    if "time" in df.columns:
        print(f"\n【⏰ 時間帯別パフォーマンス】")
        time_stats = df.groupby("time").agg(
            {
                "views": "mean",
                "likes": "mean",
                "engagement_rate": "mean",
                "post_id": "count",
            }
        ).round(2)
        time_stats.columns = ["平均閲覧", "平均いいね", "平均ER%", "投稿数"]
        time_stats = time_stats.sort_values("平均ER%", ascending=False)
        print(time_stats.to_string())

    # 学習プロンプト生成
    generate_learning_prompt(df)


def generate_learning_prompt(df: pd.DataFrame):
    """学習プロンプトを生成して保存"""
    ensure_dirs()

    # 高パフォーマンス投稿を抽出
    high_perform = df[(df["views"] >= 100) | (df["likes"] >= 1)].copy()

    if high_perform.empty:
        high_perform = df.nlargest(5, "engagement_rate")

    # サンプル投稿
    samples = []
    for _, row in high_perform.sort_values("engagement_rate", ascending=False).head(5).iterrows():
        content = row.get("content", "（内容未記録）")
        samples.append(
            f"""【{row['post_id']} - 👁️{row['views']} ❤️{row['likes']} ER:{row['engagement_rate']:.2f}%】
タイプ: {row.get('type', 'N/A')}
時間: {row.get('time', 'N/A')}
内容:
{content[:300]}...
"""
        )

    # タイプ別ベスト
    type_best = ""
    if "type" in df.columns:
        type_stats = df.groupby("type")["engagement_rate"].mean().sort_values(ascending=False)
        type_best = "\n".join([f"  {i+1}. {t}: {er:.2f}%" for i, (t, er) in enumerate(type_stats.head(3).items())])

    # 時間帯別ベスト
    time_best = ""
    if "time" in df.columns:
        time_stats = df.groupby("time")["engagement_rate"].mean().sort_values(ascending=False)
        time_best = "\n".join([f"  {i+1}. {t}: {er:.2f}%" for i, (t, er) in enumerate(time_stats.head(3).items())])

    prompt = f"""# レス卒先輩 21days投稿 学習データ
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 分析期間のパフォーマンス
- 分析投稿数: {len(df)}件
- 100閲覧以上: {len(df[df['views'] >= 100])}件
- いいね獲得: {len(df[df['likes'] >= 1])}件
- 平均閲覧数: {df['views'].mean():.1f}
- 平均いいね数: {df['likes'].mean():.1f}
- 平均エンゲージメント率: {df['engagement_rate'].mean():.2f}%

## 🎯 効果的な投稿タイプ
{type_best if type_best else "（データ不足）"}

## ⏰ 効果的な投稿時間
{time_best if time_best else "（データ不足）"}

## ✨ 高パフォーマンス投稿サンプル

{"".join(samples)}

## 💡 22日目以降の投稿改善指針

上記の高パフォーマンス投稿を分析した結果、以下の要素が効果的と推測されます：

1. **共感を誘う具体的シーン描写**
   - 「〜ありませんか？」という問いかけ形式
   - 日常の「あるある」を言語化

2. **適切な文字数と構成**
   - 改行を効果的に使用
   - 読みやすいリズム

3. **投稿時間の最適化**
   - 朝（7-8時）：1日の始まりに共感
   - 昼（12時）：昼休みのスマホタイム
   - 夕方-夜（17-21時）：帰宅後のリラックスタイム

4. **タイプの使い分け**
   - 本気(共感): 深い共感を誘う長文
   - 軽め(問): 考えさせる質問形式
   - 軽め(一言): サクッと読める一言

---
このプロンプトを使用して、22日目以降の投稿を生成・改善してください。
"""

    # 保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_file = LEARNING_DIR / f"threads_learning_manual_{timestamp}.md"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"\n✅ 学習プロンプト保存: {prompt_file}")

    # JSONも保存
    data = {
        "generated_at": datetime.now().isoformat(),
        "total_posts": len(df),
        "avg_views": round(df["views"].mean(), 2),
        "avg_likes": round(df["likes"].mean(), 2),
        "avg_er": round(df["engagement_rate"].mean(), 2),
        "high_perform_posts": high_perform.to_dict("records"),
    }
    data_file = LEARNING_DIR / f"threads_learning_manual_{timestamp}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 学習データ保存: {data_file}")


def import_csv(csv_path: str):
    """CSVからパフォーマンスデータをインポート"""
    if not os.path.exists(csv_path):
        print(f"❌ ファイルが見つかりません: {csv_path}")
        return

    print(f"📥 CSVインポート: {csv_path}")

    df = pd.read_csv(csv_path)
    required_cols = ["day", "no", "views", "likes"]

    for col in required_cols:
        if col not in df.columns:
            print(f"❌ 必須カラム '{col}' がありません")
            print(f"   必須: {required_cols}")
            return

    log = load_log()
    schedule = load_schedule()

    imported = 0
    for _, row in df.iterrows():
        day = int(row["day"])
        no = int(row["no"])
        post_id = f"Day{day}_No{no}"

        record = {
            "day": day,
            "no": no,
            "post_id": post_id,
            "views": int(row["views"]),
            "likes": int(row["likes"]),
            "replies": int(row.get("replies", 0)),
            "reposts": int(row.get("reposts", 0)),
            "recorded_at": datetime.now().isoformat(),
        }

        record["engagement_total"] = (
            record["likes"] + record["replies"] + record["reposts"]
        )
        record["engagement_rate"] = round(
            record["engagement_total"] / (record["views"] + 1) * 100, 2
        )

        # スケジュールから投稿内容を取得
        if not schedule.empty:
            post = schedule[(schedule["Day"] == day) & (schedule["No"] == no)]
            if not post.empty:
                record["content"] = post.iloc[0]["Content"]
                record["type"] = post.iloc[0]["Type"]
                record["time"] = post.iloc[0]["Time"]

        # 既存チェック
        existing_idx = next(
            (i for i, r in enumerate(log) if r["post_id"] == post_id), None
        )
        if existing_idx is not None:
            log[existing_idx] = record
        else:
            log.append(record)

        imported += 1

    save_log(log)
    print(f"✅ {imported}件インポート完了")


def main():
    parser = argparse.ArgumentParser(
        description="Threads Manual Performance Logger"
    )
    parser.add_argument(
        "--report", action="store_true", help="記録データからレポート生成"
    )
    parser.add_argument("--import", dest="import_csv", help="CSVからインポート")

    args = parser.parse_args()

    if args.report:
        generate_report()
    elif args.import_csv:
        import_csv(args.import_csv)
    else:
        interactive_log()


if __name__ == "__main__":
    main()
