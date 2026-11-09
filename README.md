# Machine Learning Club — Seven Hills International School

Static GitHub Pages website for the 2026–2027 club.

- **15 weekly sessions**, Wednesday 16:00–17:00 (proposed), from **2 December 2026 to 7 April 2027**, excluding winter and February breaks.
- **70 RON per student per session**; group size up to 10 students.
- Weeks 1–9: fundamentals; Weeks 10–12: integrated AI systems; Weeks 13–15: FIICode preparation.
- Each week has separate **Course**, **Laboratory**, **Homework**, and **Advanced** pages with measurable objectives and tasks.
- The existing interactive Week 1 course, laboratory, slides and PDF are retained.

## Editing the programme

The source of truth is `scripts/generate_curriculum.py`. Update its `DATA` and `TASKS` records, then regenerate all pages from the repository root:

```bash
python3 scripts/generate_curriculum.py
```

No Node.js build step is needed. GitHub Pages serves the committed HTML/CSS files directly. The script is idempotent and preserves the detailed Week 1 interactive material.

All dates are proposed and must be confirmed with the school's calendar. FIICode 2027 contest dates are not assumed.
