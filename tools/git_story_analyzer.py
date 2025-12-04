#!/usr/bin/env python3
"""
Git Story Analyzer - コミット履歴から開発ストーリーの素材を抽出
MVP版：統計分析 + GPTプロンプト生成
"""

import re
from pathlib import Path
from datetime import datetime
from typing import NamedTuple
from collections import defaultdict


class CommitStats(NamedTuple):
    """コミット統計データ"""
    total_commits: int
    total_insertions: int
    total_deletions: int
    net_lines: int
    files_changed: int
    
    # タイプ別
    fix_count: int
    feat_count: int
    refactor_count: int
    test_count: int
    
    # 月別
    monthly_commits: dict
    
    # 重要コミット
    top_commits: list  # (date, hash, message, changes)


def parse_detailed_commits(file_path: str) -> list:
    """詳細コミット履歴ファイルをパース"""
    commits = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # ヘッダーをスキップ
    in_data = False
    for line in lines:
        if line.strip().startswith('2025-'):
            in_data = True
        
        if not in_data:
            continue
        
        try:
            # Format: TIMESTAMP|HASH|[TAGS]|CHANGES|MESSAGE|REPO
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            
            timestamp_str, hash_str, tags_str, changes_str, message, repo = parts
            
            # 日時パース
            dt = datetime.strptime(timestamp_str.split('+')[0].strip(), '%Y-%m-%d %H:%M:%S')
            
            # タグ抽出
            tags = []
            if tags_str.strip():
                tags = re.findall(r'\[(.*?)\]', tags_str)
                if tags:
                    tags = tags[0].split(',')
            
            # 変更量パース (+123/-45 (10files))
            insertions = 0
            deletions = 0
            files = 0
            
            match = re.search(r'\+(\d+)/-(\d+) \((\d+)files?\)', changes_str)
            if match:
                insertions = int(match.group(1))
                deletions = int(match.group(2))
                files = int(match.group(3))
            
            commits.append({
                'datetime': dt,
                'hash': hash_str.strip(),
                'tags': tags,
                'insertions': insertions,
                'deletions': deletions,
                'files': files,
                'message': message.strip(),
                'repo': repo.strip()
            })
            
        except Exception as e:
            # パースエラーは無視
            continue
    
    return commits


def analyze_commits(commits: list) -> CommitStats:
    """コミット統計を計算"""
    total_insertions = sum(c['insertions'] for c in commits)
    total_deletions = sum(c['deletions'] for c in commits)
    total_files = sum(c['files'] for c in commits)
    
    # タイプ別カウント
    fix_count = sum(1 for c in commits if any('FIX' in t for t in c['tags']))
    feat_count = sum(1 for c in commits if any('FEAT' in t for t in c['tags']))
    refactor_count = sum(1 for c in commits if any('REFACTOR' in t for t in c['tags']))
    test_count = sum(1 for c in commits if any('TEST' in t for t in c['tags']))
    
    # 月別集計
    monthly = defaultdict(int)
    for c in commits:
        month_key = c['datetime'].strftime('%Y-%m')
        monthly[month_key] += 1
    
    # 大規模変更トップ10
    top_commits = sorted(
        commits,
        key=lambda c: c['insertions'] + c['deletions'],
        reverse=True
    )[:10]
    
    top_list = [
        (
            c['datetime'].strftime('%Y-%m-%d'),
            c['hash'],
            c['message'],
            f"+{c['insertions']}/-{c['deletions']} ({c['files']}files)"
        )
        for c in top_commits
    ]
    
    return CommitStats(
        total_commits=len(commits),
        total_insertions=total_insertions,
        total_deletions=total_deletions,
        net_lines=total_insertions - total_deletions,
        files_changed=total_files,
        fix_count=fix_count,
        feat_count=feat_count,
        refactor_count=refactor_count,
        test_count=test_count,
        monthly_commits=dict(monthly),
        top_commits=top_list
    )


def find_phase_transitions(commits: list) -> list:
    """開発フェーズの転換点を検出"""
    transitions = []
    
    keywords = [
        # リファクタリング・再設計
        ('reorganize', '構造再編成'),
        ('refactor', 'リファクタリング'),
        ('phase', 'フェーズ移行'),
        
        # 機能追加の節目
        ('system', 'システム追加'),
        ('cache', 'キャッシュ設計'),
        ('ci', 'CI/CD導入'),
        ('test', 'テスト基盤'),
        ('scheduler', '自動化'),
        
        # 品質改善
        ('coverage', 'カバレッジ向上'),
        ('diagnostics', '診断機能'),
        ('performance', 'パフォーマンス改善'),
    ]
    
    for commit in commits:
        msg_lower = commit['message'].lower()
        
        for keyword, label in keywords:
            if keyword in msg_lower:
                # 大規模変更のみ（100行以上）
                if commit['insertions'] + commit['deletions'] >= 100:
                    transitions.append({
                        'date': commit['datetime'].strftime('%Y-%m-%d'),
                        'hash': commit['hash'],
                        'label': label,
                        'message': commit['message'],
                        'impact': f"+{commit['insertions']}/-{commit['deletions']}"
                    })
                    break
    
    return transitions[:15]  # 上位15件


