# Palynodata (paleobotany.ru) in situ publications vs. Sporae Dispersae network
# Input: pd_pubs_genera.tsv (one row per Palynodata publication; genera listed on its page;
#        badge prefixes P:=Plants, A/C/D/F/S = acritarch/chitinozoan/dinoflagellate/fungal/scolecodont)
suppressMessages(library(utils))
pubs  <- read.delim("data/palynodata/palynodata_pubs_genera.tsv", quote = "", stringsAsFactors = FALSE)
nodes <- tolower(read.csv("data/palynodata/sd_node_genera.csv")$genus)
words <- tolower(read.csv("data/palynodata/sd_text_words.csv")$word)
pairs <- read.csv("data/palynodata/sd_insitu_pairs.csv"); pairkey <- paste(pairs$from, pairs$to)
generic <- c("spore","pollen","megaspore","microspore","microspores","trilete","monolete","monoletes",
             "tricolpate","monocolpate","bisaccate","laevigate","apiculate","verrucate","gen.nov.",
             "cycads","disaccites","sporites","sporangium")
disp_re <- "(sporites|spora|sporis|pollenites|pollis|triletes|tetras|letes|saccites|colpites|zonates|dites|cites)$"
disp_extra <- c("lycospora","calamospora","triletes","lagenicula","cystosporites","torispora","thymospora",
  "vesicaspora","raistrickia","classopollis","monosulcites","aneurospora","scylaspora","crassispora",
  "convolutispora","setispora","spermatites","elaterites","florinites","cingulizonates","radiizonates",
  "normapolles","perinopollenites","rugapites","osmundacidites","araucariacites","alisporites","pityosporites",
  "acanthotriletes","contignisporites","bensonites","didymosporites")
status <- function(g) ifelse(tolower(g) %in% nodes, "node", ifelse(tolower(g) %in% words, "mentioned", "absent"))
out <- list()
pubs <- pubs[pubs$genera != "BIG" & (is.na(pubs$n_records) | pubs$n_records <= 25), ]
for (i in seq_len(nrow(pubs))) {
  p <- pubs[i, ]
  au <- sub(" (\\d{4}) \\|.*", "", p$citation); yr <- as.integer(sub(".* (\\d{4}) \\|.*", "\\1", p$citation))
  title <- sub(".*? \\| ", "", p$citation)
  g <- strsplit(p$genera, ",")[[1]]; g <- g[!grepl("^[ACDFS]:", g)]; g <- sub("^P:", "", g)
  g <- g[!tolower(g) %in% generic & !grepl("aceae$", g)]
  isd <- (grepl(disp_re, g, ignore.case = TRUE) | tolower(g) %in% disp_extra) & !tolower(g) %in% c("todites","pinus")
  org <- g[!isd]; sp <- g[isd]
  tw <- unique(regmatches(title, gregexpr("[A-Z][a-z]{4,}", title))[[1]])
  tw <- tw[!grepl("aceae$", tw) & tolower(tw) %in% nodes & !tolower(tw) %in% c(tolower(sp), disp_extra) & !grepl(disp_re, tw)]
  org <- unique(c(org, tw))
  multi <- length(org) > 1 & length(sp) > 1
  if (!length(org)) org <- NA; if (!length(sp)) sp <- NA
  grid <- expand.grid(parent_organ = org, dispersed_genus = sp, stringsAsFactors = FALSE)
  grid$author <- au; grid$year <- yr; grid$title <- substr(title, 1, 200); grid$palynodata_pub_ids <- p$pub_ids
  grid$pairing_needs_check <- multi
  out[[i]] <- grid
}
L <- do.call(rbind, out)
L$parent_status    <- ifelse(is.na(L$parent_organ), NA, status(L$parent_organ))
L$dispersed_status <- ifelse(is.na(L$dispersed_genus), NA, status(L$dispersed_genus))
L$link_status <- ifelse(is.na(L$parent_organ) | is.na(L$dispersed_genus), NA,
  ifelse(paste(tolower(L$dispersed_genus), tolower(L$parent_organ)) %in% pairkey, "in_SD", "new"))
L$source <- "Palynodata via paleobotany.ru/palynodata (harvested 2026-11-27)"
L <- L[order(L$year, L$author), c("author","year","title","palynodata_pub_ids","parent_organ","parent_status",
        "dispersed_genus","dispersed_status","link_status","pairing_needs_check","source")]
write.csv(L, "data/palynodata/candidate_links_all.csv", row.names = FALSE, na = "")
cat("rows", nrow(L), "\n"); print(table(L$link_status, useNA = "ifany"))
cat("\nparents absent from SD:\n"); print(sort(unique(L$parent_organ[L$parent_status %in% "absent"])))
cat("\nparents only mentioned in SD text:\n"); print(sort(unique(L$parent_organ[L$parent_status %in% "mentioned"])))
cat("\ndispersed genera absent:\n"); print(sort(unique(L$dispersed_genus[L$dispersed_status %in% "absent"])))
cat("\npost-1994 papers:\n"); print(unique(L[L$year > 1994, c("author","year","parent_organ","dispersed_genus","link_status")]))
cat("\nclean new links (single-organ papers):\n")
cl <- unique(L[L$link_status %in% "new" & !L$pairing_needs_check, c("dispersed_genus","parent_organ","author","year")]); print(nrow(cl))
