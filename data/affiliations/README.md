# First-author affiliations (Link colours: Author affiliation)

- `cites.json`: every paper cited first by a network link (built from `index.html`), with the links it supports.
- `author_affiliations.csv`: institution of each first author over a span of years. `source` says where each row came from. Most are **background knowledge (verify)**; a few were matched in OpenAlex (`oa.json`, a search of all 342 papers that matched only 13 of them).
- `affil.R`: joins the two and writes `affiliations_by_cite.csv`. As of 27 Nov 2026, 152 of 342 papers (506 of 797 links) have an affiliation; the rest show grey on the page.

To correct or add an affiliation, edit `author_affiliations.csv`, run `Rscript affil.R`, and rebuild the `AFF` constant in `index.html`.
