#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SNS統合分析ツール
X・note・Threadsのデータを一元管理し、週次・月次レポートを自動生成

使い方:
    python tools/sns_integrated_analyzer.py --report weekly
    python tools/sns_integrated_analyzer.py --report monthly
    python tools/sns_integrated_analyzer.py --update-manual
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# カラー出力
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Color.HEADER}{Color.BOLD}{'=' * 60}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{text}{Color.END}")
    print(f"{Color.HEADER}{Color.BOLD}{'=' * 60}{Color.END}\n")


def print_success(text):
    print(f"{Color.GREEN}✓ {text}{Color.END}")


def print_info(text):
    print(f"{Color.BLUE}ℹ {text}{Color.END}")


def print_warning(text):
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")


def print_error(text):
    print(f"{Color.RED}✗ {text}{Color.END}")


# プロジェクト定義
PROJECTS = {
    "1": {"id": "relationship", "name": "夫婦関係再構築 (note-articles)"},
    "2": {"id": "quant_system", "name": "米国株自動売買 (quant_trading_system)"},
}


class SNSIntegratedAnalyzer:
    """SNS統合分析クラス"""

    def __init__(
        self,
        project_id: str,
        project_name: str,
        data_dir: str = "outputs/sns_tracking",
    ):
        self.project_id = project_id
        self.project_name = project_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / f"sns_data_{self.project_id}.json"

        # 旧ファイルからの移行チェック
        old_file = self.data_dir / "sns_data.json"
        if (
            self.project_id == "relationship"
            and old_file.exists()
            and not self.data_file.exists()
        ):
            print_info(f"旧データファイルを移行します: {old_file} -> {self.data_file}")
            import shutil

            shutil.move(old_file, self.data_file)

        self.data = self.load_data()
        
    def load_data(self) -> Dict:
        """データ読み込み"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # デフォルト設定（プロジェクトごとに変える場合はここで分岐）
        default_goals = {
            "1month": {
                "note_sales": 20,
                "note_revenue": 50000,
                "threads_followers": 200
            },
            "3month": {
                "note_sales": 80,
                "note_revenue": 150000,
                "magazine_subscribers": 30,
                "threads_followers": 800
            },
            "6month": {
                "community_members": 50,
                "monthly_revenue": 300000
            },
            "12month": {
                "monthly_revenue": 500000
            }
        }
        
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "records": [],
            "goals": default_goals
        }
    
    def save_data(self):
        """データ保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print_success(f"データを保存しました: {self.data_file}")
    
    def add_record(self, record: Dict):
        """レコード追加"""
        record["timestamp"] = datetime.now().isoformat()
        self.data["records"].append(record)
        self.save_data()
    
    def manual_update(self):
        """手動データ入力"""
        print_header(f"📝 SNSデータ手動更新: {self.project_name}")
        
        print_info("現在のデータを入力してください（Enter で スキップ）\n")
        
        record = {}
        
        # note
        note_pv = input(f"{Color.CYAN}note 総PV数: {Color.END}").strip()
        if note_pv:
            record["note_total_pv"] = int(note_pv)

        note_sales = input(
            f"{Color.CYAN}note 有料記事販売数（累計）: {Color.END}"
        ).strip()
        if note_sales:
            record["note_total_sales"] = int(note_sales)

        note_revenue = input(
            f"{Color.CYAN}note 売上（累計・円）: {Color.END}"
        ).strip()
        if note_revenue:
            record["note_total_revenue"] = int(note_revenue)

        magazine_subs = input(
            f"{Color.CYAN}note マガジン会員数: {Color.END}"
        ).strip()
        if magazine_subs:
            record["magazine_subscribers"] = int(magazine_subs)

        # Threads
        threads_followers = input(
            f"{Color.CYAN}Threads フォロワー数: {Color.END}"
        ).strip()
        if threads_followers:
            record["threads_followers"] = int(threads_followers)

        threads_posts = input(
            f"{Color.CYAN}Threads 今日の投稿数: {Color.END}"
        ).strip()
        if threads_posts:
            record["threads_posts_today"] = int(threads_posts)

        # コミュニティ
        community = input(f"{Color.CYAN}コミュニティ会員数: {Color.END}").strip()
        if community:
            record["community_members"] = int(community)

        # その他収益
        other_revenue = input(
            f"{Color.CYAN}その他収益（ココナラ等・円）: {Color.END}"
        ).strip()
        if other_revenue:
            record["other_revenue"] = int(other_revenue)

        # メモ
        memo = input(
            f"{Color.CYAN}メモ（今日の気づき・反省など）: {Color.END}"
        ).strip()
        if memo:
            record["memo"] = memo
        
        if record:
            self.add_record(record)
            print_success("\n✅ データを記録しました！")
            self.show_latest_progress()
        else:
            print_warning("データが入力されませんでした")
    
    def show_latest_progress(self):
        """最新の進捗表示"""
        if not self.data["records"]:
            print_warning("まだデータがありません")
            return

        latest = self.data["records"][-1]
        goals_1m = self.data["goals"]["1month"]

        print_header(f"📊 現在の進捗状況: {self.project_name}")

        # note
        if "note_total_sales" in latest:
            note_progress = (
                latest["note_total_sales"] / goals_1m["note_sales"]
            ) * 100
            print(
                f"note 販売数: {latest['note_total_sales']} / "
                f"{goals_1m['note_sales']} ({note_progress:.1f}%)"
            )

        if "note_total_revenue" in latest:
            revenue_progress = (
                latest["note_total_revenue"] / goals_1m["note_revenue"]
            ) * 100
            print(
                f"note 売上: ¥{latest['note_total_revenue']:,} / "
                f"¥{goals_1m['note_revenue']:,} ({revenue_progress:.1f}%)"
            )

        # Threads
        if "threads_followers" in latest:
            threads_progress = (
                latest["threads_followers"] / goals_1m["threads_followers"]
            ) * 100
            print(
                f"Threads フォロワー: {latest['threads_followers']} / "
                f"{goals_1m['threads_followers']} ({threads_progress:.1f}%)"
            )

        print()

    def generate_weekly_report(self):
        """週次レポート生成"""
        print_header(f"📋 週次レポート: {self.project_name}")

        if len(self.data["records"]) < 2:
            print_warning("データが不足しています（最低2回の記録が必要）")
            return

        # 過去7日間のデータ取得
        week_ago = datetime.now() - timedelta(days=7)
        recent_records = [
            r
            for r in self.data["records"]
            if datetime.fromisoformat(r["timestamp"]) > week_ago
        ]

        if not recent_records:
            print_warning("過去7日間のデータがありません")
            return

        first = recent_records[0]
        latest = recent_records[-1]

        # 成長率計算
        print("## 週間成長率\n")

        if "note_total_sales" in first and "note_total_sales" in latest:
            sales_growth = (
                latest["note_total_sales"] - first["note_total_sales"]
            )
            print(f"note 販売: +{sales_growth} 部")

        if "note_total_revenue" in first and "note_total_revenue" in latest:
            revenue_growth = (
                latest["note_total_revenue"] - first["note_total_revenue"]
            )
            print(f"note 売上: +¥{revenue_growth:,}")

        if "threads_followers" in first and "threads_followers" in latest:
            threads_growth = (
                latest["threads_followers"] - first["threads_followers"]
            )
            print(f"Threads フォロワー: +{threads_growth} 人")

        # 投稿頻度分析
        total_threads_posts = sum(
            r.get("threads_posts_today", 0) for r in recent_records
        )

        print(f"\n## 投稿頻度\n")
        print(
            f"Threads: {total_threads_posts} 投稿"
            f"（平均 {total_threads_posts/7:.1f} 投稿/日）"
        )

        # メモまとめ
        memos = [r.get("memo") for r in recent_records if r.get("memo")]
        if memos:
            print(f"\n## 今週の気づき\n")
            for i, memo in enumerate(memos, 1):
                print(f"{i}. {memo}")

        print()
    
    def generate_monthly_report(self):
        """月次レポート生成"""
        print_header(f"📊 月次レポート: {self.project_name}")

        if len(self.data["records"]) < 2:
            print_warning("データが不足しています")
            return

        # 過去30日間のデータ取得
        month_ago = datetime.now() - timedelta(days=30)
        month_records = [
            r
            for r in self.data["records"]
            if datetime.fromisoformat(r["timestamp"]) > month_ago
        ]

        if not month_records:
            print_warning("過去30日間のデータがありません")
            return

        first = month_records[0]
        latest = month_records[-1]
        goals = self.data["goals"]["1month"]

        # 目標達成率
        print("## 1ヶ月目標 達成状況\n")

        if "note_total_sales" in latest:
            sales_achievement = (
                latest["note_total_sales"] / goals["note_sales"]
            ) * 100
            status = "✅" if sales_achievement >= 100 else "🔄"
            print(
                f"{status} note 販売数: {latest['note_total_sales']} / "
                f"{goals['note_sales']} ({sales_achievement:.1f}%)"
            )

        if "note_total_revenue" in latest:
            revenue_achievement = (
                latest["note_total_revenue"] / goals["note_revenue"]
            ) * 100
            status = "✅" if revenue_achievement >= 100 else "🔄"
            print(
                f"{status} note 売上: ¥{latest['note_total_revenue']:,} / "
                f"¥{goals['note_revenue']:,} ({revenue_achievement:.1f}%)"
            )

        if "threads_followers" in latest:
            threads_achievement = (
                latest["threads_followers"] / goals["threads_followers"]
            ) * 100
            status = "✅" if threads_achievement >= 100 else "🔄"
            print(
                f"{status} Threads フォロワー: {latest['threads_followers']} / "
                f"{goals['threads_followers']} ({threads_achievement:.1f}%)"
            )

        # 月間成長率
        print("\n## 月間成長\n")

        if "note_total_sales" in first and "note_total_sales" in latest:
            sales_growth = (
                latest["note_total_sales"] - first["note_total_sales"]
            )
            revenue_growth = latest.get("note_total_revenue", 0) - first.get(
                "note_total_revenue", 0
            )
            print(f"note 販売: +{sales_growth} 部（+¥{revenue_growth:,}）")

        # 次月への提案
        print("\n## 次月への改善提案\n")

        if (
            "note_total_sales" in latest
            and latest["note_total_sales"] < goals["note_sales"]
        ):
            print("🔄 Threads宣伝スレッドを週2回に増やす")
            print("🔄 無料記事を1本追加して集客強化")

        print()
    
    def export_csv(self):
        """CSV出力"""
        import csv

        csv_file = (
            self.data_dir
            / f"sns_data_{self.project_id}_"
            f"{datetime.now().strftime('%Y%m%d')}.csv"
        )

        if not self.data["records"]:
            print_warning("データがありません")
            return

        # すべてのキーを収集
        all_keys = set()
        for record in self.data["records"]:
            all_keys.update(record.keys())

        all_keys = sorted(all_keys)

        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(self.data["records"])

        print_success(f"CSVを出力しました: {csv_file}")


