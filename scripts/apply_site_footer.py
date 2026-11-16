#!/usr/bin/env python3
"""Apply the same generated, minimal site footer to existing public HTML pages.

Includes authored lessons that the curriculum builder intentionally preserves,
plus the independent quiz catalogue and Week 1 slides. Running twice is safe.
"""
from pathlib import Path
import re
from site_footer import site_footer

ROOT=Path(__file__).resolve().parents[1]
LINK='<link rel="stylesheet" href="/assets/site-footer.css">'
FOOTER=site_footer()
EXCLUDED_ROOTS={'jupyter','data'}
def process(path):
    content=path.read_text(encoding='utf-8')
    if path.parts and path.relative_to(ROOT).parts[0] in EXCLUDED_ROOTS:
        return False
    # Preserve the quiz's in-dialog exam-footer controls; only replace its
    # original page footer (which lives inside <main>).
    if path.relative_to(ROOT).as_posix()=='quiz/index.html':
        pattern=r'<footer class="(?:footer|site mlclub-footer)"[^>]*>.*?</footer>'
    elif path.relative_to(ROOT).as_posix()=='w1/slides/index.html':
        pattern=r'<footer(?: class="site mlclub-footer"[^>]*)?>.*?</footer>'
    else:
        pattern=r'<footer class="site(?: mlclub-footer)?"[^>]*>.*?</footer>'
    content,n=re.subn(pattern,lambda _:FOOTER,content,count=1,flags=re.S)
    if n!=1:
        raise RuntimeError(f'Expected one site-wide footer in {path}; found {n}')
    if LINK not in content:
        if '</head>' not in content:
            raise RuntimeError(f'Missing </head> in {path}')
        content=content.replace('</head>',LINK+'</head>',1)
    if content!=path.read_text(encoding='utf-8'):
        path.write_text(content,encoding='utf-8')
        return True
    return False
def main():
    modified=[]
    for path in sorted(ROOT.rglob('*.html')):
        if process(path):
            modified.append(path.relative_to(ROOT))
    print(f'Updated shared footer on {len(modified)} public pages')
    return modified
if __name__=='__main__':main()
