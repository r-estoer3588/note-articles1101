# 米国株自動売買システム開発の全記録：3ヶ月で7システム実装の軌跡

## はじめに

2025年8月、一つの挑戦を始めました。**7つの異なる戦略で米国株の自動売買システムを構築する**というプロジェクトです。

本記事では、8月17日から11月末までの約3.5ヶ月間で、どのようにして完全動作する自動売買フレームワークを一人で構築したかを記録します。

## プロジェクト最終成果

### システム構成

**7つの売買システム:**
- **System 1-2**: ロング戦略（トレンドフォロー）
- **System 3**: ショート戦略（逆張り）
- **System 4**: ブレイクアウト戦略
- **System 5**: モメンタム戦略
- **System 6**: 平均回帰戦略
- **System 7**: SPYヘッジ専用

**最終スペック:**
- 対応銘柄数: 6,200+
- テストカバレッジ: 61%
- 総コード行数: 8,500行
- 総コミット数: 476回
- リポジトリサイズ: 926MB

**技術スタック:**
- Python 3.11
- Streamlit（WebUI）
- pandas, numpy（データ分析）
- EOD Historical Data API
- Alpaca Trading API（ペーパートレード）
- pytest, GitHub Actions（CI/CD）

## 開発の4つのフェーズ

### Phase 1: 基盤構築（8月17日-31日）

**実装内容:**
- System 1-7の基本ロジック
- Streamlit UI
- データキャッシュシステム
- コードフォーマット統一（Black, ruff, isort）

**最初の課題:**
```python
# 問題: データ取得に10分かかる
for symbol in symbols:  # 6,200銘柄
    df = fetch_from_api(symbol)  # API呼び出し

# 解決: キャッシュシステム導入
df = load_cached_data(symbol)  # 5秒で完了（200倍高速化）
```

**キャッシュアーキテクチャ:**
```
full_backup/  (原本: CSV)
    ↓
base/  (指標計算済み: Feather形式)
    ↓
rolling/  (直近60日: 高速アクセス)
```

### Phase 2: アーキテクチャ改善（9月1日-30日）

**3層分離の実現:**
```
Before:
app_system1.py (500行、UI+ロジック混在)

After:
core/system1.py (150行、純粋ロジック)
strategies/system1_strategy.py (100行、キャッシュ連携)
apps/app_system1.py (250行、UIのみ)
```

**メリット:**
- テスト容易性: 純粋関数でユニットテスト可能
- 再利用性: 同じロジックを別UIでも使用可能
- 保守性: UIの変更がロジックに影響しない

**通知システム実装:**
```python
# Slack/Discord Webhook統合
notifier = Notifier(webhook_url=os.getenv("SLACK_WEBHOOK_URL"))
notifier.send_backtest_result({
    'final_equity': 125000,
    'total_return': 25.0,
    'max_drawdown': -12.5,
    'win_rate': 65.0
})
```

### Phase 3: 診断API統合（10月1日-31日）

**課題:**
「なぜこの銘柄が候補に選ばれたのか？」が不透明。

**解決: 診断API導入**
```python
# 全システム共通の診断情報
candidates, diagnostics = generate_system1_candidates(df, current_date)

print(diagnostics)
# {
#   'setup_predicate_count': 150,    # Setup条件を満たした行数
#   'ranked_top_n_count': 10,        # 最終候補数
#   'ranking_source': 'latest_only', # 最新日のみ or 全期間
# }
```

**効果:**
- デバッグ時間: 30分 → 5分（6倍高速化）
- 候補ゼロ時の原因特定が容易に
- システム間の比較が可能に

### Phase 4: 最適化と品質向上（11月1日-30日）

**並列処理導入:**
```python
# Before: 順次処理（20分）
for symbol in symbols:
    result = process_symbol(symbol)

# After: 並列処理（2分、10倍高速化）
from concurrent.futures import ProcessPoolExecutor

workers = int(multiprocessing.cpu_count() * 0.7)
with ProcessPoolExecutor(max_workers=workers) as executor:
    results = list(executor.map(process_symbol, symbols))
```

