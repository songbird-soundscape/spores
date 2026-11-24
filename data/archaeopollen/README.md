# Archaeopollen: extant angiosperm taxa in archaeological pollen records (North America pilot)

This folder holds a hand-compiled table of **extant flowering-plant taxa** (species, genus, family or pollen type) whose pollen has been reported from **archaeological contexts** in North America: coprolites, midden fill, house floors, metate/mano surfaces, vessel interiors, hearths, burials and site columns. It is a pilot that should later be extended worldwide.

Compiled 2026-11-24. **Every record needs hand-checking against the cited page or table before you use it in analysis.**

## Files

| File | What it is |
|---|---|
| `records_north_america.csv` | One row per taxon x site x context x source. 268 records. |
| `sources.csv` | Every source consulted (28), how it was accessed, and how many records came from it (`records_taken`, 0 if none). |
| `families_summary.csv` | Made by `R/archaeopollen_tidy.R`: family, n_records, n_sites, n_genera, genera, earliest_bp, latest_bp, contexts, n_high_conf. |
| `archaeopollen.json` | Made by `R/archaeopollen_tidy.R`: records grouped by family with summary fields, for a web page. |
| `staging/sources.psv`, `staging/sites.psv`, `staging/records.psv` | The hand-entered master tables (pipe-separated). **Edit these, not the CSV.** |

Scripts (run them from the `spores/` folder):

```
Rscript R/archaeopollen_build.R   # staging/*.psv -> records_north_america.csv + sources.csv
Rscript R/archaeopollen_tidy.R    # checks fields, normalises families -> families_summary.csv + archaeopollen.json
```

`archaeopollen_build.R` checks field counts and that every record points to a known source and site. A site's default dates apply unless the record has its own. `archaeopollen_tidy.R` checks required fields and the allowed values for `id_level`, `context` and `confidence`. It also checks that ages are numeric and that age_min <= age_max, maps old family names to APG IV (for example Compositae to Asteraceae, Chenopodiaceae to Amaranthaceae, Hydrophyllaceae to Boraginaceae, Agavaceae to Asparagaceae), and fixes the family for genera whose placement changed (Cleome to Cleomaceae, Celtis to Cannabaceae, Acer to Sapindaceae, Sarcobatus to Sarcobataceae). It stops if anything fails.

## Column notes

- `taxon_as_reported`: exactly as written in the source, including spelling quirks ("Soledago", "Graminae", "Ligulafloreae"). Common names are kept where the source gave only a common name ("sotol", "cenizo"). In those rows the inferred genus is in `genus` and the inference is stated in `notes`.
- `id_level`: `species`, `genus`, `family`, or `pollen_type`. Morphological groups are `pollen_type`: Cheno-Am, high- and low-spine Asteraceae, Liguliflorae, Platyopuntia, Liliaceae s.l., "Long spine type cf. Helianthus".
- `family`: APG IV. **"Liliaceae s.l."** is kept for the old broad "Liliaceae" pollen category, which can't be assigned to one APG IV family (it could be Asparagaceae, Liliaceae, Commelinaceae and others). The JSON flags it with `family_uncertain`.
- `latitude`/`longitude`: left **blank throughout**. None of the sources read gave coordinates, and the brief allowed only source-given or published coordinates. Adding them from site files or Smithsonian trinomial records is a next step. Note that many sites have restricted locations.
- `age_min_bp`/`age_max_bp`: the basis differs between rows, so read `age_basis`. Most sources give calendar AD/BC ranges, which were converted with BP = 1950 - AD, or 1950 + BC with no year-zero correction. Baker Cave uses a radiocarbon date (1090 +/- 100 RCYBP, 1-sigma range). Hinds Cave Lens 13 uses calibrated BP as given by Texas Beyond History. Varga uses "B.P." as reported, with the basis not stated. **Don't treat these as one calibrated timescale.**
- `context`: hearth, pit, floor, grinding_stone, vessel, coprolite, calculus, burial, midden, other. `other` covers site stratigraphic columns, pooled sediment samples (Antelope House, Dairy Site), and field or alluvial sediments (Cienega Creek, Marana).
- `interpretation`: the author's own wording, shortened. "not interpreted" means the author tabulated the taxon without comment. "not identified as economic" (Frightful Cave) means Bryant did not list it among the economic types.
- `confidence`: **high** means I read the statement in the full text of the source cited, via the PDF or HTML text. **medium** means it came from an abstract, a secondary synthesis citing the primary study, a machine-summarised full text (Pucu et al. 2020; Reinhard & Bryant 2008), or a taxon read from a garbled OCR figure that the text supports. **low** means it needs checking: OCR-only taxon names, ambiguous column placement, or statements that may not mean pollen.

