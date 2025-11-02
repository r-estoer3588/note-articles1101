# ✅ n8n Notes to Notion Organizer - 最終セットアップ手順

## 🎉 現在の状態

### ✅ 完了したこと
1. **Docker マウント設定修正**: `C:\Notes` → `/notes` に正しくマウント済み
2. **コンテナ再起動完了**: 新しい設定が反映された
3. **ファイル確認済み**: コンテナ内で `/notes` ディレクトリにファイルが見える状態

### 📋 残っているタスク
1. **Notion 認証情報の確認と再登録**
2. **手動テストで Notion への書き込み確認**
3. **実ファイルでの自動検知テスト**

---

## 🔧 次のステップ（すぐにやってください）

### Step 1: n8n UI で Notion 認証を確認

1. **ブラウザで開く**
   ```
   http://localhost:5678
   ```

2. **ログイン**
   - ユーザー名: `admin`
   - パスワード: `change_this_password_123`

3. **左下のアイコン（⚙️）をクリック → Credentials**

4. **「Notion account」を探す**
   - ✅ 存在する場合:
     - クリック → "Test Connection" を実行
     - ✅ 成功なら次へ
     - ❌ 失敗なら削除して再作成

   - ❌ 存在しない場合:
     - 下記の「Notion 認証情報の新規作成」へ

---

### Notion 認証情報の新規作成（必要な場合のみ）

#### 1. Notion Integration Token を取得

1. https://www.notion.so/my-integrations にアクセス
2. **"+ New integration"** をクリック
3. 以下を設定:
   - **Name**: `n8n-notes-organizer`
   - **Associated workspace**: 自分のワークスペースを選択
   - **Capabilities**: 
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content
4. **Submit** をクリック
5. **Internal Integration Secret** をコピー（`secret_xxxxx...` の形式）

#### 2. Notion Database に Integration を接続

1. Notion で対象の Database を開く
2. 右上の **"..."** → **"Add connections"**
3. 先ほど作成した **"n8n-notes-organizer"** を選択
4. **Confirm** をクリック

#### 3. Database ID を取得

1. Notion Database のページで **URL をコピー**
   ```
   https://www.notion.so/xxxxxxxxxxxxx?v=yyyyyyyyyy
   ```
2. `xxxxxxxxxxxxx` の部分（32文字のハッシュ）が Database ID

#### 4. n8n に登録

1. n8n UI の **Credentials** ページで **"+ Create New"**
2. **Type** で **"Notion API"** を選択
3. 以下を入力:
   - **Credential Name**: `Notion account`
   - **Internal Integration Secret**: コピーした `secret_xxxxx...`
4. **Save** をクリック

---

### Step 2: ワークフローで認証情報を紐付け

#### 既存ワークフロー「Notes to Notion Auto Organizer」

1. **Workflows** → **"Notes to Notion Auto Organizer"** を開く

2. **「Notion Create Item」ノードをクリック**

3. **右パネルの "Credential to connect with" セクション**
   - Dropdown から **"Notion account"** を選択
   - Database ID が正しいか確認: `29e1972f485180c89c68d77f1b82e39f`

4. **「Get All Notes from Notion」ノードも同様に設定**

5. **Save** をクリック（右上）

---

### Step 3: 手動テストで動作確認

#### テストデータで Notion 書き込みをテスト

現在のワークフローには手動トリガーがないため、以下の方法でテストします：

**方法 A: Execute Node で個別テスト**

1. **「Set Note Metadata」ノードを右クリック**
2. **"Execute Node"** を選択
3. 入力データを手動で設定:
   ```json
   {
     "fileName": "test_manual.txt",
     "fileContent": "これは手動テストです。\n\nPython と機械学習について学習中。",
     "filePath": "/notes/test_manual.txt",
     "createdDate": "2025-11-02T22:00:00+09:00"
   }
   ```
4. **「OpenAI Category Tagging」→「Parse AI Response」→「Format for Notion」→「Notion Create Item」** を順に実行

5. **Notion Database で新規ページが作成されたか確認**