**CI/CD統合:**
```yaml
# .github/workflows/ci-unified.yml
- name: Lint
  run: |
    ruff check .
    black --check .
    isort --check-only .

- name: Test
  run: pytest --cov=core --cov=common --cov-report=term-missing
```

**カバレッジ向上:**
- 初期: 30%
- 中間: 45%
- 最終: 61%

## 技術的チャレンジと解決策

### チャレンジ1: データ取得の遅さ

**問題:**
6,200銘柄 × 毎日取得 = 10分以上

**試行錯誤:**
1. ❌ 並列API呼び出し → レート制限で失敗
2. ❌ バッチサイズ縮小 → 効果わずか
3. ✅ 3層キャッシュ → 5秒に短縮（成功）

**最終実装:**
```python
class CacheManager:
    def load_price(self, symbol, cache_profile="rolling"):
        # rolling → base → full_backup の順で探索
        for profile in ["rolling", "base", "full_backup"]:
            df = self._try_load(symbol, profile)
            if df is not None:
                return df
        
        # なければAPI取得
        return self.fetch_from_api(symbol)
```

### チャレンジ2: テストの遅さ

**問題:**
全銘柄でテストすると30分かかる。

**解決: テストモード導入**
```python
# scripts/run_all_systems_today.py
python scripts/run_all_systems_today.py --test-mode mini  # 10銘柄、2秒
python scripts/run_all_systems_today.py --test-mode quick  # 50銘柄、10秒
python scripts/run_all_systems_today.py --test-mode sample  # 113銘柄、1分
```

**効果:**
- 開発サイクル: 30分 → 2秒（900倍高速化）
- テスト実行頻度: 1日2回 → 1時間10回

### チャレンジ3: 文字化け問題

**問題:**
Slack通知で日本語が文字化け（`譖ｴ譁ｰ`）

**原因:**
WindowsのデフォルトエンコーディングがCP932

**解決:**
```python
import sys
import io

# 標準出力をUTF-8に強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 開発統計

### 時間配分

**合計開発時間:** 約350時間（3.5ヶ月）

| フェーズ | 時間 | 割合 |
|---------|------|------|
| コーディング | 175時間 | 50% |
| デバッグ | 70時間 | 20% |
| リファクタリング | 53時間 | 15% |
| テスト作成 | 35時間 | 10% |
| ドキュメント | 17時間 | 5% |

### コミット分析

**総コミット数:** 476回
**平均コミット頻度:** 4.5回/日

**コミットメッセージ分類:**
- `feat`: 42% - 新機能追加
- `fix`: 28% - バグ修正
- `refactor`: 15% - リファクタリング
- `chore`: 10% - 環境整備
- `docs`: 3% - ドキュメント
- `test`: 2% - テスト追加

### パフォーマンス改善

| 項目 | Before | After | 改善率 |
|------|--------|-------|--------|
| データ読み込み | 10分 | 5秒 | **120倍** |
| バックテスト | 30分 | 3分 | **10倍** |
| シグナル生成 | 20分 | 2分 | **10倍** |
| テスト実行 | 30分 | 2秒 | **900倍** |

## 学んだ教訓

### 1. 早期リファクタリングの価値

**戦略:**
```
Week 1-2: とにかく動かす（プロトタイプ）
Week 3-4: 設計を整える（リファクタリング）
Week 5-12: 機能拡充（スムーズな開発）
```

**効果:**
- バグ修正時間: 平均1時間 → 20分（67%短縮）
- 新機能追加時間: 平均3時間 → 1時間（67%短縮）

### 2. キャッシュ戦略の重要性

**教訓:**
I/O ボトルネックは最優先で解決すべき。

**数字:**
- 開発サイクル高速化: 200倍
- APIコスト削減: 80%
- ストレス軽減: 計り知れず

### 3. テスト駆動の段階的導入

**失敗したアプローチ:**
最初から100%カバレッジを目指す → 開発が止まる

**成功したアプローチ:**
```
Phase 1: テストなし（0%）
Phase 2: クリティカルパスのみ（30%）
Phase 3: 主要モジュール（45%）
Phase 4: 全モジュール（61%）
```

### 4. AI活用で生産性10倍

**使用したAI:**
- GitHub Copilot: コード補完（60%の時間）
- Claude: アーキテクチャ設計（30%）
- ChatGPT: ドキュメント生成（10%）

**効果:**
- コーディング時間: 60時間 → 6時間（10倍）
- テスト作成時間: 30時間 → 3時間（10倍）
- ドキュメント作成: 15時間 → 1.5時間（10倍）

## コードハイライト

### 診断API（全システム統一）

```python
from core.system1 import generate_system1_candidates

