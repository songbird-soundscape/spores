# archaeopollen_tidy.R
# Reads data/archaeopollen/records_north_america.csv, checks required fields,
# normalises family names to APG IV, and writes:
#   data/archaeopollen/families_summary.csv
#   data/archaeopollen/archaeopollen.json   (records grouped by family, for a web page)
#
# Usage (from the 'spores' project root):
#   Rscript R/archaeopollen_tidy.R            # default input
#   Rscript R/archaeopollen_tidy.R path/to/records.csv
# Needs: base R + jsonlite.

suppressPackageStartupMessages(library(jsonlite))

args <- commandArgs(trailingOnly = TRUE)
infile <- if (length(args) >= 1) args[1] else file.path("data", "archaeopollen", "records_north_america.csv")
outdir <- dirname(infile)

rec <- read.csv(infile, stringsAsFactors = FALSE, na.strings = c("", "NA"),
                colClasses = "character", encoding = "UTF-8")
cat("Read", nrow(rec), "records from", infile, "\n")

# ---- 1. required fields -------------------------------------------------------
required <- c("record_id", "taxon_as_reported", "id_level", "family", "site", "region",
              "context", "reference_short", "reference_full", "confidence")
missing_cols <- setdiff(required, names(rec))
if (length(missing_cols)) stop("Missing columns: ", paste(missing_cols, collapse = ", "))

problems <- list()
for (v in required) {
  bad <- rec$record_id[is.na(rec[[v]]) | !nzchar(trimws(rec[[v]]))]
  if (length(bad)) problems[[v]] <- bad
}
if (anyDuplicated(rec$record_id)) problems$duplicate_record_id <- rec$record_id[duplicated(rec$record_id)]

allowed <- list(
  id_level   = c("species", "genus", "family", "pollen_type"),
  context    = c("hearth", "pit", "floor", "grinding_stone", "vessel", "coprolite",
                 "calculus", "burial", "midden", "other"),
  confidence = c("high", "medium", "low"))
for (v in names(allowed)) {
  bad <- rec$record_id[!is.na(rec[[v]]) & !(rec[[v]] %in% allowed[[v]])]
  if (length(bad)) problems[[paste0("bad_", v)]] <- bad
}
# numeric ages, and min <= max
for (v in c("age_min_bp", "age_max_bp", "latitude", "longitude")) {
  x <- rec[[v]]
  bad <- rec$record_id[!is.na(x) & is.na(suppressWarnings(as.numeric(x)))]
  if (length(bad)) problems[[paste0("non_numeric_", v)]] <- bad
}
amin <- suppressWarnings(as.numeric(rec$age_min_bp))
amax <- suppressWarnings(as.numeric(rec$age_max_bp))
bad <- rec$record_id[!is.na(amin) & !is.na(amax) & amin > amax]
if (length(bad)) problems$age_min_gt_max <- bad

if (length(problems)) {
  cat("\nValidation problems:\n")
  for (p in names(problems)) cat(" -", p, ":", paste(head(problems[[p]], 20), collapse = ", "),
                                 if (length(problems[[p]]) > 20) "..." else "", "\n")
  stop("Fix the problems above and re-run.")
}
cat("All required fields present; controlled vocabularies OK.\n")

# ---- 2. normalise family names (APG IV) ---------------------------------------
# Old/alternative names -> APG IV. Extend this table when adding other regions.
fam_map <- c(
  "Compositae" = "Asteraceae", "Gramineae" = "Poaceae", "Graminae" = "Poaceae",
  "Cruciferae" = "Brassicaceae", "Umbelliferae" = "Apiaceae", "Labiatae" = "Lamiaceae",
  "Leguminosae" = "Fabaceae", "Palmae" = "Arecaceae", "Guttiferae" = "Clusiaceae",
  "Chenopodiaceae" = "Amaranthaceae", "Cheno-Am" = "Amaranthaceae",
  "Hydrophyllaceae" = "Boraginaceae", "Capparaceae (Cleome)" = "Cleomaceae",
  "Agavaceae" = "Asparagaceae", "Nolinaceae" = "Asparagaceae", "Ruscaceae" = "Asparagaceae",
  "Celtidaceae" = "Cannabaceae", "Aceraceae" = "Sapindaceae", "Hippocastanaceae" = "Sapindaceae",
  "Taxodiaceae" = "Cupressaceae", "Sterculiaceae" = "Malvaceae", "Tiliaceae" = "Malvaceae",
  "Bombacaceae" = "Malvaceae", "Asclepiadaceae" = "Apocynaceae", "Scrophulariaceae (Plantago)" = "Plantaginaceae",
  "Liliaceae sensu lato" = "Liliaceae s.l.")
