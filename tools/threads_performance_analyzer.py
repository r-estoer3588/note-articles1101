#!/usr/bin/env python3
"""
Threads Performance Analyzer - レス卒先輩21daysキャンペーン分析ツール

Threads API v1.0を使用して投稿パフォーマンスを分析し、
高エンゲージメント投稿のパターンを学習して次期投稿に反映する。

必要なライブラリ:
    pip install requests pandas openai python-dotenv

環境変数(.env):
    THREADS_ACCESS_TOKEN=取得したアクセストークン
    THREADS_USER_ID=取得したユーザーID
    openai_API=OpenAI APIキー（学習分析用）

Usage:
    # 投稿パフォーマンス分析
    python threads_performance_analyzer.py --analyze

    # 高パフォーマンス投稿の学習
    python threads_performance_analyzer.py --learn

    # 22日目以降の投稿を改善生成
    python threads_performance_analyzer.py --generate --day 22

    # Threads API認証ヘルプ
    python threads_performance_analyzer.py --setup
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from dotenv import load_dotenv

# Configuration paths
BASE_DIR = Path(__file__).parent.parent
TOOLS_DIR = Path(__file__).parent
ENV_FILE = TOOLS_DIR / ".env"
SCHEDULE_FILE = BASE_DIR / "research_ideas" / "relationship" / "600_posts_schedule.csv"
LEARNING_OUTPUT_DIR = BASE_DIR / "learning"
ANALYSIS_OUTPUT_DIR = BASE_DIR / "analyses"

# Threads API endpoints
THREADS_API_BASE = "https://graph.threads.net/v1.0"


class ThreadsAPIClient:
    """Threads API v1.0 クライアント"""

    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id
        self.base_url = THREADS_API_BASE

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Dict:
        """API リクエストを実行"""
        if params is None:
            params = {}
        params["access_token"] = self.access_token

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            raise Exception(
                f"Threads API Error: {response.status_code} - {response.text}"
            )

        return response.json()

    def get_user_threads(
        self,
        limit: int = 25,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> List[Dict]:
        """
        ユーザーの投稿一覧を取得

        Args:
            limit: 取得件数（最大100）
            since: 取得開始日時
            until: 取得終了日時

        Returns:
            投稿データのリスト
        """
        params = {
            "fields": "id,text,timestamp,media_type,permalink,is_quote_post",
            "limit": min(limit, 100),
        }

        if since:
            params["since"] = int(since.timestamp())
        if until:
            params["until"] = int(until.timestamp())

        result = self._make_request(f"{self.user_id}/threads", params)
        return result.get("data", [])

    def get_thread_insights(self, thread_id: str) -> Dict:
        """
        投稿のインサイト（いいね、閲覧数等）を取得

        Args:
            thread_id: 投稿ID

        Returns:
            インサイトデータ
        """
        params = {
            "metric": "views,likes,replies,reposts,quotes",
        }

        result = self._make_request(f"{thread_id}/insights", params)

        # インサイトデータを整形
        insights = {}
        for item in result.get("data", []):
            metric_name = item.get("name")
            values = item.get("values", [{}])
            insights[metric_name] = values[0].get("value", 0) if values else 0

        return insights


class ThreadsPerformanceAnalyzer:
    """Threads投稿パフォーマンス分析クラス"""

    def __init__(self):
        load_dotenv(ENV_FILE)
        self.access_token = os.getenv("THREADS_ACCESS_TOKEN")
        self.user_id = os.getenv("THREADS_USER_ID")
        self.openai_api = os.getenv("openai_API")

        if self.access_token and self.user_id:
            self.client = ThreadsAPIClient(self.access_token, self.user_id)
        else:
            self.client = None

    def fetch_campaign_posts(
        self, start_date: datetime, end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        キャンペーン期間の投稿データを取得

        Args:
            start_date: キャンペーン開始日
            end_date: 終了日（Noneの場合は現在まで）

        Returns:
            投稿データのDataFrame
        """
        if not self.client:
            raise ValueError(
                "Threads API認証情報が設定されていません。--setup を実行してください。"
            )

        if end_date is None:
            end_date = datetime.now()

        print(f"📥 投稿データを取得中... ({start_date.date()} ~ {end_date.date()})")

        # 投稿一覧取得
        threads = self.client.get_user_threads(
            limit=100, since=start_date, until=end_date
        )

        if not threads:
            print("⚠️ 対象期間の投稿が見つかりませんでした")
            return pd.DataFrame()

        # インサイトを取得して結合
        records = []
        for i, thread in enumerate(threads):
            print(f"  インサイト取得中... {i+1}/{len(threads)}", end="\r")

            try:
                insights = self.client.get_thread_insights(thread["id"])
            except Exception as e:
                print(f"\n  ⚠️ インサイト取得失敗: {thread['id']} - {e}")
                insights = {}

            record = {
                "thread_id": thread["id"],
                "text": thread.get("text", ""),
                "timestamp": thread.get("timestamp"),
                "media_type": thread.get("media_type", "TEXT"),
                "permalink": thread.get("permalink", ""),
                "views": insights.get("views", 0),
                "likes": insights.get("likes", 0),
                "replies": insights.get("replies", 0),
                "reposts": insights.get("reposts", 0),
                "quotes": insights.get("quotes", 0),
            }
            records.append(record)

        print()  # 改行

        df = pd.DataFrame(records)

        # 計算フィールド追加
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["engagement_total"] = (
            df["likes"] + df["replies"] + df["reposts"] + df["quotes"]
        )
        df["engagement_rate"] = (df["engagement_total"] / (df["views"] + 1)) * 100
        df["posting_hour"] = df["timestamp"].dt.hour
        df["posting_day"] = df["timestamp"].dt.day_name()

        return df

    def analyze_top_performers(
        self, df: pd.DataFrame, top_n: int = 10
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        高パフォーマンス投稿を分析

        Args:
            df: 投稿データ
            top_n: 上位何件を抽出するか

        Returns:
            (トップ投稿DataFrame, 分析サマリーDict)
        """
        if df.empty:
            return pd.DataFrame(), {}

        # 100閲覧以上 OR いいね1以上のものを抽出
        high_perform = df[(df["views"] >= 100) | (df["likes"] >= 1)].copy()

        # エンゲージメント率でソート
        high_perform = high_perform.sort_values("engagement_rate", ascending=False)

        # 分析サマリー
        summary = {
            "total_posts": len(df),
            "high_perform_posts": len(high_perform),
            "posts_over_100_views": len(df[df["views"] >= 100]),
            "posts_with_likes": len(df[df["likes"] >= 1]),
            "avg_views": df["views"].mean(),
            "avg_likes": df["likes"].mean(),
            "avg_engagement_rate": df["engagement_rate"].mean(),
            "best_hour": (
                df.groupby("posting_hour")["engagement_rate"].mean().idxmax()
                if not df.empty
                else None
            ),
            "best_day": (
                df.groupby("posting_day")["engagement_rate"].mean().idxmax()
                if not df.empty
                else None
            ),
        }

        return high_perform.head(top_n), summary

    def extract_patterns(self, top_posts: pd.DataFrame) -> Dict:
        """
        高パフォーマンス投稿からパターンを抽出

        Args:
            top_posts: トップ投稿のDataFrame

        Returns:
            パターン分析結果
        """
        if top_posts.empty:
            return {}

        patterns = {
            "common_lengths": [],
            "common_keywords": [],
            "common_structures": [],
            "time_patterns": [],
            "sample_posts": [],
        }

        for _, row in top_posts.iterrows():
            text = row["text"]

            # 文字数
            patterns["common_lengths"].append(len(text))

            # 時間帯
            patterns["time_patterns"].append(row["posting_hour"])

            # サンプル（上位5件）
            if len(patterns["sample_posts"]) < 5:
                patterns["sample_posts"].append(
                    {
                        "text": text[:200] + "..." if len(text) > 200 else text,
                        "views": row["views"],
                        "likes": row["likes"],
                        "engagement_rate": round(row["engagement_rate"], 2),
                    }
                )

        # 統計
        patterns["avg_length"] = (
            sum(patterns["common_lengths"]) / len(patterns["common_lengths"])
            if patterns["common_lengths"]
            else 0
        )
        patterns["best_hours"] = list(
            pd.Series(patterns["time_patterns"]).value_counts().head(3).index
        )

        return patterns

    def generate_learning_prompt(
        self, patterns: Dict, summary: Dict, top_posts: pd.DataFrame
    ) -> str:
        """
        学習結果をプロンプトに変換

        Args:
            patterns: パターン分析結果
            summary: 分析サマリー
            top_posts: トップ投稿

        Returns:
            学習プロンプト文字列
        """
        sample_texts = "\n\n".join(
            [
                f"【{i+1}. 閲覧{p['views']}回 / いいね{p['likes']}】\n{p['text']}"
                for i, p in enumerate(patterns.get("sample_posts", []))
            ]
        )

        prompt = f"""# レス卒先輩 21days投稿 学習データ

## 📊 全体パフォーマンス
- 総投稿数: {summary.get('total_posts', 0)}件
- 高パフォーマンス投稿: {summary.get('high_perform_posts', 0)}件
- 100閲覧以上: {summary.get('posts_over_100_views', 0)}件
- いいね獲得: {summary.get('posts_with_likes', 0)}件
- 平均閲覧数: {summary.get('avg_views', 0):.1f}
- 平均いいね数: {summary.get('avg_likes', 0):.1f}
- 平均エンゲージメント率: {summary.get('avg_engagement_rate', 0):.2f}%

## 🎯 発見されたパターン
- 最適な投稿時間帯: {patterns.get('best_hours', [])}時台
- 理想的な文字数: 約{patterns.get('avg_length', 0):.0f}文字
- 最も反応が良い曜日: {summary.get('best_day', 'N/A')}

## ✨ 高パフォーマンス投稿サンプル
{sample_texts}

## 💡 22日目以降の投稿改善指針
上記の高パフォーマンス投稿を分析した結果、以下の要素が効果的：

1. **具体的な数字を含める** - 「年間130回」のような具体性
2. **共感を誘う問いかけ** - 「ありませんか？」「どうですか？」
3. **適度な改行** - 読みやすさを重視
4. **時間帯の最適化** - {patterns.get('best_hours', [])}時台を優先

---
生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return prompt

    def save_learning_data(self, prompt: str, patterns: Dict, summary: Dict):
        """
        学習データを保存

        Args:
            prompt: 学習プロンプト
            patterns: パターン分析
            summary: サマリー
        """
        LEARNING_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # プロンプトをMarkdownで保存
        prompt_file = LEARNING_OUTPUT_DIR / f"threads_learning_{timestamp}.md"
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"✅ 学習プロンプト保存: {prompt_file}")

        # JSON形式でも保存（プログラム利用用）
        data_file = LEARNING_OUTPUT_DIR / f"threads_learning_{timestamp}.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(
                {"summary": summary, "patterns": patterns},
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"✅ 学習データ保存: {data_file}")

        return prompt_file, data_file


