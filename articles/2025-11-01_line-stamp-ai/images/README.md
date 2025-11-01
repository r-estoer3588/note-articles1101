# 画像フォルダ

このフォルダには、記事で使用する画像を配置します。

## 推奨ファイル名

- `thumbnail.png` - 記事のサムネイル（推奨サイズ：1280x670px）
- `screenshot_leonardo_01.png` - Leonardo.aiの操作画面
- `screenshot_pixai_01.png` - PixAiの操作画面
- `screenshot_nanobana_01.png` - Nano Bananaの操作画面
- `result_all_16.png` - 完成した16種類のスタンプ一覧
- `comparison_before_after.png` - 修正前後の比較
- `workflow_diagram.png` - 作業フローの図解

## 画像最適化

noteにアップロードする前に、以下のツールで最適化推奨：

```bash
# 将来実装予定
python ../../../tools/image_optimizer.py .
```

## note掲載時の注意

- 画像サイズ：最大5MB
- 推奨形式：PNG、JPEG
- 著作権：AI生成画像の利用規約を確認
  - Leonardo.ai：商用利用可（有料プラン）
  - PixAi：規約確認必要
  - Google AI Studio：規約確認必要
