"""Builds corpus.d/10-lei-organica.json for the Município do Natal from the Câmara Municipal's updated edition of the
Lei Orgânica in its SAPL ("lei_organica_atualizada.pdf", a PDF with a text layer; no network).

    python -X utf8 parse.py --today YYYY-MM-DD

The PDF holds the cover and table of contents (pages 1-3), the Lei Orgânica with its Ato das Disposições Transitórias
(pages 4-48; the main text and the transitional provisions each end "Natal, 3 de abril de 1990."), then the signatures and the texts of the amendments and court
decisions. Only the Lei Orgânica is taken: from "PREÂMBULO" on page 4 to the last "Natal, 3 de abril de 1990." (the end of the transitional provisions). It is read
with PyMuPDF line by line; each page's number (its first line) is left out, and lines are joined into paragraphs (a
new paragraph at a provision label, a heading line, or after a line ending in ".", ";" or ":"). The notes in
parentheses that start with "*" or "Redação", "Incluído", "Revogado", "Suprimido", "Artigo incluído", "Inciso
suprimido", "Parágrafo incluído" or "Invalidad-" are left out of the text; the latest date the amendment notes cite
dates the version.
"""
import argparse, re, sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import units_of, write_part, sha, norm  # noqa: E402

BASE = 'https://sapl.natal.rn.leg.br'
PDF_URL = 'http://sapl.natal.rn.leg.br/media/sapl/public/normajuridica/1990/193/lei_organica_atualizada.pdf'
PAGE_URL = BASE + '/norma/193'
PDF = HERE / '.cache' / 'sapl' / 'raw' / sha(PDF_URL.encode())
NOTE = re.compile(r'\(\s*(?:\*|Reda[çc][ãa]o|Inclu[íi]d|Revogad|Suprimid|Artigo\s+inclu|Inciso\s+suprim|'
                  r'Par[áa]grafo\s+inclu|Invalidad)[^()]*\)', re.I)
END = 'Natal, 3 de abril de 1990.'
STARTS = re.compile(r'^(?:Art\.|§|Par[áa]grafo|[IVXLC]+\s*[-–]|[a-z]\)|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|'
                    r'Subse[çc][ãa]o|ATO\b|PRE[ÂA]MBULO)')
HEADING = re.compile(r'^(?:T[ÍI]TULO|CAP[ÍI]TULO|SE[ÇC][ÃA]O|Se[çc][ãa]o|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O|ATO\b)')
DMY = re.compile(r'\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b')


def text_and_notes():
    raw = []
    for p in pymupdf.open(PDF):
        ls = [norm(l) for l in p.get_text().split('\n')]
        ls = [l for l in ls if l]
        if ls and re.fullmatch(r'\d{1,3}', ls[0]):
            ls = ls[1:]  # the page number
        raw += ls
    start = next(i for i, l in enumerate(raw) if l == 'PREÂMBULO' and i > 0 and not raw[i + 1].startswith('TÍTULO'))
    # "Natal, 3 de abril de 1990." closes both the main text and the Ato das Disposições Transitórias (each followed
    # by the signatures); the last one before the first publication note "(Publicada no DOE ...)" ends the Lei Orgânica.
    pub = next(i for i, l in enumerate(raw) if i > start and l.startswith('(Publicad'))
    end = max(i for i, l in enumerate(raw[:pub]) if i > start and l == END)
    paras = []
    for l in raw[start:end + 1]:
        head = HEADING.match(l) or (l == l.upper() and re.search(r'[A-ZÀ-Ý]{3}', l))
        prev = paras[-1] if paras else None
        if prev is None or STARTS.match(l) or head or re.search(r'[.;:]["”]?$', prev[1]) or prev[0]:
            paras.append([bool(head), l])
        elif prev[1].endswith('-'):
            prev[1] += l
        else:
            prev[1] += ' ' + l
    s = '\n'.join(p[1] for p in paras)
    notes = []
    while NOTE.search(s):
        notes += [re.sub(r'\s+', ' ', n) for n in NOTE.findall(s)]
        s = NOTE.sub(' ', s)
    out = [norm(l) for l in s.split('\n')]
    return [l for l in out if l and re.search(r'\w', l)], notes


