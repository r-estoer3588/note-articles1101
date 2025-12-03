# AI駆動開発で3ヶ月で926MBのシステムを構築：GitHub Copilot、Claude、ChatGPTを使い分けた実践記録

## はじめに

「AIに仕事を奪われる」という話をよく耳にします。しかし、私は逆に**AIを徹底活用して、一人で大規模システムを構築する**という挑戦をしました。

結果：**3ヶ月で926MB、8,500行のコードベース、7つの自動売買システムを実装**

本記事では、GitHub Copilot、Claude、ChatGPTの3つのAIをどう使い分けたか、そしてAI駆動開発で生産性を10倍にした実践ノウハウを全公開します。

## プロジェクト概要

### 開発したシステム

**米国株自動売買システム（教育目的）**
- 7つの異なる売買戦略（Long/Short混合）
- 6,200+銘柄対応
- Streamlit WebUI
- バックテスト機能
- リアルタイムシグナル生成
- Slack/Discord通知

**技術スタック:**
- Python 3.11
- pandas, numpy（データ分析）
- Streamlit（UI）
- pytest（テスト、カバレッジ61%）
- CI/CD（GitHub Actions）

**開発期間:** 2025年8月17日 - 11月末（約3.5ヶ月）
**総コミット数:** 476回
**開発者:** 1名（私）+ 3つのAI

## AI使い分け戦略：適材適所で生産性10倍

### 1. GitHub Copilot：リアルタイムコーディングアシスタント

**使用場面（60%の時間）:**
- コード補完
- 定型処理の自動生成
- リファクタリング支援
- テストコード生成

**具体例1: テクニカル指標の実装**

```python
# コメントを書くだけでCopilotが実装を提案
def calculate_bollinger_bands(df, window=20, num_std=2):
    """ボリンジャーバンド計算"""
    # Copilotが以下を自動生成 ↓
    
    df['SMA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()
    df['BB_upper'] = df['SMA'] + (df['STD'] * num_std)
    df['BB_lower'] = df['SMA'] - (df['STD'] * num_std)
    df['BB_width'] = (df['BB_upper'] - df['BB_lower']) / df['SMA']
    
    return df
```

**Copilotの提案を受け入れた結果:**
- コーディング時間: 5分 → 30秒（10倍高速化）
- タイポエラー: ほぼゼロ

**具体例2: テストコード自動生成**

```python
# test_system1.pyを開いた瞬間、Copilotがテンプレート提案
import pytest
import pandas as pd
from core.system1 import generate_system1_candidates

# "test_"と入力した瞬間に以下を提案
def test_generate_system1_candidates_basic():
    # テストデータ作成
    df = pd.DataFrame({
        'Date': pd.date_range('2025-01-01', periods=100),
        'Close': 100 + pd.Series(range(100)) * 0.5,
        'Volume': 1000000
    })
    
    candidates, diagnostics = generate_system1_candidates(df, '2025-04-10')
    
    assert isinstance(candidates, pd.DataFrame)
    assert 'score' in candidates.columns
```

**テスト作成時間: 20分 → 2分（10倍高速化）**

**Copilotの強み:**
- コンテキスト理解が優秀（既存コードのパターンを学習）
- リアルタイム補完で思考が途切れない
- 命名規則を自動で統一

**Copilotの弱み:**
- 複雑なアーキテクチャ設計は苦手
- 長文の説明や文書生成には不向き

### 2. Claude（Sonnet 4.5）：アーキテクチャ設計と複雑なロジック

**使用場面（30%の時間）:**
- システム全体の設計相談
- 複雑なバグのデバッグ
- パフォーマンス最適化提案
- コードレビュー

**具体例1: キャッシュアーキテクチャ設計**

**私の質問:**
```
6,200銘柄のデータを毎日取得すると10分かかります。
以下の要件でキャッシュシステムを設計してください：
1. 過去データは保持（バックテスト用）
2. 当日データは高速アクセス
3. APIコスト削減
```

