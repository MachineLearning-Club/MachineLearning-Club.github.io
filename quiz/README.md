# Machine Learning Club — Weekly Quiz prototype

This is a **functional, frontend-only demo** inspired by the eQuiz interface in the supplied screenshots. It is not connected to the real Java Technologies eQuiz service and is not a grading or access-control system.

## Current status

- Quizzes are planned for **Weeks 2 through 15**; all 14 entries exist in the catalog, with provisional calendar dates.
- **Week 2** (statistics, probability, entropy) and **Week 3** (decision trees / ID3) have ten original draft questions each.
- Weeks **4–15** are explicit placeholders. Their banks should be authored only after deciding the exact taught syllabus.
- The prepared demos have five-minute clocks, ten questions and ten points total. All values are editable.
- Both **single-select** and **multi-select** questions are supported. All correct choices must be selected to earn the question's point; there is no partial credit or penalty.
- The interface reveals correct choices and reasoning only after submission. However, the JSON bank itself is public; this is **not suitable for a real secure exam**.
- Attempts are stored only in the current browser using localStorage, without a student name, password, network submission or official grade.
- Learners can review attempts, see a score history, retake the demo, clear local results and export results as CSV.

## Demo codes

Open /quiz/, click **Take a test** and enter:

- **MLC02** — Week 2
- **MLC03** — Week 3

These are visible public shortcuts, *not secret access codes*. Opening /quiz/?week=2 pre-fills the code modal.

## Authoring weekly quiz banks

The catalog is located at quiz/data/catalog.json. Question files follow quiz/data/week-02.json and quiz/data/week-03.json.

A question contains: a unique id; a type of single or multiple; a prompt; an array of exactly four options; an array of correct option indices (zero-based); an explanation; a topic and a point value. The full JSON for Week 2 is the schema example. When a new question bank is approved, change the corresponding catalog entry to status=demo and update the question-count and max-points metadata.

Keep questions precisely tied to what was taught in Course and Laboratory that week. Do not publish unreviewed external Olympiad questions as assessment material.

## Test locally

From the repository root, use a static server such as Python http.server 8765, then run node quiz/test_quiz.js on a computer with Chromium and Puppeteer. The test simulates attempts and checks scoring, review and responsive layout.

## Requirements before real student use

GitHub Pages is static. For a real class grading system, we will need:

1. Authenticated school identities and separate teacher/student roles. Never request real passwords in a mock UI.
2. Server-side question storage with secret answer keys, authoritative scoring and submission timestamps.
3. Secure time-limited access tokens and availability windows; don't publish real access codes in source code.
4. A teacher dashboard for authoring, review, scheduled release and grade exports.
5. Privacy-by-design for minors, school-authorized data retention and deletion policies.
6. Accessibility, timing accommodations, sensible scoring and limited retry policies.
7. Resilience to interrupted connections and abuse, and an auditable gradebook.
8. A weekly content approval workflow matching the real course, rather than the current outline.

We should select a backend only after agreeing on the assessment and privacy requirements.

## Design reference

The supplied eQuiz screenshots informed the action button, scores/history table, access-code modal, radio/checkbox questions, navigation, timer, points and review. This is an independently implemented ML Club quiz interface with its own branding and original questions.
