# Palynodata in situ pass, 27 November 2026

Source: [Palynodata](https://paleobotany.ru/palynodata/taxa), a bibliographic and taxonomic database of fossil palynomorphs, served online by the Laboratory of Paleobotany, A.A. Borissiak Paleontological Institute. Thanks to its keepers for making it available.

The 283 publications Palynodata lists as in situ records were read, with the taxa named under each. They were compared with this network as it stood before the pass.

| File | Contents |
|---|---|
| `palynodata_pubs_genera.tsv` | One row per publication: Palynodata id(s), citation as listed, record count, genera named (prefix `P:` = listed under Plants; `A:`/`C:`/`D:`/`F:`/`S:` = acritarch, chitinozoan, dinoflagellate, fungal, scolecodont). Catalogues over 400 records are marked `BIG` and were not used. |
| `sd_node_genera.csv`, `sd_text_words.csv`, `sd_insitu_pairs.csv` | The network before this pass: node genera, every capitalized word on the page, and spore-to-parent links. |
| `palynodata_compare.R` | Builds `candidate_links_all.csv` from the files above: `Rscript data/palynodata/palynodata_compare.R` (run from the repo root). |
| `candidate_links_all.csv` | Every spore x organ pairing per publication, with whether each genus and link was already in the network. `pairing_needs_check = TRUE` where a paper names several organs and several spores. |
| `added_links_2026-11-27.csv`, `added_nodes_2026-11-27.csv` | What was actually added to `index.html`: 71 links and 36 genera, from papers about a single organ, hand-placed in their interval and group. Each cites the original paper; status "Palynodata listing, original not yet read". |
| `references_2026-11-27.csv` | Citation keys used on the page, with the Palynodata publication id. |

Not added: pairings from papers on several organs (to be hand-checked), the 28 publications whose lists did not load, Spermatites (a seed genus), Milleria (a synonym of Rellimia) and an Alisporites–Pinus comparison.