**Claudeの回答（要約）:**
```
3層キャッシュアーキテクチャを推奨します：

1. full_backup/ (原本)
   - 全履歴データ（CSV形式）
   - APIから取得した生データ
   - 読み取り専用

2. base/ (指標付与済み)
   - full_backupに指標を計算して追加
   - Feather形式（高速読み込み）
   - 日次更新

3. rolling/ (当日用)
   - 直近60日分のみ
   - 最も頻繁にアクセス
   - メモリキャッシュ可能

フォールバック順序: rolling → base → full_backup
```

**実装コード（Claudeの提案を基に実装）:**
```python
# common/cache_manager.py
class CacheManager:
    def load_price(self, symbol, cache_profile="rolling"):
        """キャッシュからデータ読み込み"""
        
        # 優先順位でフォールバック
        if cache_profile == "rolling":
            for profile in ["rolling", "base", "full_backup"]:
                df = self._try_load(symbol, profile)
                if df is not None:
                    return df
        
        # 見つからなければAPI取得
        return self.fetch_from_api(symbol)
    
    def _try_load(self, symbol, profile):
        """キャッシュから読み込み試行"""
        path = self.cache_dir / profile / f"{symbol}.feather"
        
        if path.exists():
            return pd.read_feather(path)
        
        # Featherがなければ.csv も試す
        csv_path = path.with_suffix('.csv')
        if csv_path.exists():
            return pd.read_csv(csv_path, index_col=0, parse_dates=True)
        
        return None
```

**成果:**
- データ読み込み時間: 10分 → 5秒（120倍高速化）
- APIコスト: 月$50 → $10（80%削減）

**具体例2: 並列処理最適化**

**私の質問:**
```python
# 現在のコード（遅い）
results = []
for symbol in symbols:  # 6,200銘柄
    df = load_data(symbol)
    result = process_data(df)
    results.append(result)
# 実行時間: 約20分
```

**Claudeの提案:**
```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def process_symbol(symbol):
    """単一銘柄の処理（並列化可能な形式）"""
    df = load_data(symbol)
    return process_data(df)

# CPU数の70%を使用（安全マージン）
max_workers = int(multiprocessing.cpu_count() * 0.7)

with ProcessPoolExecutor(max_workers=max_workers) as executor:
    results = list(executor.map(process_symbol, symbols))

# 実行時間: 約2分（10倍高速化）
```

**Claudeからの追加アドバイス:**
```
注意点:
1. Windows環境では if __name__ == "__main__": が必須
2. load_data()がI/O bound の場合は ThreadPoolExecutor を検討
3. メモリ使用量に注意（1プロセスあたり約200MB）
4. プログレスバー表示で進捗可視化を推奨
```

**Claudeの強み:**
- 複雑な設計相談に強い
- 複数の選択肢と理由を提示
- エッジケースの指摘が的確
- 長文での詳細説明

**Claudeの弱み:**
- リアルタイムコーディング支援には不向き
- コードベース全体の把握に制限（コンテキスト制約）

### 3. ChatGPT（GPT-4）：ドキュメント生成と学習

**使用場面（10%の時間）:**
- README、ドキュメント作成
- 技術調査
- エラーメッセージの解説
- 初学者向け説明

**具体例1: README自動生成**

**プロンプト:**
```
以下のプロジェクト構成からREADME.mdを作成してください：
- 7つの売買システム
- Streamlit UI
- バックテスト機能
- テストカバレッジ61%
```

**ChatGPTの出力（一部）:**
```markdown
# Quant Trading System

![CI](https://github.com/.../workflows/CI/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-61%25-brightgreen)

## Features

- **7 Trading Systems**: Long/Short strategies
- **Web UI**: Built with Streamlit
- **Backtesting**: Historical performance analysis
- **Real-time Signals**: Daily signal generation

## Quick Start

\```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app_integrated.py
\```
```

**ドキュメント作成時間: 1時間 → 5分（12倍高速化）**

**具体例2: エラー解説**

**エラーメッセージ:**
```
IndexError: index 10312 is out of bounds for axis 0 with size 252
```

**ChatGPTへの質問:**
```
pandasで "index 10312 is out of bounds" エラーが出ました。
原因と解決策を教えてください。

コード:
df.loc[10312, 'Close']
```

