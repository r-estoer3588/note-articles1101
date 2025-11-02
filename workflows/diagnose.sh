#!/bin/bash

# === n8n Notes to Notion Organizer 実行スクリプト ===
# このスクリプトは以下の操作を行います:
# 1. Docker コンテナの状態確認
# 2. マウント設定の検証
# 3. ワークフロー実行テスト

echo "=== n8n Notes to Notion Organizer - 診断スクリプト ==="
echo ""

# 1. Docker 状態確認
echo "[1] Docker コンテナの状態"
docker ps --filter "name=n8n-notes-organizer" --format "table {{.Names}}\t{{.Status}}"
echo ""

# 2. マウント確認
echo "[2] /notes マウント状態"
docker exec n8n-notes-organizer ls -la /notes 2>&1
echo ""

# 3. n8n が見つけたファイル
echo "[3] ワークフロー実行履歴"
docker exec n8n-notes-organizer cat /home/node/.n8n/config/n8n.config.json 2>/dev/null || echo "設定ファイルが見つかりません（初回起動の可能性）"
echo ""

# 4. 最後のスキャン時刻（未実装の場合は作成）
echo "[4] 最後のスキャン時刻更新"
docker exec n8n-notes-organizer touch /tmp/last_scan
echo "タイムスタンプ更新完了"
echo ""

echo "=== 診断完了 ==="
echo ""
echo "次のステップ:"
echo "1. n8n UI (http://localhost:5678) で手動テストを実行してください"
echo "2. Notion DB に新規ページが作成されたか確認してください"
echo "3. C:\Notes に新規ファイルを作成して、5分後に自動処理を確認してください"
