# Machine Learning Club — two-week teaching material prototype

These are **independent preview pages**. They do not replace the production lesson pages.

- [Preview index](/preview/)
- Week 1: [Course](/preview/w1/course/), [Laboratory](/preview/w1/lab/), [Homework](/preview/w1/homework/), [Advanced](/preview/w1/advanced/)
- Week 3: [Course](/preview/w3/course/), [Laboratory](/preview/w3/lab/), [Homework](/preview/w3/homework/), [Advanced](/preview/w3/advanced/)

## Goals

1. Course: Bogdan Pătruț-style structured electronic textbook; numbered definitions, complete examples, concise per-topic references, executable code and small diagrams.
2. Laboratory: predict → experiment with a webapp → inspect Colab → modify code → reflect. Existing Google and Experience AI resources are used only by linking; no third-party lesson content is reproduced.
3. Homework: UAIC Java Technologies-style task specification, Context → Mandatory (1p) → Homework (2p) → Submission. Complete CSV files and a data loader are provided; GitHub is optional until the engineering stage.
4. Advanced: Ciortuz-style progressive algorithmic reasoning, a worked example, counterexamples, selected solutions and a printable A4 PDF with an editable LaTeX source. **No Dafny, SAT solver or formal verification tool is expected.**

## Rebuild

From the repository root:

```sh
python3 preview/notebooks.py
python3 preview/build.py
python3 preview/advanced_print.py
node preview/make_pdfs.js
node preview/test_layout.js
```

The PDF generation step uses the local Chromium/Puppeteer renderer to print the accessible Advanced exercise HTML; equivalent editable LaTeX sources are included for later refinement into a LaTeX-first publication pipeline. All layouts use `preview/assets/poc.css` and are isolated from the live course styles.

## References

Experience AI Foundations lessons 1–4; CBSE XI AI Student Handbook; pyml.ro; IOAI classical-ML syllabus; Google Quick, Draw!, Teachable Machine; and the two UAIC examples supplied in the design discussion. Mathematical examples, synthetic datasets, Python and problem explanations are original for this preview.