## Method

1. Web searches (WebSearch tool) for open full texts, followed by direct PDF download and `pdftotext -layout` where hosts allowed it. Where curl was blocked, I used the WebFetch tool's text summary.
2. I extracted taxa only from tables and statements in the sources. Nothing came from memory. Where a source cites another study (for example Sobolik 1988 summarising Williams-Dean 1978), the row is attributed to the source I actually read, and the primary study is named in `notes`. Those rows are `medium`.
3. Only angiosperms. Pinus, Juniperus, Abies, Picea, Ephedra, ferns and fungi (for example Ustilago maydis in Pucu et al. 2020) were skipped, even when they were reported and interpreted.
4. Granularity: one row per taxon per site per context per source. At Grasshopper Pueblo, floor, vessel and metate samples are separate rows, and the rooms and samples are given in `notes`. Percentages and concentrations are summarised in `notes` but not systematically transcribed.

### Search terms used (WebSearch)

- coprolite pollen analysis Hinds Cave Lower Pecos taxa Opuntia Agave Allium
- Ancestral Pueblo coprolites pollen concentration Cleome Zea Cucurbita Reinhard Antelope House
- pollen wash metate mano pollen analysis Zea Cheno-Am Cleome archaeological site report pdf
- site:scholarworks.sfasu.edu pollen analysis coprolites Lower Pecos
- Pohl 2007 microfossil evidence pre-Columbian maize dispersals San Andres Tabasco pollen
- npshistory.com pollen analysis Mesa Verde / Chaco / Walnut Canyon; npshistory Antelope House coprolites pollen
- digitalcommons.unl.edu Reinhard coprolite pollen Salmon Ruin
- coprolites Great Basin dry cave Lovelock / Hogup / Danger Cave pollen Typha
- Salts Cave Mammoth Cave paleofeces pollen Bryant Schoenwetter
- ethnobiology.org JoE pdf pollen coprolites / metate / pollen wash
- texasbeyondhistory pollen analysis results; Bulletin of the Texas Archeological Society Bryant 1975 Coahuila; Sobolik Baker Cave
- Hohokam pollen analysis Agave Zea Cheno-Am Cylindropuntia; open.uapress.arizona.edu anthropological papers pollen
- Ontario Iroquoian village pollen Zea; dental calculus pollen North America; Guila Naquitz pollen; coprolites pollen Mexico Tehuacan
- pollen analysis Kentucky / Tennessee / Illinois rockshelter Zea Cucurbita Chenopodium Iva

Most useful open hosts: ethnobiology.org (Journal of Ethnobiology back issues), texashistory.unt.edu (Bulletin of the Texas Archeological Society), open.uapress.arizona.edu (Anthropological Papers of the University of Arizona), npshistory.com, digitalassets.lib.berkeley.edu (Kroeber Anthropological Society Papers), in.nau.edu (NAU archaeology reports). tDAR (PaleoResearch Institute reports by Cummings and others) returns abstracts only without a login. PMC, Europe PMC, UNL DigitalCommons, CORE and Wright State CORE Scholar blocked scripted access during this session.

## Coverage

