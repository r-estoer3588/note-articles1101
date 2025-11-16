#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Learning Manager - 自動学習ループツール

4つのステップで投稿成果を自動改善：
1. X/note/Threads指標収集
2. 目的と成果物の明確化
3. 数値検証とAI改善指示
4. 過去の成功例で再教育

Usage:
    python learning_manager.py                # 対話モード（全ステップ）
    python learning_manager.py --ingest       # 指標収集のみ
    python learning_manager.py --review       # KPI分析のみ
    python learning_manager.py --replay       # 成功例参照のみ
    python learning_manager.py --goal "noteリード10件" --deliverable "2600文字記事"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False


class Colors:
    """ANSIカラーコード"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """ヘッダー表示"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(Colors.OKCYAN + "=" * len(text) + Colors.ENDC)


def print_success(text: str):
    """成功メッセージ"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_warning(text: str):
    """警告メッセージ"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    """エラーメッセージ"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text: str):
    """情報メッセージ"""
    print(f"{Colors.OKBLUE}💡 {text}{Colors.ENDC}")


def ensure_directories():
    """必要なディレクトリ構造を作成"""
    base_dir = Path(__file__).parent.parent / "learning"
    dirs = [
        base_dir / "snapshots",
        base_dir / "prompts",
        base_dir / "feedback"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    return base_dir


def step1_ingest_social_stats() -> Dict:
    """
    ステップ1: X/note/Threads指標収集
    
    X: API → CSV → 手動の優先順位で取得
    note: 手動入力のみ
    Threads: 手動入力のみ
    """
    print_header("📥 ステップ1: X/note/Threads指標を収集")
    print("\nハイブリッド方式で各プラットフォームの指標を収集します。\n")
    
    stats: Dict = {}
    source: Dict[str, str] = {}
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # X (Twitter)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"{Colors.BOLD}X (Twitter){Colors.ENDC}")
    print("-" * 60)
    
    x_result = ingest_x_stats()
    stats["x"] = x_result["stats"]
    source["x"] = x_result["source"]
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # note
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n{Colors.BOLD}note{Colors.ENDC}")
    print("-" * 60)
    print("📝 note Analytics画面の直近記事指標を入力してください")
    print(f"（{Colors.OKCYAN}スキップ: Enter{Colors.ENDC}）\n")
    
    views = input("  閲覧数（View）: ").strip()
    likes = input("  スキ数: ").strip()
    comments = input("  コメント数: ").strip()
    
    stats["note"] = {
        "views": int(views) if views else 0,
        "likes": int(likes) if likes else 0,
        "comments": int(comments) if comments else 0,
        "like_rate": (
            (int(likes) / int(views) * 100)
            if views and likes and int(views) > 0
            else 0
        )
    }
    source["note"] = "manual"
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Threads
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n{Colors.BOLD}Threads{Colors.ENDC}")
    print("-" * 60)
    print("📝 Threads投稿の指標を入力してください")
    print(f"（{Colors.OKCYAN}スキップ: Enter{Colors.ENDC}）\n")
    
    t_views = input("  閲覧数: ").strip()
    t_likes = input("  いいね数: ").strip()
    t_replies = input("  リプライ数: ").strip()
    t_reposts = input("  再投稿数: ").strip()
    
    total_engagement = (
        (int(t_likes) if t_likes else 0) +
        (int(t_replies) if t_replies else 0) +
        (int(t_reposts) if t_reposts else 0)
    )
    
    stats["threads"] = {
        "views": int(t_views) if t_views else 0,
        "likes": int(t_likes) if t_likes else 0,
        "replies": int(t_replies) if t_replies else 0,
        "reposts": int(t_reposts) if t_reposts else 0,
        "engagement_rate": (
            (total_engagement / int(t_views) * 100)
            if t_views and int(t_views) > 0
            else 0
        )
    }
    source["threads"] = "manual"
    
    # スナップショット保存
    base_dir = ensure_directories()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    snapshot_path = base_dir / "snapshots" / f"{timestamp}_stats.json"
    
    snapshot_data = {
        "timestamp": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "source": source,
        "stats": stats
    }
    
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
    
    print()
    print_success(f"スナップショット保存: {snapshot_path.name}")
    
    # サマリー表示
    print("\n📊 収集結果サマリー:")
    print("=" * 60)
    for platform, data in stats.items():
        print(f"\n{Colors.BOLD}{platform.upper()}{Colors.ENDC} "
              f"[{Colors.OKCYAN}{source[platform]}{Colors.ENDC}]")
        for key, value in data.items():
            if "rate" in key:
                print(f"  {key}: {value:.2f}%")
            else:
                print(f"  {key}: {value:,}")
    
    return snapshot_data


def ingest_x_stats() -> Dict:
    """
    X指標を取得（API → CSV → 手動の優先順位）
    
    Returns:
        {"stats": {...}, "source": "api"|"csv"|"manual"}
    """
    # 優先度1: API取得
    if os.path.exists(".env"):
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            bearer_token = os.getenv("X_BEARER_TOKEN")
            username = os.getenv("X_USERNAME_GETHINU") or "gethinu"
            
            if bearer_token:
                print(f"🔌 X API接続試行中（@{username}）...")
                
                # x_api_analyzer.pyを動的インポート
                import sys
                sys.path.insert(0, str(Path(__file__).parent))
                from x_api_analyzer import XAnalyzer
                
                analyzer = XAnalyzer(bearer_token)
                df = analyzer.fetch_user_tweets(
                    username=username,
                    max_results=10
                )
                
                if not df.empty:
                    total_impressions = int(df["impression_count"].sum())
                    total_engagements = int(df["engagement_total"].sum())
                    
                    stats = {
                        "impressions": total_impressions,
                        "engagements": total_engagements,
                        "likes": int(df["like_count"].sum()),
                        "retweets": int(df["retweet_count"].sum()),
                        "replies": int(df["reply_count"].sum()),
                        "quotes": int(df["quote_count"].sum()),
                        "engagement_rate": (
                            (total_engagements / total_impressions * 100)
                            if total_impressions > 0
                            else 0
                        ),
                        "avg_engagement_per_post": (
                            total_engagements / len(df)
                            if len(df) > 0
                            else 0
                        ),
                        "sample_size": len(df)
                    }
                    
                    print_success(f"X API取得成功（{len(df)}投稿）")
                    return {"stats": stats, "source": "api"}
        
        except Exception as e:
            print_warning(f"X API取得失敗: {e}")
    
    # 優先度2: CSV読み込み
    input_dir = Path(__file__).parent.parent / "input"
    csv_files = sorted(
        input_dir.glob("TwExportly_*.csv"),
        reverse=True
    )
    
    if csv_files:
        print(f"\n📂 CSVファイル検出: {csv_files[0].name}")
        use_csv = input("  このCSVを使用しますか？ (y/n): ").strip().lower()
        
        if use_csv == "y":
            try:
                import pandas as pd
                df = pd.read_csv(csv_files[0])
                
                # TwExportly形式のカラム名
                # favorite_count, retweet_count, reply_count, quote_count, view_count
                total_likes = int(df["favorite_count"].sum()) if "favorite_count" in df.columns else 0
                total_retweets = int(df["retweet_count"].sum()) if "retweet_count" in df.columns else 0
                total_replies = int(df["reply_count"].sum()) if "reply_count" in df.columns else 0
                total_quotes = int(df["quote_count"].sum()) if "quote_count" in df.columns else 0
                total_impressions = int(df["view_count"].sum()) if "view_count" in df.columns else 0
                total_engagements = total_likes + total_retweets + total_replies + total_quotes
                
                stats = {
                    "impressions": total_impressions,
                    "engagements": total_engagements,
                    "likes": total_likes,
                    "retweets": total_retweets,
                    "replies": total_replies,
                    "quotes": total_quotes,
                    "engagement_rate": (
                        (total_engagements / total_impressions * 100)
                        if total_impressions > 0
                        else 0
                    ),
                    "avg_engagement_per_post": (
                        total_engagements / len(df)
                        if len(df) > 0
                        else 0
                    ),
                    "sample_size": len(df)
                }
                
                print_success(f"CSV読み込み成功（{len(df)}投稿）")
                return {"stats": stats, "source": "csv"}
            
            except Exception as e:
                print_warning(f"CSV読み込み失敗: {e}")
    
    # 優先度3: 手動入力
    print("\n📝 X指標を手動で入力してください")
    print(f"（直近10投稿の合計値を推奨、{Colors.OKCYAN}スキップ: Enter{Colors.ENDC}）\n")
    
    impressions = input("  インプレッション数: ").strip()
    likes = input("  いいね数: ").strip()
    retweets = input("  リポスト数: ").strip()
    replies = input("  リプライ数: ").strip()
    quotes = input("  引用RT数: ").strip()
    
    total_impressions = int(impressions) if impressions else 0
    total_likes = int(likes) if likes else 0
    total_retweets = int(retweets) if retweets else 0
    total_replies = int(replies) if replies else 0
    total_quotes = int(quotes) if quotes else 0
    total_engagements = total_likes + total_retweets + total_replies + total_quotes
    
    stats = {
        "impressions": total_impressions,
        "engagements": total_engagements,
        "likes": total_likes,
        "retweets": total_retweets,
        "replies": total_replies,
        "quotes": total_quotes,
        "engagement_rate": (
            (total_engagements / total_impressions * 100)
            if total_impressions > 0
            else 0
        ),
        "avg_engagement_per_post": 0,  # 手動入力では投稿数不明
        "sample_size": 1
    }
    
    return {"stats": stats, "source": "manual"}


def step2_define_goal_deliverable(goal: Optional[str] = None, deliverable: Optional[str] = None) -> Dict:
    """
    ステップ2: 目的と成果物の明確化
    
    Args:
        goal: コマンドラインから指定された目的（オプション）
        deliverable: コマンドラインから指定された成果物（オプション）
    """
    print_header("🎯 ステップ2: 目的と成果物を明確化")
    print("\n今回の投稿の目的と成果物を定義します。\n")
    
    # 目的の定義
    if not goal:
        print("💡 目的の例:")
        print("  - noteでリード（メールアドレス）10件獲得")
        print("  - Xでフォロワー50人増加")
        print("  - 特定記事への誘導100クリック")
        print()
        goal = input("📌 今回の目的: ").strip()
        if not goal:
            goal = "エンゲージメント向上"
    
    # 成果物の定義
    if not deliverable:
        print("\n💡 成果物の例:")
        print("  - 2600文字のnote記事")
        print("  - 280文字以内のX投稿3本")
        print("  - Threads投稿（画像3枚付き）")
        print()
        deliverable = input("📦 成果物の形式: ").strip()
        if not deliverable:
            deliverable = "SNS投稿"
    
    # ターゲットペルソナ
    print("\n💡 ターゲットペルソナの例:")
    print("  - 30代会社員（副業検討中）")
    print("  - 20代フリーランス（収入不安定）")
    print()
    persona = input("👤 ターゲットペルソナ: ").strip()
    if not persona:
        persona = "一般ユーザー"
    
    # KPI設定
    print("\n💡 KPIの例:")
    print("  - エンゲージメント率3%以上")
    print("  - 保存率1.5%以上")
    print("  - クリック率5%以上")
    print()
    kpi = input("📈 目標KPI: ").strip()
    if not kpi:
        kpi = "エンゲージメント率向上"
    
    definition = {
        "goal": goal,
        "deliverable": deliverable,
        "persona": persona,
        "kpi": kpi,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 確認表示
    print("\n✅ 定義完了:")
    print("-" * 50)
    print(f"目的      : {goal}")
    print(f"成果物    : {deliverable}")
    print(f"ペルソナ  : {persona}")
    print(f"目標KPI   : {kpi}")
    
    return definition


def step3_review_and_improve(snapshot_data: Optional[Dict] = None) -> str:
    """
    ステップ3: 数値検証とAI改善指示
    
    前回の成果を分析し、AI向けの改善指示プロンプトを生成
    """
    print_header("📊 ステップ3: 数値検証とAI改善指示")
    
    base_dir = ensure_directories()
    snapshots_dir = base_dir / "snapshots"
    
    # 前回のスナップショット読み込み
    snapshots = sorted(snapshots_dir.glob("*_stats.json"), reverse=True)
    
    if len(snapshots) < 2:
        print_warning("前回データが不足しています（最低2回分必要）")
        print("   初回実行の場合は、次回から改善提案が表示されます。")
        return ""
    
    # 最新2件を比較
    with open(snapshots[0], "r", encoding="utf-8") as f:
        latest = json.load(f)
    with open(snapshots[1], "r", encoding="utf-8") as f:
        previous = json.load(f)
    
    print(f"\n比較対象:")
    print(f"  前回: {previous['timestamp']}")
    print(f"  今回: {latest['timestamp']}")
    print()
    
    # プラットフォームごとの変動分析
    improvements = []
    concerns = []
    
    for platform in ["x", "note", "threads"]:
        if platform not in latest["stats"] or platform not in previous["stats"]:
            continue
        
        latest_stats = latest["stats"][platform]
        previous_stats = previous["stats"][platform]
        
        print(f"{Colors.BOLD}{platform.upper()}{Colors.ENDC}")
        print("-" * 40)
        
        for key in latest_stats.keys():
            if key not in previous_stats:
                continue
            
            current = latest_stats[key]
            prev = previous_stats[key]
            
            if prev == 0:
                change_pct = 0
            else:
                change_pct = ((current - prev) / prev) * 100
            
            # 色分け表示
            if change_pct > 10:
                color = Colors.OKGREEN
                symbol = "📈"
                improvements.append(f"{platform}の{key}が{change_pct:.1f}%向上")
            elif change_pct < -10:
                color = Colors.FAIL
                symbol = "📉"
                concerns.append(f"{platform}の{key}が{change_pct:.1f}%低下")
            else:
                color = Colors.ENDC
                symbol = "➡️ "
            
            if "rate" in key:
                print(f"  {symbol} {key}: {prev:.2f}% → {current:.2f}% ({color}{change_pct:+.1f}%{Colors.ENDC})")
            else:
                print(f"  {symbol} {key}: {prev:,} → {current:,} ({color}{change_pct:+.1f}%{Colors.ENDC})")
        
        print()
    
    # AI改善指示プロンプト生成
    prompt = generate_improvement_prompt(improvements, concerns, latest, previous)
    
    # プロンプト保存
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    prompt_path = base_dir / "prompts" / f"{timestamp}_improvement.md"
    
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    print_success(f"改善指示プロンプト保存: {prompt_path.name}")
    
    # プロンプト表示
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}🤖 AIへの改善指示プロンプト{Colors.ENDC}")
    print("=" * 60)
    print(prompt)
    print("=" * 60)
    
    # クリップボードコピー
    if HAS_CLIPBOARD:
        try:
            pyperclip.copy(prompt)
            print_success("クリップボードにコピーしました！")
            print_info("GitHub Copilot Chatに貼り付けて使用してください")
        except Exception:
            pass
    
    return prompt


def generate_improvement_prompt(improvements: List[str], concerns: List[str], 
                                latest: Dict, previous: Dict) -> str:
    """AI改善指示プロンプトを生成"""
    
    prompt = f"""# 投稿成果分析と改善指示

## 📊 前回との比較結果

### ✅ 改善されたポイント
"""
    
    if improvements:
        for item in improvements:
            prompt += f"- {item}\n"
    else:
        prompt += "- （該当なし）\n"
    
    prompt += "\n### ⚠️ 懸念点\n"
    
    if concerns:
        for item in concerns:
            prompt += f"- {item}\n"
    else:
        prompt += "- （該当なし）\n"
    
    prompt += """

## 🎯 改善指示

上記の分析結果を踏まえ、以下の観点で次回投稿の改善案を3つ提案してください：

1. **エンゲージメント率向上**: どのような工夫でユーザーの反応を引き出せるか
2. **リーチ拡大**: インプレッション数を増やすための施策
3. **コンバージョン改善**: 目的（リード獲得/フォロワー増加等）達成のための導線設計

### 提案フォーマット
各改善案は以下の形式で記載してください：

```
【改善案1】タイトル
- 現状の問題: 
- 改善アクション: 
- 期待効果: 
```

### 制約条件
- 実装可能な具体的施策に絞る
- 過去のデータに基づいた根拠を示す
- 1つの改善案は200文字以内で簡潔に
"""
    
    return prompt


def step4_replay_success_cases() -> None:
    """
    ステップ4: 過去の成功例で再教育
    
    過去の高成果投稿を参照してベストプラクティスを抽出
    """
    print_header("🔄 ステップ4: 過去の成功例を参照")
    
    base_dir = ensure_directories()
    feedback_dir = base_dir / "feedback"
    
    # フィードバックファイル読み込み
    feedback_files = sorted(feedback_dir.glob("*.json"), reverse=True)
    
    if not feedback_files:
        print_warning("フィードバックデータがありません")
        print_info("初回実行後、learning/feedback/にJSONファイルを作成してください")
        print()
        print("📝 フィードバックファイル例:")
        print('```json')
        print('''{
  "date": "2025-11-15",
  "platform": "note",
  "content_summary": "1日15分副業術",
  "metrics": {
    "views": 1200,
    "likes": 85,
    "comments": 12,
    "like_rate": 7.08
  },
  "insights": "共感フックが強く、具体的な数字（15分）が刺さった",
  "what_worked": "時間制約の明示、シーン描写、3ステップ構成",
  "what_failed": "CTA弱い（次回は質問形式で締める）"
}''')
        print('```')
        return
    
    # 上位3件を表示（like_rateやengagement_rate順）
    print("\n📈 過去の高成果投稿Top 3:\n")
    
    success_cases = []
    for fb_file in feedback_files[:10]:  # 最大10件チェック
        try:
            with open(fb_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # 成果指標を抽出（like_rate, engagement_rateなど）
                metrics = data.get("metrics", {})
                score = metrics.get("like_rate", 0) + metrics.get("engagement_rate", 0)
                
                success_cases.append({
                    "file": fb_file.name,
                    "score": score,
                    "data": data
                })
        except Exception:
            continue
    
    # スコア順にソート
    success_cases.sort(key=lambda x: x["score"], reverse=True)
    
    if not success_cases:
        print_warning("有効なフィードバックデータがありません")
        return
    
    # 上位3件表示
    for i, case in enumerate(success_cases[:3], 1):
        data = case["data"]
        print(f"{Colors.BOLD}【{i}位】 {data.get('date', 'N/A')} - {data.get('platform', 'N/A')}{Colors.ENDC}")
        print(f"  内容: {data.get('content_summary', 'N/A')}")
        print(f"  成果: {case['score']:.2f}点")
        
        metrics = data.get("metrics", {})
        print(f"  指標: ", end="")
        print(" / ".join([f"{k}={v}" for k, v in metrics.items()]))
        
        print(f"  {Colors.OKGREEN}✅ 成功要因: {data.get('what_worked', 'N/A')}{Colors.ENDC}")
        print(f"  {Colors.WARNING}⚠️  改善点: {data.get('what_failed', 'N/A')}{Colors.ENDC}")
        print()
    
    # ベストプラクティス抽出
    print(f"{Colors.BOLD}💡 抽出されたベストプラクティス:{Colors.ENDC}")
    print("-" * 50)
    
    all_insights = [case["data"].get("insights", "") for case in success_cases[:3]]
    all_what_worked = [case["data"].get("what_worked", "") for case in success_cases[:3]]
    
    print("【共通の成功パターン】")
    for insight in all_insights:
        if insight:
            print(f"  - {insight}")
    
    print("\n【効果的だった施策】")
    for worked in all_what_worked:
        if worked:
            print(f"  - {worked}")
    
    print()
    print_info("これらのパターンを次回投稿に活用してください")


def interactive_mode():
    """対話モード: 全ステップを順次実行"""
    print_header("🤖 Learning Manager - 自動学習ループツール")
    print("\n4つのステップで投稿成果を自動改善します。\n")
    
    # ステップ1: 指標収集
    snapshot_data = step1_ingest_social_stats()
    
    input("\n⏸️  Enterキーで次のステップへ...")
    
    # ステップ2: 目的・成果物定義
    definition = step2_define_goal_deliverable()
    
    input("\n⏸️  Enterキーで次のステップへ...")
    
    # ステップ3: 数値検証と改善指示
    step3_review_and_improve(snapshot_data)
    
    input("\n⏸️  Enterキーで最終ステップへ...")
    
    # ステップ4: 成功例参照
    step4_replay_success_cases()
    
    print("\n" + "=" * 60)
    print_success("全ステップ完了！")
    print_info("生成されたプロンプトをGitHub Copilot Chatで使用してください")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Learning Manager - 自動学習ループツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python learning_manager.py                # 対話モード（全ステップ）
  python learning_manager.py --ingest       # 指標収集のみ
  python learning_manager.py --review       # KPI分析のみ
  python learning_manager.py --replay       # 成功例参照のみ
  python learning_manager.py --goal "noteリード10件" --deliverable "2600文字記事"
"""
    )
    
    parser.add_argument("--ingest", action="store_true", help="指標収集のみ実行")
    parser.add_argument("--review", action="store_true", help="KPI分析のみ実行")
    parser.add_argument("--replay", action="store_true", help="成功例参照のみ実行")
    parser.add_argument("--goal", type=str, help="目的を指定")
    parser.add_argument("--deliverable", type=str, help="成果物を指定")
    
    args = parser.parse_args()
    
    # ディレクトリ確認
    ensure_directories()
    
    # 個別ステップ実行
    if args.ingest:
        step1_ingest_social_stats()
    elif args.review:
        step3_review_and_improve()
    elif args.replay:
        step4_replay_success_cases()
    elif args.goal or args.deliverable:
        # 目的・成果物指定時は定義ステップのみ
        step2_define_goal_deliverable(args.goal, args.deliverable)
    else:
        # 対話モード
        interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  中断されました")
        sys.exit(0)
    except Exception as e:
        print_error(f"エラー: {e}")
        sys.exit(1)