**方法 B: 改善版ワークフローをインポート**

1. **右上メニュー → "Import from File"**
2. `c:\Repos\note-articles\workflows\notes-to-notion-improved.json` を選択
3. インポート後、「Manual Test Trigger」ノードから実行
4. Notion に新規ページが作成されることを確認

---

### Step 4: 実ファイルで自動検知テスト

#### Watch ノードでのテスト（元のワークフロー）

1. **C:\Notes に新規ファイルを作成**
   ```powershell
   @"
   今日の学び
   
   n8n を使った自動化について学んだ。
   Docker でのファイルマウントの重要性を理解した。
   "@ | Out-File -Encoding UTF8 C:\Notes\test_auto_$(Get-Date -Format 'yyyyMMddHHmmss').txt
   ```

2. **n8n UI の "Executions" タブで実行履歴を確認**
   - Watch Notes Folder がトリガーされているか
   - Notion Create Item まで到達しているか

3. **Notion Database で新規ページを確認**

#### Cron ベースのテスト（改善版ワークフロー）

1. **改善版ワークフローを Active にする**
2. **5分待つ**（Cron が `/notes` をスキャン）
3. **Executions タブで実行ログを確認**

---

## 🐛 よくある問題と対処

### ❌ "Node does not have any credentials set for 'notionApi'"

**原因**: ワークフローノードに認証情報が紐付いていない

**対処**:
1. ワークフロー編集画面を開く
2. 「Notion Create Item」ノードをクリック
3. Credential dropdown で「Notion account」を選択
4. Save

---

### ❌ Notion API "Unauthorized (401)"

**原因**: Integration Token が無効または Database に接続されていない

**対処**:
1. Notion で Database を開く
2. "..." → "Add connections" → "n8n-notes-organizer" を追加
3. Integration Token を再生成して n8n に再登録

---

### ❌ Watch ノードがファイルを検知しない

**原因**: Docker 環境では `localFileTrigger` が動作しない場合がある

**対処**:
- **改善版ワークフロー（Cron ベース）を使用**
- 5分ごとに `/notes` をスキャンして新規ファイルを検出
- より確実に動作します

---

## 📊 確認チェックリスト

- [ ] n8n UI にログインできる
- [ ] Credentials に「Notion account」が登録されている
- [ ] Test Connection が成功する
- [ ] ワークフローの Notion ノードに認証情報が紐付いている
- [ ] 手動テストで Notion に新規ページが作成される
- [ ] C:\Notes に新規ファイルを作成すると自動で Notion に登録される

---

## 🎉 完成後の運用

### 日常的な使い方

```powershell
# n8n 起動（設定は永続化されているのでこれだけ）
cd c:\Repos\note-articles\workflows
.\start-n8n.ps1

# ノート作成（自動的に Notion に登録される）
notepad C:\Notes\今日のメモ.txt

# n8n 停止（設定は保持される）
.\stop-n8n.ps1
```

### 完全自動化

```powershell
# コンテナを自動起動に設定
docker update --restart=always n8n-notes-organizer

# PC 起動時に自動で n8n が起動します
```

---

## 🆘 さらにサポートが必要な場合

### ログ確認

```powershell
# n8n コンテナログ
docker logs n8n-notes-organizer --tail 50

# リアルタイムログ
docker logs n8n-notes-organizer -f
```

### ワークフロー実行履歴

n8n UI → **Executions** タブで各ノードの入出力を確認

### Docker コンテナ内部確認

```powershell
# コンテナ内のファイル確認
docker exec n8n-notes-organizer ls -la /notes

# コンテナに入る
docker exec -it n8n-notes-organizer /bin/sh
```

---

## 📚 参考ドキュメント

- **永続化の仕組み**: `PERSISTENT_SETUP.md`
- **トラブルシューティング**: `TROUBLESHOOTING.md`
- **カスタマイズ**: `CUSTOMIZATION.md`
- **簡単ガイド**: `HOW_TO_USE.md`

---

**次は上記 Step 1 から順に進めてください！** 🚀
