"""Independent letters-and-digits check of the Lei Orgânica against the PDF, read with a second PDF reader (poppler's
pdftotext, not the builder's PyMuPDF) and none of the builder's code.

    python -X utf8 check_letters.py [part.json ...]

The pdftotext text from the second "PREÂMBULO" (the first is in the table of contents) to the last "Natal, 3 de abril
de 1990." before the first "(Publicad" note, with lines that hold only a page number and every note in parentheses
starting with "*", "Redação", "Incluíd-", "Revogad-", "Suprimid-", "Artigo inclu-", "Inciso suprim-", "Parágrafo
inclu-" or "Invalidad-" removed, reduced to letters and digits, must equal the version's unit files reduced the same
way, each unit found at its place in document order.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPENERS = ('*', 'Redação', 'Redacao', 'Incluíd', 'Incluid', 'Revogad', 'Suprimid', 'Artigo inclu', 'Inciso suprim',
           'Parágrafo inclu', 'Paragrafo inclu', 'Invalidad')


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def strip_notes(t):
    out, changed = t, True
    while changed:
        changed = False
        for m in list(re.finditer(r'\(([^()]*)\)', out))[::-1]:
            inner = m.group(1).lstrip()
            if any(inner.lower().startswith(o.lower()) for o in OPENERS):
                out = out[:m.start()] + ' ' + out[m.end():]
                changed = True
    return out


def pdf_text(path):
    t = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(path), '-'], capture_output=True, check=True).stdout.decode()
    t = re.sub(r'(?m)^\s*\d{1,3}\s*$', ' ', t.replace('\f', '\n'))
    a = [m.start() for m in re.finditer(r'PREÂMBULO', t)][1]
    pub = t.index('(Publicad', a)
    b = t.rindex('Natal, 3 de abril de 1990.', a, pub) + len('Natal, 3 de abril de 1990.')
    return strip_notes(t[a:b])


def main(paths):
    bad = total = 0
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            for v in a['versions']:
                path = HERE / '.cache' / 'sapl' / 'raw' / hashlib.sha256(v['source_url'].encode()).hexdigest()
                assert hashlib.sha256(path.read_bytes()).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                src = ld(pdf_text(path))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                total += 1
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
