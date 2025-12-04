#!/usr/bin/env python3
"""
X投稿用のビジュアル画像生成スクリプト
Git Story Analyzerの統計をかっこよく可視化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# 日本語フォント設定（Windows環境）
plt.rcParams['font.family'] = ['MS Gothic', 'Yu Gothic', 'Meiryo']

# スタイル設定
plt.style.use('dark_background')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.facecolor'] = '#0d1117'  # GitHub Dark風
plt.rcParams['axes.facecolor'] = '#161b22'

# データ
stats = {
    'total_commits': 691,
    'months': 5,
    'insertions': 7263077,
    'deletions': 7026126,
    'net_lines': 236951,
    'feat': 338,
    'fix': 137,
    'refactor': 220,
    'test': 82,
    'monthly': {
        '2025-08': 68,
        '2025-09': 442,
        '2025-10': 144,
        '2025-11': 35,
        '2025-12': 2
    }
}

# 図を作成（16:9比率でX最適化）
fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3, left=0.08, right=0.95, top=0.92, bottom=0.08)

# タイトル
fig.suptitle('Git Story Generator - 開発統計ダッシュボード', 
             fontsize=28, fontweight='bold', color='#58a6ff')

# 1. 大きな数字（左上）
ax1 = fig.add_subplot(gs[0, :2])
ax1.axis('off')
ax1.text(0.5, 0.7, '691', ha='center', va='center', 
         fontsize=80, fontweight='bold', color='#58a6ff')
ax1.text(0.5, 0.3, 'コミット / 3.5ヶ月', ha='center', va='center',
         fontsize=20, color='#8b949e')
ax1.text(0.5, 0.05, '1日平均 4.5 コミット', ha='center', va='center',
         fontsize=16, color='#30363d', style='italic')

# 2. コード変更量（右上）
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
ax2.text(0.5, 0.75, '+7.2M', ha='center', va='center',
         fontsize=36, fontweight='bold', color='#3fb950')
ax2.text(0.5, 0.5, '-7.0M', ha='center', va='center',
         fontsize=36, fontweight='bold', color='#f85149')
ax2.text(0.5, 0.2, '純増: 237K行', ha='center', va='center',
         fontsize=18, color='#58a6ff')

# 3. 月別コミット数（中央）
ax3 = fig.add_subplot(gs[1, :])
months = list(stats['monthly'].keys())
counts = list(stats['monthly'].values())
colors = ['#238636', '#238636', '#1f6feb', '#1f6feb', '#8b949e']

bars = ax3.barh(months, counts, color=colors, edgecolor='#30363d', linewidth=2)
ax3.set_xlabel('コミット数', fontsize=14, color='#c9d1d9')
ax3.set_title('月別コミット推移', fontsize=18, fontweight='bold', color='#c9d1d9', pad=10)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#30363d')
ax3.spines['bottom'].set_color('#30363d')
ax3.tick_params(colors='#8b949e')
ax3.grid(axis='x', alpha=0.2, color='#30363d')

# 数字ラベル
for i, (bar, count) in enumerate(zip(bars, counts)):
    ax3.text(count + 10, i, f'{count}', va='center', fontsize=14, 
             color='#c9d1d9', fontweight='bold')

# 4. タイプ別円グラフ（左下）
ax4 = fig.add_subplot(gs[2, 0])
type_labels = ['新機能\n48.9%', '修正\n19.8%', 'リファク\n31.8%', 'テスト\n11.9%']
type_values = [stats['feat'], stats['fix'], stats['refactor'], stats['test']]
type_colors = ['#3fb950', '#f85149', '#a371f7', '#d29922']

wedges, texts = ax4.pie(type_values, labels=type_labels, colors=type_colors,
                        startangle=90, textprops={'fontsize': 12, 'color': 'white', 'fontweight': 'bold'})
ax4.set_title('コミットタイプ', fontsize=16, fontweight='bold', color='#c9d1d9', pad=10)

# 5. ハイライト（中央下）
ax5 = fig.add_subplot(gs[2, 1])
ax5.axis('off')
highlights = [
    ('🔥 最多月', '9月: 442コミット'),
    ('⚡ 1日最大', '14.7コミット'),
    ('📈 最大追加', '+7,686行（8/17）'),
]
y_pos = 0.8
for emoji, text in highlights:
    ax5.text(0.1, y_pos, emoji, fontsize=24, va='center')
    ax5.text(0.3, y_pos, text, fontsize=14, va='center', color='#c9d1d9')
    y_pos -= 0.3

# 6. ロゴ/ブランディング（右下）
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')
ax6.text(0.5, 0.6, 'Git Story\nGenerator', ha='center', va='center',
         fontsize=22, fontweight='bold', color='#58a6ff', style='italic')
ax6.text(0.5, 0.3, 'by @your_handle', ha='center', va='center',
         fontsize=12, color='#8b949e')
# GitHubアイコン風の装飾
circle = patches.Circle((0.5, 0.1), 0.08, color='#58a6ff', alpha=0.3)
ax6.add_patch(circle)

# 保存
output_path = Path(r'C:\Repos\note-articles\results_images\git_story_stats.png')
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
print(f'✅ 画像を保存しました: {output_path}')
print(f'📊 サイズ: 16:9 (X最適化)')
print(f'🎨 スタイル: GitHub Dark Theme')

plt.close()

# 追加: シンプル版も作成（モバイル表示用）
fig2, ax = plt.subplots(figsize=(10, 10), facecolor='#0d1117')
ax.set_facecolor('#161b22')
ax.axis('off')

# 中央に大きく数字
ax.text(0.5, 0.75, '691', ha='center', va='center',
        fontsize=120, fontweight='bold', color='#58a6ff', 
        transform=ax.transAxes)
ax.text(0.5, 0.6, 'コミット', ha='center', va='center',
        fontsize=32, color='#c9d1d9', transform=ax.transAxes)

# サブ情報
ax.text(0.5, 0.45, '3.5ヶ月で 23万行のコード', ha='center', va='center',
        fontsize=20, color='#8b949e', transform=ax.transAxes)
ax.text(0.5, 0.38, '新機能 338 | 修正 137 | リファク 220', ha='center', va='center',
        fontsize=16, color='#8b949e', transform=ax.transAxes)

# ボトム
ax.text(0.5, 0.15, 'Git Story Generator', ha='center', va='center',
        fontsize=28, fontweight='bold', color='#58a6ff', 
        style='italic', transform=ax.transAxes)
ax.text(0.5, 0.08, '開発履歴を自動でストーリー化', ha='center', va='center',
        fontsize=18, color='#c9d1d9', transform=ax.transAxes)

output_path_simple = Path(r'C:\Repos\note-articles\results_images\git_story_stats_simple.png')
plt.savefig(output_path_simple, dpi=300, bbox_inches='tight', facecolor='#0d1117')
print(f'✅ シンプル版も保存: {output_path_simple}')

plt.close()

print('\n📱 X投稿用画像の準備完了！')
print('次のステップ: results_images/ フォルダの画像をXに添付して投稿')
