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
python3 scripts/build_python_foundations.py # Generate the beginner Python guide from its editable JSON content
python3 scripts/test_python_foundations.py  # Check all 42 runnable example and solution programs
python3 scripts/generate_v3_notebooks.py    # Refresh aligned student notebook files for Weeks 3–15
node quiz/test_quiz.js                      # Run the older catalogue / test-dialog regression suite (Chromium required)
```

All public pages are **static HTML, CSS and JavaScript**, styled with `assets/academic.css` and `assets/v3.css`. No framework build or database is needed.

## Student work without accounts

- Laboratories include a short, in-page Python exercise powered by **Pyodide in a Web Worker**. It loads on demand from a version-pinned CDN. No account, and student code runs in the student's own browser.
- Each lab supplies an editable notebook `wN/lab/starter.ipynb`. Students may download it and open it in **JupyterLite** (no account) by dragging the file into JupyterLite's file browser. Google Colab is optional and needs an account for execution.
- Before Module I: `/guides/python/` teaches the English-language Python and algorithmic foundations in 21 short expandable topics. Source data lives in `data/python_foundations_lessons.json`; all 42 runnable examples are checked offline. The tutorial draws on Grade 9 `Informatică 9` topics but uses original explanations and programs.
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

## Week 1 exploratory laboratory and probability practice

Week 1 has an authored laboratory (`data/week1_lab_active.html`), probability homework (`data/week1_probability_homework.html`), and additional advanced problems (`data/week1_advanced_additions.html`). After changing any of those fragments, execute `python3 scripts/update_week1_practice.py`. The main curriculum generator deliberately preserves Week 1 to avoid overwriting teacher-approved materials. Its remaining weeks are still generated normally.

The Week 1 lab uses the same sticky chapter navigation as the first Course, and links to Quick, Draw!, HF Pixel Search, a browser-only HF image classifier, Google creative experiments and account-free generative HTML tools. The editable coffee-shop prompt specifies a simulated, non-payment checkout. Always confirm external service availability and school policies before a lesson.

The laboratory also contains three **run-now Python examples** plus three complete notebooks. The club's account-free JupyterLite lives under `/jupyter/lab/index.html`, with direct `?path=01-nearest-prototype.ipynb` (or `02-biased-die.ipynb`, `03-learn-thermostat.ipynb`) links. To update or rebuild this JupyterLite distribution:

```bash
python3 scripts/generate_week1_notebooks.py
bash scripts/build_jupyterlite.sh
```

The JupyterLite bundle is committed as static files. It uses a Python (Pyodide) kernel running in the browser, with no login. The initial visit requires an internet connection to download the engine. Its build script removes unused JavaScript source maps to reduce repository size. No uploaded class data are sent to a backend.

The Homework includes a worked formula guide, elementary probability events, distribution selection and an interactive probability chart. The advanced page extends the original problem set with weighted sums, expected values, variance and covariance, including SVG graphs and worked solutions.

## Detailed Weeks 2 and 3 — teacher-authored sequence

Weeks 2 and 3 now have their own source fragments in `data/week23/` for Course, Laboratory, Homework and Advanced. Update the fragments, then execute `python3 scripts/update_week23.py`. The main curriculum generator **preserves** these pages instead of replacing them with generic summaries. Teacher-reviewed source content and reusable interactions live in `assets/week23-interactive.js` and `assets/week23.css`.

Week 2 uses the same 12-entry fictional school activity dataset throughout Course, Lab and Homework (`w2/homework/club-events.csv`). Students progress through features/labels, pure and mixed splits, entropy, weighted gain, categorical tree construction, handling unseen values, and testing on held-out records. The live visualization computes information gain for sky (~0.667), wind (~0.082) and temperature (0). The Advanced exercises include an elementary greedy counterexample and a preserved downloadable PDF booklet.

Week 3 adapts the **mathematical data** of Liviu Ciortuz's K-means solved problem 7 (§7.1.2, printed pp. 853–856) to a delivery-service story: A(-1,0), B(1,0), C(0,1), D(3,0), E(3,1). K=2 starts at centroids A and E, yields clusters ABC and DE, then new centres (0,1/3) and (3,1/2), reducing squared error from 7 to 19/6. Students explore assignments, arithmetic means, convergence, initialisation and outliers. A separate ten-point fictional neighbourhood appears in `w3/homework/delivery-points.csv` and the delivery notebook.

The handbook files supplied by the teacher are **not rehosted** in this public repository; each page cites the original author, section and printed page numbers. Student exercises and explanatory prose are original adaptations, with selected links to public external training resources.

There are two additional preloaded JupyterLite notebooks per week, under `w2/lab/notebooks/` and `w3/lab/notebooks/`. `scripts/generate_week23_notebooks.py` creates them. Run `bash scripts/build_jupyterlite.sh` to include all seven introductory notebooks (three from Week 1, two from Week 2, two from Week 3) in `/jupyter/lab/`. `scripts/refresh_week23_quizzes.py` regenerates draft practice questions based on the actual lesson datasets, not unrelated sample gains.

Useful checks (when the site is served locally at port 8877):

```sh
node tests/test_week23.js
node quiz/test_quiz.js
```

All exercises remain classroom materials awaiting final teacher review; not all final real-world constraints, grades or challenge formats are fixed.

## Detailed pre-university teaching — Weeks 4–7

The complete academic source for these four weeks lives in `data/week47/w{4,5,6,7}_{course,lab,homework,advanced}.html`. Run `python3 scripts/update_week47.py` to publish changes; `scripts/publish_v3.py` preserves these pages when rebuilding the 15-week navigation. Each Course follows a consistent chain: concrete situation, visual or numeric observation, worked calculation, algorithm, independent practice, and explicit limits. The established minimalist Georgia/white layout is retained.

- **Week 4 — Revision:** retrieve Week 2 ID3 and Week 3 K-means from the original datasets, then briefly compare KNN's supervised voting and a six-example confusion matrix. The objective is revision, not a third algorithm-heavy lesson.
- **Week 5 — Images as data:** original synthetic grayscale pixel matrix, RGB averaging and luminance, thresholding, 3×3 averaging and a custom sharpening kernel; editable pixel-grid visualisation. Grounded in the uploaded UAIC Vision Lab 1–2; camera/pixel sensor context can optionally refer to Timofte's Computer Vision lectures. No real student photographs are required.
- **Week 6 — Perceptrons:** a binary 0/1 AND classifier, full weighted-sum truth table, interactive linear boundary, manual mistake update and epochs of online training. The notation is explicitly adapted from Ciortuz's ±1 representation (§6.1.1, §6.1.2).
- **Week 7 — Neural networks:** a hand-specified hidden-layer XOR network, then a deliberately separate sigmoid neuron with squared loss and gradient descent. Two-layer chain-rule gradients and finite differences are in the optional notebook/Advanced material, following Ciortuz §6.1.3. We do not misrepresent supplied XOR weights as weights learned by gradient descent.

Each week has two original self-contained Pyodide notebooks under `wN/lab/notebooks/`, built into the shared JupyterLite with `python3 scripts/generate_week47_notebooks.py` and `bash scripts/build_jupyterlite.sh`. The corresponding quiz bank has ten school-level practice items in `quiz/data/week-0N.json`, generated by `scripts/generate_week47_quizzes.py`. Quizzes are marked drafts, not official grades.

Browser regression tests (server on `127.0.0.1:8877`): `node tests/test_week47.js`, `node tests/test_week47_quizzes.js`. All source PDFs were used for research, mathematical alignment and citations, not copied into this public static repository.

## Site footer and attribution

The project is independently operated by **BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ**; partner schools are not listed as owners. The shared, accessible, responsive footer lives in `scripts/site_footer.py`, with styling in `assets/site-footer.css`. It links to the author’s personal website, https://dragosandreibobu.github.io/, the lesson index, timetable, bibliography, weekly quizzes, MachineLearning-Club GitHub organisation, repository source, and current partner school.

`python3 scripts/generate_curriculum.py` regenerates the core pages and applies the same footer to teacher-authored lessons, the quiz catalogue and the slide landing page. To reapply the footer without regenerating content, run `python3 scripts/apply_site_footer.py`. The Python foundations guide also imports the shared footer directly from its generator.

Browser check against local server on port 8877: `node tests/test_site_footer.js` (homepage, lessons, guides, quiz and slides at mobile, tablet and desktop widths).

## School-level Generative AI and Software Engineering — Weeks 10–11

`data/week1011/` is the source for the eight authored Course, Laboratory, Homework and Advanced pages. `scripts/update_week1011.py` installs these into the existing minimalist page chrome; `scripts/generate_week1011_starters.py` creates one eight-cell, account-free notebook per week. Both are called by `scripts/generate_curriculum.py`. `assets/week1011.js` provides local, deterministic teaching examples (token splitter, invented next-token candidates, two-category recommendation ranking, sensor-to-display pipeline), styled by `assets/week1011.css`. No API keys, accounts, third-party file uploads or live model endpoints are needed.

The following references inform **teacher preparation** but are not pupil requirements or copied to the public repository:
- Dragoș Gavriluț, *Agentic AI Course 1–3*, *Labs 1–4*, *Lab 1–3 Solutions*, and *Behind the Scenes*. Week 10 extracts the intuition behind tokens, text generation, observed behaviour, fact checking, and human approval. Week 11 uses the source's division of a product idea into verifiable parts and its example of correcting an AI coding agent mid-task.
- UAIC-BSc-ComputerScience/CS2203-SoftwareEngineering, `course/eng` at `ade24aaa04cfea686fc476387d15320100e4860f`: SE02 requirements, SE03 class diagrams, SE06 unit tests, SE11 usability and quality. The student-facing course uses only a tiny Sensor/Validator/Controller/Display example, simple classes and three assertions; full UML, SOLID, design pattern catalogues, formal Scrum and Java testing frameworks are excluded.
- GitHub Docs *Hello World* and GitHub Skills *Introduction to GitHub* are linked in `/guides/github-ai/`, with real GitHub accounts and a commit/push-to-main workflow in the current tutorial; an account-free introduction is no longer the primary route. VS Code's official Copilot setup is an optional, account-based reference.

Regression: `node tests/test_week1011.js` against the local server on port 8877; the notebooks are executable with standard Python, no third-party libraries. Existing quiz placeholders for Weeks 10–11 are intentionally unchanged until the teacher reviews these lessons.

## Screenshot-led GitHub/Codespaces/VS Code Agent tutorial

The Module III prerequisite lives at `/guides/github-ai/`. Its authored body is `data/guides/github-ai.html`, and `scripts/publish_v3.py` wraps it with the existing school website chrome. CSS and small controls live at `assets/github-guide.css` and `assets/github-guide.js`. The tutorial is regenerated with `python3 scripts/generate_curriculum.py` and is stable across runs.

Instructional route: student creates their own eligible GitHub account → creates a **public** repository (`my-first-ai-site`, initial README) → uses **Code → Codespaces → Create codespace on main** (browser VS Code running in a cloud container) → creates a self-contained `index.html` → works with the VS Code agent in the Chat view (Copilot sign-in/allowance as applicable) → previews on port 8000 → inspects, commits and **pushes to main** → enables **Settings → Pages → Deploy from a branch → main / (root)** → checks the public project-site URL → stops the Codespace. Branches and pull requests are explained as later collaboration techniques, not mandatory first-day steps. Underage students must not be asked to create prohibited accounts; GitHub's minimum is 13 with possible higher local minimums.

There are 13 *annotated real interface screenshots* in `assets/guides/github-ai/*.webp` (~400 KB combined), adapted from official GitHub Docs, VS Code Docs or an unsigned public ML Club repository capture. Captions credit original sources and note where labels or example repository names differ. The blue arrows are teaching annotations, not synthetic interface elements; screenshot layouts can evolve. Do not redistribute raw screenshot sources or suggest that unauthenticated GitHub views show Codespaces controls.

A fully offline-inference, browser-only sample coffee-shop cart is available at `/guides/github-ai/starter/`. It uses basic HTML, CSS and JavaScript, with no payments, third-party services, secret keys or server. Both the guide and starter retain the shared site footer.

Regression: `node tests/test_github_guide.js` with the local site running on port 8877 checks annotated screenshot loading, responsive mobile/tablet/desktop layout, in-page links, public project URL generation and working café cart. Official references include GitHub account onboarding and Terms, GitHub Codespaces quickstart, VS Code agent quickstart, GitHub Pages quickstart and publishing configuration. GitHub Codespaces and Copilot have variable usage quotas; they are not unlimited free services.

## Updated prerequisite guides — sidebar and notebook screenshots

The Python foundations guide (`guides/python/`) preserves its 21 teaching units and 42 browser-executable scripts. Its original content generator is `scripts/build_python_foundations.py` and the new desktop sticky left-hand navigation plus collapsible mobile contents panel are in `assets/python-foundations.css` and `assets/python-foundations-nav.js`. A TOC link automatically expands its destination lesson.

The notebooks guide (`guides/notebooks/`) uses `data/guides/notebooks.html` as its reviewed source. It reuses the GitHub guide layout (`assets/github-guide.css`) with minor notebook-specific rules (`assets/notebook-guide.css`). It is regenerated by `scripts/publish_v3.py` and shows seven arrow-annotated actual screenshots captured from the club's live JupyterLite installation, stored in `assets/guides/notebooks/*.webp`. The images document its file browser, upload button, code cell, Run button, actual output, File > Save Notebook As and File > Download. This tutorial is account-free. Published notebooks may be read-only, so an editable browser copy and a downloaded portable `.ipynb` are distinguished.

Official reference manuals: [JupyterLite usage](https://jupyterlite.readthedocs.io/en/stable/quickstart/using.html), [JupyterLab Notebooks](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html), [JupyterLab Interface](https://jupyterlab.readthedocs.io/en/stable/user/interface.html), [JupyterLite read-only content](https://jupyterlite.readthedocs.io/en/latest/howto/content/readonly.html). Screenshots reflect the ML Club JupyterLite interface as of November 2026 and have instructional arrow overlays. No academic PDF materials or student data were used to make these screenshots.

Regression: `python3 scripts/test_python_foundations.py` and `node tests/test_guides_sidebar_notebooks.js` (against local server port 8877) cover content counts, navigation, image loading, and responsive layout.

## Embedded notebooks and Kaggle competition introduction

The `/guides/notebooks/` prerequisite now includes two **real, interactive `.ipynb` notebooks** (`01-nearest-prototype.ipynb` and `02-biased-die.ipynb`) from the existing account-free JupyterLite bundle. A learner clicks **Run inside this page** to lazily create an iframe with `/jupyter/lab/index.html?path=...`, keeping only one JupyterLite editor/kernel open at a time. Every example also links to its full-screen editor and to the original `.ipynb` download. Only explicit student action loads the potentially heavy runtime; phone users are advised to use the full-screen link. The source is `data/guides/notebooks.html`, with controls in `assets/notebook-guide.js` and styling in `assets/notebook-guide.css`.

The separate `/guides/kaggle/` prerequisite lives in `data/guides/kaggle.html` and is generated through `scripts/publish_v3.py` with `assets/kaggle-guide.css` and `assets/kaggle-guide.js`. It includes five original screenshots of Kaggle's **public** user interface with blue instructional arrows, credited to Kaggle, saved in `assets/guides/kaggle/*.webp` (~250KB). It teaches official rules, tabular labelled/unlabelled data, the distinction between training and validation, a small Titanic decision-tree baseline, required submission columns, classical CSV upload versus executed-notebook submissions, and public/private leaderboards. An interactive three-row `practice_only.csv` download intentionally cannot be confused with a real Titanic submission (which requires predictions for 418 rows).

Both guides use official Kaggle learning resources and docs (`https://www.kaggle.com/learn`, `https://www.kaggle.com/learn-guide/kaggle-competitions`, `https://www.kaggle.com/docs/competitions`, `https://www.kaggle.com/docs/notebooks`, `https://www.kaggle.com/competitions/titanic`). The homepage now links the competition guide directly **before Week 12 / FiiCode**. Whether a future FiiCode edition will actually use Kaggle is **unverified**; there is no official FiiCode workflow presented as fact.

Run `node tests/test_embedded_notebooks_and_kaggle.js` against the local site on port 8877. It verifies 390/820/1280px layouts, 12 screenshots and 22 guide anchors, lazy loading of an actual JupyterLite notebook, swapping between the two notebooks without parallel kernels, and live CSV predictions. The authored page files are regeneration-safe when `python3 scripts/generate_curriculum.py` runs.
