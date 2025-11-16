# 教育カテゴリ別投稿生成 - 3分クイックスタート

## 💡 3ヶ月後でも忘れない！超簡単3ステップ

### ステップ1: PowerShellを開く

```powershell
cd C:\Repos\note-articles
```

⚠️ **重要**: `note-articles` ディレクトリから実行してください！

### ステップ2: コマンド実行

```powershell
.\education.ps1
```

### ステップ3: 質問に答える

1. カテゴリ番号（1〜6）
2. ゴール（Enter でスキップ可）
3. ペルソナ（Enter でスキップ可）
4. 問題点（Enter でスキップ可）
5. トーン（Enter でスキップ可）
6. **テーマ**（必須）

→ **AIが3つの投稿案を自動生成！**

---

## 🎯 それだけ！

- コマンドは `.\education.ps1` だけ
- あとは質問に答えるだけ
- 迷ったらEnterで次へ

---

## 🔧 初回のみ（セットアップ）

```powershell
.\education.ps1 -Setup
```

これで依存関係とAPIキー設定ができます。

---

## 📝 困ったら

```powershell
.\education.ps1 -Help
```

使い方とカテゴリ説明が表示されます。

---

## 🎨 6つのカテゴリ

| 番号 | 名前 | 用途 |
|------|------|------|
| 1 | 信用 | 信頼構築・共感 |
| 2 | 目的 | 理想未来・動機 |
| 3 | 問題 | 危機感・真因 |
| 4 | 手段 | 解決策・期待 |
| 5 | 投資 | 価値・正当化 |
| 6 | 行動 | 今すぐ行動 |

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

```powershell
# 起動
.\education.ps1

# カテゴリ: 1
# ゴール: フォロワー獲得
# ペルソナ: 30代会社員
# 問題: 時間がない
# トーン: 共感的
# テーマ: 1日15分でできる副業習慣

→ 投稿案3つが表示される
→ クリップボードに自動コピー
```

---

## 📱 スマホからでも

このREADMEをGitHubで見れば、いつでもコマンドが確認できます：

https://github.com/r-estoer3588/note-articles1101/blob/master/QUICKSTART.md

---

## ⚡ ショートカット集

```powershell
# ヘルプ
.\education.ps1 -Help

# セットアップ
.\education.ps1 -Setup

# カテゴリ一覧
.\education.ps1 -List

# 通常起動（これだけ覚えればOK）
.\education.ps1
```

---

**最終更新**: 2025-11-16  
**1コマンドで完結**: `.\education.ps1`  
**迷ったら**: `.\education.ps1 -Help`
