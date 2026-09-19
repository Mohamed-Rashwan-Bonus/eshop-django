"""Generate one Arabic PDF per team-member guide (docs/0*.md -> docs/pdf/*.pdf).

Usage:  python docs/make_pdfs.py
Needs:  pip install fpdf2 arabic-reshaper python-bidi
"""
import re
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
FONTS = BASE / 'fonts'
PDFS = BASE / 'pdf'
FONTS.mkdir(exist_ok=True)
PDFS.mkdir(exist_ok=True)


def dl(url, dest):
    if dest.exists():
        return
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    print('downloaded', dest.name, dest.stat().st_size, 'bytes')


dl('https://fonts.gstatic.com/s/amiri/v30/J7aRnpd8CGxBHqUp.ttf', FONTS / 'Amiri-Regular.ttf')
dl('https://fonts.gstatic.com/s/amiri/v30/J7acnpd8CGxBHp2VkZY4.ttf', FONTS / 'Amiri-Bold.ttf')

import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF, XPos, YPos

AR_RE = re.compile(r'[\u0600-\u06FF]')
SANITIZE = {'→': '->', '←': '<-', '•': '-', '…': '...', '✓': '[ok]', '✗': '[x]'}


def ar(t):
    for k, v in SANITIZE.items():
        t = t.replace(k, v)
    t = t.replace('**', '').replace('`', '')
    if AR_RE.search(t):
        return get_display(arabic_reshaper.reshape(t))
    return t


def mc(pdf, h, text, align='R', **kw):
    """multi_cell that always restarts at the left margin (w=0 needs this)."""
    pdf.multi_cell(0, h, text, align=align, new_x=XPos.LMARGIN, new_y=YPos.NEXT, **kw)


class Guide(FPDF):
    def __init__(self, subtitle):
        super().__init__()
        self.subtitle = subtitle

    def footer(self):
        self.set_y(-15)
        self.set_font('Amiri', '', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, ar(f'{self.subtitle} - صفحة {self.page_no()}'), align='C')


INDIGO = (55, 48, 163)


def build(md_path, pdf_path):
    lines = md_path.read_text(encoding='utf-8').splitlines()
    title = lines[0].lstrip('# ').strip()
    pdf = Guide(title)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_font('Amiri', '', str(FONTS / 'Amiri-Regular.ttf'))
    pdf.add_font('Amiri', 'B', str(FONTS / 'Amiri-Bold.ttf'))
    pdf.add_page()
    pdf.set_font('Amiri', 'B', 24)
    pdf.set_text_color(*INDIGO)
    mc(pdf, 12, ar(title), align='C')
    pdf.set_draw_color(*INDIGO)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(8)

    in_code, buf = False, []

    def flush_code():
        if not buf:
            return
        pdf.set_fill_color(243, 244, 246)
        pdf.set_text_color(30, 30, 30)
        for bl in buf:
            if AR_RE.search(bl):
                pdf.set_font('Amiri', '', 10)
                mc(pdf, 6, ar(bl), align='L', fill=True)
            else:
                pdf.set_font('Courier', '', 9)
                mc(pdf, 5.5, bl, align='L', fill=True)
        pdf.ln(2)
        buf.clear()

    for raw in lines[1:]:
        s = raw.rstrip()
        if s.strip().startswith('```'):
            if in_code:
                flush_code()
            in_code = not in_code
            continue
        if in_code:
            buf.append(s)
            continue
        if not s.strip():
            pdf.ln(3)
            continue
        if s.strip() == '---':
            pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
            pdf.ln(4)
            continue
        if s.startswith('## '):
            pdf.set_font('Amiri', 'B', 15)
            pdf.set_text_color(*INDIGO)
            mc(pdf, 9, ar(s[3:].strip()))
            pdf.ln(1)
            continue
        if s.startswith('# '):
            continue
        if s.startswith('### '):
            pdf.set_font('Amiri', 'B', 12)
            pdf.set_text_color(30, 30, 30)
            mc(pdf, 8, ar(s[4:].strip()))
            continue
        if s.lstrip().startswith('- '):
            pdf.set_font('Amiri', '', 11)
            pdf.set_text_color(20, 20, 20)
            mc(pdf, 7, ar('- ' + s.lstrip()[2:].strip()))
            continue
        if s.lstrip().startswith('> '):
            pdf.set_font('Amiri', '', 11)
            pdf.set_text_color(80, 80, 80)
            mc(pdf, 7, ar(s.lstrip()[2:].strip()))
            continue
        pdf.set_font('Amiri', '', 11)
        pdf.set_text_color(20, 20, 20)
        mc(pdf, 7, ar(s.strip()))
    if in_code:
        flush_code()
    pdf.output(str(pdf_path))
    print('wrote', pdf_path.name, pdf.pages_count, 'pages')


for md in sorted(BASE.glob('[01]*.md')):
    build(md, PDFS / (md.stem + '.pdf'))
print('DONE')
