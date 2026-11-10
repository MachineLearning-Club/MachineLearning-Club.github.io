# Machine Learning Club — Seven Hills International School

Static GitHub Pages website for the 2026–2027 Machine Learning Club.

The club has **15 planned one-hour weekly meetings**, from December 2026 to April 2027, with dates subject to school calendar confirmation. The programme includes three stages: ML fundamentals (Weeks 1–9), integrated AI systems with introductory Git/GitHub (Weeks 10–12), and competition/project work (Weeks 13–15).

## Learning materials

Each week has four separately linked, deliberately minimalist pages:

- **Course** — three related conceptual sections, with source-specific bibliography for each.
- **Laboratory** — a webapp, a runnable club-owned Colab starter, an external study notebook, and guided activities.
- **Homework** — a transfer exercise based on the same lab code, including expected deliverables and references.
- **Advanced** — optional experiments and adapted Olympiad-level work.

The original extended Week 1 course and its interactive matching exercise are preserved, with a separate bibliography and notebook section.

The `syllabus/` page maps stages to frameworks, and `resources/` is the consolidated source bibliography.

### Colab notebooks

Club notebooks live at `w1/lab/starter.ipynb` through `w15/lab/starter.ipynb`. Open any file using `https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/wN/lab/starter.ipynb`.

They use CPU-only Python and small synthetic/public datasets. Typical dependencies: NumPy, matplotlib, pandas and scikit-learn. Additional public Olympiad notebooks are linked only as references; they can be longer and written in Polish.

## Updating content

Do not edit generated HTML directly if it should survive regeneration.

- `scripts/generate_curriculum.py`: main week titles, dates and high-level objective lists.
- `data/weeks_01_05.json`, `data/weeks_06_10.json`, `data/weeks_11_15.json`: course sections, lab webapps and references, homework and advanced tasks.
- `data/bibliography.json`: source titles and URLs.
- `scripts/generate_colab_starters.py`: working Python starter cells.
- `scripts/render_curriculum_sources.py`: student-facing pages.
- `scripts/render_overview.py`: syllabus and bibliography index.
- `scripts/apply_classic_theme.py`: original homepage layout and plain styling.

Regenerate the site from the repository root:

```bash
python3 scripts/generate_curriculum.py
```

The generator is idempotent. The website uses static HTML and CSS without a Node.js build step.

No external notebook, site or competition archive is represented as an official endorsement. The Romanian secondary-school ML optional programme is the principal technical anchor, while non-mandated topics (ID3, CNN internals and neural networks) are explicitly sourced from other courses or Olympiad material.

Official dates of FIICode 2027 are not assumed.

The minimalist `/materials/` index maps concrete source chapters, teaching worksheets, interactive tools, external notebooks and optional competition tasks to each week. Its editable source is `data/week_materials_map.json`.

## Weekly quiz prototype

Starting with Week 2, the homepage links to `/quiz/`. There are 14 catalogue entries and two complete **draft** quiz banks (Weeks 2 and 3), each with ten questions / five minutes / ten points. The frontend-only preview displays the eQuiz-style test history, access-code dialog, timed attempt, navigation, scoring, explanation review and CSV export. The demonstration has no authentication; scores are stored in the local browser and are **not** official grades. See `quiz/README.md` for the security and rollout requirements.
