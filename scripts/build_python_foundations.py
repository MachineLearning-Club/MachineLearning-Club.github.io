#!/usr/bin/env python3
"""Publish the original, progressive Python foundations guide for ML Club."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data/python_foundations_lessons.json"
TARGET = ROOT / "guides/python/index.html"

def e(text: object) -> str:
    return html.escape(str(text), quote=True)

def python_runner(code: str, number: int, kind: str) -> str:
    widget_id = f"foundation-{number}-{kind}"
    rows = min(24, max(5, len(code.splitlines()) + 1))
    return (
        '<div class="python-runner">'
        f'<label for="{widget_id}">Editable Python program</label>'
        f'<textarea id="{widget_id}" class="py-source" rows="{rows}" '
        f'spellcheck="false" aria-label="Python example {number}: {e(kind)}">{e(code)}</textarea>'
        '<div class="runner-actions"><button type="button" class="run-python">Run Python</button>'
        '<span>Runs locally in your browser</span></div>'
        '<output class="py-output" aria-live="polite">Edit the code and run it to see the output.</output>'
        '</div>'
    )

def page() -> str:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    lessons = data["lessons"]
    assert len(lessons) >= 15, "Expected comprehensive coverage"
    groups = list(dict.fromkeys(item["group"] for item in lessons))
    html_parts = [
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta name="description" content="A free, beginner-friendly introduction to Python programming, algorithmic thinking, functions, loops and lists. Includes editable code you can run in your browser.">',
        '<title>Python Programming Foundations · Machine Learning Club</title>',
        '<link rel="stylesheet" href="/assets/academic.css">',
        '<link rel="stylesheet" href="/assets/v3.css">',
        '<link rel="stylesheet" href="/assets/v4.css">',
        '<link rel="stylesheet" href="/assets/python-foundations.css">',
        '<script defer src="/assets/academic-ui.js"></script></head><body>',
        '<a class="foundations-skip" href="#lessons">Skip to lessons</a>',
        '<header class="foundations-head">',
        '<p class="foundations-back"><a href="/">← Machine Learning Club</a></p>',
        '<p class="foundations-overline">Before Module I · Preparation</p>',
        '<h1>Python Programming Foundations</h1>',
        '<p class="foundations-lede">From your first program to the algorithms behind data processing. '
        'Read a short explanation, expand a worked example, edit the code, and run it directly in your browser.</p>',
        '<p class="foundations-meta">Beginner-friendly · 21 short topics · 42 editable programs · No account required</p>',
        '</header>',
        '<main class="foundations-page">',
        '<section class="foundations-intro" aria-labelledby="how-to-use">',
        '<h2 id="how-to-use">How to use this guide</h2>',
        '<ol><li>Start with Topics 1–16 if you are new to programming. '
        'You can skip anything you already know.</li>',
        '<li>For each topic, predict what the sample prints, then select <strong>Run Python</strong>. '
        'Change an input value and run it again.</li>',
        '<li>Try the challenge before expanding its solution. Topics 17–20 are optional deeper algorithms; '
        'Topic 21 connects the basics with Machine Learning.</li></ol>',
        '<p class="foundations-note"><strong>Browser execution:</strong> The first run downloads a Python engine '
        '(Pyodide) over the internet. Programs run in an isolated browser worker. '
        'The examples use editable preset inputs, because interactive terminal input prompts are not supported here. '
        'Use <strong>Stop</strong> to interrupt a long-running program.</p>',
        '</section>',
        '<nav class="foundations-toc" aria-label="Python foundations contents">',
        '<h2>Contents</h2>',
    ]
    for group in groups:
        group_lessons = [(i, l) for i, l in enumerate(lessons, 1) if l["group"] == group]
        html_parts.append(f'<div class="foundations-toc-group"><h3>{e(group)}</h3><ol>')
        for i, lesson in group_lessons:
            html_parts.append(f'<li><a href="#topic-{i:02d}">{e(lesson["title"])}</a></li>')
        html_parts.append('</ol></div>')
    html_parts.extend(['</nav>', '<div id="lessons" class="foundations-sections">'])
    for group in groups:
        group_lessons = [(i,l) for i,l in enumerate(lessons,1) if l["group"] == group]
        name_id = f"group-{groups.index(group)+1}"
        html_parts.append(f'<section class="foundations-group" aria-labelledby="{name_id}">')
        html_parts.append(f'<h2 id="{name_id}">{e(group)}</h2>')
        if group == "Further algorithmic practice":
            html_parts.append('<p class="foundations-group-note">Optional extensions from the textbook. '
                              'Understand the idea and run the examples; these are not prerequisites for Week 1.</p>')
        for i, lesson in group_lessons:
            open_attribute = ' open' if i == 1 else ''
            html_parts.append(f'<details class="foundation-lesson" id="topic-{i:02d}"{open_attribute}>')
            html_parts.append(
                '<summary>'
                f'<span class="foundation-no">{i:02d}</span>'
                f'<span class="foundation-summary"><strong>{e(lesson["title"])}</strong>'
                f'<small>{e(lesson["lead"])}</small></span>'
                f'<span class="foundation-tag">{e(lesson["tag"])}</span>'
                '</summary>'
            )
            html_parts.append('<div class="foundation-body">')
            html_parts.append('<h3>Core idea</h3><p>'+e(lesson["lead"])+'</p><ol class="foundation-steps">')
            for step in lesson["steps"]:
                html_parts.append('<li>'+e(step)+'</li>')
            html_parts.append('</ol>')
            html_parts.append(f'<details class="foundation-subdetail"{" open" if i == 1 else ""}>'
                              '<summary>Worked example · Run and modify</summary>'
                              f'<p>{e(lesson["demo"])}</p>'
                              +python_runner(lesson["code"],i,"example")+'</details>')
            html_parts.append('<details class="foundation-subdetail"><summary>Check your understanding</summary>'
                              f'<p>{e(lesson["question"])}</p>'
                              '<details class="foundation-solution"><summary>Show a possible solution</summary>'
                              +python_runner(lesson["solution"],i,"solution")+'</details></details>')
            html_parts.append('<details class="foundation-subdetail"><summary>Common pitfall and teacher note</summary>'
                              '<p>'+e(lesson["tip"])+'</p></details>')
            html_parts.append('<p class="foundation-connection"><strong>Connection to ML:</strong> '
                              +e(lesson["ml"])+'</p>')
            html_parts.append('</div></details>')
        html_parts.append('</section>')
    html_parts.extend([
        '</div><section class="foundations-next"><h2>What comes next?</h2>',
        '<p>Once you can work with conditions, loops, functions and lists, begin&nbsp;',
        '<a href="/w1/course/">Week 1 — What Is AI? Rules and Learning</a>. '
        'You can revisit this guide whenever an algorithm or Python concept needs a refresher.</p>',
        '<p class="foundations-source"><strong>Reference:</strong> Cezara Benegui, Ana-Cristina Iova, '
        'Rodica Smîntînă, Andrei Păun, Ciprian-Mihai Ceaușescu and Paul Enache, '
        '<em>Informatică 9</em> (Corint), especially chapters 1, 2.1 and 4. '
        'This is independently written English material with original examples. '
        'Text-file processing, graphical interfaces and object-oriented programming from the wider textbook '
        'are intentionally deferred beyond this introductory guide.</p></section>',
        '</main><footer class="site"><span>Independent educational project operated by '
        '<a href="https://github.com/dbxdrgsl" target="_blank" rel="noopener noreferrer">'
        'BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ</a></span> · '
        '<a href="https://github.com/MachineLearning-Club" target="_blank" rel="noopener noreferrer">'
        'GitHub organisation</a></footer>',
        '</body></html>'])
    return "\n".join(html_parts)+"\n"

if __name__ == "__main__":
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(page(), encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")
