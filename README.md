# سي إقرأ — الشروحات الإضافية

موقع ثابت (GitHub Pages) فيه ٤ أقسام × ٧ دروس. الرابط بعد التفعيل:
https://abdallameen.github.io/ciqraa-desc/

## التفعيل
Settings ← Pages ← Source: `Deploy from a branch` ← Branch: `main` / `(root)`.

## إضافة الشروحات
عدّل ملف `assets/media.js` فقط: ضع رابط كل شرح (يوتيوب / درايف / فيميو / ملف mp3-mp4).

## الأكواد (QR)
مولّدة في مجلد `qr/` باسم `القسم-رقم.png` (مثال: `audio-1.png`).
لو غيّرت رابط الموقع: عدّل `BASE_URL` في `tools/build.py` ثم شغّل:

    pip install qrcode pillow
    python3 tools/build.py
