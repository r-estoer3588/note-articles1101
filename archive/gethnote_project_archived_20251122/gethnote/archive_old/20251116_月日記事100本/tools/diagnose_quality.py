#!/usr/bin/env python3
"""
記事品質自動診断スクリプト
- タイトルの適切性チェック
- 文字数・構成チェック
- ターゲット層マッチング判定
- 改善優先度スコア算出
"""

import json
import re
from pathlib import Path
from collections import defaultdict


# NG ワード（底辺層向け）
BOTTOM_TIER_WORDS = [
    'パチ', '競馬', '競艇', '競輪', 'ギャンブル', 'タバコ', '酒',
    'コンビニ', '底辺', 'バカ', 'カモ', 'げす', 'マジで', 'ホゲー',
    'お前', '俺', 'ガチで', 'ぶっちゃけ'
]

# OK ワード（会社員向け）
TARGET_WORDS = [
    '会社員', '30代', '実録', '損した', '税金', '確定申告',
    '副業', 'フリーランス', '投資', 'NISA', 'iDeCo',
    '転職', 'キャリア', '年収', '節税', '法人設立'
]

# データソースキーワード
EVIDENCE_WORDS = [
    '国税庁', '金融庁', '厚生労働省', '総務省', '統計',
    '調査', 'データ', '法律', '条文', '制度'
]


