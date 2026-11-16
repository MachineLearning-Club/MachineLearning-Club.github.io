"""One source of truth for the public site's attribution and navigation footer.

Independent club ownership belongs to the PFA, not the partner schools.
"""
from html import escape

PERSONAL_URL = "https://dragosandreibobu.github.io/"
AUTHOR = "Dragoș-Andrei Bobu"
LEGAL_OPERATOR = "BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ"
ORG_URL = "https://github.com/MachineLearning-Club"
CODE_URL = "https://github.com/MachineLearning-Club/MachineLearning-Club.github.io"
SCHOOL_URL = "https://sevenhills.ro/"
PROFILE_URL = "https://github.com/dragosandreibobu"

def link(url, label, *, external=True):
    attributes=' target="_blank" rel="noopener noreferrer"' if external else ''
    return '<a href="'+escape(url,quote=True)+'"'+attributes+'>'+escape(label)+'</a>'

def site_footer():
    return (
        '<footer class="site mlclub-footer" aria-label="Machine Learning Club footer">'
        '<div class="mlclub-footer-grid">'
        '<div class="mlclub-footer-about">'
        '<a class="mlclub-footer-brand" href="/">Machine Learning Club</a>'
        '<p>Independent educational project created by '
        + link(PERSONAL_URL,AUTHOR)
        + '.</p>'
        '</div>'
        '<nav class="mlclub-footer-links" aria-label="Explore the club">'
        '<h2>Explore</h2><ul>'
        '<li>'+link('/','All lessons',external=False)+'</li>'
        '<li>'+link('/timetable/','Timetable',external=False)+'</li>'
        '<li>'+link('/resources/','Bibliography',external=False)+'</li>'
        '<li>'+link('/quiz/','Weekly quizzes',external=False)+'</li>'
        '</ul></nav>'
        '<nav class="mlclub-footer-links" aria-label="Project and partners">'
        '<h2>Project &amp; partners</h2><ul>'
        '<li>'+link(ORG_URL,'GitHub organisation')+'</li>'
        '<li>'+link(CODE_URL,'Website source')+'</li>'
        '<li>'+link(SCHOOL_URL,'Seven Hills International School')+'</li>'
        '</ul></nav>'
        '</div>'
        '<div class="mlclub-footer-bottom">'
        '<p>© 2026 '+escape(LEGAL_OPERATOR)+'</p>'
        '<p>'+link(PERSONAL_URL,'Personal website')
        +' <span aria-hidden="true">·</span> '+link(PROFILE_URL,'GitHub profile')+'</p>'
        '</div></footer>'
    )
