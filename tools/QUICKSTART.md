# ホゲーアルゴリズム クイックスタート

5分で始めるホゲーアルゴリズム

## 1. インストール

```powershell
cd c:\Repos\note-articles\tools
pip install pandas
```

## 2. デモ実行

```powershell
python hogey_algorithm.py --type demo --theme "貧乏脱出"
```

出力例:
```
==================================================
ホゲーアルゴリズム デモ実行
==================================================

【バズ投稿生成】
ホゲーっと生きてる。
気づいたら何も変わってない。

でもある日、「このままじゃ終われない」って思った。

あの時から少しずつ変えた。
情報に金を払うようにして、人生が動き出した。

試してみて。

教育タイプ: 行動の教育
フレームワーク: PASONA法則
```

## 3. バズ投稿を10件生成

```powershell
python hogey_algorithm.py --count 10 --theme "人生逆転" --output my_posts.csv
```

## 4. 3部作ストーリー生成

```powershell
python hogey_algorithm.py --type trilogy --theme "停滞からの逆転"
```

## 5. CSV学習を使う

```powershell
# サンプルCSVをコピー
copy my_posts_sample.csv my_posts.csv
copy bench_posts_sample.csv bench_posts.csv

# 学習実行
python hogey_algorithm.py --learn --count 5 --theme "貧乏脱出"
```

## 6. JSON出力（n8n連携用）

```powershell
python hogey_algorithm.py --count 3 --theme "副業" --json
```

出力例:
```json
[
  {
    "post_id": 1,
    "text": "ホゲーっと生きてる...",
    "education_type": "行動の教育",
    "theme": "副業",
    "hashtags": "#げすいぬ #底辺脱出"
  }
]
```

## よくある使い方

### パターン1: 毎日3件自動生成

```powershell
# スケジューラーに登録
python hogey_algorithm.py --count 3 --theme "日替わり" --output daily_posts.csv
```

### パターン2: 学習→生成のループ

```powershell
# 1. 学習
python hogey_algorithm.py --learn

# 2. 生成
python hogey_algorithm.py --count 10 --output learned_posts.csv
```

### パターン3: テーマ別バッチ生成

```powershell
# 金・ギャンブル
python hogey_algorithm.py --theme "ギャンブル依存" --count 5 --output gambling.csv

# 人間関係
python hogey_algorithm.py --theme "人間関係" --count 5 --output relationship.csv

# 仕事・キャリア
python hogey_algorithm.py --theme "ブラック企業" --count 5 --output career.csv
```

## トラブルシューティング

### pandasがない

```powershell
pip install pandas
```

### CSVが読めない

エンコーディングをUTF-8 BOMに変更:
```powershell
# PowerShellで変換
Get-Content my_posts.csv | Set-Content -Encoding UTF8 my_posts_utf8.csv
```

### 生成がワンパターン

学習データを増やす:
```powershell
# 自分の過去投稿をmy_posts.csvに追加
# 強者アカウントをbench_posts.csvに追加
python hogey_algorithm.py --learn
```

## 次のステップ

1. ✅ デモ実行で動作確認
2. ✅ サンプルCSVで学習テスト
3. ✅ 10件生成して投稿内容確認
4. ✅ 自分の投稿データをCSVに蓄積
5. ✅ n8nワークフロー構築

詳細は以下を参照:
- `HOGEY_ALGORITHM_README.md` - 詳細ドキュメント
- `N8N_WORKFLOW_GUIDE.md` - n8n連携ガイド

---

**ホゲーっとしてる暇はない。今すぐ動け。**
