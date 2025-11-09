# ホゲーアルゴリズム - 実装完了報告

## 📦 作成したファイル

### 1. コア実装
- **`hogey_algorithm.py`** - メイン実装（450行）
  - 6つの教育タイプ
  - 8テンプレ構造
  - バズ構成（7行）
  - 3部作ストーリー生成
  - CSV学習機能
  - CLI対応

### 2. ドキュメント
- **`HOGEY_ALGORITHM_README.md`** - 詳細ドキュメント
- **`N8N_WORKFLOW_GUIDE.md`** - n8n連携ガイド
- **`QUICKSTART.md`** - クイックスタートガイド

### 3. サンプルデータ
- **`my_posts_sample.csv`** - 自分の投稿サンプル（10件）
- **`bench_posts_sample.csv`** - 強者アカウントサンプル（15件）

## ✅ 実装済み機能

### コア機能
- [x] 6つの教育タイプ（目的・問題・価値・信頼・親近感・行動）
- [x] 8テンプレ構造（感情爆発型、自虐型、ストーリー型など）
- [x] バズ構成（起承転結 7行）
- [x] 3部作ストーリー（起→転→解）
- [x] 泥人間ペルソナ向けフック
- [x] 固有名詞・数字の自動挿入

### 学習機能
- [x] CSV読み込み（自分の投稿 + 強者アカウント）
- [x] エンゲージメントスコアリング
- [x] 高スコア投稿のパターン抽出
- [x] 語尾・フック・固有名詞の学習
- [x] 学習済みパターンの優先使用

### 出力機能
- [x] 単発バズ投稿生成
- [x] 3部作ストーリー生成
- [x] 一括生成（CSV出力）
- [x] JSON出力（n8n連携用）
- [x] CLI対応（テーマ・件数指定）

## 🎯 使い方

### 基本的な使い方

```powershell
# デモ実行
python hogey_algorithm.py --type demo --theme "貧乏脱出"

# バズ投稿10件生成
python hogey_algorithm.py --count 10 --theme "人生逆転"

# 3部作ストーリー
python hogey_algorithm.py --type trilogy --theme "停滞からの逆転"

# CSV学習 + 生成
python hogey_algorithm.py --learn --count 5 --theme "貧乏脱出"

# JSON出力（n8n用）
python hogey_algorithm.py --count 3 --json
```

### n8n連携

```json
{
  "node": "Execute Command",
  "command": "python",
  "arguments": [
    "hogey_algorithm.py",
    "--theme=副業",
    "--count=5",
    "--json"
  ]
}
```

## 📊 生成例

### バズ投稿（7行構成）

```
ホゲーっと生きてる。
気づいたら何も変わってない。

でもある日、「このままじゃ終われない」って思った。

あの時から少しずつ変えた。
情報に金を払うようにして、人生が動き出した。

試してみて。
```

### 3部作ストーリー

**① 起（共感・導入）**
```
夜中2時。
冷めたカップ麺すすりながら、
Xで他人の成功話見てた。

何も変わらんまま、
明日も同じ朝が来ると思ってた。
```

**② 転（崩壊・気づき）**
```
でもある日、上司が笑いながら言った。
「お前、夢とかないの？」

頭の中が真っ白になった。
あの瞬間、「このままじゃ終われない」って思った。
```

**③ 解（逆転・希望）**
```
あの時から少しずつ変えた。
情報に金を払うようにして、
気づけば人生が静かに動き出した。

泥の中でも、足を動かせば沈まない。
そろそろ浮上しようぜ。
```

## 🔄 自律学習ループ

```
投稿生成 → X投稿 → 反応取得 → CSV保存 → 学習更新 → 投稿生成...
```

### CSV形式

**my_posts.csv**
```csv
post_id,text,datetime,likes,retweets,comments,hashtags
1,"残高274円の夜...",2025-01-01 20:00,150,30,5,#げすいぬ
```

**bench_posts.csv**
```csv
account_name,text,datetime,likes,retweets,comments
@example,"成功者の投稿...",2025-01-01 19:00,5000,800,100
```

## 🎨 カスタマイズポイント

### フックワードの追加
```python
hogey = HogeyAlgorithm()
hogey.learned_patterns['hooks'].append("新しいフック")
```

### 語尾の追加
```python
hogey.learned_patterns['endings'].append("新しい語尾")
```

### 教育タイプの調整
```python
# HogeyAlgorithmクラス内
EDUCATION_TYPES = [
    "目的の教育",
    "問題の教育",
    "価値の教育",
    "信頼の教育",
    "親近感の教育",
    "行動の教育",
    "未来の教育"  # 追加
]
```

## 🚀 次のステップ

### 1. データ蓄積（推奨）
```powershell
# 1. 自分の過去投稿をmy_posts.csvに追加
# 2. 強者アカウントをbench_posts.csvに追加
# 3. 学習実行
python hogey_algorithm.py --learn
```

### 2. n8nワークフロー構築
詳細は `N8N_WORKFLOW_GUIDE.md` を参照

### 3. 定期自動実行
```powershell
# Windowsタスクスケジューラーに登録
# 毎日9時に5件生成
schtasks /create /tn "Hogey投稿生成" /tr "python c:\Repos\note-articles\tools\hogey_algorithm.py --count 5" /sc daily /st 09:00
```

### 4. 反応データ取得＆学習
- X APIで投稿の反応（いいね・リツイート）を取得
- my_posts.csvに追記
- 定期的に学習実行

## 📝 技術仕様

### 依存ライブラリ
- Python 3.8+
- pandas

### 対応OS
- Windows 10/11
- Linux
- macOS

### ファイルエンコーディング
- UTF-8 BOM推奨（CSV）
- UTF-8（Pythonコード）

## ⚠️ 注意事項

1. **CSV形式**: 列名は厳密に一致させること（text, likes, retweets等）
2. **文字エンコーディング**: UTF-8 BOM推奨
3. **X API制限**: 自動投稿時はレート制限に注意
4. **学習データ**: 最低10件以上推奨

## 🐛 トラブルシューティング

### pandasがない
```powershell
pip install pandas
```

### CSVが読めない
```powershell
# UTF-8 BOMで保存
Get-Content my_posts.csv | Set-Content -Encoding UTF8 my_posts_utf8.csv
```

### 生成がワンパターン
学習データを増やして再学習:
```powershell
python hogey_algorithm.py --learn
```

## 📚 関連ドキュメント

- **HOGEY_ALGORITHM_README.md** - 詳細ドキュメント
- **N8N_WORKFLOW_GUIDE.md** - n8n連携ガイド
- **QUICKSTART.md** - クイックスタートガイド

## 🎉 完成

ホゲーアルゴリズムの実装が完了しました。

**泥人間の心を動かす投稿を量産し、X運用を自動化せよ。**

---

開発: げすいぬくん | 底辺脱出マガジン
実装日: 2025年11月8日