def analyze_article(file_path):
    """個別記事を解析"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None
    
    # 基本情報抽出
    lines = content.split('\n')
    title = ''
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break
    
    # 無料部分と有料部分を分離
    free_part = ''
    paid_part = ''
    
    if '【有料部分】' in content or '## 【有料部分】' in content:
        parts = re.split(r'##?\s*【有料部分】', content)
        free_part = parts[0]
        paid_part = parts[1] if len(parts) > 1 else ''
    else:
        free_part = content
    
    # スコアリング
    score = {
        'title_quality': 0,  # タイトル品質（0-10）
        'target_match': 0,   # ターゲット適合度（0-10）
        'evidence_level': 0,  # エビデンスレベル（0-10）
        'structure_score': 0,  # 構造スコア（0-10）
        'total': 0
    }
    
    # 1. タイトル品質
    if '【実録】' in title or '【' in title:
        score['title_quality'] += 3
    if any(word in title for word in ['損した', '失敗', '罠']):
        score['title_quality'] += 3
    if re.search(r'\d+万円', title):
        score['title_quality'] += 2
    if '｜' in title:  # サブタイトルがある
        score['title_quality'] += 2
    
    # 2. ターゲット適合度
    bottom_count = sum(1 for word in BOTTOM_TIER_WORDS if word in content)
    target_count = sum(1 for word in TARGET_WORDS if word in content)
    
    if target_count > bottom_count:
        score['target_match'] = min(10, target_count * 2)
    else:
        score['target_match'] = max(0, 10 - bottom_count)
    
    # 3. エビデンスレベル
    evidence_count = sum(1 for word in EVIDENCE_WORDS if word in content)
    score['evidence_level'] = min(10, evidence_count * 3)
    
    # 4. 構造スコア
    free_length = len(free_part)
    if 800 <= free_length <= 1500:
        score['structure_score'] += 4
    elif free_length > 500:
        score['structure_score'] += 2
    
    if paid_part and len(paid_part) > 1000:
        score['structure_score'] += 3
    
    if '### ' in content:  # 見出し構造がある
        score['structure_score'] += 3
    
    # 総合スコア
    score['total'] = sum([
        score['title_quality'],
        score['target_match'],
        score['evidence_level'],
        score['structure_score']
    ]) / 4
    
    return {
        'title': title,
        'file': str(file_path),
        'free_length': free_length,
        'paid_length': len(paid_part),
        'total_length': len(content),
        'bottom_words': bottom_count,
        'target_words': target_count,
        'evidence_words': evidence_count,
        'score': score,
        'issues': []
    }


def categorize_article(analysis):
    """記事を分類"""
    score = analysis['score']['total']
    issues = []
    
    # 問題点の列挙
    if analysis['bottom_words'] > 5:
        issues.append(f"底辺語彙多数（{analysis['bottom_words']}個）")
    
    if analysis['target_words'] < 3:
        issues.append("会社員向けキーワード不足")
    
    if analysis['evidence_words'] == 0:
        issues.append("エビデンス不足")
    
    if analysis['free_length'] < 500:
        issues.append(f"無料部分が短い（{analysis['free_length']}文字）")
    
    if analysis['paid_length'] < 1000:
        issues.append(f"有料部分が短い（{analysis['paid_length']}文字）")
    
    analysis['issues'] = issues
    
    # 分類
    if score >= 7:
        return 'OK', analysis
    elif score >= 4:
        return '要改善', analysis
    else:
        return '削除候補', analysis


def main():
    print("=" * 80)
    print("📊 げすいぬ記事品質自動診断")
    print("=" * 80)
    
    base_dir = Path(__file__).parent.parent
    master_path = base_dir / "article_master.json"
    
    # マスターデータ読み込み
    with open(master_path, 'r', encoding='utf-8') as f:
        master = json.load(f)
    
    print(f"\n📚 対象記事: {len(master['articles'])}本")
    print("\n🔍 解析中...")
    
    results = {
        'OK': [],
        '要改善': [],
        '削除候補': []
    }
    
    for article in master['articles']:
        article_id = article['id']
        file_path = base_dir / (article['file'] + '.md')
        
        if not file_path.exists():
            continue
        
        analysis = analyze_article(file_path)
        if analysis:
            analysis['id'] = article_id
            analysis['master_title'] = article['title']
            category, analysis = categorize_article(analysis)
            results[category].append(analysis)
    
    # 結果表示
    print(f"\n" + "=" * 80)
    print("📋 診断結果:")
    print(f"  ✅ OK: {len(results['OK'])}本")
    print(f"  ⚠️  要改善: {len(results['要改善'])}本")
    print(f"  ❌ 削除候補: {len(results['削除候補'])}本")
    print("=" * 80)
    
    # 削除候補を表示
    if results['削除候補']:
        print(f"\n❌ 削除候補（{len(results['削除候補'])}本）:")
        for item in sorted(results['削除候補'],
                          key=lambda x: x['score']['total'])[:20]:
            print(f"  ID{item['id']:03d}: {item['master_title'][:40]}")
            print(f"    スコア: {item['score']['total']:.1f}/10")
            print(f"    問題: {', '.join(item['issues'][:3])}")
    
    # 要改善を優先度順に表示
    if results['要改善']:
        print(f"\n⚠️  要改善（優先度順TOP20）:")
        sorted_items = sorted(results['要改善'],
                             key=lambda x: x['score']['total'])
        for item in sorted_items[:20]:
            print(f"  ID{item['id']:03d}: {item['master_title'][:40]}")
            print(f"    スコア: {item['score']['total']:.1f}/10")
            print(f"    問題: {', '.join(item['issues'][:2])}")
    
    # OKリストも表示
    if results['OK']:
        print(f"\n✅ 高品質記事（TOP10）:")
        sorted_items = sorted(results['OK'],
                             key=lambda x: x['score']['total'],
                             reverse=True)
        for item in sorted_items[:10]:
            print(f"  ID{item['id']:03d}: {item['master_title'][:40]}")
            print(f"    スコア: {item['score']['total']:.1f}/10")
    
    # 改善推奨アクション
    print(f"\n" + "=" * 80)
    print("💡 推奨アクション:")
    print(f"  1. 削除候補{len(results['削除候補'])}本を削除 or 大幅書き直し")
    print(f"  2. 要改善{len(results['要改善'])}本を優先度順に修正")
    print(f"  3. OK{len(results['OK'])}本をベースに品質基準を確立")
    print("=" * 80)
    
    # JSON出力
    output_path = base_dir / "tools" / "quality_report.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 詳細レポート: {output_path}")


if __name__ == "__main__":
    main()
