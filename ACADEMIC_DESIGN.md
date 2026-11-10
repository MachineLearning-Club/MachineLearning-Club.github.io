# Academic learning experience

The reviewed working curriculum lives in `data/curriculum_2026.json` and is generated from `scripts/publish_academic.py`.

- **Course**: white serif electronic textbook, intended to progress from concrete problem through intuition, examples, algorithms, Python and limitations. Week 1 and Week 2 have detailed migrated proof-of-concept content; the rest currently have editorial outlines, not finished textbook chapters.
- **Laboratory**: accountless browser activities and guided executable notebooks are the target. Existing starter notebooks are downloads; this migration does **not** claim that all 15 labs already have a JupyterLite embed.
- **Quiz**: preserve the existing eQuiz engine and presentation. Weeks 2 and 3 retain provisional draft banks; other weeks await teacher review. Ten questions / five minutes / ten points remains the target; opt-in emailed results require future mail infrastructure.
- **Homework**: UAIC Java-Technologies-style Context / Mandatory (1p) / Homework (2p) / optional Research / Submission.
- **Advanced**: printable, rigorous study booklets. Week 1 and Week 2 contain the existing complete PDFs; remaining weeks are outlines.

All site pages use the white `assets/academic.css` style, initially migrated from `/preview/assets/poc.css`. The old `/preview` route was removed. Avoid reintroducing legacy themes through obsolete generators.

To regenerate: `python3 scripts/publish_academic.py` (idempotent). Always review `git diff` and run link checks before publishing. Do not describe outlines as completed lessons.
