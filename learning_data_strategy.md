# Learning Manager - データ収集戦略

## 📊 各プラットフォームの指標取得方法

### 1. **X (Twitter)** - 3つの方法

#### ✅ 方法A: X API v2（推奨、自動化可能）
- **メリット**: 自動取得、リアルタイム、正確
- **デメリット**: Developer Account必須、レート制限あり
- **取得可能指標**:
  - `impression_count`: インプレッション数
  - `like_count`: いいね数
  - `retweet_count`: リツイート数
  - `reply_count`: リプライ数
  - `quote_count`: 引用数
- **実装**: 既存の`tools/x_api_analyzer.py`を活用
- **セットアップ**: `tools/x_api_setup_guide.md`参照

```python
from tools.x_api_analyzer import XAnalyzer
analyzer = XAnalyzer(bearer_token)
df = analyzer.fetch_user_tweets("gethinu", max_results=10)
# → impression_count, like_count, retweet_count, reply_count取得
```

#### ⚡ 方法B: CSVエクスポート（TwExportly等）
- **メリット**: API不要、無料、簡単
- **デメリット**: 手動エクスポート必要、インプレッション数未対応の場合あり
- **対応ツール**:
  - TwExportly（ブラウザ拡張）
  - X Analytics CSV（公式、月1回更新）
- **実装**: `input/TwExportly_*.csv`を読み込み

```python
df = pd.read_csv("input/TwExportly_gethinu_tweets_2025_11_16.csv")
# カラム: tweet_id, favorite_count, retweet_count, reply_count, view_count
```

#### 📝 方法C: 手動入力（フォールバック）
- **メリット**: 確実、特定投稿のみ分析時に有効
- **デメリット**: 手間、スケールしない
- **実装**: 対話モードで1投稿ずつ入力

---

### 2. **note** - 2つの方法

#### ❌ 公式API: **存在しない**
noteは公式APIを提供していないため、自動取得不可。

#### 📊 方法A: Analytics画面からスクレイピング（非推奨）
- **メリット**: 自動取得可能
- **デメリット**: 
  - 規約違反のリスク
  - HTML構造変更で動作停止
  - ログイン必要（Selenium/Playwright）
- **実装難易度**: 高
- **判断**: **実装しない**（規約遵守）

#### 📝 方法B: 手動入力（推奨）
- **メリット**: 規約準拠、確実
- **デメリット**: 手動コピペ必要
- **手順**:
  1. noteダッシュボード → 記事一覧
  2. 各記事の「閲覧数」「スキ」「コメント」をコピー
  3. learning_manager.pyの対話モードで入力
- **実装**: 対話プロンプトで入力受付

```
📝 note指標を入力してください：
  記事タイトル: 1日15分副業術
  閲覧数（View）: 1200
  スキ数: 85
  コメント数: 12
```

#### 💡 方法C: スプレッドシート連携（中間案）
- Google SpreadsheetにnoteのAnalyticsを手動転記
- `learning_manager.py`がスプレッドシートをCSV読み込み
- **実装**: 後日追加可能（`--import-sheet`オプション）

---

### 3. **Threads** - 2つの方法

#### ❓ 公式API: **限定的**
- Threads APIは2024年6月公開だが、**Analytics系APIは未提供**
- 投稿・返信は可能、指標取得は不可

#### 📝 方法A: 手動入力（現状唯一の方法）
- **メリット**: 確実
- **デメリット**: 手動コピペ必要
- **手順**:
  1. Threadsアプリ → プロフィール → 投稿タップ
  2. 画面下部の「閲覧数」「いいね」「返信」「再投稿」を確認
  3. learning_manager.pyの対話モードで入力
- **実装**: 対話プロンプトで入力受付

```
📝 Threads指標を入力してください：
  投稿内容（要約）: 副業マインド転換3ステップ
  閲覧数: 450
  いいね数: 28
  返信数: 5
  再投稿数: 3
```

#### 🔮 方法B: スクレイピング（将来的）
- Threads Web版（threads.net）からHTML解析
- **問題**: 公式Web版が不安定、API待ち推奨
- **判断**: **実装しない**（API正式対応待ち）

---

## 🎯 最終的な実装方針

