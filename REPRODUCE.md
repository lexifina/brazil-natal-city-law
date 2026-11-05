# How this repository was made (Natal)

This file is written by the build on 2026-11-05, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Câmara Municipal do Natal, SAPL: Lei Orgânica do Município, texto atualizado (PDF) | <https://sapl.natal.rn.leg.br/norma/193> | 2026-11-05 | Text: Câmara Municipal do Natal, SAPL, Lei Orgânica do Município do Natal (texto atualizado), sapl.natal.rn.leg.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not protected by copyright. Non-official text: only the official gazette is authoritative. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `lei-organica` | Lei Orgânica do Município do Natal | 1 | 2020-12-23 to 2020-12-23 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futuro`: laws not yet in force on 2026-11-05.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 1 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/Fortaleza) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: The Lei Orgânica and its amendments are promulgated by the Mesa da Câmara and take effect on publication; this record holds only the updated text, dated by the latest amendment it cites. https://sapl.natal.rn.leg.br/norma/193

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `b87eebd2f257278426f9ba01438bd5db456546b43480b7352a85b853855bccc8` (177515 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `35388bee5aa05369f7da68f5a8fa015ea8d442b8`, `check.py` `5d719354ea4c62d240c93d2cae446307d81d9e81`, `on.py` `aff48cf1b68d50c7ba8f399ca32261871c301824`.
- Python 3.14.4; git version 2.53.0.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- The Lei Orgânica is given only as the Câmara's updated edition in its SAPL, credited to the Câmara as the oldest version available and dated by the latest date among the amendments its notes cite. The text as promulgated on 3 April 1990 and the wordings the amendments replaced are not reconstructed.
- Only the Lei Orgânica is taken from the PDF: from "PREÂMBULO" to the "Natal, 3 de abril de 1990." that closes the transitional provisions (the signatures after the main text stay with its last article); the cover, the table of contents, page numbers, the signatures at the end and the texts of the amendments and court decisions printed after it are left out, as are the notes in parentheses ("(Redação conferida pela Emenda à Lei Orgânica nº ...)", "(Incluído pela ...)", "(*Invalidado pela ADI ...)" and other notes starting with "*"). Provisions a court invalidated stay in the text as the edition prints them.
- Lines are joined into paragraphs: a new paragraph starts at a provision label, a heading line, or after a line ending in ".", ";" or ":". One file per Art.; headings stand above the first article under them; the Ato das Disposições Transitórias, numbered from 1 again, is adt-*.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal text or dates: every word comes from the Câmara's PDF.
