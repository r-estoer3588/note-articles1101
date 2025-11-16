#!/usr/bin/env python3
"""
厳選30本の記事選定スクリプト
品質スコア・テーマの重要度・市場需要から最適な30本を抽出
"""

import json
from pathlib import Path

# テーマ別の重要度スコア（市場需要）
THEME_PRIORITY = {
    '税金': 10,
    '確定申告': 10,
    '副業': 9,
    'フリーランス': 9,
    '投資': 9,
    'NISA': 9,
    'iDeCo': 9,
    '転職': 8,
    '年収': 8,
    '節税': 8,
    '法人設立': 8,
    '相続': 7,
    '保険': 7,
    '電子マネー': 7,
    '暗号資産': 7,
    '不動産': 7,
    '住宅ローン': 7,
    'キャリア': 6,
    '起業': 6,
    '退職': 6,
    'テレワーク': 5,
}


def calculate_priority_score(article, analysis):
    """記事の優先度スコアを計算"""
    # 基本スコア（品質スコア）
    quality_score = analysis['score']['total']
    
    # テーマスコア
    theme_score = 0
    title = article['title']
    for theme, priority in THEME_PRIORITY.items():
        if theme in title:
            theme_score = priority
            break
    
    # 総合スコア
    total = quality_score + theme_score
    
    return {
        'id': article['id'],
        'title': article['title'],
        'quality_score': quality_score,
        'theme_score': theme_score,
        'total_score': total,
        'category': article['category'],
        'issues': analysis['issues']
    }


def main():
    print("=" * 80)
    print("🎯 厳選30本の記事選定")
    print("=" * 80)
    
    base_dir = Path(__file__).parent.parent
    master_path = base_dir / "article_master.json"
    report_path = base_dir / "tools" / "quality_report.json"
    
    # データ読み込み
    with open(master_path, 'r', encoding='utf-8') as f:
        master = json.load(f)
    
    with open(report_path, 'r', encoding='utf-8') as f:
        quality_report = json.load(f)
    
    # 全記事の優先度スコアを計算
    all_analyses = {}
    for category in ['OK', '要改善', '削除候補']:
        for analysis in quality_report[category]:
            all_analyses[analysis['id']] = analysis
    
    candidates = []
    for article in master['articles']:
        if article['id'] in all_analyses:
            analysis = all_analyses[article['id']]
            priority = calculate_priority_score(article, analysis)
            candidates.append(priority)
    
    # 優先度順にソート
    candidates.sort(key=lambda x: x['total_score'], reverse=True)
    
    # TOP30を抽出
    selected_30 = candidates[:30]
    
    print(f"\n📊 選定結果:")
    print(f"  対象候補: {len(candidates)}本")
    print(f"  選定: 30本")
    print()
    
    print("=" * 80)
    print("✅ 厳選30本リスト（優先度順）")
    print("=" * 80)
    
    for i, item in enumerate(selected_30, 1):
        print(f"\n{i:2d}. ID{item['id']:03d}: {item['title']}")
        print(f"    総合: {item['total_score']:.1f} "
              f"(品質: {item['quality_score']:.1f} + "
              f"テーマ: {item['theme_score']})")
        print(f"    カテゴリ: {item['category']}")
        if item['issues']:
            print(f"    修正要: {', '.join(item['issues'][:2])}")
    
    # カテゴリ別の分布
    print(f"\n" + "=" * 80)
    print("📋 カテゴリ別分布:")
    category_count = {}
    for item in selected_30:
        cat = item['category']
        category_count[cat] = category_count.get(cat, 0) + 1
    
    for cat, count in sorted(category_count.items(),
                             key=lambda x: x[1],
                             reverse=True):
        print(f"  {cat}: {count}本")
    
    # リライト優先度グループ分け
    print(f"\n" + "=" * 80)
    print("🔧 リライト戦略:")
    print("=" * 80)
    
    high_priority = [x for x in selected_30 if x['quality_score'] >= 7]
    mid_priority = [x for x in selected_30
                    if 4 <= x['quality_score'] < 7]
    low_priority = [x for x in selected_30 if x['quality_score'] < 4]
    
    print(f"\n【Phase 1】軽微な修正（{len(high_priority)}本）")
    print("  - エビデンス追加")
    print("  - タイトル最適化")
    print("  - 底辺語彙の置換")
    print("  対象ID:", [x['id'] for x in high_priority])
    
    print(f"\n【Phase 2】中程度の書き直し（{len(mid_priority)}本）")
    print("  - ストーリー強化")
    print("  - データ追加")
    print("  - 構成見直し")
    print("  対象ID:", [x['id'] for x in mid_priority][:10], "...")
    
    print(f"\n【Phase 3】ゼロから書き直し（{len(low_priority)}本）")
    print("  - 完全リライト")
    print("  - テーマ再設定")
    print("  - 実体験追加")
    print("  対象ID:", [x['id'] for x in low_priority][:10], "...")
    
    # 推定工数
    print(f"\n" + "=" * 80)
    print("⏱️  推定工数:")
    print("=" * 80)
    
    phase1_hours = len(high_priority) * 0.5
    phase2_hours = len(mid_priority) * 1.5
    phase3_hours = len(low_priority) * 2.5
    total_hours = phase1_hours + phase2_hours + phase3_hours
    
    print(f"  Phase 1: {phase1_hours:.1f}時間")
    print(f"  Phase 2: {phase2_hours:.1f}時間")
    print(f"  Phase 3: {phase3_hours:.1f}時間")
    print(f"  合計: {total_hours:.1f}時間（約{total_hours/8:.1f}営業日）")
    
    # 選定リストをJSON保存
    output_path = base_dir / "tools" / "selected_30.json"
    output_data = {
        'selected_articles': selected_30,
        'phase1': [x['id'] for x in high_priority],
        'phase2': [x['id'] for x in mid_priority],
        'phase3': [x['id'] for x in low_priority],
        'estimated_hours': total_hours
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 選定リスト: {output_path}")
    
    print(f"\n" + "=" * 80)
    print("🚀 次のステップ:")
    print("  1. Phase 1から着手（ID:", high_priority[0]['id'] if high_priority else 'なし', "）")
    print("  2. リライトツール実行")
    print("  3. 1記事完成→即テスト投稿")
    print("=" * 80)


if __name__ == "__main__":
    main()
