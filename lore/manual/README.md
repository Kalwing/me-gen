# Manual lore

Hand-corrected lore pages sourced from YouTube video transcripts (auto-generated
captions from `ddl/*.txt`). Each file has been de-ASR'd, re-punctuated, stripped of
channel boilerplate, and reflowed into prose. Lore claims are preserved as the
source stated them; where a transcript contradicts established canon the wording is
kept and flagged with an inline `<!-- transcript unclear: ... -->` comment rather
than "corrected". The raw transcripts stay in `ddl/` as the source of record.

`scripts/page-summarizer` and the rest of the pipeline treat these exactly like
scraped wiki pages.

## Frontmatter shape

```yaml
title:      Clean human title (not the raw filename)
url:        YouTube URL if recoverable from the filename, else ""
game:       Mass Effect | Mass Effect 2 | Mass Effect 3 | Mass Effect (series)
type:       character | faction | location | tech | species | timeline | lore
characters: [named individuals actually discussed]
source:     youtube-transcript
corrected:  2026-08-28
```

Sources larger than ~10 kB are split at topic boundaries into `<slug>-01.md`,
`<slug>-02.md`, …; each part carries full frontmatter (`title` + ` (Part N)`) and
opens with a `**Summary:**` paragraph so it stands alone.
