# Coprolite catalogue for Community Paleoecology, all ages.
# Keeps the hand-curated rows (Rhynie chert and Carboniferous, with sizes and shapes from the papers) and adds one row
# per paper, place and age for every other coprolite or fossil-dung record in the interaction network.
# Inputs: data/records_export.csv (network records), data/coprolites_curated.csv. Output: data/coprolites_all_ages.csv
recs <- read.csv("data/community_paleoecology/records_export.csv", stringsAsFactors = FALSE, fileEncoding = "UTF-8")
cur  <- read.csv("data/community_paleoecology/coprolites_curated.csv", stringsAsFactors = FALSE, fileEncoding = "UTF-8")
txt  <- tolower(paste(recs$evidence, recs$interaction))
is_dung <- grepl("coprolit|dung|faec|fece|latrine|droppings|frass", txt) & !grepl("intestin|colon content|gut content|stomach|no coprolit|without coprolit|no frass|leaf mine| mines? |pocket rot", txt)
cp <- recs[is_dung, ]
# leave out papers already covered row by row in the curated table
first_author <- function(x) tolower(sub("[,. ].*$", "", trimws(x)))
cur_keys <- unique(paste(first_author(cur$citation), regmatches(cur$citation, regexpr("(19|20)[0-9]{2}", cur$citation))))
cp_keys  <- paste(first_author(cp$citation), ifelse(grepl("(19|20)[0-9]{2}", cp$citation), regmatches(cp$citation, regexpr("(19|20)[0-9]{2}", cp$citation)), ""))
cp <- cp[!(cp_keys %in% cur_keys), ]
# first sentence: stop at ". " + capital, but not after abbreviations like "c." or "ca." or a decimal point
first_sentence <- function(x) {
  m <- regexpr("(?<![ (]c|ca|cf|sp|al|fig|e\\.g|i\\.e|[0-9])\\. (?=[A-Z])", x, perl = TRUE)
  out <- if (m > 0) substr(x, 1, m) else x
  short(sub("[.;:]$", "", out), 110)
}
short <- function(x, n = 260) ifelse(nchar(x) > n, paste0(substr(x, 1, n - 1), "…"), x)
uniq_join <- function(v, n = 6) { v <- unique(trimws(v[nzchar(trimws(v))])); if (length(v) > n) c(v[1:n], sprintf("and %d more", length(v) - n)) else v }
grp <- paste(cp$citation, cp$locality, cp$age, sep = "\r")
rows <- lapply(split(cp, grp), function(g) {
  ev <- g$evidence[1]
  data.frame(
    id = "", type_or_name = first_sentence(ev),
    size_um_or_mm = "see paper", shape = "",
    contents = short(paste(uniq_join(g$plant), collapse = "; ")),
    inferred_producer = short(paste(uniq_join(g$interactor, 3), collapse = "; "), 160),
    setting = short(paste(uniq_join(g$preservation, 2), collapse = "; "), 120),
    locality = g$locality[1], unit = g$unit[1], basin_region = g$basin_region[1], age = g$age[1],
    citation = g$citation[1], doi = if ("doi" %in% names(g)) g$doi[1] else "", figure_refs = "", photo = "",
    confidence = if ("confidence" %in% names(g)) g$confidence[1] else "",
    notes = "Summarised from the interaction records; size and shape are in the paper.",
    period = g$period[1], stringsAsFactors = FALSE)
})
auto <- do.call(rbind, rows)
auto$id <- sprintf("NET-%03d", seq_len(nrow(auto)))
# periods for the curated rows
cur$period <- ifelse(grepl("Devonian", cur$age), "Devonian",
              ifelse(grepl("Permian|Asselian|Sakmarian", cur$age), "Permian",
              ifelse(grepl("Mississippian|Visean|Tournaisian|Serpukhovian", cur$age), "Mississippian", "Pennsylvanian")))
out <- rbind(cur, auto[, names(cur)])
order_p <- c("Ordovician","Silurian","Devonian","Mississippian","Pennsylvanian","Permian","Triassic","Jurassic","Cretaceous","Late Cretaceous","Paleogene","Neogene–Pleistocene","Modern")
out$period[grepl("Neogene", out$period)] <- "Neogene–Pleistocene"
out <- out[order(match(out$period, order_p), seq_len(nrow(out))), ]
write.csv(out, "data/community_paleoecology/coprolites_all_ages.csv", row.names = FALSE, fileEncoding = "UTF-8")
print(table(factor(out$period, levels = order_p)))
cat(nrow(cur), "curated +", nrow(auto), "from the network =", nrow(out), "rows\n")
