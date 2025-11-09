# LINE Bot メニュー実装ガイド

**ボタン操作だけで使えるLINE Botの作り方**

## 📋 実装の全体像

```
1. リッチメニュー作成 → LINE Developers
2. n8nワークフロー拡張 → 状態管理追加
3. クイックリプライ実装 → ボタン生成
4. カルーセル実装 → 複数投稿表示
```

## 🎨 ステップ1: リッチメニュー作成

### 1-1. LINE Developers でリッチメニュー作成

1. LINE Developers → Messaging API設定
2. 「リッチメニュー」タブ
3. 「作成」ボタン

### 1-2. リッチメニュー設定

#### 基本設定

```
タイトル: ホゲーメニュー
表示期間: 常に表示
メニューバーのテキスト: メニュー
```

#### レイアウト

```
テンプレート: 6分割（2列×3行）

┌──────┬──────┐
│  A   │  B   │
├──────┼──────┤
│  C   │  D   │
├──────┼──────┤
│  E   │  F   │
└──────┴──────┘
```

#### 各エリアの設定

**A: 投稿生成**
```
アクション: テキスト送信
テキスト: menu:generate
ラベル: 📝投稿生成
```

**B: 3部作生成**
```
アクション: テキスト送信
テキスト: menu:trilogy
ラベル: 📖3部作
```

**C: 今日のテーマ**
```
アクション: テキスト送信
テキスト: menu:today
ラベル: 📚今日
```

**D: 学習実行**
```
アクション: テキスト送信
テキスト: menu:learn
ラベル: 🎓学習
```

**E: 状態確認**
```
アクション: テキスト送信
テキスト: menu:status
ラベル: 📊状態
```

**F: ヘルプ**
```
アクション: テキスト送信
テキスト: menu:help
ラベル: ❓ヘルプ
```

### 1-3. 画像アップロード

Canvaなどで以下を作成（2500×1686px）:

```
┌─────────┬─────────┐
│ 📝      │ 📖      │
│ 投稿生成│ 3部作   │
├─────────┼─────────┤
│ 📚      │ 🎓      │
│ 今日    │ 学習    │
├─────────┼─────────┤
│ 📊      │ ❓      │
│ 状態    │ ヘルプ  │
└─────────┴─────────┘
```

または、シンプルに文字だけでもOK。

## 🔧 ステップ2: n8nワークフロー拡張

### 2-1. 状態管理用のGoogle Sheets作成

**シート名**: `ユーザー状態管理`

| user_id | state | count | theme | posts_data | current_index | updated_at |
|---------|-------|-------|-------|------------|---------------|------------|
| U123... | selecting_count | null | null | null | 0 | 2025-11-08... |

**各カラムの意味**:
- `user_id`: LINEユーザーID
- `state`: 現在の状態（idle/selecting_count/selecting_theme/viewing_posts）
- `count`: 選択した件数
- `theme`: 選択したテーマ
- `posts_data`: 生成した投稿データ（JSON）
- `current_index`: 現在表示中の投稿番号
- `updated_at`: 最終更新日時

### 2-2. n8nワークフロー: メインフロー

```javascript
// コマンド解析（拡張版）
const event = $input.item.json.events[0];
const text = event.message.text;
const userId = event.source.userId;
const replyToken = event.replyToken;

// ユーザー状態を取得
const userState = await getUserState(userId); // Google Sheetsから取得

let result = {
  userId: userId,
  replyToken: replyToken,
  text: text
};

// リッチメニューコマンド判定
if (text.startsWith('menu:')) {
  const menuAction = text.split(':')[1];
  
  switch(menuAction) {
    case 'generate':
      result.action = 'show_count_selection';
      result.type = 'buzz';
      break;
      
    case 'trilogy':
      result.action = 'show_theme_selection';
      result.type = 'trilogy';
      break;
      
    case 'today':
      result.action = 'show_count_selection';
      result.type = 'today';
      break;
      
    case 'learn':
      result.action = 'show_learn_confirm';
      break;
      
    case 'status':
      result.action = 'show_status';
      break;
      
    case 'help':
      result.action = 'show_help';
      break;
  }
} 
// 状態に応じた処理
else if (userState.state === 'selecting_count') {
  // 件数が選択された
  result.count = parseInt(text);
  result.action = 'show_theme_selection';
  result.type = userState.type;
}
else if (userState.state === 'selecting_theme') {
  // テーマが選択された
  result.theme = text;
  result.count = userState.count;
  result.action = 'generate_posts';
  result.type = userState.type;
}

return { json: result };
```

### 2-3. クイックリプライ生成関数

