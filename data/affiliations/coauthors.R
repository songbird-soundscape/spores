# Full author lists for the papers Sporae Dispersae cites, so that hovering one link can light up
# every link sharing any of its authors. Sources, in order: the full reference in cites.json,
# then OpenAlex (first author and year must match; title kept for hand-checking), else the
# surnames written in the citation itself ("et al." papers then carry only the first author).
library(jsonlite)
cj <- fromJSON("cites.json", simplifyVector = FALSE)
ascii <- function(x) stringi::stri_trans_general(x, "Latin-ASCII")
sur_of <- function(name) { p <- strsplit(trimws(name), "\\s+")[[1]]; p <- p[!grepl("^[A-Z][a-z]?\\.?$|^[A-Z]\\.", p) & !p %in% c("van", "von", "de", "du", "le", "der")]; tail(p, 1) }
from_who <- function(who) { w <- gsub("\\s+et al\\.?", "", who); s <- trimws(strsplit(w, "\\s*(&|,| and )\\s*")[[1]]); s <- s[nzchar(s)]; vapply(s, function(x) tail(strsplit(x, " ")[[1]], 1), "") }
from_full <- function(full) {           # "Looy, C.V., Stevenson, R.A., Van Hoof, T.B. & Mander, L. 2014. ..."
  head <- sub("\\s*\\(?(1[789]|20)\\d\\d.*$", "", full)
  s <- regmatches(head, gregexpr("(?:^|,\\s*|&\\s*)([A-Z][\\p{L}'\\-]+(?:\\s+[A-Z][\\p{L}'\\-]+)?)(?=,\\s*[A-Z]\\.)", head, perl = TRUE))[[1]]
  s <- trimws(gsub("^[,&\\s]+", "", s, perl = TRUE)); vapply(s, function(x) tail(strsplit(x, " ")[[1]], 1), "") }
BOT <- "spore|pollen|fossil|flora|plant|fern|lycop|gen\\. ?nov|sp\\. ?nov|devonian|silurian|carbonifer|pennsylvan|permian|jurassic|cretac|eocene|paleocene|miocene|fructif|inflorescen|flower|seed|cone|sporang|aperture|palyno|in situ"
oa_lookup <- function(first, yr, about) {
  terms <- unique(c(unlist(strsplit(unlist(about), " ")), ""))
  for (t in head(terms, 4)) {
    u <- sprintf("https://api.openalex.org/works?filter=publication_year:%d-%d,raw_author_name.search:%s%s&per-page=10&select=title,publication_year,authorships",
                 yr - 1, yr + 1, URLencode(first), if (nzchar(t)) paste0("&search=", URLencode(t)) else "")
    r <- tryCatch(fromJSON(u, simplifyVector = FALSE)$results, error = function(e) list()); Sys.sleep(0.15)
    for (w in r) { a <- vapply(w$authorships, function(x) x$author$display_name %||% "", "")
      if (length(a) >= 2 && grepl(BOT, w$title %||% "", ignore.case = TRUE) && tolower(ascii(sur_of(a[1]))) == tolower(ascii(first)))
        return(list(authors = vapply(a, sur_of, ""), title = w$title %||% "", term = t)) } }
  NULL }
`%||%` <- function(a, b) if (is.null(a)) b else a
rows <- list()
for (k in names(cj)) { v <- cj[[k]]; who <- v$who; yr <- v$year; first <- from_who(who)[1]
  au <- NULL; src <- "citation"; title <- ""
  if (!is.null(v$full) && nzchar(v$full)) { f <- from_full(v$full); if (length(f) >= length(from_who(who))) { au <- f; src <- "full reference" } }
  if (is.null(au) && grepl("et al", who)) { o <- oa_lookup(first, yr, v$about)
    if (!is.null(o)) { au <- o$authors; src <- "OpenAlex (check title)"; title <- o$title } }
  if (is.null(au)) au <- from_who(who)
  rows[[k]] <- data.frame(cite = k, authors = paste(ascii(au), collapse = "; "), n = length(au), source = src, oa_title = title, stringsAsFactors = FALSE) }
out <- do.call(rbind, rows)
write.csv(out, "coauthors_by_cite.csv", row.names = FALSE)
write(toJSON(setNames(lapply(strsplit(out$authors, "; "), unname), out$cite), auto_unbox = FALSE), "coauthors.json")
print(table(out$source)); print(out[grepl("et al", out$cite), c("cite", "authors", "source", "oa_title")], right = FALSE)
