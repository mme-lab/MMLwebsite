# main.py
from pathlib import Path
import re
from datetime import datetime

def define_env(env):
    root = Path(__file__).resolve()
    docs = (root / "docs") if (root / "docs").exists() else (root.parent / "docs")
    news_md = docs / "news.md"
    pat = re.compile(r"^\s*-\s*(?P<date>\d{4}-\d{2}-\d{2})\s*:\s*(?P<body>.+)$", re.MULTILINE)

    @env.macro
    def latest_news(n=5):
        text = news_md.read_text(encoding="utf-8")
        items = []
        for m in pat.finditer(text):
            d = datetime.strptime(m.group("date"), "%Y-%m-%d")
            items.append((d, f"- {m.group('date')}: {m.group('body').strip()}"))
        if not items:
            return "（最新ニュースは未登録です）"
        items.sort(key=lambda x: x[0], reverse=True)
        return "\n".join(x[1] for x in items[:int(n)])

