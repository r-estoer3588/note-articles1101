from pathlib import Path
WORKFLOW = Path('c:/Repos/note-articles/workflows/Notes to Notion Auto Organizer (Schedule Fixed).json')
text = WORKFLOW.read_text(encoding='utf-8')
needle = '{"category": "カテゴリ名"'
index = text.index(needle)
snippet = text[index-80:index+120]
print(repr(snippet))