**ChatGPTの回答:**
```
このエラーは、DataFrame に 10312 行目が存在しないことを示しています。

原因:
- df の行数が 252 行しかない
- 10312 は年（西暦）が誤って解釈された可能性

解決策:
1. DatetimeIndex を確認:
   print(df.index.dtype)
   
2. 数値インデックスではなく日付で指定:
   df.loc['2025-04-10', 'Close']
   
3. または .iloc で位置指定:
   df.iloc[-1, df.columns.get_loc('Close')]  # 最終行
```

**ChatGPTの強み:**
- わかりやすい説明
- 複数の解決策を提示
- ドキュメント生成が得意

**ChatGPTの弱み:**
- コード生成精度はCopilot/Claudeに劣る
- リアルタイム性がない

## AI駆動開発のワークフロー

### Phase 1: 設計（Claude）

```
1. Claudeに全体設計を相談
   ↓
2. アーキテクチャドキュメント生成
   ↓
3. ディレクトリ構成決定
```

**実際のやり取り:**
```
私: 7つの売買システムを実装したい。拡張性の高い設計を提案してください。

Claude:
以下の3層アーキテクチャを推奨します：

1. core/ - 純粋ロジック
   - 入出力はDataFrame
   - UIから独立
   - テストが容易

2. strategies/ - 戦略ラッパー
   - キャッシュI/O
   - UI連携
   - 設定管理

3. apps/ - Streamlit UI
   - 表示のみ
   - ロジックを含まない

メリット:
- 各層が独立してテスト可能
- UIの変更がロジックに影響しない
- 新しいシステム追加が容易
```

### Phase 2: 実装（Copilot + Claude）

```
1. Copilotでコード補完
   ↓
2. 複雑な部分はClaudeに相談
   ↓
3. Copilotで実装
   ↓
4. Claudeでコードレビュー
```

**実際のコーディング:**

```python
# 1. コメント書く
def calculate_atr(df, period=14):
    """ATR（Average True Range）計算"""
    
# 2. Copilotが実装を提案 ↓

    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    
    atr = true_range.rolling(period).mean()
    
    return atr

# 3. Claudeにレビュー依頼
# → "NaNの最初のN行を考慮すべき"との指摘

# 4. 修正版（Copilotが提案）
    atr = true_range.rolling(period).mean()
    atr = atr.fillna(method='bfill')  # 初期NaNを後方埋め
    
    return atr
```

### Phase 3: テスト（Copilot + Claude）

```
1. Copilotがテストテンプレート生成
   ↓
2. エッジケースをClaudeに相談
   ↓
3. Copilotで追加テスト実装
```

**実装例:**

```python
# Copilot生成のテスト
def test_calculate_atr_basic():
    df = pd.DataFrame({
        'High': [101, 102, 103],
        'Low': [99, 98, 97],
        'Close': [100, 101, 102]
    })
    
    atr = calculate_atr(df, period=2)
    
    assert len(atr) == 3
    assert not atr.isna().all()

# Claudeが提案したエッジケーステスト
def test_calculate_atr_empty():
    """空のDataFrameの場合"""
    df = pd.DataFrame(columns=['High', 'Low', 'Close'])
    atr = calculate_atr(df)
    assert len(atr) == 0

def test_calculate_atr_single_row():
    """1行のみの場合"""
    df = pd.DataFrame({
        'High': [101],
        'Low': [99],
        'Close': [100]
    })
    atr = calculate_atr(df, period=14)
    assert len(atr) == 1
    # periodより短い場合はNaNになる
```

### Phase 4: ドキュメント（ChatGPT）

```
1. ChatGPTにコードを渡す
   ↓
2. README、APIドキュメント生成
   ↓
3. 手動で微調整
```

## 生産性比較：AI有り vs AI無し

### 実測データ（開発3ヶ月間）

| タスク | AI無し | AI有り | 高速化率 |
|--------|--------|--------|----------|
| コーディング | 60時間 | 6時間 | **10倍** |
| テスト作成 | 30時間 | 3時間 | **10倍** |
| バグ修正 | 20時間 | 4時間 | **5倍** |
| ドキュメント | 15時間 | 1.5時間 | **10倍** |
| **合計** | **125時間** | **14.5時間** | **8.6倍** |

