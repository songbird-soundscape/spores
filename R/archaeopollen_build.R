# archaeopollen_build.R
# Assemble data/archaeopollen/records_north_america.csv and sources.csv from
# the hand-entered staging tables in data/archaeopollen/staging/:
#   sources.psv  - one row per source consulted (source_id key)
#   sites.psv    - one row per site (site_key), with default dates
#   records.psv  - one row per taxon x site x context x source
# Staging files are pipe-separated ("|") so free text can contain commas.
# A record's age fields, when filled, override the site's defaults.
#
# Usage (from the project root, i.e. the 'spores' folder):
#   Rscript R/archaeopollen_build.R
# then
#   Rscript R/archaeopollen_tidy.R

args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args) >= 1) args[1] else "."
stg  <- file.path(root, "data", "archaeopollen", "staging")
out  <- file.path(root, "data", "archaeopollen")

read_psv <- function(f, n_expected) {
  lines <- readLines(f, encoding = "UTF-8", warn = FALSE)
  lines <- lines[nzchar(trimws(lines))]
  parts <- strsplit(lines, "|", fixed = TRUE)
  # strsplit drops trailing empty fields; pad them back
  hdr <- parts[[1]]
  n <- length(hdr)
  if (!missing(n_expected) && n != n_expected)
    stop(f, ": header has ", n, " fields, expected ", n_expected)
  raw_n <- lengths(regmatches(lines, gregexpr("|", lines, fixed = TRUE))) + 1
  bad <- which(raw_n != n)
  if (length(bad)) stop(f, ": wrong field count on line(s) ", paste(bad, collapse = ", "))
  body <- lapply(parts[-1], function(p) { length(p) <- n; p[is.na(p)] <- ""; trimws(p) })
  df <- as.data.frame(do.call(rbind, body), stringsAsFactors = FALSE)
  names(df) <- hdr
  df
}

src  <- read_psv(file.path(stg, "sources.psv"), 6)
site <- read_psv(file.path(stg, "sites.psv"), 11)
rec  <- read_psv(file.path(stg, "records.psv"), 15)

# referential integrity
miss_src  <- setdiff(rec$source_id, src$source_id)
miss_site <- setdiff(rec$site_key, site$site_key)
if (length(miss_src))  stop("records reference unknown source_id: ", paste(miss_src, collapse = ", "))
if (length(miss_site)) stop("records reference unknown site_key: ", paste(miss_site, collapse = ", "))
if (anyDuplicated(src$source_id)) stop("duplicate source_id in sources.psv")
if (anyDuplicated(site$site_key)) stop("duplicate site_key in sites.psv")

m <- merge(rec, site, by = "site_key", all.x = TRUE, sort = FALSE, suffixes = c("", ".site"))
# record-level age overrides
for (v in c("age_text", "age_min_bp", "age_max_bp", "age_basis")) {
  sv <- paste0(v, ".site")
  m[[v]] <- ifelse(nzchar(m[[v]]), m[[v]], m[[sv]])
}
m <- merge(m, src[, c("source_id", "reference_short", "reference_full", "doi_or_url")],
           by = "source_id", all.x = TRUE, sort = FALSE)

# stable order: as entered in records.psv
m$ord <- match(paste(m$source_id, m$site_key, m$taxon_as_reported, m$context, m$page_or_table),
               paste(rec$source_id, rec$site_key, rec$taxon_as_reported, rec$context, rec$page_or_table))
m <- m[order(m$ord), ]
m$record_id <- sprintf("NA-AP-%04d", seq_len(nrow(m)))

cols <- c("record_id", "taxon_as_reported", "id_level", "genus", "family", "site", "site_code",
          "region", "latitude", "longitude", "culture_period", "age_text", "age_min_bp",
          "age_max_bp", "age_basis", "context", "interpretation", "reference_short",
          "reference_full", "doi_or_url", "page_or_table", "notes", "confidence", "source_id")
records <- m[, cols]
write.csv(records, file.path(out, "records_north_america.csv"), row.names = FALSE, na = "")

n_by_src <- table(factor(records$source_id, levels = src$source_id))
sources <- data.frame(
  source_id      = src$source_id,
  reference_short = src$reference_short,
  reference_full = src$reference_full,
  doi_or_url     = src$doi_or_url,
  how_accessed   = src$access,
  records_taken  = as.integer(n_by_src),
  notes          = src$source_notes,
  stringsAsFactors = FALSE)
write.csv(sources, file.path(out, "sources.csv"), row.names = FALSE, na = "")

cat("records:", nrow(records), " sites:", length(unique(records$site)),
    " sources consulted:", nrow(sources), " sources with records:", sum(sources$records_taken > 0), "\n")