### フェーズ1（即日実装）: ハイブリッド方式
| プラットフォーム | 優先度1 | 優先度2 | 優先度3 |
|-----------------|---------|---------|---------|
| **X** | API自動取得 | CSVインポート | 手動入力 |
| **note** | 手動入力 | - | スプレッドシート（将来） |
| **Threads** | 手動入力 | - | API待ち |

### 実装詳細

#### `learning_manager.py`の`step1_ingest_social_stats()`を拡張

```python
def step1_ingest_social_stats() -> Dict:
    """ステップ1: X/note/Threads指標収集"""
    
    # X: API優先 → CSV → 手動
    x_stats = ingest_x_stats()
    
    # note: 手動入力のみ
    note_stats = ingest_note_stats_manual()
    
    # Threads: 手動入力のみ
    threads_stats = ingest_threads_stats_manual()
    
    # スナップショット保存
    save_snapshot(x_stats, note_stats, threads_stats)
```

#### X API連携の実装

```python
def ingest_x_stats() -> Dict:
    """X指標を取得（API → CSV → 手動の順）"""
    
    # 1. API試行
    if has_x_api_credentials():
        try:
            from tools.x_api_analyzer import XAnalyzer
            analyzer = XAnalyzer(os.getenv("X_BEARER_TOKEN"))
            df = analyzer.fetch_user_tweets(
                username=get_x_username(),
                max_results=10  # 直近10投稿
            )
            return aggregate_x_metrics(df)
        except Exception as e:
            print_warning(f"X API取得失敗: {e}")
    
    # 2. CSV試行
    csv_files = sorted(Path("input").glob("TwExportly_*.csv"), reverse=True)
    if csv_files:
        print_info(f"CSVファイル検出: {csv_files[0].name}")
        if confirm("このCSVを使用しますか？"):
            df = pd.read_csv(csv_files[0])
            return aggregate_x_metrics_from_csv(df)
    
    # 3. 手動入力フォールバック
    return ingest_x_stats_manual()
```

---

## 📦 必要な追加パッケージ

```bash
pip install tweepy pandas python-dotenv openpyxl  # 既存
# 追加不要（手動入力メイン）
```

---

## 🔧 セットアップ手順

### X API（オプション）
```bash
# 1. .envファイル作成
cd C:\Repos\note-articles
notepad .env

# 2. 以下を記載
X_BEARER_TOKEN=your_bearer_token_here
X_USERNAME_GETHINU=gethinu
X_USERNAME_AI_NARRATIVE=AI_Narrative_Studio

# 3. tools/x_api_setup_guide.mdの手順でBearer Token取得
```

### note/Threads
セットアップ不要（手動入力のみ）

---

## 💡 使い方

### ケース1: X APIあり
```powershell
learning -Ingest
# → X: API自動取得
# → note: 手動入力
# → Threads: 手動入力
```

### ケース2: X APIなし、CSVあり
```powershell
# 1. TwExportlyでCSVエクスポート → input/に配置
# 2. 実行
learning -Ingest
# → X: CSV読み込み
# → note: 手動入力
# → Threads: 手動入力
```

### ケース3: 全て手動
```powershell
learning -Ingest
# → X: 手動入力
# → note: 手動入力
# → Threads: 手動入力
```

---

## 📊 スナップショットJSON例

```json
{
  "timestamp": "2025-11-16_143000",
  "date": "2025-11-16",
  "source": {
    "x": "api",
    "note": "manual",
    "threads": "manual"
  },
  "stats": {
    "x": {
      "impressions": 15200,
      "engagements": 456,
      "likes": 320,
      "retweets": 89,
      "replies": 47,
      "engagement_rate": 3.0,
      "sample_size": 10
    },
    "note": {
      "views": 1200,
      "likes": 85,
      "comments": 12,
      "like_rate": 7.08
    },
    "threads": {
      "views": 450,
      "likes": 28,
      "replies": 5,
      "reposts": 3,
      "engagement_rate": 8.0
    }
  }
}
```

---

## 🚀 フェーズ2（将来拡張）

### note: Google Sheets連携
```python
# Google Sheets APIで自動読み込み
def ingest_note_stats_from_sheet():
    import gspread
    gc = gspread.service_account()
    sheet = gc.open("note_analytics").sheet1
    data = sheet.get_all_records()
    # ...
```

### Threads: 公式API待ち
Threads APIがAnalytics対応したら実装

---

**保存場所**: `C:\Repos\note-articles\learning_data_strategy.md`