def select_project() -> tuple[str, str]:
    """プロジェクト選択"""
    print_header("📂 プロジェクト選択")

    for key, proj in PROJECTS.items():
        print(f"{key}. {proj['name']}")

    while True:
        choice = input(
            f"\n{Color.CYAN}プロジェクト番号を選択してください (1-{len(PROJECTS)}): {Color.END}"
        ).strip()
        if choice in PROJECTS:
            return PROJECTS[choice]["id"], PROJECTS[choice]["name"]
        print_warning("無効な選択です。もう一度入力してください。")


def select_action() -> str:
    """アクション選択"""
    print_header("🚀 アクション選択")
    print("1. 📝 データ入力 (今日の記録)")
    print("2. 📊 現在の進捗確認")
    print("3. 📋 週次レポート (分析)")
    print("4. 📅 月次レポート (分析)")
    print("5. 💾 CSV出力")
    print("0. 🚪 終了")

    while True:
        choice = input(
            f"\n{Color.CYAN}アクションを選択してください (0-5): {Color.END}"
        ).strip()
        if choice in ["0", "1", "2", "3", "4", "5"]:
            return choice
        print_warning("無効な選択です")


def main():
    parser = argparse.ArgumentParser(
        description="SNS統合分析ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python tools/sns_integrated_analyzer.py --update-manual     # 手動データ入力
  python tools/sns_integrated_analyzer.py --report weekly     # 週次レポート
  python tools/sns_integrated_analyzer.py --report monthly    # 月次レポート
  python tools/sns_integrated_analyzer.py --export-csv        # CSV出力

推奨ワークフロー:
  1. 毎日: --update-manual でデータ記録
  2. 毎週日曜: --report weekly で振り返り
  3. 毎月1日: --report monthly で目標確認
        """
    )

    parser.add_argument(
        '--update-manual',
        action='store_true',
        help='手動でデータを入力'
    )

    parser.add_argument(
        '--report',
        choices=['weekly', 'monthly'],
        help='レポート生成（weekly or monthly）'
    )

    parser.add_argument(
        '--export-csv',
        action='store_true',
        help='CSVファイルに出力'
    )

    parser.add_argument(
        '--show-progress',
        action='store_true',
        help='現在の進捗を表示'
    )

    parser.add_argument(
        '--project',
        help='プロジェクトIDを指定（対話モードをスキップ）'
    )

    args = parser.parse_args()

    # プロジェクト決定
    project_id = None
    project_name = None

    if args.project:
        # 引数で指定された場合
        for p in PROJECTS.values():
            if p["id"] == args.project:
                project_id = p["id"]
                project_name = p["name"]
                break
        if not project_id:
            print_error(f"指定されたプロジェクトIDが見つかりません: {args.project}")
            return
    else:
        # 対話モードで選択
        project_id, project_name = select_project()

    analyzer = SNSIntegratedAnalyzer(project_id, project_name)

    if args.update_manual:
        analyzer.manual_update()
    elif args.report == 'weekly':
        analyzer.generate_weekly_report()
    elif args.report == 'monthly':
        analyzer.generate_monthly_report()
    elif args.export_csv:
        analyzer.export_csv()
    elif args.show_progress:
        analyzer.show_latest_progress()
    else:
        # デフォルト: アクション選択メニュー
        while True:
            action = select_action()
            if action == "0":
                print_info("終了します")
                break
            elif action == "1":
                analyzer.manual_update()
            elif action == "2":
                analyzer.show_latest_progress()
            elif action == "3":
                analyzer.generate_weekly_report()
            elif action == "4":
                analyzer.generate_monthly_report()
            elif action == "5":
                analyzer.export_csv()

            input(f"\n{Color.GREEN}Enterキーでメニューに戻ります...{Color.END}")


if __name__ == "__main__":
    main()