```javascript
// 件数選択ボタン
function createCountSelection() {
  return {
    type: 'text',
    text: '何件生成しますか？',
    quickReply: {
      items: [
        {
          type: 'action',
          action: {
            type: 'message',
            label: '3件',
            text: '3'
          }
        },
        {
          type: 'action',
          action: {
            type: 'message',
            label: '5件',
            text: '5'
          }
        },
        {
          type: 'action',
          action: {
            type: 'message',
            label: '10件',
            text: '10'
          }
        },
        {
          type: 'action',
          action: {
            type: 'message',
            label: '20件',
            text: '20'
          }
        }
      ]
    }
  };
}

// テーマ選択ボタン
function createThemeSelection() {
  const themes = [
    { emoji: '💰', name: '貧乏脱出' },
    { emoji: '🎰', name: 'ギャンブル依存' },
    { emoji: '💼', name: '副業' },
    { emoji: '🏢', name: 'ブラック企業' },
    { emoji: '💸', name: '無駄遣い' },
    { emoji: '📱', name: 'SNS依存' },
    { emoji: '😴', name: '人間関係' },
    { emoji: '⏰', name: '時間術' },
    { emoji: '✏️', name: '自由入力' }
  ];
  
  return {
    type: 'text',
    text: 'テーマを選んでください',
    quickReply: {
      items: themes.map(t => ({
        type: 'action',
        action: {
          type: 'message',
          label: `${t.emoji} ${t.name}`,
          text: t.name
        }
      }))
    }
  };
}

// 投稿アクションボタン
function createPostActions(postIndex, totalPosts) {
  return {
    quickReply: {
      items: [
        {
          type: 'action',
          action: {
            type: 'postback',
            label: '🚀 X投稿',
            data: `action=post&index=${postIndex}`
          }
        },
        {
          type: 'action',
          action: {
            type: 'postback',
            label: '💾 保存',
            data: `action=save&index=${postIndex}`
          }
        },
        {
          type: 'action',
          action: {
            type: 'postback',
            label: '➡️ 次へ',
            data: `action=next&index=${postIndex + 1}`,
            displayText: postIndex < totalPosts - 1 ? '次を見る' : '最初に戻る'
          }
        },
        {
          type: 'action',
          action: {
            type: 'message',
            label: '🗑️ 破棄',
            text: '破棄'
          }
        }
      ]
    }
  };
}
```

### 2-4. カルーセル表示（複数投稿）

```javascript
function createPostCarousel(posts) {
  return {
    type: 'template',
    altText: '投稿が生成されました',
    template: {
      type: 'carousel',
      columns: posts.slice(0, 10).map((post, index) => ({
        text: post.text.substring(0, 60) + '...',
        actions: [
          {
            type: 'postback',
            label: '投稿する',
            data: `action=post&index=${index}`
          },
          {
            type: 'postback',
            label: '保存',
            data: `action=save&index=${index}`
          },
          {
            type: 'postback',
            label: '詳細',
            data: `action=detail&index=${index}`
          }
        ]
      }))
    }
  };
}
```

## 📱 ステップ3: 実装パターン別コード

### パターンA: 投稿生成フロー

```javascript
// 1. メニューから「投稿生成」
if (action === 'show_count_selection') {
  // 状態を保存
  await updateUserState(userId, {
    state: 'selecting_count',
    type: 'buzz'
  });
  
  // 件数選択ボタン表示
  return createCountSelection();
}

// 2. 件数選択 → テーマ選択へ
if (userState.state === 'selecting_count') {
  await updateUserState(userId, {
    state: 'selecting_theme',
    count: parseInt(text)
  });
  
  return createThemeSelection();
}

// 3. テーマ選択 → 生成実行
if (userState.state === 'selecting_theme') {
  const count = userState.count;
  const theme = text;
  
  // Python実行
  const result = await executePython(count, theme);
  
  // 状態保存
  await updateUserState(userId, {
    state: 'viewing_posts',
    posts_data: JSON.stringify(result),
    current_index: 0
  });
  
  // 最初の投稿を表示
  const firstPost = result[0];
  return {
    type: 'text',
    text: `🐶 投稿1/${result.length}\n\n${firstPost.text}\n\nテーマ: ${firstPost.theme}\n教育: ${firstPost.education_type}`,
    ...createPostActions(0, result.length)
  };
}
```

### パターンB: 今日のテーマ（ワンタップ）

