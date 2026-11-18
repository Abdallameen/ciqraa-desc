#!/usr/bin/env python3
"""يولّد صفحات الموقع (٤ أقسام × ٧ دروس) وأكواد QR لكل صفحة.

التشغيل من جذر المستودع:
    pip install qrcode pillow
    python3 tools/build.py

لو غيّرت رابط الموقع (دومين خاص مثلًا) عدّل BASE_URL تحت ثم أعد التشغيل.
"""
import os
import html

BASE_URL = "https://abdallameen.github.io/ciqraa-desc/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECTIONS = [
    ("audio",  "شرح صوتي",            "🎧", "استمع للشرح خطوة بخطوة في أي وقت، حتى وأنت بعيد عن الشاشة."),
    ("video",  "شرح صوت وصورة",       "🎬", "شاهد الخطوات مطبّقة على الموقع بالصوت والصورة."),
    ("remote", "شرح من دورة عن بعد",  "💻", "مقاطع مسجّلة من الدورة التي أُقيمت عن بعد."),
    ("onsite", "شرح من دورة حضورية",  "🏫", "مقاطع مسجّلة من الدورة الحضورية."),
]

LESSONS = [
    "تمهيد",
    "إنشاء خطة للطالب / الطلاب",
    "الترشيح المباشر",
    "الإرسال إلى صندوق الترشيحات",
    "إنشاء استمارة الترشيح",
    "إضافة الطالب / الطلاب إلى الاستمارة",
    "إرسال الاستمارة",
]

AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"


def ar(n):
    return "".join(AR_DIGITS[int(c)] for c in str(n))


def esc(s):
    return html.escape(s, quote=True)


FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Ctext y='.9em' font-size='90'%3E📖%3C/text%3E%3C/svg%3E")


def page(title, body, depth, script=True, extra_body_attrs=""):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0B5D4B">
<title>{esc(title)}</title>
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body{extra_body_attrs}>
{body}
<footer class="foot">دليل ترشيح الطلاب — <a href="https://ciqraa.com/" rel="noopener">سي إقرأ</a></footer>
{'<script src="' + up + 'assets/media.js"></script><script src="' + up + 'assets/app.js"></script>' if script else ''}
</body>
</html>
"""


def topbar(depth, crumbs):
    up = "../" * depth
    items = [f'<a href="{up}index.html">الشروحات الإضافية</a>'] + crumbs
    return ('<header class="top"><div class="wrap"><span class="logo">📖</span>'
            '<nav class="crumbs" aria-label="مسار التنقل">' + '<span class="sep">‹</span>'.join(items) +
            '</nav></div></header>')


def build_home():
    cards = ""
    for slug, name, icon, desc in SECTIONS:
        cards += f"""
    <a class="card" href="{slug}/index.html">
      <span class="ico">{icon}</span>
      <h2>{esc(name)}</h2>
      <p>{esc(desc)}</p>
      <span class="count">{ar(len(LESSONS))} دروس</span>
    </a>"""
    body = f"""{topbar(0, [])}
<main class="wrap">
  <section class="hero">
    <p class="eyebrow">دليل ترشيح الطلاب — سي إقرأ</p>
    <h1>الشروحات الإضافية</h1>
    <p class="lead">اختر طريقة الشرح التي تناسبك، ثم تابع الدروس بالترتيب: من تمهيد إلى إرسال الاستمارة.</p>
  </section>
  <section class="grid">{cards}
  </section>
</main>"""
    write("index.html", page("الشروحات الإضافية — دليل ترشيح الطلاب | سي إقرأ", body, 0, script=False))


def build_section(slug, name, icon, desc):
    rows = ""
    for i, t in enumerate(LESSONS, 1):
        rows += f"""
      <li><a href="{i}.html"><span class="num">{ar(i)}</span><span class="t">{esc(t)}</span><span class="go">←</span></a></li>"""
    body = f"""{topbar(1, [esc(name)])}
<main class="wrap narrow">
  <section class="hero small">
    <span class="ico big">{icon}</span>
    <h1>{esc(name)}</h1>
    <p class="lead">{esc(desc)}</p>
  </section>
  <ol class="lessons">{rows}
  </ol>
  <div class="actions"><a class="btn primary" href="1.html">ابدأ من الدرس الأول ←</a></div>
</main>"""
    write(f"{slug}/index.html", page(f"{name} — الشروحات الإضافية | سي إقرأ", body, 1, script=False))


def build_lesson(slug, name, icon, i):
    title = LESSONS[i - 1]
    n = len(LESSONS)
    prev_html = (f'<a class="btn" href="{i-1}.html">→ السابق</a>' if i > 1
                 else '<span class="btn disabled" aria-disabled="true">→ السابق</span>')
    next_html = (f'<a class="btn primary" href="{i+1}.html">التالي ←</a>' if i < n
                 else '<a class="btn primary" href="index.html">قائمة الدروس ←</a>')
    pills = ""
    for k in range(1, n + 1):
        cls = "pill on" if k == i else "pill"
        cur = ' aria-current="page"' if k == i else ""
        pills += f'<a class="{cls}" href="{k}.html" title="{esc(LESSONS[k-1])}"{cur}>{ar(k)}</a>'

    others = "".join(
        f'<a class="alt" href="../{s}/{i}.html"><span>{ic}</span>{esc(nm)}</a>'
        for s, nm, ic, _ in SECTIONS if s != slug)
    body = f"""{topbar(1, [f'<a href="index.html">{esc(name)}</a>', f'الدرس {ar(i)}'])}
<main class="wrap narrow">
  <article>
    <p class="eyebrow">{icon} {esc(name)} · الدرس {ar(i)} من {ar(n)}</p>
    <h1>{ar(i)}. {esc(title)}</h1>
    <div id="player" class="player" data-section="{slug}" data-lesson="{i}"></div>
    <div class="pager">
      {prev_html}
      {next_html}
    </div>
    <div class="pills" aria-label="دروس القسم">{pills}</div>
  </article>
  <aside class="others">
    <h3>نفس الدرس بطريقة أخرى</h3>
    <div class="alts">{others}</div>
  </aside>
</main>"""
    write(f"{slug}/{i}.html", page(f"{ar(i)}. {title} — {name} | سي إقرأ", body, 1,
                                    extra_body_attrs=f' data-prev="{i-1 if i > 1 else ""}" data-next="{i+1 if i < n else ""}"'))


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_qr():
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M
    os.makedirs(os.path.join(ROOT, "qr"), exist_ok=True)
    for slug, *_ in SECTIONS:
        for i in range(1, len(LESSONS) + 1):
            url = f"{BASE_URL}{slug}/{i}.html"
            qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=12, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            qr.make_image(fill_color="#063d31", back_color="white").save(
                os.path.join(ROOT, "qr", f"{slug}-{i}.png"))


if __name__ == "__main__":
    build_home()
    for slug, name, icon, desc in SECTIONS:
        build_section(slug, name, icon, desc)
        for i in range(1, len(LESSONS) + 1):
            build_lesson(slug, name, icon, i)
    build_qr()
    print("تم: 1 رئيسية + 4 فهارس + 28 درسًا + 28 باركود")
