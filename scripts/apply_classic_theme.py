#!/usr/bin/env python3
"""Restore the original minimalist GitHub Pages appearance after curriculum generation.

The old homepage is the design reference; no frameworks, cards or coloured panels.
"""
from html import escape as E
from pathlib import Path

root = Path(__file__).resolve().parents[1]
template = (root / "templates/classic-home.template").read_text(encoding="utf-8")
source = (root / "scripts/generate_curriculum.py").read_text(encoding="utf-8")
# The generator currently writes a static DATA table. Read it without re-executing generation.
raw = source.split('DATA = """', 1)[1].split('""".strip()', 1)[0].strip()
lessons = []
for line in raw.splitlines():
    cols = line.split("|")
    if len(cols) != 8:
        raise ValueError("Malformed lesson source")
    n, date, name, summary, *_ = cols
    lessons.append((int(n), date, name, summary))
assert [n for n, *_ in lessons] == list(range(1, 16))

# Exactly preserve the original home's inline CSS and fundamental markup.
begin = template.index("  <main>")
end = template.index("  </main>", begin) + len("  </main>")
lines = ['  <main>', '    <section>', '      <h2>Course</h2>']
for n, date, name, summary in lessons:
    lines.extend([
        '      <article class="week">',
        f'        <div class="week-title">Week {n} — {E(name)} · {E(date)}</div>',
        '        <ul class="materials">',
    ])
    for k, label in [("course", "Course"), ("lab", "Laboratory"), ("homework", "Homework"), ("advanced", "Advanced")]:
        lines.extend([
            '          <li>',
            f'            <a href="/w{n}/{k}/">{label}</a>',
            '          </li>',
        ])
    if n >= 2:
        lines.append(f'          <li><a href="/quiz/?week={n}">Quiz</a></li>')
    lines.append("        </ul>")
    if n == 1:
        lines.append('        <div class="extra"><a href="/w1/slides/">Slides</a></div>')
    lines.append("      </article>")
lines += [
    '    </section>',
    '    <section>',
    '      <h2>General resources</h2>',
    '      <ul>',
    '        <li><a href="/syllabus/">Syllabus</a></li>',
    '        <li><a href="/calendar/">Calendar</a></li>',
    '        <li><a href="/resources/">Resources</a></li>',
    '        <li><a href="/materials/">Teaching material map</a></li>',
    '        <li><a href="/quiz/">Weekly quizzes</a></li>',
    '        <li><a href="/projects/">Projects</a></li>',
    '      </ul>',
    '    </section>',
    '  </main>',
]
homepage = template[:begin] + "\n".join(lines) + template[end:]
assert "Week 15" in homepage and "Register here" in homepage
(root / "index.html").write_text(homepage, encoding="utf-8")

# All newer pages retain their teaching content, but use restrained typography
# to match the original site's Georgia / white / blue links layout.
css = r"""
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  max-width: 780px;
  margin: 60px auto;
  padding: 0 24px;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 17px;
  line-height: 1.55;
  color: #222;
  background: #fff;
}
a { color: #174a7e; text-decoration: none; }
a:hover { text-decoration: underline; }
a:focus-visible { outline: 2px solid #174a7e; outline-offset: 3px; }
h1 { font-size: 2rem; margin: 0 0 6px; font-weight: normal; }
h2 {
  margin-top: 42px;
  margin-bottom: 12px;
  padding-bottom: 6px;
  font-size: 1.2rem;
  font-weight: normal;
  border-bottom: 1px solid #ddd;
}
h3 { font-size: 1.05rem; font-weight: bold; margin: 22px 0 6px; }
p { margin: 10px 0 16px; }
header.site { margin-bottom: 48px; }
.brand { color: #222; text-decoration: none; font-size: 1.1rem; }
.brand small { display: block; font-size: .85rem; color: #777; font-weight: normal; }
.topnav { margin-top: 18px; display: flex; gap: 0 15px; flex-wrap: wrap; font-size: .9rem; }
.shell, footer.site { width: 100%; }
.hero { margin: 0 0 36px; }
.hero h1 { margin-bottom: 10px; }
.eyebrow { font-size: .85rem; color: #777; margin: 0 0 8px; }
.meta { color: #777; font-size: .86rem; }
.pill { display: inline; }
.pill + .pill::before { content: " · "; }
.module-nav { margin: 20px 0 36px; font-size: .92rem; }
.module-nav a { display: inline; margin-right: 16px; }
.module-nav a[aria-current="page"] { text-decoration: underline; text-underline-offset: 3px; }
.block { margin: 28px 0; }
.objectives { display: block; padding-left: 24px; margin: 8px 0 20px; }
.objectives li { margin: 7px 0; }
.cards { display: block; }
.card { padding: 0; margin: 0 0 16px; }
.card h3 { margin: 16px 0 4px; font-size: 1rem; }
.card p { margin: 4px 0 12px; }
.panel { padding: 0; }
.panel li { margin: 7px 0; }
.callout { margin: 10px 0; padding: 0; }
.note { color: #666; font-size: .93rem; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 10px 12px 10px 0; text-align: left; border-bottom: 1px solid #ddd; }
th { font-weight: bold; }
.phase { margin: 34px 0; }
.phase>p { color: #666; }
.week { padding: 0; margin: 28px 0; }
.week h3 { margin: 0 0 7px; }
.week p { margin: 6px 0 10px; }
.date { color: #666; font-size: .85rem; }
.links { display: block; }
.links a { display: block; margin: 6px 0; }
.links small { display: none; }
.skip { position: absolute; left: -10000px; }
.skip:focus { left: 15px; top: 15px; background: #fff; padding: 8px; }
footer.site {
  margin-top: 70px;
  padding: 14px 0 0;
  border-top: 1px solid #ddd;
  font-size: .85rem;
  color: #777;
}
@media (max-width: 680px) {
  body { margin: 28px auto; padding: 0 18px; font-size: 16px; }
  header.site { margin-bottom: 32px; }
  .module-nav a { margin-right: 10px; }
}
@media print {
  body { max-width: none; margin: 0; color: #000; }
  .topnav, .module-nav { display: none; }
  a { color: #000; }
}
""".strip() + "\n"
# Minimal, fully wrapping text navigation on every generated lesson page.
css += """
.site-subtitle { margin: 6px 0 0; color: #666; font-size: .9rem; }
.lesson-meta { margin: 0 0 8px; color: #666; font-size: .87rem; }
.lesson-nav { display: flex; flex-wrap: wrap; gap: 7px 20px; margin: 23px 0 32px; padding: 0 0 12px; border-bottom: 1px solid #ddd; font-size: .95rem; }
.lesson-nav a { display: inline-block; white-space: nowrap; }
.lesson-nav a[aria-current="page"] { color: #222; font-weight: bold; text-decoration: underline; text-underline-offset: 3px; }
.lesson-pagination { margin-top: 38px; padding-top: 14px; border-top: 1px solid #ddd; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 14px; }
main.shell section { margin: 28px 0; }
main.shell h1 { margin-bottom: 12px; }
main.shell ul, main.shell ol { padding-left: 24px; }
main.shell li { margin: 7px 0; }
@media (max-width: 680px) { .lesson-nav { gap: 7px 15px; } }
"""
(root / "assets/site.css").write_text(css, encoding="utf-8")
print("Restored original homepage structure; simplified CSS for curriculum pages.")
