# Rebuild occurrences.json for Sporae Dispersae from the Paleobiology Database (PBDB).
#
# For every dispersed spore, pollen or megaspore genus on the page, download its PBDB
# occurrences (the genus and everything filed under it) and write:
#   occurrences.json               the file the page reads (one entry per genus)
#   data/pbdb_occurrences.csv      the same records as a tidy table, one row per occurrence
#   data/pbdb_query_log.csv        one row per genus: records found, or the error PBDB gave
#
# Run from the repository root:   Rscript R/rebuild_occurrences.R
# Input: data/genera_by_interval.csv (genus, interval), exported from the page's datasets.
#
# Only records identified under the genus's own name are kept (see the filter below).
#
# Point layout in occurrences.json, as the page expects:
#   [lng, lat, paleolng, paleolat, max_ma, min_ma, cc, formation,
#    occurrence_no, collection_no, reference_no, identified_name]
# Palaeocoordinates are PBDB's own (GPlates model, mid-age of each record).

suppressPackageStartupMessages({ library(jsonlite); library(httr) })

genera <- read.csv("data/genera_by_interval.csv", stringsAsFactors = FALSE)
genera <- sort(unique(genera$genus))

base <- "https://paleobiodb.org/data1.2/occs/list.json"
fields <- "coords,paleoloc,strat,ident,refattr,loc"

fetch_genus <- function(g, tries = 3) {
  for (i in seq_len(tries)) {
    r <- try(GET(base, query = list(base_name = g, show = fields, vocab = "pbdb", limit = "all"),
                 timeout(120), user_agent("Sporae Dispersae rebuild (songbird-soundscape/spores)")),
             silent = TRUE)
    if (!inherits(r, "try-error")) {
      txt <- content(r, as = "text", encoding = "UTF-8")
      j <- try(fromJSON(txt, simplifyVector = TRUE), silent = TRUE)
      if (!inherits(j, "try-error")) {
        # PBDB answers an unknown name with HTTP 400 or a warning and no records: that is "none", not an error
        if (status_code(r) == 200 || !is.null(j$warnings) || !is.null(j$errors)) {
          recs <- j$records
          note <- paste(c(j$warnings, j$errors), collapse = "; ")
          if (is.null(recs) || length(recs) == 0) return(list(df = NULL, status = "none", note = note))
          return(list(df = as.data.frame(recs, stringsAsFactors = FALSE), status = "ok", note = note))
        }
      }
    }
    Sys.sleep(2 * i)
  }
  list(df = NULL, status = "error", note = "no answer from PBDB")
}

col_or_na <- function(df, nm) if (nm %in% names(df)) df[[nm]] else rep(NA, nrow(df))
num <- function(x, d) round(suppressWarnings(as.numeric(x)), d)
int <- function(x) suppressWarnings(as.integer(x))

out <- list(); rows <- list(); log <- list()
for (k in seq_along(genera)) {
  g <- genera[k]
  res <- fetch_genus(g)
  n <- if (is.null(res$df)) 0L else nrow(res$df)
  log[[k]] <- data.frame(genus = g, status = res$status, records = n, kept = 0L, note = res$note, stringsAsFactors = FALSE)
  if (res$status == "error") { out[[g]] <- list(n = 0L, pts = list(), refs = setNames(list(), character()), error = TRUE); next }
  if (n == 0) { out[[g]] <- list(n = 0L, pts = list(), refs = setNames(list(), character())); next }

  d <- res$df
  t <- data.frame(
    genus = g,
    lng = num(col_or_na(d, "lng"), 2), lat = num(col_or_na(d, "lat"), 2),
    paleolng = num(col_or_na(d, "paleolng"), 2), paleolat = num(col_or_na(d, "paleolat"), 2),
    max_ma = num(col_or_na(d, "max_ma"), 2), min_ma = num(col_or_na(d, "min_ma"), 2),
    cc = col_or_na(d, "cc"), formation = col_or_na(d, "formation"),
    occurrence_no = int(col_or_na(d, "occurrence_no")), collection_no = int(col_or_na(d, "collection_no")),
    reference_no = int(col_or_na(d, "reference_no")), identified_name = col_or_na(d, "identified_name"),
    accepted_name = col_or_na(d, "accepted_name"),
    ref_author = col_or_na(d, "ref_author"), ref_pubyr = col_or_na(d, "ref_pubyr"),
    stringsAsFactors = FALSE)
  t <- t[!is.na(t$lng) & !is.na(t$lat) & !is.na(t$max_ma) & !is.na(t$min_ma), ]
  # keep only records identified under this genus's own name. PBDB's base_name also returns
  # names it treats as synonyms, and for some form genera that pulls in unrelated taxa
  # (Polyporina, a pollen genus, brought in ~700 records of the bryozoan Polypora).
  id_genus <- vapply(strsplit(gsub("[?\"()]|\\b(cf|aff)\\.", " ", t$identified_name), "\\s+"),
                     function(w) { w <- w[nzchar(w)]; if (length(w)) w[1] else "" }, "")
  t <- t[id_genus == g, ]
  log[[k]]$kept <- nrow(t)
  rows[[g]] <- t
  if (nrow(t) == 0) { out[[g]] <- list(n = 0L, pts = list(), refs = setNames(list(), character())); next }

  pts <- lapply(seq_len(nrow(t)), function(i) list(
    t$lng[i], t$lat[i],
    if (is.na(t$paleolng[i])) NULL else t$paleolng[i],
    if (is.na(t$paleolat[i])) NULL else t$paleolat[i],
    t$max_ma[i], t$min_ma[i],
    if (is.na(t$cc[i])) "" else t$cc[i],
    if (is.na(t$formation[i])) "" else t$formation[i],
    t$occurrence_no[i], t$collection_no[i],
    if (is.na(t$reference_no[i])) NULL else t$reference_no[i],
    if (is.na(t$identified_name[i])) "" else t$identified_name[i]))
  rk <- unique(t[!is.na(t$reference_no), c("reference_no", "ref_author", "ref_pubyr")])
  refs <- setNames(as.list(trimws(paste(rk$ref_author, rk$ref_pubyr))), rk$reference_no)
  out[[g]] <- list(n = nrow(t), pts = pts, refs = refs)
  if (k %% 25 == 0) message(k, " / ", length(genera), " genera")
  Sys.sleep(0.3)
}

dir.create("data", showWarnings = FALSE)
write_json(out, "occurrences.json", auto_unbox = TRUE, null = "null", na = "null", digits = NA)
write.csv(do.call(rbind, rows), "data/pbdb_occurrences.csv", row.names = FALSE, na = "")
logdf <- do.call(rbind, log)
write.csv(logdf, "data/pbdb_query_log.csv", row.names = FALSE, na = "")
message("Done: ", sum(logdf$kept), " occurrences kept (of ", sum(logdf$records), " returned) for ", sum(logdf$kept > 0), " of ", nrow(logdf),
        " genera; ", sum(logdf$status == "error"), " genera got no answer.")