**3ヶ月で110時間節約 = 約14日分の時間を創出**

### コスト比較

**AI利用コスト:**
- GitHub Copilot: $10/月 × 3ヶ月 = $30
- Claude Pro: $20/月 × 3ヶ月 = $60
- ChatGPT Plus: $20/月 × 3ヶ月 = $60
- **合計: $150**

**節約した人件費（時給$50として）:**
- 110時間 × $50 = **$5,500**

**ROI: $5,500 / $150 = 36.7倍**

## AI活用のベストプラクティス

### 1. プロンプトエンジニアリングの基本

**悪い例:**
```
エラーが出ます。直してください。
```

**良い例:**
```
以下のコードで "index 10312 is out of bounds" エラーが発生します。

【コード】
df.loc[10312, 'Close']

【環境】
- pandas 2.0.3
- df.shape: (252, 5)
- df.index: DatetimeIndex

【期待動作】
最新日の終値を取得したい

【質問】
1. エラーの原因は何ですか？
2. 日付ベースでアクセスする方法は？
3. 最終行を取得する一般的な方法は？
```

**5W1Hを意識:**
- What: 何をしたいか
- Why: なぜそれが必要か
- Where: どの部分で問題が起きているか
- When: いつエラーが発生するか
- Who: 誰が使うか（自分、チーム、ユーザー）
- How: どうやって実現するか（複数案を求める）

### 2. コンテキストの与え方

**Claudeに設計相談する際のテンプレート:**

```
【プロジェクト概要】
米国株自動売買システム（Python 3.11、Streamlit）

【現在の構成】
- core/: ビジネスロジック
- apps/: UI
- data_cache/: データキャッシュ（926MB）

【課題】
データ読み込みに10分かかる

【制約条件】
- メモリ: 最大8GB
- 同時ユーザー: 1名（個人開発）
- 更新頻度: 1日1回

【質問】
キャッシュ戦略を提案してください。
```

### 3. 段階的な質問

**一度に全部聞かない:**

```
❌ 悪い例:
「7つのシステム全部の実装方法を教えてください」

✅ 良い例:
Step 1: 「System1のアーキテクチャを設計してください」
Step 2: 「System1のコアロジックを実装してください」
Step 3: 「System1のテストを作成してください」
Step 4: 「他のシステムにも適用できるよう汎用化してください」
```

### 4. AIの出力を鵜呑みにしない

**必ず検証するポイント:**

```python
# AIが生成したコード
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# ✅ 検証すべきこと:
# 1. avg_loss が 0 の場合に ZeroDivisionError が起きないか？
# 2. 初期の period 行は NaN になるか？
# 3. RSI の値域は 0-100 か？

# テストで確認
def test_rsi_edge_cases():
    # ゼロ除算テスト
    df = pd.DataFrame({'Close': [100] * 20})  # 価格変動なし
    rsi = calculate_rsi(df)
    assert not rsi.isna().all()  # NaNだらけにならないか
    
    # 値域テスト
    assert (rsi >= 0).all() and (rsi <= 100).all()
```

### 5. バージョン管理との組み合わせ

**Copilotの提案を受け入れる前にコミット:**

```bash
# 1. 現在の状態をコミット
git add .
git commit -m "feat: add ATR calculation (before Copilot)"

# 2. Copilotの提案を受け入れ

# 3. 動作確認

# 4. 問題なければコミット
git commit -m "feat: ATR with Copilot suggestions"

# 5. 問題があれば元に戻す
git reset --hard HEAD^
```

## トラブルシューティング：AI活用で陥りやすい罠

### 罠1: Copilotの提案に依存しすぎる

**問題:**
Copilotが提案しないと手が止まる。

**解決策:**
```
1. まず自分で考える（3分）
2. 分からなければCopilotに補完させる
3. それでも不明ならClaudeに相談
```

**実例:**
```python
# 自分で書き始める
def merge_signals(signals):
    # TODO: 優先度でマージ
    
# ↑ ここまで書くとCopilotが提案してくる
    merged = {}
    for signal in signals:
        symbol = signal['symbol']
        if symbol not in merged:
            merged[symbol] = signal
        else:
            # スコア比較
            if signal['score'] > merged[symbol]['score']:
                merged[symbol] = signal
    return merged
```