def print_setup_guide():
    """Threads API セットアップガイドを表示"""
    guide = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Threads API セットアップガイド                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

【Step 1: Meta for Developersでアプリ作成】
1. https://developers.facebook.com/ にアクセス
2. 「マイアプリ」→「アプリを作成」
3. 「その他」→「次へ」→「ビジネス」選択
4. アプリ名を入力して作成

【Step 2: Threads APIを追加】
1. 作成したアプリのダッシュボードで「プロダクトを追加」
2. 「Threads API」を探して「設定」をクリック
3. 「Threads APIを追加」

【Step 3: アクセストークン取得】
1. Threads API > Settings に移動
2. 「Threads User Token Generator」でトークン生成
3. 必要なスコープを選択:
   - threads_basic
   - threads_content_publish (投稿用)
   - threads_manage_insights (分析用)
4. 「Generate Token」をクリック

【Step 4: 環境変数設定】
以下を note-articles/tools/.env に追加:

THREADS_ACCESS_TOKEN=取得したアクセストークン
THREADS_USER_ID=あなたのThreadsユーザーID

※ユーザーIDはAPI経由で取得可能:
curl "https://graph.threads.net/v1.0/me?access_token=YOUR_TOKEN"

【注意事項】
- アクセストークンは60日で期限切れ（長期トークンに変換推奨）
- 本番環境ではアプリ審査が必要な場合あり
- 詳細: https://developers.facebook.com/docs/threads

