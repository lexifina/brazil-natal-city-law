# Natal (city): law history in git

The municipal law of the Município do Natal, the city of Natal (Rio Grande do Norte) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `lei-organica/` | Lei Orgânica do Município do Natal (1990), as updated by the Câmara | 1 |

**Lei Orgânica only, for now.** The text is given **only as the Câmara's updated edition**, credited to the Câmara as the oldest version available. Federal law is in [brazil-law](https://github.com/lexifina/brazil-law).

## Source

[Câmara Municipal do Natal, SAPL](https://sapl.natal.rn.leg.br/norma/193), published by the Câmara Municipal do Natal. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

The one version is dated by the latest date among the amendments the edition's notes cite (Emenda of 23 December 2020; the PDF was last saved on 28 April 2022). Commits are at noon in Natal.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

Only the Lei Orgânica is taken from the PDF (from the preamble to the end of the Ato das Disposições Transitórias); the cover, table of contents, page numbers, the signatures at the end and the amendments and court decisions printed after the text are left out. The text layer is read with PyMuPDF line by line and lines are joined into paragraphs (a new paragraph at each provision label, heading, or after a line ending in ".", ";" or ":"). Notes in parentheses ("(Redação conferida pela Emenda à Lei Orgânica nº ...)", "(Incluído pela ...)", "(*Invalidado pela ADI ...)") are left out. One file per Art.; the transitional provisions are `adt-*`.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a history: the Lei Orgânica as promulgated on 3 April 1990 and the wordings its amendments replaced are not reconstructed. Provisions the courts invalidated stay in the text as the edition prints them (the notes saying so are left out). The edition may lag behind amendments made after its last update. The text is not the official version.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Câmara Municipal do Natal, SAPL, Câmara Municipal do Natal.