### 罠2: コンテキスト不足で的外れな回答

**問題:**
Claudeの回答が期待と違う。

**原因:**
プロジェクト全体の構成を伝えていない。

**解決策:**
```
毎回以下を冒頭に追加:

【前提】
- Python 3.11
- pandas 2.0.3
- Streamlit WebUI
- 個人開発
- データサイズ: 6,200銘柄 × 1,000日 = 約926MB

【既存実装】
- CacheManager: 3層キャッシュ
- System1-7: 7つの売買戦略
- 診断API: 統一キーで候補数追跡

【今回の質問】
...
```

### 罠3: AI生成コードのテスト不足

**問題:**
Copilotが生成したコードをそのまま本番投入→バグ発生。

**対策:**
```python
# AI生成コードには必ず「AI生成」コメントを付ける
def calculate_indicators(df):
    """指標計算（Copilot生成）"""  # ← マーク
    
    # ... AIが生成したコード ...
    
    return df

# テストを必ず書く
def test_calculate_indicators():
    """AI生成コードの検証"""
    df = create_test_data()
    result = calculate_indicators(df)
    
    # エッジケース確認
    assert not result.isna().all()
    assert len(result) == len(df)
```

## 実際の開発フロー：1日の作業例

### 朝（9:00-12:00）：設計とコアロジック

**9:00 - 9:30: Claudeに設計相談**
```
今日の実装: System6（平均回帰戦略）

Claude, System6の設計を相談したい。
- 過去のSystem1-5と同じアーキテクチャで
- ボリンジャーバンド逆張り
- リスク管理は他システムと共通化
```

**9:30 - 11:30: Copilotでコーディング**
```python
# core/system6.py
def generate_system6_candidates(df, current_date):
    """System6: 平均回帰戦略"""
    
    # Copilotが以下を提案↓
    # Setup: 価格がBB下限を下回る
    setup_mask = (df['Close'] < df['BB_lower'])
    
    candidates = df[setup_mask].copy()
    
    # スコアリング: BB幅の逆数（狭いほど高スコア）
    candidates['score'] = 1 / candidates['BB_width']
    
    return candidates
```

**11:30 - 12:00: Claudeでレビュー**
```
Claude, このコードをレビューしてください。

【懸念点】
1. BB_widthが0の場合にZeroDivisionError
2. NaN処理
3. エッジケース
```

### 昼（13:00-14:00）：テスト作成

**13:00 - 13:30: Copilotでテストテンプレート生成**
```python
# tests/test_system6.py
def test_generate_system6_candidates_basic():
    # Copilotが自動生成
    pass

def test_generate_system6_candidates_empty():
    # Copilotが自動生成
    pass
```

**13:30 - 14:00: Claudeが提案したエッジケースを追加**
```python
def test_generate_system6_bb_width_zero():
    """BB幅がゼロの場合"""
    # Claudeの提案を実装
```

### 午後（14:00-17:00）：UI実装とドキュメント

**14:00 - 16:00: CopilotでStreamlit UI**
```python
# apps/app_system6.py
import streamlit as st
from strategies.system6_strategy import System6Strategy

st.title("System 6: 平均回帰戦略")

# Copilotが以下を提案↓
strategy = System6Strategy()
candidates = strategy.run(date=st.date_input("Date"))

st.dataframe(candidates)
```

**16:00 - 17:00: ChatGPTでドキュメント**
```
以下のコードからREADMEを生成してください：
- System6: 平均回帰戦略
- ボリンジャーバンド下限で買い
- BB幅の逆数でスコアリング
```

## 成果物：3ヶ月の開発成果

### 定量的成果

**コードベース:**
- 総行数: 8,500行
- コミット数: 476回
- テストカバレッジ: 61%
- ファイル数: 150+

**パフォーマンス:**
- データ読み込み: 10分 → 5秒（120倍）
- バックテスト実行: 30分 → 3分（10倍）
- シグナル生成: 20分 → 2分（10倍）

