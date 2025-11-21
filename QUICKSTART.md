# 教育ツール＆品質向上ツール - 3分クイックスタート

## 💡 3ヶ月後でも忘れない！超簡単スタート

### 🎯 3つのツール

1. **Education Tool** - 教育カテゴリ別X投稿自動生成
2. **BlushUp Tool** - プロンプト品質向上（GitHub Copilot Chat用）
3. **Learning Tool** - 自動学習ループ（X/note/Threads指標→改善）

---

## 📝 Education Tool（投稿生成）

### 使い方（どこからでも）

```powershell
education
# または短縮形
edu
```

### 動作フロー

1. カテゴリ選択（1〜6）
2. ゴール、ペルソナ、問題点、トーン入力
3. テーマ入力
4. **AIが投稿案を自動生成！**

---

## 🎯 BlushUp Tool（プロンプト品質向上）

### 使い方（どこからでも）

```powershell
blushup
# または短縮形
bu
```

### 動作フロー

1. プロンプト選択（1〜5）
2. **@workspace付きでクリップボードにコピー**
3. GitHub Copilot Chatに貼り付けて使用

---

## 🤖 Learning Tool（自動学習ループ）

### 使い方（どこからでも）

```powershell
learning
# または短縮形
le
```

### 動作フロー

1. X/note/Threads指標を収集（-Ingest）
2. 目的と成果物を設定（-Goal/-Deliverable）
3. 前回成果を数値検証（-Review）
4. AIへの改善指示を自動生成
5. 過去の成功例で再教育（-Replay）

---

## 🔧 初回セットアップ

```powershell
education -Setup    # Education Tool
blushup -Setup      # BlushUp Tool
learning -Setup     # Learning Tool

# または手動で
pip install openai pyperclip
```

---

## 📋 Education カテゴリ一覧

| 番号 | カテゴリ | 説明 |
|------|---------|------|
| 1 | 信用の教育 | 信頼構築、実績提示 |
| 2 | 目的の教育 | ゴール設定、ベネフィット訴求 |
| 3 | 問題の教育 | 課題の可視化、損失回避 |
| 4 | 手段の教育 | 具体的な方法論 |
| 5 | 投資の教育 | ROI、費用対効果 |
| 6 | 行動の教育 | クロージング、即行動促進 |

## 📋 コマンド一覧

| コマンド | エイリアス | 説明 |
|----------|------------|------|
| `education` | `edu` | 教育カテゴリ別投稿生成 |
| `blushup` | `bu` | プロンプト品質向上 |
| `learning` | `le` | 自動学習ループ |
| `monetize` | `mz` | マネタイズプラン生成 |
| `renkin` | `rk` | 錬金王スタイル記事リライト |
| `sns` | - | SNS統合分析（プロジェクト選択可） |

## 📋 BlushUp プロンプト一覧

| 番号 | プロンプト | 説明 |
|------|-----------|------|
| 1 | 品質担保 | 細かいことでも全て質問 |
| 2 | 前提確認 | 解釈を箇条書きで確認 |
| 3 | チェックリスト | 見落とし指摘 |
| 4 | 自己評価 | 尋ねるべきだった質問 |
| 5 | 全部盛り | 1+2+3の組み合わせ |

---

## 💾 このファイルの場所

```
C:\Repos\note-articles\QUICKSTART.md
```

忘れたらこれを見る！

---

## 🔥 どこからでも実行できるようにする（オプション）

PowerShellプロファイルに以下を追加：

```powershell
# プロファイルを開く
notepad $PROFILE

# 以下を追加
function Start-EducationTool {
    Push-Location C:\Repos\note-articles
    try { .\education.ps1 @args }
    finally { Pop-Location }
}
Set-Alias education Start-EducationTool
```

これで **どこからでも** `education` と入力するだけで起動！

---

## 🚀 使用例

### Education Tool
```powershell
education

# カテゴリ: 1（信用の教育）
# ゴール: フォロワー獲得
# ペルソナ: 30代会社員
# 問題: 時間がない
# トーン: 共感的
# テーマ: 1日15分でできる副業習慣

→ 投稿案が表示＆クリップボードにコピー
```

### BlushUp Tool
```powershell
blushup

# プロンプト: 5（全部盛り）

→ @workspace付きでクリップボードにコピー
→ GitHub Copilot Chatに貼り付けて使用
```

### Learning Tool
```powershell
learning -Ingest    # X/note/Threadsから指標収集
learning -Review    # 前回投稿のKPI分析
learning -Replay    # 成功例を元に再生成
```

---

## 🚀 PowerShellプロファイル設定済み

どこからでも `education` / `edu` / `blushup` / `bu` / `learning` / `le` で起動できます！

再起動後も有効です。

---

## �📱 スマホからでも確認可能

このREADMEをGitHubで見れば、いつでもコマンドが確認できます：

https://github.com/r-estoer3588/note-articles1101/blob/master/QUICKSTART.md

---

**最終更新**: 2025-11-21  
**Education**: `education` または `edu`  
**BlushUp**: `blushup` または `bu`  
**Learning**: `learning` または `le`  
**Monetize**: `monetize` または `mz`  
**Renkin**: `renkin` または `rk`  
**SNS Analysis**: `sns`  
**困ったら**: `education -Help` / `blushup -Help` / `learning -Help`
