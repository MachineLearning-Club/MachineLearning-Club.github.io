# Machine Learning Club

Independent educational project operated by **BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ**.

Website: https://machinelearning-club.github.io/ · Source: https://github.com/MachineLearning-Club/MachineLearning-Club.github.io

The club can partner with multiple schools. The first listed partner is Seven Hills International School, Iași, 2026–2027. Partner details, registration links, teachers and *unconfirmed* session assignments are configured in `data/schools.json`; they are not a statement that the school owns the club.

## Current academic plan: 3 + 6 + 6 weeks

- **Module I (1–3):** What Is AI? Rules and Learning; Supervised Learning: ID3; Unsupervised Learning: K-Means.
- **Module II (4–9):** Revision: supervised/unsupervised ML including KNN; images and computer vision; perceptrons; neural networks; revision; mid-term evaluation.
- **Module III (10–15):** GPT and its social/ethical impact; software engineering including elementary OOP; four FIICode weeks, culminating in the real hackathon.

The syllabus is a **working draft** and will be reviewed with the teacher one week at a time. Do not imply that the final competition challenge, school meeting times, student groups or rooms are fixed.

Each week has **Course**, **Laboratory**, **Homework**, **Advanced** and **Quiz**. Quiz banks exist as draft practice for Weeks 1–3; the other weeks explicitly await content approval.

## Authoring and regeneration

The publisher is `scripts/publish_v3.py`, with compatible aliases in `scripts/generate_curriculum.py` and `scripts/publish_academic.py`.

To update course content, edit:
- `data/outline_v3_01_05.json`
- `data/outline_v3_06_10.json`
- `data/outline_v3_11_15.json`

Each week defines a title, motivating real-life scenario, worked course sections, runnable examples, app, laboratory steps, homework context and task, research challenge and selected bibliography IDs.

The detailed Week 1 and ID3 course/lab/homework/advanced bodies are preserved as source fragments in `data/legacy_content/`. They can be refined individually without rewriting the entire site.

Useful commands:

```sh
python3 scripts/generate_curriculum.py      # Generate HTML, navigation, timetable, bibliography, guide pages
python3 scripts/generate_v3_notebooks.py    # Refresh aligned student notebook files for Weeks 3–15
node quiz/test_quiz.js                      # Run the older catalogue / test-dialog regression suite (Chromium required)
```

All public pages are **static HTML, CSS and JavaScript**, styled with `assets/academic.css` and `assets/v3.css`. No framework build or database is needed.

## Student work without accounts

- Laboratories include a short, in-page Python exercise powered by **Pyodide in a Web Worker**. It loads on demand from a version-pinned CDN. No account, and student code runs in the student's own browser.
- Each lab supplies an editable notebook `wN/lab/starter.ipynb`. Students may download it and open it in **JupyterLite** (no account) by dragging the file into JupyterLite's file browser. Google Colab is optional and needs an account for execution.
- Before Module II: `/guides/notebooks/` explains the notebook workflow step by step.
- Before Module III: `/guides/github-ai/` contains an account-free Git-history simulation and a guide to collaborating with a code editor and optional AI assistance.
- A valid but **local-only** laboratory submission workflow asks for the student's name and files, then downloads a named ZIP with `README.txt`. It does **not** upload anything.

For real submissions, create a school-approved **Dropbox File Request** and add its URL to `data/submissions.json` (field `request_url`). The UI then exposes an external upload link. No Dropbox credentials, access tokens or secrets belong in public files. Until this is configured, students should keep their prepared ZIP locally.

## Timetable

The internal `/timetable/` page mimics a clean university timetable grid and links each activity to Course, Lab, Homework, Advanced and Quiz. All unknown day/time, room and group slots remain explicitly unassigned. No external eOra licence or integration is used. `data/schools.json` is the school-partner registry for later expansion.

## Quizzes

The primary student experience is a **lightweight inline quiz** at `/wN/quiz/`, visually integrated with that week's lesson. An optional legacy `/quiz/` catalogue remains available with a more compact layout. Draft practice banks and notes live in `quiz/data/`.

There is **no backend, secure examination mode, authentication, server-side grading or official gradebook**. Public static JSON contains correct answers, so quiz scores are practice-only and kept in the current browser. An optional emailed copy of results is a future feature requiring a protected sending endpoint, consent and limits.

## Academic references

The `/resources/` page is titled **Bibliography**. Each Course, Lab, Homework and Advanced page includes a *selected*, relevant bibliography rather than a generic list. Sources include Experience AI, Romanian ML materials, CBSE school AI handbooks, the Polish AI Olympiad course, IOAI/ONIA references, Microsoft AI/ML for Beginners and educational browser visualisers.

## Ownership and contact

The club and website are independently operated by **BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ**. The hosting repository is maintained by the [MachineLearning-Club GitHub organisation](https://github.com/MachineLearning-Club). The participating school is a programme partner, not the owner of the club.
