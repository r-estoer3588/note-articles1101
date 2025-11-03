from pathlib import Path
WORKFLOW = Path('c:/Repos/note-articles/workflows/Notes to Notion Auto Organizer (Schedule Fixed).json')
text = WORKFLOW.read_text(encoding='utf-8')
UNESCAPED = '{"category": "カテゴリ名", "tags": ["タグ1"]}'
ESCAPED = '{\\"category\\": \\"カテゴリ名\\", \\"tags\\": [\\"タグ1\\"]}'
if UNESCAPED not in text:
    raise SystemExit('target substring not found')
WORKFLOW.write_text(text.replace(UNESCAPED, ESCAPED, 1), encoding='utf-8')
