# First-author affiliation for each paper cited by a Sporae Dispersae link.
# author_affiliations.csv: one row per author and span of years (source flags background knowledge to verify, or OpenAlex).
A <- read.csv("author_affiliations.csv", stringsAsFactors = FALSE)
cj <- jsonlite::fromJSON("cites.json")
out <- do.call(rbind, lapply(names(cj), function(k) {
  who <- cj[[k]]$who; yr <- cj[[k]]$year
  sur <- trimws(strsplit(who, "\\s+(&|and|et al\\.)\\s*")[[1]][1]); sur <- tail(strsplit(sur, " ")[[1]], 1)
  sur <- iconv(sur, to = "ASCII//TRANSLIT")
  m <- A[A$surname == sur & A$from_year <= yr & A$to_year >= yr, ]
  data.frame(cite = k, first_author = sur, year = yr, n_links = length(cj[[k]]$about),
             institution = if (nrow(m) == 1) m$institution else NA, country = if (nrow(m) == 1) m$country else NA,
             source = if (nrow(m) == 1) m$source else NA, stringsAsFactors = FALSE)
}))
write.csv(out, "affiliations_by_cite.csv", row.names = FALSE, na = "")
cat(sum(!is.na(out$institution)), "of", nrow(out), "papers;", sum(out$n_links[!is.na(out$institution)]), "of", sum(out$n_links), "links\n")