# 候補生成と診断情報を同時取得
candidates, diagnostics = generate_system1_candidates(
    df, 
    current_date='2025-04-10',
    latest_only=True
)

# 診断情報の活用
if diagnostics['ranked_top_n_count'] == 0:
    logger.warning(f"候補ゼロ: Setup通過={diagnostics['setup_predicate_count']}")
```

### 並列処理最適化

```python
from common.performance_optimization import (
    get_optimal_worker_count,
    ParallelBacktestRunner
)

# CPU使用率70%で自動調整
workers = get_optimal_worker_count()

runner = ParallelBacktestRunner(max_workers=workers)
results = runner.run_all_systems(symbols, start_date, end_date)
```

### アラートフレームワーク

```python
from common.alert_framework import AlertManager, make_freshness_alert

manager = AlertManager()
manager.register_condition(
    make_freshness_alert(max_age_seconds=86400)  # 24時間
)

# データ鮮度チェック
manager.check_and_handle({
    'symbol': 'AAPL',
    'last_update': timestamp
})
```

## 今後の展開

### 短期（1-3ヶ月）

- [ ] リアルマネー運用への移行（慎重に）
- [ ] 追加戦略の実装（System 8-10）
- [ ] バックテスト精度向上

### 中期（3-6ヶ月）

- [ ] 機械学習モデルの統合
- [ ] 動的リバランシング
- [ ] リスク管理の高度化

### 長期（6ヶ月以上）

- [ ] マルチアセット対応（暗号通貨、FX等）
- [ ] SaaS化（他のトレーダー向け）
- [ ] オープンソース化（教育目的部分）

## まとめ

3.5ヶ月で一人で926MBのシステムを構築できたのは、以下の要因が大きいです：

1. **AI駆動開発**: GitHub Copilot、Claude、ChatGPTの徹底活用
2. **段階的アプローチ**: 完璧を目指さず、まず動かす
3. **早期リファクタリング**: 2週目で設計を整える
4. **キャッシュ最適化**: ボトルネック解消を最優先
5. **テスト文化**: 段階的にカバレッジを向上

**最も重要な学び:**
「一人でも、適切な設計とツールがあれば大規模システムは作れる」

しかし同時に、「AIは道具であり、設計判断は人間が行う」という原則も再確認しました。

次は、このノウハウを他のプロジェクトにも展開していきます。

---

**プロジェクト情報:**
- リポジトリ: https://github.com/r-estoer3588/quant_trading_system_0510to0906
- 開発期間: 2025年8月17日 - 11月30日
- 開発者: 1名 + AI（Copilot, Claude, ChatGPT）

**技術スタック:**
- Python 3.11
- Streamlit, pandas, numpy
- EOD Historical Data API
- Alpaca Trading API
- pytest, GitHub Actions

**記事執筆日:** 2025年12月3日

#自動売買 #Python #システム開発 #株式投資 #バックテスト #Streamlit #AI駆動開発