- **268 records, 26 sites, 42 families, 18 sources with records** (28 consulted).
- Most-represented families: Asteraceae (46 records), Poaceae (36, including Zea at 11 sites), Amaranthaceae (16, mostly Cheno-Am), Cactaceae (16), Asparagaceae (15: Agave, Dasylirion, Yucca, Nolina), Typhaceae (12), Fabaceae (11), Fagaceae (9), Brassicaceae (8), Salicaceae (8).
- Regions: US Southwest (Ancestral Puebloan: Antelope House, Inscription House, Hoy House, Glen Canyon, Salmon Ruin, Broken K; Mogollon/Mimbres: Grasshopper, NAN Ranch; Hohokam: Dairy Site, Marana, Cienega Creek); Texas Trans-Pecos and Lower Pecos (Caldwell Shelter 1, Caldwell Cave, Granado, Baker, Hinds, Conejo, Parida, Varga); Great Basin and California deserts (Lovelock, Danger, Bighorn, La Quinta); Mexico (Frightful Cave in Coahuila; Cueva de los Muertos Chiquitos in Durango); Eastern Woodlands (Mammoth Cave, 2 secondary rows only).
- Contexts: coprolite 161, other (columns/pooled sediments) 33, floor 19, midden 19, vessel 19, grinding_stone 13, burial 3, hearth 1. **No dental-calculus records:** the two calculus studies found (Paquime; Central Plains) do not say in their abstracts whether the microfossils were pollen.

## Gaps (priorities for the next pass)

1. **Reinhard et al. 2006** (Palaeo3 237:92-109; Salmon Ruin and Antelope House coprolite pollen concentrations). Only the abstract was reachable. This is the key Ancestral Puebloan dataset. Also Williams-Dean & Bryant 1975 (Antelope House, Kiva 41), Scott 1979 (Hoy House), Martin & Sharrock 1964 (full tables), Bryant 1974 (Conejo Shelter, Am. Antiquity 39), Williams-Dean 1978 (Hinds Cave dissertation), Riskind 1970 (Parida Cave), Holloway 1983/1985 (Caldwell), Murry 1980 (Granado), Hill & Hevly 1968 (Broken K).
2. **Eastern Woodlands**: Bryant 1974 and Schoenwetter 1974 (Salts and Mammoth Cave paleofeces, in Watson ed. 1974), Gremillion & Sobolik 1996, Ozark bluff shelters, and Cummings/PaleoResearch reports on tDAR. Nearly empty now.
3. **Canada**: no records. Candidates are Iroquoian village and field pollen (Zea, Cucurbita; for example the Palynology 31 paper on cultigen pollen in Iroquoian fields) and Northwest Coast middens.
4. **Mexico** beyond the two caves: Guila Naquitz (Schoenwetter & Smith 1986), Tehuacan, Oaxaca and Basin of Mexico sites, and Maya-area sites within Mexico (San Andres, Tabasco: Pope et al. 2001, Pohl et al. 2007; PMC was blocked).
5. **Pollen washes of ground stone** are under-represented (only Grasshopper). The CRM literature (Cummings, Gish, Holloway, Smith, Geib & Smith 2008) is large but mostly behind tDAR logins.
6. Site coordinates, as noted above.

## Known caveats