# genus-level corrections where the genus decides the APG IV family
genus_family <- c(
  "Cleome" = "Cleomaceae", "Peritoma" = "Cleomaceae", "Agave" = "Asparagaceae",
  "Yucca" = "Asparagaceae", "Dasylirion" = "Asparagaceae", "Nolina" = "Asparagaceae",
  "Celtis" = "Cannabaceae", "Acer" = "Sapindaceae", "Phacelia" = "Boraginaceae",
  "Sarcobatus" = "Sarcobataceae", "Leucophyllum" = "Scrophulariaceae", "Plantago" = "Plantaginaceae")

rec$family_reported <- rec$family
fam <- trimws(rec$family)
fam <- ifelse(fam %in% names(fam_map), fam_map[fam], fam)
g <- trimws(ifelse(is.na(rec$genus), "", rec$genus))
fam <- ifelse(g %in% names(genus_family), genus_family[g], fam)
changed <- which(fam != rec$family_reported)
if (length(changed)) {
  cat("Family names normalised for", length(changed), "records:\n")
  print(unique(data.frame(from = rec$family_reported[changed], to = fam[changed])), row.names = FALSE)
}
rec$family <- unname(fam)

# flag pollen types that cannot be resolved to a single APG IV family
rec$family_uncertain <- rec$family %in% c("Liliaceae s.l.")

# ---- 3. family summary --------------------------------------------------------
num <- function(x) suppressWarnings(as.numeric(x))
rec$age_min_num <- num(rec$age_min_bp)
rec$age_max_num <- num(rec$age_max_bp)

fams <- sort(unique(rec$family))
summ <- do.call(rbind, lapply(fams, function(f) {
  d <- rec[rec$family == f, ]
  gen <- unique(na.omit(d$genus[nzchar(d$genus)]))
  data.frame(
    family      = f,
    n_records   = nrow(d),
    n_sites     = length(unique(d$site)),
    n_genera    = length(gen),
    genera      = paste(sort(gen), collapse = "; "),
    earliest_bp = if (all(is.na(d$age_max_num))) NA else max(d$age_max_num, na.rm = TRUE),
    latest_bp   = if (all(is.na(d$age_min_num))) NA else min(d$age_min_num, na.rm = TRUE),
    contexts    = paste(sort(unique(d$context)), collapse = "; "),
    n_high_conf = sum(d$confidence == "high"),
    stringsAsFactors = FALSE)
}))
summ <- summ[order(-summ$n_records, summ$family), ]
write.csv(summ, file.path(outdir, "families_summary.csv"), row.names = FALSE, na = "")
cat("Wrote families_summary.csv (", nrow(summ), " families)\n", sep = "")

# ---- 4. JSON grouped by family ------------------------------------------------
keep <- c("record_id", "taxon_as_reported", "id_level", "genus", "site", "site_code", "region",
          "latitude", "longitude", "culture_period", "age_text", "age_min_bp", "age_max_bp",
          "age_basis", "context", "interpretation", "reference_short", "doi_or_url",
          "page_or_table", "notes", "confidence")
groups <- lapply(summ$family, function(f) {
  d <- rec[rec$family == f, keep]
  d$age_min_bp <- num(d$age_min_bp); d$age_max_bp <- num(d$age_max_bp)
  d$latitude <- num(d$latitude); d$longitude <- num(d$longitude)
  s <- summ[summ$family == f, ]
  list(family = f,
       n_records = s$n_records, n_sites = s$n_sites, n_genera = s$n_genera,
       earliest_bp = s$earliest_bp, latest_bp = s$latest_bp,
       contexts = strsplit(s$contexts, "; ", fixed = TRUE)[[1]],
       family_uncertain = any(rec$family_uncertain[rec$family == f]),
       records = d)
})
meta <- list(
  title = "Extant angiosperm taxa recovered by archaeopalynology - North America pilot",
  generated = format(Sys.time(), "%Y-%m-%d"),
  n_records = nrow(rec), n_sites = length(unique(rec$site)), n_families = length(fams),
  n_sources = length(unique(rec$reference_short)),
  age_note = "age_min_bp/age_max_bp mix calendar-converted, radiocarbon and calibrated values; see age_basis per record.",
  source_file = basename(infile))
write_json(list(meta = meta, families = groups),
           file.path(outdir, "archaeopollen.json"), auto_unbox = TRUE, pretty = TRUE,
           na = "null", digits = NA)
cat("Wrote archaeopollen.json\n")