**品質:**
- CI/CD: GitHub Actions統合
- 自動テスト: pytest
- コードフォーマット: black, ruff, isort
- 型チェック: mypy

### 定性的成果

**学んだスキル:**
- AI プロンプトエンジニアリング
- システムアーキテクチャ設計
- テスト駆動開発
- パフォーマンス最適化
- CI/CD構築

**副次的効果:**
- AI活用ノウハウの蓄積
- 他プロジェクトへの応用（note記事自動化等）
- AI時代の開発者としての自信

## 他の開発にも応用できる汎用フレームワーク

### AI駆動開発の5ステップ

**Step 1: 設計相談（Claude）**
```
プロジェクトの全体像をClaudeに相談
↓
アーキテクチャドキュメント作成
↓
ディレクトリ構成決定
```

**Step 2: 実装（Copilot）**
```
コメントベースでCopilotに補完させる
↓
複雑な部分はClaudeに相談
↓
Copilotで実装
```

**Step 3: テスト（Copilot + Claude）**
```
Copilotでテストテンプレート
↓
Claudeでエッジケース洗い出し
↓
Copilotで実装
```

**Step 4: レビュー（Claude）**
```
実装コードをClaudeに渡す
↓
改善点の指摘を受ける
↓
Copilotで修正
```

**Step 5: ドキュメント（ChatGPT）**
```
コードをChatGPTに渡す
↓
README、API doc生成
↓
手動で微調整
```

### 他プロジェクトへの応用例

**Webアプリ開発:**
```
Claude: アーキテクチャ設計（React? Vue? Next.js?）
Copilot: コンポーネント実装
Claude: 状態管理設計（Redux? Context API?）
ChatGPT: ユーザードキュメント
```

**データ分析:**
```
Claude: 分析フロー設計
Copilot: pandas/numpy コーディング
Claude: 統計手法の選定
ChatGPT: 分析レポート生成
```

**機械学習:**
```
Claude: モデル選定相談
Copilot: 前処理コード
Claude: ハイパーパラメータチューニング戦略
ChatGPT: 論文形式のドキュメント
```

## まとめ：AI時代の開発者として

### AI駆動開発の本質

AIは**道具**です。万能ではありません。

**重要なのは:**
1. 何を作りたいか（ビジョン）
2. どう設計するか（アーキテクチャ）
3. AIをどう使うか（使い分け）

**AIが得意:**
- 定型処理の自動化
- 既知パターンの適用
- ドキュメント生成

**人間が得意:**
- 要件定義
- 創造的な設計
- 最終判断

### 3ヶ月で学んだ最大の教訓

**「AIに任せる」のではなく「AIと協働する」**

```
悪い例:
「AIが全部やってくれる」→ 思考停止

良い例:
「AIに叩き台を作らせて、人間が判断・改善」→ 生産性10倍
```

### 次のステップ

**短期（1ヶ月）:**
- 他プロジェクトでもAI活用
- プロンプトライブラリ構築
- チーム開発での応用

**中期（3ヶ月）:**
- AI駆動開発の社内展開
- 独自GPTsの開発
- 自動化ツールの構築

**長期（6ヶ月）:**
- AI開発フレームワークのOSS化
- 講演・執筆活動
- コンサルティング事業

## おわりに

3ヶ月前、「AIで本当に開発できるのか？」と半信半疑でした。

今では、**AIなしの開発は考えられません**。

しかし、AIが仕事を奪うのではなく、**AIを使いこなせる人が、使えない人の仕事を奪う**時代が来ています。

本記事があなたのAI駆動開発の第一歩になれば幸いです。

---

**開発環境:**
- GitHub Copilot: $10/月
- Claude Pro: $20/月
- ChatGPT Plus: $20/月
- **合計: $50/月でROI 36.7倍**

**プロジェクト:**
- 米国株自動売買システム（教育目的）
- リポジトリ: https://github.com/r-estoer3588/quant_trading_system_0510to0906
- コンテンツ制作自動化: https://github.com/r-estoer3588/note-articles

**記事執筆日:** 2025年12月3日

#AI #GitHub Copilot #Claude #ChatGPT #プロンプトエンジニアリング #開発生産性 #自動化 #Python