def generate_gpt_prompt(commits: list, stats: CommitStats, transitions: list) -> str:
    """GPT用のストーリー生成プロンプトを作成"""
    
    # フェーズ分割（月単位）
    phases = defaultdict(list)
    for c in commits:
        month = c['datetime'].strftime('%Y-%m')
        phases[month].append(c)
    
    prompt = f"""# 開発ストーリー生成プロンプト

## プロジェクト概要
- 期間: {commits[0]['datetime'].strftime('%Y年%m月')} ～ {commits[-1]['datetime'].strftime('%Y年%m月')} ({len(stats.monthly_commits)}ヶ月)
- 総コミット数: {stats.total_commits}
- コード変更: +{stats.total_insertions:,}行 / -{stats.total_deletions:,}行 (純増: {stats.net_lines:,}行)
- 変更ファイル数: {stats.files_changed:,}

## コミット内訳
- 新機能(FEAT): {stats.feat_count} ({stats.feat_count/stats.total_commits*100:.1f}%)
- 修正(FIX): {stats.fix_count} ({stats.fix_count/stats.total_commits*100:.1f}%)
- リファクタリング(REFACTOR): {stats.refactor_count} ({stats.refactor_count/stats.total_commits*100:.1f}%)
- テスト(TEST): {stats.test_count} ({stats.test_count/stats.total_commits*100:.1f}%)

## 月別推移
"""
    
    for month in sorted(stats.monthly_commits.keys()):
        count = stats.monthly_commits[month]
        prompt += f"- {month}: {count} commits\n"
    
    prompt += f"""
## 開発の転換点（重要コミット）
"""
    
    for trans in transitions:
        prompt += f"- **{trans['date']}** [{trans['label']}] {trans['message']} ({trans['impact']})\n"
    
    prompt += f"""

---

## 指示

上記のGit履歴データをもとに、以下の形式で「開発ストーリー記事」の骨組みを作成してください。

### 出力形式

#### タイトル案（3つ提案）
1. [読者の感情を刺激するタイトル]
2. [技術的な成長を強調するタイトル]
3. [数字を使った具体的なタイトル]

#### 構成案

**序章：なぜこの開発を始めたのか**（200-300字）
- 開発前の課題・痛み
- 「こうなりたい」という理想
- 決断した瞬間

**フェーズ1：[月]（約X commits）**
- 見出し: [このフェーズの目的を一言で]
- 主な取り組み:
  - [重要コミット1]から何をしようとしたか
  - [重要コミット2]でどんな失敗をしたか
- 学び: このフェーズで得た教訓

**フェーズ2：[月]（約Y commits）**
（同様の構成）

**フェーズ3：[月]（約Z commits）**
（同様の構成）

**終章：今、そしてこれから**（200-300字）
- 開発を通じて変わったこと
- 今も続けている改善
- 読者へのメッセージ

### 制約条件
1. 各フェーズは「挑戦→挫折→突破」の物語構造にする
2. 技術用語は必ず一言で補足説明を入れる
3. 数字（コミット数、変更行数など）を積極的に使う
4. 読者が「自分もできそう」と思える書き方にする
5. 感情の動き（焦り・迷い・手応え）を最低1つは入れる

### ターゲット読者
- 同じような開発を考えている人
- ポートフォリオ作成に悩んでいるエンジニア
- 個人開発の進め方を知りたい人
"""
    
    return prompt


def main():
    # 既存の詳細コミット履歴を読み込み
    input_file = Path(r"C:\Repos\note-articles\articles\2025-12-03_quant_trading_journey\commit_history_detailed.txt")
    
    if not input_file.exists():
        print(f"エラー: {input_file} が見つかりません")
        return
    
    print("📊 コミット履歴を解析中...")
    commits = parse_detailed_commits(str(input_file))
    print(f"  {len(commits)} commits を読み込みました")
    
    print("\n📈 統計を計算中...")
    stats = analyze_commits(commits)
    
    print("\n🔍 フェーズ転換点を検出中...")
    transitions = find_phase_transitions(commits)
    
    # 統計レポート表示
    print("\n" + "="*60)
    print("📊 統計レポート")
    print("="*60)
    print(f"総コミット数: {stats.total_commits}")
    print(f"開発期間: {len(stats.monthly_commits)}ヶ月")
    print(f"コード変更: +{stats.total_insertions:,} / -{stats.total_deletions:,} (純増: {stats.net_lines:,}行)")
    print(f"\nタイプ別:")
    print(f"  新機能: {stats.feat_count} ({stats.feat_count/stats.total_commits*100:.1f}%)")
    print(f"  修正: {stats.fix_count} ({stats.fix_count/stats.total_commits*100:.1f}%)")
    print(f"  リファクタ: {stats.refactor_count} ({stats.refactor_count/stats.total_commits*100:.1f}%)")
    print(f"  テスト: {stats.test_count} ({stats.test_count/stats.total_commits*100:.1f}%)")
    
    print("\n月別コミット数:")
    for month in sorted(stats.monthly_commits.keys()):
        count = stats.monthly_commits[month]
        bar = "█" * (count // 10)
        print(f"  {month}: {count:3d} {bar}")
    
    print("\n🎯 開発の転換点（上位10件）:")
    for i, trans in enumerate(transitions[:10], 1):
        print(f"{i:2d}. {trans['date']} [{trans['label']}]")
        print(f"    {trans['message'][:60]}... ({trans['impact']})")
    
    # GPTプロンプト生成
    print("\n🤖 GPTプロンプトを生成中...")
    prompt = generate_gpt_prompt(commits, stats, transitions)
    
    # プロンプトをファイルに保存
    output_dir = Path(r"C:\Repos\note-articles\tools")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    prompt_file = output_dir / "gpt_story_prompt.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"\n✅ 完了！")
    print(f"📄 GPTプロンプト: {prompt_file}")
    print(f"\n次のステップ:")
    print(f"1. {prompt_file} を開く")
    print(f"2. 内容をコピーしてChatGPT/Claudeに投げる")
    print(f"3. 生成された記事骨組みを note 記事に展開する")


if __name__ == "__main__":
    main()
