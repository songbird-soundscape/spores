# Sporae Dispersae

An interactive network linking dispersed fossil spores and pollen to the plant organs they were found in and the whole plants those organs belong to, from the Silurian to the Cenozoic, with the history of when each link was made (1780 to now).

**Live page:** https://songbird-soundscape.github.io/spores/

## What's here

| Path | Contents |
|---|---|
| `index.html` | The page (self-contained apart from the data files below) |
| `families_tree.json`, `ptt_tree.json` | Plant family and lineage trees |
| `literature_penn.json` | Pennsylvanian literature: sources, genera and plants (partly OCR-transcribed; check against the originals before citing) |
| `modern_referents.json` | Modern relatives used for comparison |
| `paleopos/`, `paleocoast/` | Site palaeopositions and palaeocoastlines, 5–535 Ma in 10 Myr steps |
| `spore_photos/` | One photomicrograph per genus |
| `occurrences.json` | Fossil occurrence records behind each taxon's "where it has been found" map, from the Paleobiology Database |
| `data/pbdb_occurrences.csv` | The same records as a table, one row per occurrence |
| `data/pbdb_query_log.csv` | One row per genus: records returned, records kept, and any note from PBDB |
| `data/genera_by_interval.csv` | The dispersed spore and pollen genera on each interval's page |
| `R/rebuild_occurrences.R` | Rebuilds the three files above: `Rscript R/rebuild_occurrences.R` |

## Occurrence data

Downloaded from the [Paleobiology Database](https://paleobiodb.org) on 24 November 2026 with `R/rebuild_occurrences.R`: 44,021 occurrences for 435 of 503 genera. Only records identified under each genus's own name are kept, because PBDB's synonym handling can pull in unrelated taxa (for example, the pollen genus *Polyporina* brought in the bryozoan *Polypora*). Palaeocoordinates are PBDB's (GPlates). PBDB data are CC BY 4.0.

## Day and night

The page switches itself to the night theme about 30 minutes before local sunset and back to day at sunrise. Sunset is worked out from a rough position guessed from your time zone, or from your own position if you click "Use my location for sunset" (kept only in your browser). The button in the corner switches between auto, day and night.

## Images

Photomicrographs come from published sources and may be under copyright. This is a freely distributed educational resource, made to encourage collaboration among people who study spores and plants. If an image is yours and you would like it credited differently or removed, please open an issue and it will be done.

## Contributing

Know a state survey bulletin, thesis, guidebook or report with spore or plant data? Please [open an issue](https://github.com/songbird-soundscape/spores/issues/new) with the citation.
