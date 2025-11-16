// デバッグ用：状態判定ロジックのテストスクリプト

const userId = $input.item.json.userId;
const menuAction = $input.item.json.menuAction;
const text = $input.item.json.text || '';
const action = $input.item.json.action;

const normalizeDigits = (value = '') => value.replace(/[０-９]/g, (d) => String.fromCharCode(d.charCodeAt(0) - 0xFEE0));
const parsePostsData = (raw) => {
  if (!raw) {
    return [];
  }
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (err) {
    return [];
  }
};

const userStateRaw = $node['ユーザー状態取得'].json;
let userState = userStateRaw;
if (!userState || userState.error) {
  userState = { state: 'initial' };
}

// ========== デバッグログ追加 ==========
console.log('========== 状態判定デバッグ ==========');
console.log('入力テキスト:', text);
console.log('menuAction:', menuAction);
console.log('action:', action);
console.log('userState:', JSON.stringify(userState, null, 2));
console.log('userState.state:', userState.state);
console.log('======================================');
// =====================================

const withClearedPosts = (overrides = {}) => ({
  posts_data: null,
  current_index: 0,
  ...overrides
});

const makeResetState = () => withClearedPosts({
  state: 'idle',
  count: null,
  theme: null,
  type: null
});

let result = {
  userId,
  replyToken: $input.item.json.replyToken,
  currentState: userState,
  nextAction: null,
  updateState: null
};

const buildGenerateParams = (count, theme, type) => ({
  count: count ?? userState.count ?? null,
  theme: theme ?? userState.theme ?? '不明',
  type: type ?? userState.type ?? 'buzz'
});

const postsFromState = parsePostsData(userState.posts_data);

if (menuAction) {
  console.log('→ menuActionブランチに入った');
  switch (menuAction) {
    case 'generate':
      result.nextAction = 'show_count_selection';
      result.updateState = withClearedPosts({ state: 'selecting_count', type: 'buzz', count: null, theme: null });
      break;
    case 'trilogy':
      result.nextAction = 'show_theme_selection';
      result.updateState = withClearedPosts({ state: 'selecting_theme', type: 'trilogy', count: 3 });
      break;
    case 'today':
      const cats = ['日曜_趣味遊び', '月曜_ギャンブル金', '火曜_ビジネスキャリア', '水曜_生活節約', '木曜_社会ネット裏事情', '金曜_健康美容', '土曜_恋愛人間関係'];
      const todayTheme = cats[new Date().getDay()];
      result.nextAction = 'show_count_selection';
      result.updateState = withClearedPosts({ state: 'selecting_count', type: 'today', theme: todayTheme });
      result.todayTheme = todayTheme;
      break;
    case 'help':
      result.nextAction = 'show_help';
      result.updateState = makeResetState();
      break;
    case 'discard':
      result.nextAction = 'discard_posts';
      result.updateState = makeResetState();
      break;
    default:
      result.nextAction = 'show_help';
      result.updateState = makeResetState();
      break;
  }
}
else if (action) {
  console.log('→ actionブランチに入った');
  const posts = postsFromState;
  if (!Array.isArray(posts) || posts.length === 0) {
    result.nextAction = 'error';
    result.errorMessage = '表示できる投稿がありません';
  } else {
    const providedIndex = Number.isInteger($input.item.json.index)
      ? $input.item.json.index
      : (Number.isInteger(userState.current_index) ? userState.current_index : 0);
    const normalizedIndex = Math.min(posts.length - 1, Math.max(0, providedIndex));
    let targetIndex = normalizedIndex;

    if (action === 'next') {
      targetIndex = (normalizedIndex + 1) % posts.length;
    } else if (action === 'prev') {
      targetIndex = (normalizedIndex - 1 + posts.length) % posts.length;
    } else if (action === 'first') {
      targetIndex = 0;
    } else if (action === 'last') {
      targetIndex = posts.length - 1;
    }

    if (action === 'discard') {
      result.nextAction = 'discard_posts';
      result.updateState = makeResetState();
    } else {
      const targetPost = posts[targetIndex] || posts[0];
      const generateParams = {
        count: userState.count || posts.length,
        theme: userState.theme || targetPost?.theme || '不明',
        type: userState.type || 'buzz'
      };

      if (action === 'post' || action === 'save') {
        result.nextAction = 'post_action';
        result.actionIntent = action;
        result.postContent = targetPost;
        result.postIndex = targetIndex;
      } else {
        result.nextAction = 'show_post';
        result.postContent = targetPost;
        result.postIndex = targetIndex;
      }

      result.totalPosts = posts.length;
      result.generateParams = generateParams;
      result.updateState = {
        state: 'viewing_posts',
        posts_data: userState.posts_data,
        current_index: targetIndex,
        count: generateParams.count,
        theme: generateParams.theme,
        type: generateParams.type
      };
    }
  }
}
else if (userState.state === 'selecting_count') {
  console.log('→ selecting_countブランチに入った');
  const normalized = normalizeDigits(text).replace(/[^0-9]/g, '');
  console.log('正規化後の数字:', normalized);
  const count = parseInt(normalized, 10);
  console.log('パースした件数:', count);
  if (Number.isFinite(count) && count > 0 && count <= 50) {
    console.log('件数は有効範囲内');
    if (userState.type === 'today') {
      result.nextAction = 'generate_posts';
      result.generateParams = { count, theme: userState.theme, type: userState.type };
      result.updateState = withClearedPosts({
        state: 'generating',
        count,
        theme: userState.theme,
        type: userState.type
      });
    } else {
      result.nextAction = 'show_theme_selection';
      result.updateState = withClearedPosts({
        state: 'selecting_theme',
        count,
        type: userState.type || 'buzz'
      });
    }
  } else {
    console.log('件数が無効:', count);
    result.nextAction = 'error';
    result.errorMessage = '1〜50の数字を入力してください';
  }
}
else if (userState.state === 'selecting_theme') {
  console.log('→ selecting_themeブランチに入った');
  result.nextAction = 'generate_posts';
  result.generateParams = { count: userState.count, theme: text, type: userState.type || 'buzz' };
  result.updateState = withClearedPosts({
    state: 'generating',
    theme: text,
    count: userState.count,
    type: userState.type || 'buzz'
  });
}
else {
  console.log('→ デフォルト（ヘルプ）ブランチに入った');
  console.log('理由: userState.state =', userState.state);
  result.nextAction = 'show_help';
  result.updateState = makeResetState();
}

console.log('最終的なnextAction:', result.nextAction);
console.log('========================================');

return { json: result };
