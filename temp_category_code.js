// Categorize note with OpenAI when possible and provide fallback heuristics
const inputData = $input.item.json;
const apiKey = $env.OPENAI_API_KEY;

const buildFallback = () => {
  const text = `${inputData.fileName || ''}\n${inputData.fileContent || ''}`.toLowerCase();
  const pathLower = (inputData.filePath || '').toLowerCase();
  const tagsSet = new Set();

  const segments = (inputData.filePath || '')
    .split('/')
    .map(segment => segment.trim())
    .filter(Boolean);

  // Use folder names as tags when available
  segments.slice(0, -1).forEach(segment => tagsSet.add(segment));

  const rules = [
    { pattern: /(meeting|議事録|会議|mtg)/i, category: '会議メモ', tags: ['会議'] },
    { pattern: /(reading|読書|書評|要約)/i, category: '読書メモ', tags: ['読書'] },
    { pattern: /(idea|アイデア|企画|brainstorm)/i, category: 'アイデア', tags: ['アイデア'] },
    { pattern: /(todo|task|日報|振り返り|学習|メモ)/i, category: '個人メモ', tags: ['メモ'] },
    { pattern: /(code|開発|python|bug|技術|sql|api)/i, category: '技術メモ', tags: ['技術'] }
  ];

  for (const rule of rules) {
    if (rule.pattern.test(text) || rule.pattern.test(pathLower)) {
      if (Array.isArray(rule.tags)) {
        rule.tags.forEach(tag => tagsSet.add(tag));
      }
      return {
        category: rule.category,
        tags: Array.from(tagsSet)
      };
    }
  }

  if (segments.length > 1) {
    const folder = segments[segments.length - 2] || '未分類';
    tagsSet.add(folder);
    return {
      category: folder,
      tags: Array.from(tagsSet)
    };
  }

  return {
    category: '未分類',
    tags: Array.from(tagsSet)
  };
};

const mergeResult = result => {
  const category = result.category || '未分類';
  const tags = Array.isArray(result.tags) ? result.tags : [];
  const uniqueTags = Array.from(new Set(tags.map(tag => String(tag).trim()).filter(Boolean)));
  return { ...inputData, category, tags: uniqueTags };
};

if (!apiKey) {
  return mergeResult(buildFallback());
}

try {
  const response = await $http.post('https://api.openai.com/v1/chat/completions', {
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'user',
        content: `あなたはノート分類の専門家です。以下のノート内容を読んで、適切なカテゴリとタグを提案してください。\n\n【カテゴリ候補】\n- 技術メモ\n- 読書メモ\n- アイデア\n- 会議メモ\n- 個人メモ\n\n【出力形式】\nJSON形式で返してください:\n{"category": "カテゴリ名", "tags": ["タグ1"]}\n\nファイル名: ${inputData.fileName}\n内容: ${inputData.fileContent}`
      }
    ],
    temperature: 0.3,
    response_format: { type: 'json_object' }
  }, {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    }
  });

  const content = response.data.choices?.[0]?.message?.content;
  if (!content) {
    return mergeResult(buildFallback());
  }

  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (parseError) {
    console.error('OpenAI parse error:', parseError.message);
    return mergeResult(buildFallback());
  }

  const fallback = buildFallback();
  const category = parsed.category || fallback.category;
  const combinedTags = new Set();
  (fallback.tags || []).forEach(tag => combinedTags.add(String(tag)));
  (Array.isArray(parsed.tags) ? parsed.tags : []).forEach(tag => combinedTags.add(String(tag)));

  return {
    ...inputData,
    category: category || '未分類',
    tags: Array.from(combinedTags).map(tag => tag.trim()).filter(Boolean)
  };
} catch (error) {
  console.error('OpenAI API Error:', error.message);
  return mergeResult(buildFallback());
}