╔══════════════════════════════════════════════════════════════════════════════╗
"""
    print(guide)


def simulate_analysis():
    """API未設定時のシミュレーション分析（ローカルデータ使用）"""
    print("\n📊 ローカルデータからのシミュレーション分析を実行...")

    # スケジュールファイルから投稿済みデータを読み込み
    if not SCHEDULE_FILE.exists():
        print(f"❌ スケジュールファイルが見つかりません: {SCHEDULE_FILE}")
        return

    df = pd.read_csv(SCHEDULE_FILE)

    # Day 1-15の投稿を抽出（2025-11-22開始）
    start_date = datetime(2025, 11, 22)
    today = datetime.now()
    days_passed = (today - start_date).days + 1

    posted = df[df["Day"] <= days_passed]

    print(f"\n【キャンペーン状況】")
    print(f"  開始日: {start_date.strftime('%Y-%m-%d')}")
    print(f"  経過日数: {days_passed}日目")
    print(f"  投稿済み予定: {len(posted)}件")
    print(f"  残り投稿: {len(df) - len(posted)}件")

    # 投稿タイプ別の分布
    print(f"\n【投稿タイプ分布】")
    type_counts = posted["Type"].value_counts()
    for t, count in type_counts.items():
        print(f"  {t}: {count}件")

    # 時間帯分布
    print(f"\n【投稿時間帯分布】")
    time_counts = posted["Time"].value_counts().sort_index()
    for t, count in time_counts.items():
        print(f"  {t}: {count}件")

    print(
        """
╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️  Threads API未設定のため、実際のパフォーマンスデータは取得できません        ║
║                                                                              ║
║  実際の「いいね」「閲覧数」を分析するには:                                      ║
║  python threads_performance_analyzer.py --setup                              ║
║                                                                              ║
║  でセットアップガイドを確認してください。                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    )


def main():
    parser = argparse.ArgumentParser(
        description="Threads Performance Analyzer - レス卒先輩21daysキャンペーン分析"
    )
    parser.add_argument("--setup", action="store_true", help="Threads APIセットアップガイド表示")
    parser.add_argument("--analyze", action="store_true", help="投稿パフォーマンス分析")
    parser.add_argument("--learn", action="store_true", help="高パフォーマンス投稿から学習")
    parser.add_argument("--simulate", action="store_true", help="APIなしでシミュレーション分析")
    parser.add_argument("--day", type=int, help="改善投稿生成対象の日数")

    args = parser.parse_args()

    if args.setup:
        print_setup_guide()
        return

    if args.simulate or (not args.analyze and not args.learn):
        simulate_analysis()
        return

    # 実際のAPI分析
    analyzer = ThreadsPerformanceAnalyzer()

    if not analyzer.client:
        print("❌ Threads API認証情報が未設定です")
        print("   --setup でセットアップガイドを確認してください")
        print("   または --simulate でローカルシミュレーションを実行")
        return

    if args.analyze or args.learn:
        # キャンペーン開始日（2025-11-22）
        start_date = datetime(2025, 11, 22)

        try:
            df = analyzer.fetch_campaign_posts(start_date)

            if df.empty:
                print("❌ 分析対象の投稿がありません")
                return

            top_posts, summary = analyzer.analyze_top_performers(df)
            patterns = analyzer.extract_patterns(top_posts)

            print("\n" + "=" * 60)
            print("📊 分析結果サマリー")
            print("=" * 60)
            for key, value in summary.items():
                print(f"  {key}: {value}")

            if args.learn:
                prompt = analyzer.generate_learning_prompt(patterns, summary, top_posts)
                prompt_file, data_file = analyzer.save_learning_data(
                    prompt, patterns, summary
                )

                print("\n" + "=" * 60)
                print("🎓 学習データを保存しました")
                print("=" * 60)
                print(f"\n22日目以降の投稿改善に使用してください:")
                print(f"  プロンプト: {prompt_file}")
                print(f"  データ: {data_file}")

        except Exception as e:
            print(f"❌ エラー: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