def dates(s):
    return [f'{int(y):04d}-{int(m):02d}-{int(d):02d}' for d, m, y in DMY.findall(s) if 1 <= int(m) <= 12]


COUNTRY = {
    'code': 'BR-RN-NATAL', 'name': 'Natal', 'slug': 'brazil-natal-city', 'lang': 'pt', 'tz': 'America/Fortaleza',
    'future_branch': 'futuro',
    'publisher': {'name': 'Câmara Municipal do Natal', 'email': 'sapl@natal.rn.leg.br.invalid'},
    'default_in_force_rule': {
        'text': 'The Lei Orgânica and its amendments are promulgated by the Mesa da Câmara and take effect on '
                'publication; this record holds only the updated text, dated by the latest amendment it cites.',
        'source': PAGE_URL},
    'licence_note': 'Text: Câmara Municipal do Natal, SAPL, Lei Orgânica do Município do Natal (texto atualizado), '
                    'sapl.natal.rn.leg.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not '
                    'protected by copyright. Non-official text: only the official gazette is authoritative.',
}
DECISIONS = [
    'The Lei Orgânica is given only as the Câmara\'s updated edition in its SAPL, credited to the Câmara as the oldest '
    'version available and dated by the latest date among the amendments its notes cite. The text as promulgated on 3 '
    'April 1990 and the wordings the amendments replaced are not reconstructed.',
    'Only the Lei Orgânica is taken from the PDF: from "PREÂMBULO" to the "Natal, 3 de abril de 1990." that closes the '
    'transitional provisions (the signatures after the main text stay with its last article); the cover, the '
    'table of contents, page numbers, the signatures at the end and the texts of the amendments and court decisions printed after '
    'it are left out, as are the notes in parentheses ("(Redação conferida pela Emenda à Lei Orgânica nº ...)", '
    '"(Incluído pela ...)", "(*Invalidado pela ADI ...)" and other notes starting with "*"). Provisions a court '
    'invalidated stay in the text as the edition prints them.',
    'Lines are joined into paragraphs: a new paragraph starts at a provision label, a heading line, or after a line '
    'ending in ".", ";" or ":". One file per Art.; headings stand above the first article under them; the Ato das '
    'Disposições Transitórias, numbered from 1 again, is adt-*.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Câmara's PDF."]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    a = ap.parse_args()
    lines, notes = text_and_notes()
    ds = sorted(d for n in notes if 'Emenda' in n for d in dates(n) if d <= a.today)
    units = units_of([('p', l) for l in lines], title_label='Preâmbulo', adt=True)
    b = PDF.read_bytes()
    key = 'lei-organica-1990'
    laws = {key: {'label': 'Lei Orgânica do Município do Natal, de 3 de abril de 1990',
                  'title': 'Lei Orgânica do Município do Natal', 'kind': 'law', 'enacted': '1990-04-03',
                  'published': '1990-04-03', 'url': PAGE_URL, 'temporary_until': None, 'restores': None, 'note': None}}
    v = {'from': ds[-1], 'source_url': PDF_URL, 'sha256': sha(b), 'units': units,
         'note': f'Text in force as updated by the Câmara Municipal do Natal; its notes cite amendments of '
                 f'{len(set(ds))} dates, the latest {ds[-1]}.'}
    act = {'slug': 'lei-organica', 'short': 'LOM-Natal', 'title': 'Lei Orgânica do Município do Natal', 'url': PAGE_URL,
           'first_law': None, 'earlier_laws': [key], 'versions': [v]}
    c = {'country': COUNTRY,
         'sources': [{'name': 'Câmara Municipal do Natal, SAPL: Lei Orgânica do Município, texto atualizado (PDF)',
                      'url': PAGE_URL, 'retrieved': a.today, 'licence': COUNTRY['licence_note'], 'notes': '1 act.'}],
         'laws': laws, 'acts': [act], 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    print(write_part(HERE / 'corpus.d', '10-lei-organica', c), len(units), ds[-1], len(notes))


if __name__ == '__main__':
    main()
