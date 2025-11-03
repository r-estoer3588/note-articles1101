# 📝 note記事リライト - 完全自動プロンプト

このプロンプトをGitHub Copilot Chatに貼り付けるだけで、記事のリライトからファイル保存まで自動実行されます。

## 🚀 使い方

### ステップ1: 記事本文を用意

リライトしたい記事を`drafts/input.txt`などに保存しておく

### ステップ2: このプロンプトをコピー

以下のプロンプトをGitHub Copilot Chatに貼り付け

---

## 📋 プロンプト（コピペ用）

```
@workspace 以下のタスクを実行してください:

1. `c:\Repos\note-articles\prompt\note_prompt.txt` の内容を読み込む
2. `c:\Repos\note-articles\drafts\input.txt` の記事本文を読み込む（またはクリップボードから）
3. note_prompt.txt の指示に従って、記事を完全にリライトする
4. リライト結果を以下の形式でMarkdownファイルとして保存:
   - ファイル名: `YYYYMMDD_HHMMSS_タイトル.md`
   - 保存先: `c:\Repos\note-articles\drafts\`
   - フォーマット:
     ```markdown
     ---
     title: （タイトル）
     created: （作成日時）
     source: GitHub Copilot Chat
     ---
     
     # （タイトル）
     
     （リライト後の本文）
     
     ---
     
     ## メタ情報
     - 作成日時: （日時）
     - 生成元: note_prompt.txt
     - ステータス: 下書き
     
     ## 次のアクション
     - [ ] タイトルの最終確認
     - [ ] 本文の誤字脱字チェック
     - [ ] noteに投稿
     - [ ] SNSでシェア
     ```
5. 保存したファイルパスを教えてください

【記事本文】
（ここに記事本文を貼り付け、または input.txt を参照）
```

---

## 📝 さらに簡易版（直接記事を貼り付け）

```
@workspace 以下のタスクを実行してください:

1. `note_prompt.txt` のリライト手順に従って、以下の記事を完全リライト
2. リライト結果を `drafts/YYYYMMDD_HHMMSS_タイトル.md` に保存
3. note投稿用のMarkdown形式（メタ情報・次のアクション含む）で出力

【記事本文】
AIで書いたnote、なんか、つまらない。
読んでも心動かない。なぜなのか。

実は、AI×noteで難しいことがあるんよ。
ただAI使ってるだけだと「教育」ができない。

本質、教えるぞ。

noteが売れるのは、情報じゃない。教育。

（以下、記事本文を貼り付け）
```

---

## 🎯 超時短版（ワンライナー）

```
@workspace note_prompt.txtで drafts/input.txt をリライトして drafts/YYYYMMDD_タイトル.md に保存
```

---

## 💡 使用例

### 例1: ファイル参照版

```
@workspace 以下のタスクを実行:
1. note_prompt.txt を読む
2. drafts/ai_video_draft.txt を読む
3. リライトして drafts/20251103_AI動画で稼ぐ.md に保存
```

### 例2: 直接記事貼り付け版

```
@workspace note_prompt.txtでこの記事をリライトして保存:

【記事】
AIで書いたnote、なんか、つまらない。
（以下本文）
```

### 例3: クリップボード参照版

```
@workspace note_prompt.txtでクリップボードの記事をリライトして drafts に保存
```

---

## 🔧 カスタマイズ例

### タイトル指定

```
@workspace note_prompt.txtで記事をリライト。タイトルは「AI動画×収益化の完全ガイド」で drafts に保存
```

### 商品設計プロンプト使用

```
@workspace product_design_prompt.txtでペルソナ100個→商品案10個を生成して drafts に保存
```

### 動画プロンプト使用

```
@workspace ai_video_monetization_prompt.txtで収益化プラン→SNS投稿文20本を生成して drafts に保存
```

---

## 📂 ファイル構成

GitHub Copilotが参照するファイル:

```
note-articles/
├── drafts/
│   ├── input.txt              # 入力ファイル（リライト前）
│   └── 20251103_143000_タイトル.md  # 出力ファイル（リライト後）
└── prompt/
    ├── note_prompt.txt                    # 記事リライト用
    ├── product_design_prompt.txt          # 商品設計用
    └── ai_video_monetization_prompt.txt   # 動画収益化用
```

---

## 🎉 メリット

✅ **コマンド不要** - GitHub Copilot Chatに貼り付けるだけ
✅ **ファイル自動保存** - Markdownファイルが自動生成される
✅ **note投稿準備完了** - そのままコピペで投稿可能
✅ **履歴管理** - draftsフォルダに全履歴が残る

---

## 💬 実際の会話例

**あなた:**
```
@workspace note_prompt.txtで drafts/input.txt をリライトして drafts に保存
```

**Copilot:**
```
記事をリライトしました。以下のファイルに保存しました:

📄 c:\Repos\note-articles\drafts\20251103_143542_AI動画で月10万稼ぐ方法.md

タイトル: AI動画で月10万稼ぐ方法
文字数: 3,245文字

次のステップ:
1. ファイルを確認・編集
2. noteに投稿
3. 投稿後、articlesフォルダに移動
```

---

**さあ、このプロンプトをコピーして試してみよう!**