- **Pollen washes versus background rain.** Metate, vessel and floor samples collect modern and ancient ambient pollen as well as residue from use. Bohrer (1982) judged "spectral distortion" against floor and trench controls with binomial confidence limits. Fish et al. (1992) and Fall et al. (1981) read cultural signal from feature-to-feature patterns. A taxon in a wash sample is **not** evidence of processing unless the author says so. Use `interpretation`.
- **Coprolite pollen** mixes deliberate ingestion with accidental ingestion through drinking water, dust on food and inhaled pollen. Authors use different thresholds: about 10% for insect-pollinated economic types and about 40% for "special economic" wind-pollinated types (Bryant 1975); more than 100,000 grains per gram for recent intentional ingestion (Sobolik 1988a; Reinhard et al. 1991); and percentages above about 4% for entomophilous types. Dean (1993, Journal of Ethnobiology 13) criticises the concentration threshold. Pollen can persist in the gut for weeks, so a coprolite spectrum is not one meal.
- **Cheno-Am** combines Chenopodiaceae (now Amaranthaceae) and Amaranthus. It is a pollen type, not a genus, and is usually an indicator of disturbance and fields, not proof of food. Treat Cheno-Am "food" rows with care unless seeds were found too (as at Baker Cave and Lovelock).
- **High- and low-spine Asteraceae, and Liguliflorae**, are artificial groupings. Low-spine includes Ambrosia, Iva and Xanthium. High-spine includes Helianthus and many insect-pollinated genera.
- **Cleome**: archaeopalynologists' "Cleome" (beeweed, C. serrulata) is now *Peritoma serrulata* in Cleomaceae. The table keeps genus "Cleome" as reported.
- **"Liliaceae"** in older Southwest reports is a broad pollen category. Here it is mapped to "Liliaceae s.l.", not to a modern family.
- **Common-name rows** (sotol, cenizo, hackberry, pincushion cactus, gilia, spiderling, Arizona poppy) carry an inferred genus. "Pincushion cactus" is left at Cactaceae because it could be Mammillaria, Coryphantha or Escobaria.
- **Overlap**: "Caldwell Shelter 1" (Reinhard et al. 1991) and "Caldwell Cave" (Sobolik & Gerick 1992) are both Rustler Hills coprolite sites excavated by D. L. Hamilton, and they may be the same site. They are kept separate as named. Sobolik & Gerick's figures for Holloway's earlier Caldwell work (Ephedra 10.7%, Larrea 18.7%) differ slightly from Reinhard et al. (11%, 19%).
- **Same find, different readings**: Hevly's Sphaeralcea pollen in the Broken K infant burial is called ceremonial by Holloway & Bryant (1986) and medicinal by Reinhard et al. (1991). Sotol at Baker Cave is "doubtful" as food in Sobolik 1988b but a "probable economic type" in the Sobolik 1988a abstract. Both rows are kept.
- **OCR risk**: Bryant 1975 Figure 1 (Frightful Cave) is badly garbled in the scan. Taxon names there are `low` unless the text or the Figure 3 caption confirms them. The Grasshopper (Tables 13.3-13.4) and Reinhard 1991 tables have sparse rows. Where a value's column was assigned from text alignment, the row is `medium` and the notes say so.
- Hoy House "beans" (Sutton et al. 2010 citing Scott 1979) may not mean that Phaseolus pollen was identified. It is `low`.

## Extending to other regions

1. Add sources to `staging/sources.psv` (new `source_id`), sites to `staging/sites.psv` (new `site_key`, with region given as "State/Province, Country"), and records to `staging/records.psv`. Keep the same columns. Use `pollen_type` for morphological groups, and give the family exactly as reported, because the tidy script normalises it.
2. Extend `fam_map` and `genus_family` in `R/archaeopollen_tidy.R` for regional synonyms (for example Palmae, Guttiferae, Bombacaceae). The tidy script prints every family it changes.
3. Use a record_id prefix per region (the build script uses `NA-AP-`; you could use `EU-AP-`, `SA-AP-` and so on, or one global sequence). Then rename the output file or concatenate regional CSVs before running the tidy script, which takes an input path as its first argument.
4. For calibrated comparisons, add `age_min_cal_bp`/`age_max_cal_bp` columns, filled from the original radiocarbon determinations with IntCal20/SHCal20 (for example with the R package `rcarbon`), rather than reusing the mixed `age_*_bp` fields.
5. Good starting syntheses for other regions: Bryant & Holloway (eds.) 1985 *Pollen Records of Late-Quaternary North American Sediments*; Holloway & Bryant 1986; Reinhard & Bryant 1992 (coprolite review); Sutton et al. 2010 *Paleonutrition* (open access); and the Old World archaeopalynology literature, such as burial pollen at Shanidar, which Holloway & Bryant also discuss.
