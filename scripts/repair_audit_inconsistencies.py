#!/usr/bin/env python3
"""Idempotent repairs for audit findings in Week 2 and Weeks 10–11.

Keep source fragments as canonical; run the existing page builders after edits.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def change(relative, old, new):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if new in text:
        print("Already repaired:", relative)
        return
    if text.count(old) != 1:
        raise ValueError(f"{relative}: expected exactly one target, found {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Repaired:", relative)

def submission_form(week):
    return (
        f'<div class="submission-form" data-submission-week="{week}">'
        '<label>Student name<input type="text" class="student-name" '
        'placeholder="First name, last name" maxlength="90" autocomplete="name"></label>'
        '<label class="file-drop">Choose files'
        '<input class="submission-files" type="file" '
        'accept=".ipynb,.py,.csv,.pdf,.zip,.txt,.md" multiple></label>'
        '<p class="submission-selected" aria-live="polite">No file selected.</p>'
        '<button class="prepare-submission" type="button">Download named submission</button>'
        '<p class="submission-status" aria-live="polite"></p>'
        '</div>'
        '<p class="understated">Your files are bundled in a ZIP on this device. '
        'Downloading is not submitting: use the teacher-provided collection link, '
        'when available, or follow your teacher\'s hand-in instructions.</p>'
    )

change(
    "data/week1011/w10_lab.html",
    '<section id="submission"><h2>Submission</h2><p>One completed notebook or short document containing a token sequence, two feed rankings and the corrected vote claim. Use invented or anonymous data only. Your laboratory submission controls prepare a local download; they do not send files automatically.</p></section>',
    '<section id="submission" class="submission-drop"><h2>Submission</h2>'
    '<p>Prepare one completed notebook or short document containing a token sequence, '
    'two feed rankings and the corrected vote claim. Use invented or anonymous data only.</p>'
    + submission_form(10) + '</section>'
)
change(
    "data/week1011/w11_lab.html",
    '<section id="submission"><h2>Submission</h2><p>A notebook with the program, three input/output tests, one before/after code change and an informative commit-message example. No account is required and the submission preparation area does not send files automatically.</p></section>',
    '<section id="submission" class="submission-drop"><h2>Submission</h2>'
    '<p>Prepare a notebook with the program, three input/output tests, one before/after '
    'code change and an informative commit-message example. If you used GitHub, '
    'include the repository URL in a text file. Do not include secrets or personal data.</p>'
    + submission_form(11) + '</section>'
)
change(
    "data/week1011/w11_lab.html",
    '<p>Open the <a href="/guides/github-ai/">account-free Git simulation</a>. Edit the miniature program, test it, then commit a meaningful version such as <code>Add missing-sensor warning</code>. Do not create an account unless you want to continue with real GitHub later.</p>',
    '<p>Use the <a href="/guides/github-ai/">real GitHub and Codespaces tutorial</a>: '
    'create your own repository, edit the program, run the tests, inspect the diff, '
    'commit with a meaningful message such as <code>Add missing-sensor warning</code>, '
    'and push to <code>main</code>. GitHub requires a personal account. '
    'If you cannot register or use Codespaces, complete the same edits locally '
    'or in the prepared notebook, and save the code plus your proposed commit message.</p>'
)
change(
    "data/week1011/w11_course.html",
    '<p>Practise a version history without registration in the <a href="/guides/github-ai/">Git, GitHub &amp; AI Editing guide</a>. A real GitHub account is optional.</p>',
    '<p>Follow the <a href="/guides/github-ai/">Git, GitHub &amp; AI Editing guide</a> '
    'to create a real repository and practise reviewing changes, committing and pushing '
    'to <code>main</code>. This requires a GitHub account; students unable to register '
    'can demonstrate the same change-review steps with a local notebook and a written '
    'commit message.</p>'
)
change(
    "w2/advanced/print.html",
    'We work with the same eight synthetic outdoor-activity examples as in Week 2 Course and Laboratory.',
    'For these optional proof exercises we deliberately use a separate complete eight-row '
    'truth table, not the twelve-row activity diary used in the Week 2 Course and Laboratory. '
    'Do not transfer the entropy or information-gain values between the two datasets.'
)
change(
    "w2/advanced/week-02-id3.tex",
    'We use the Week 2 synthetic outdoor-activity example.',
    'For these optional proof exercises we use a separate, complete eight-row truth table, '
    'not the twelve-row activity diary in the Week 2 Course and Laboratory.'
)
change(
    "data/week23/w2_advanced.html",
    '<p>These exercises are optional. They extend Week 2 from a useful classroom classifier to a more precise understanding of <em>why</em> ID3 chooses an attribute and why that choice is not a universal guarantee of the smallest tree.</p>',
    '<p>These exercises are optional. They extend Week 2 from a useful classroom classifier to a more precise understanding of <em>why</em> ID3 chooses an attribute and why that choice is not a universal guarantee of the smallest tree.</p>'
    '<p class="understated"><strong>Dataset distinction:</strong> the printable worked sheet uses '
    'a separate eight-case truth table for a compact proof exercise; the main Course '
    'and Laboratory share a twelve-record activity diary. Their information-gain '
    'numbers are not interchangeable.</p>'
)