```javascript
if (action === 'show_count_selection' && type === 'today') {
  // 曜日別テーマを自動設定
  const themes = {
    0: '時間の使い方',
    1: 'ギャンブル依存',
    2: 'ブラック企業',
    3: '無駄遣い',
    4: 'SNS依存',
    5: '疲労',
    6: '人間関係'
  };
  const today = new Date().getDay();
  const theme = themes[today];
  
  // 件数選択のみ
  await updateUserState(userId, {
    state: 'selecting_count',
    type: 'today',
    theme: theme
  });
  
  return {
    type: 'text',
    text: `📚 今日は${theme}のテーマです\n何件生成しますか？`,
    ...createCountSelection().quickReply
  };
}
```

### パターンC: 学習実行（確認付き）

```javascript
if (action === 'show_learn_confirm') {
  // データ件数確認
  const myPostsCount = await getCSVRowCount('my_posts.csv');
  const benchPostsCount = await getCSVRowCount('bench_posts.csv');
  
  return {
    type: 'template',
    altText: '学習実行確認',
    template: {
      type: 'confirm',
      text: `CSV学習を実行します\n\n現在のデータ:\n- my_posts: ${myPostsCount}件\n- bench_posts: ${benchPostsCount}件\n\n実行しますか？`,
      actions: [
        {
          type: 'postback',
          label: '✅ 実行する',
          data: 'action=learn_execute'
        },
        {
          type: 'message',
          label: '❌ キャンセル',
          text: 'キャンセル'
        }
      ]
    }
  };
}
```

## 🎯 ステップ4: 完全版n8nワークフロー構成

```
1. LINE Webhook受信
   ↓
2. コマンド/状態判定
   ↓
3. 分岐処理
   ├→ 件数選択表示
   ├→ テーマ選択表示
   ├→ Python実行
   ├→ 投稿表示
   ├→ 学習実行
   └→ エラー処理
   ↓
4. 状態保存（Google Sheets）
   ↓
5. LINE返信
```

## 📊 状態遷移図

```
[idle] 
  ↓ menu:generate
[selecting_count] 
  ↓ 数字入力
[selecting_theme] 
  ↓ テーマ選択
[viewing_posts] 
  ↓ 投稿/保存/次へ
[idle] に戻る
```

## 🔐 セキュリティ

### ユーザー認証

```javascript
const allowedUsers = ['YOUR_USER_ID'];
if (!allowedUsers.includes(userId)) {
  return {
    type: 'text',
    text: '❌ このBotは使用できません'
  };
}
```

### セッションタイムアウト

```javascript
const lastUpdated = new Date(userState.updated_at);
const now = new Date();
const diff = (now - lastUpdated) / 1000 / 60; // 分

if (diff > 30) {
  // 30分経過したらリセット
  await updateUserState(userId, {
    state: 'idle',
    posts_data: null
  });
  
  return {
    type: 'text',
    text: 'セッションがタイムアウトしました。メニューから再度選択してください。'
  };
}
```

## 🎨 UI改善Tips

### ローディング表示

```javascript
// 生成中メッセージ
await sendLineMessage(userId, '⏳ 生成中...');

// Python実行
const result = await executePython(count, theme);

// 完了メッセージで上書き
await sendLineMessage(userId, '✅ 完了！');
```

### プログレス表示

```javascript
return {
  type: 'text',
  text: `🐶 投稿${currentIndex + 1}/${totalPosts}\n━━━━━━━━━━\n${progressBar}\n\n${post.text}`
};

function getProgressBar(current, total) {
  const filled = Math.floor((current / total) * 10);
  return '█'.repeat(filled) + '░'.repeat(10 - filled);
}
```

## 📱 完成イメージ

### 実際の使用例

```
ユーザー: [リッチメニュー] 投稿生成タップ

Bot: 何件生成しますか？
     [3件] [5件] [10件] [20件]

ユーザー: [5件]タップ

Bot: テーマを選んでください
     [💰貧乏脱出] [💼副業] [🏢ブラック企業] ...

ユーザー: [💼副業]タップ

Bot: ⏳ 生成中...
     
Bot: 🐶 投稿1/5
     ━━░░░░░░░░
     
     ホゲーっと生きてる。
     気づいたら何も変わってない。
     ...
     
     テーマ: 副業
     教育: 行動の教育
     
     [🚀 X投稿] [💾 保存] [➡️ 次へ] [🗑️ 破棄]

ユーザー: [🚀 X投稿]タップ

Bot: ✅ Xに投稿しました！
```

## 🆘 トラブルシューティング

### ボタンが表示されない

- クイックリプライの上限は13個まで
- リッチメニューが正しく登録されているか確認

### 状態がリセットされる

- Google Sheetsの書き込み権限確認
- タイムアウト設定確認

### 生成が遅い

- ローディングメッセージを先に送信
- Pythonの実行時間を最適化

次のファイルで完全なn8n JSONを提供します。

---

**コマンド不要。すべてボタンで完結。**
