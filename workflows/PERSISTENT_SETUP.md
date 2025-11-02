# 🔒 n8n 永続化セットアップ - 一度設定したら二度とやらない

## 問題点

現状のドキュメントは**毎回セットアップさせる**構成になっている:
- インポート手順
- API キー設定
- 接続設定

**これは非効率的!** n8nはDockerボリュームで設定を永久保存できます。

---

## ✅ 解決策: 永続化されたn8n環境

### 📦 1回だけやるセットアップ

#### Step 1: Docker Compose で n8n を起動(永続化付き)

`docker-compose.yml` を作成:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:1.117.3
    container_name: n8n-notes-organizer
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_secure_password_here
      - GENERIC_TIMEZONE=Asia/Tokyo
      - N8N_SECURE_COOKIE=false
    volumes:
      # 🔑 重要: これで設定が永続化される
      - n8n_data:/home/node/.n8n
      # ノートフォルダをマウント
      - C:\Users\stair\OneDrive\Documents\Notes:/notes:ro
    networks:
      - n8n-network

volumes:
  # 🔑 ここに全ての設定が保存される
  n8n_data:
    driver: local

networks:
  n8n-network:
    driver: bridge
```

#### Step 2: 起動

```powershell
# note-articles/workflows/ ディレクトリで実行
docker-compose up -d
```

#### Step 3: 初回セットアップ(一度だけ!)

1. **ブラウザで http://localhost:5678 を開く**
2. **ワークフローをインポート**: `notes-to-notion-auto-organizer.json`
3. **3つの設定を一度だけ実施**:
   - ✅ OpenAI API キー
   - ✅ Notion API キー & データベース ID
   - ✅ Watch Folder パス: `/notes`(Dockerマウントパス)
4. **ワークフローを Active にする**

---

## 🎉 以降は何もしなくていい

### Dockerを再起動しても設定は残る

```powershell
# コンテナを停止
docker-compose down

# 再起動(設定はそのまま!)
docker-compose up -d
```

### PCを再起動しても設定は残る

```powershell
# 自動起動設定
docker update --restart=always n8n-notes-organizer
```

### 設定の確認

```powershell
# ボリュームの確認
docker volume ls
# 出力: n8n_data

# 設定ファイルの場所
docker exec n8n-notes-organizer ls -la /home/node/.n8n
```

---

## 📁 永続化される内容

| 項目 | 保存場所 | 説明 |
|------|----------|------|
| ワークフロー | `/home/node/.n8n/workflows/` | インポートしたJSON |
| Credentials | `/home/node/.n8n/credentials/` | API キー(暗号化済み) |
| 設定 | `/home/node/.n8n/config/` | n8nの設定 |
| 実行履歴 | `/home/node/.n8n/executions/` | 過去の実行ログ |

---

## 🔄 バックアップ方法(オプション)

### 設定をバックアップ

```powershell
# ボリュームをバックアップ
docker run --rm -v n8n_data:/data -v ${PWD}:/backup alpine tar czf /backup/n8n_backup.tar.gz -C /data .
```

### バックアップから復元

```powershell
# ボリュームを復元
docker run --rm -v n8n_data:/data -v ${PWD}:/backup alpine tar xzf /backup/n8n_backup.tar.gz -C /data
```

---

## 🚀 新しいワークフローの追加

### 追加のワークフローも永続化される

1. **n8n UI で新しいワークフローを作成**
2. **保存すれば自動的に永続化**
3. **再起動しても残る**

### エクスポート/インポート不要!

設定済みの環境なら、ワークフローは UI 上で直接編集できます。

---

## 🛠️ トラブルシューティング

### 設定が消えた場合

**原因**: ボリュームが削除された

```powershell
# ボリュームの確認
docker volume ls | Select-String "n8n_data"
```

**復旧方法**: バックアップから復元、または再セットアップ

### ボリュームの削除(注意!)

```powershell
# ⚠️ 注意: これをやると設定が全部消える
docker-compose down -v

# 正しい停止方法(設定を残す)
docker-compose down
```

---

## 📝 更新されたドキュメント構成

### 永続化前提の新しい構成

```
workflows/
├── PERSISTENT_SETUP.md       ← このファイル(一度だけのセットアップ)
├── docker-compose.yml         ← n8n起動設定(永続化付き)
├── QUICKSTART.md              ← 簡易ガイド
├── notes-to-notion-auto-organizer.json  ← ワークフローJSON
└── TROUBLESHOOTING.md         ← トラブルシューティング
```

### 古いドキュメント(非推奨)

- ❌ SETUP_GUIDE.md - 毎回セットアップする前提
- ❌ FINAL_SETUP.md - 接続を毎回やり直す前提

---

## ✅ チェックリスト(一度だけ!)

- [ ] `docker-compose.yml` を作成
- [ ] `docker-compose up -d` で起動
- [ ] ワークフローをインポート
- [ ] OpenAI API キーを設定
- [ ] Notion API キー & データベース ID を設定
- [ ] Watch Folder パスを `/notes` に設定
- [ ] ワークフローを Active にする
- [ ] テストファイルで動作確認
- [ ] **バックアップを作成(推奨)**

---

## 🎯 まとめ

### 従来の方法(非効率)
```
毎回:
1. n8nを起動
2. ワークフローをインポート
3. API キーを設定
4. 接続を確認
5. テスト
```

### 新しい方法(効率的)
```
一度だけ:
1. docker-compose.yml を作成
2. 初回セットアップ

以降:
- docker-compose up -d だけ!
- 設定は全部残ってる
```

---

**🔒 これで永久に保存されます!**

二度と同じセットアップをする必要はありません。
