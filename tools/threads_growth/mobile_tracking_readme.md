# Mobile Tracking CSV 使用ガイド

この CSV は PC が使えない日（外出・旅行・体調不良など）に、スマートフォンから手軽にエンゲージメントデータを記録できるように作られています。

## CSV フォーマット

```
date,followers,likes,reposts,replies,clicks,note_pv
YYYY-MM-DD,整数,整数,整数,整数,整数,整数
```

- **date**: 記録した日付（例: `2025-11-25`）
- **followers**: その日の総フォロワー数
- **likes**: 受け取ったいいね数（自分がした数ではなく、受けた数）
- **reposts**: リポスト数
- **replies**: 返信数
- **clicks**: プロフィールクリック数
- **note_pv**: note.com のページビュー数

## 手順

1. スマートフォンで Google Sheets などの表計算アプリを開く。
2. 上記ヘッダー行をコピーし、1 行だけデータを入力。
3. 完了したら CSV としてエクスポート（`mobile_tracking_template.csv`）
4. PC に戻ったら次のコマンドでインポート:
   ```powershell
   python c:/Repos/note-articles/tools/daily_report.py --import mobile_tracking_template.csv
   ```
   これにより過去の日付でもデータが記録され、ストリークは維持されます。

## 注意点

- **日付は必ず `YYYY-MM-DD` 形式** で入力してください。
- **数値は整数のみ**、小数や文字はエラーになります。
- 同じ日付の重複は上書きされます（最新の行が採用されます）。

## FAQ

- **Q: 1 行だけ入力したらどうなる？**
  - A: その日のデータだけが追加され、他の日は変更されません。
- **Q: 複数日分を一度にインポートできますか？**
  - A: CSV に複数行を書けば一括インポート可能です。日付が重複した場合は最新行が採用されます。

---

_このファイルは `c:/Repos/note-articles/tools/threads_growth/` に配置されています。_
