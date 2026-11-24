# Resolve the families within each angiosperm order with the Open Tree of Life synthetic tree.
#
# The time tree's angiosperm backbone (orders and the clades above them) follows APG IV through the Plants Through Time
# lineage tree, but within each order its families were a flat fan. This script asks the Open Tree of Life for the
# induced subtree of each order's families, so that their branching order comes from the published phylogenies the
# synthesis summarises. Where the synthesis itself leaves a polytomy, it stays a polytomy.
#
# Input:  data/angiosperm_order_families.csv  (order, family), exported from ptt_tree.json
# Output: data/angiosperm_family_topology.json  {order: nested arrays of family names}, plus the OTT version used
#         data/angiosperm_family_topology_log.csv  per order: families asked, families matched, families in the tree
#
# Run from the repository root:  Rscript R/family_topology_otol.R

suppressPackageStartupMessages({ library(jsonlite); library(httr); library(ape) })
API <- "https://api.opentreeoflife.org/v3"
post <- function(path, body) {
  for (i in 1:3) {
    r <- try(POST(paste0(API, path), body = toJSON(body, auto_unbox = TRUE), content_type_json(), timeout(120)), silent = TRUE)
    if (!inherits(r, "try-error")) return(list(status = status_code(r), body = fromJSON(content(r, "text", encoding = "UTF-8"), simplifyVector = FALSE)))
    Sys.sleep(2 * i)
  }
  list(status = 0, body = NULL)
}

of <- read.csv("data/angiosperm_order_families.csv", stringsAsFactors = FALSE)
fams <- unique(of$family)

# 1. names to Open Tree taxonomy ids
m <- post("/tnrs/match_names", list(names = fams, context_name = "Land plants", do_approximate_matching = FALSE))
ott <- c()
for (res in m$body$results) {
  if (length(res$matches)) { tx <- res$matches[[1]]$taxon; ott[res$name] <- tx$ott_id }
}
# a family the synthesis does not recover as one clade has no node of its own; stand in one of its genera that is in the tree
in_tree <- function(id) { r <- post("/tree_of_life/node_info", list(ott_id = id)); r$status == 200 && identical(r$body$node_id, paste0("ott", id)) }   # a split ("broken") taxon answers with an mrca node instead
stand_in <- c()
for (f in names(ott)) {
  if (in_tree(ott[[f]])) next
  ti <- post("/taxonomy/taxon_info", list(ott_id = ott[[f]], include_children = TRUE))$body
  gens <- Filter(function(ch) identical(ch$rank, "genus"), ti$children)
  # prefer the type genus (Liliaceae: Lilium, Rosaceae: Rosa), found by the family's stem; then any genus in the tree
  stem <- tolower(sub("aceae$", "", f)); typ <- vapply(gens, function(g) startsWith(tolower(g$name), substr(stem, 1, max(3, nchar(stem) - 1))), logical(1))
  gens <- c(gens[typ], gens[!typ])
  for (g in head(gens, 25)) if (in_tree(g$ott_id)) { stand_in[f] <- g$name; ott[f] <- g$ott_id; break }
}
about <- post("/tree_of_life/about", list())
synth <- if (!is.null(about$body$synth_id)) about$body$synth_id else "unknown"

# 2. nested arrays from a tree: tips are family names
nest <- function(tr) {
  kids <- function(node) {
    ch <- tr$edge[tr$edge[, 1] == node, 2]
    lapply(ch, function(x) if (x <= length(tr$tip.label)) tr$tip.label[x] else kids(x))
  }
  kids(length(tr$tip.label) + 1)
}
tipname <- function(lbl) {   # labels come back as "Musaceae_ott123" or "Musaceae"
  sub("_ott[0-9]+$", "", gsub("_", " ", sub("(_ott[0-9]+)$", "\\1", lbl)))
}

out <- list(); log <- list()
for (o in unique(of$order)) {
  f <- of$family[of$order == o]; ids <- ott[f]; ids <- ids[!is.na(ids)]
  entry <- data.frame(order = o, families = length(f), matched = length(ids), in_tree = 0, note = "", stringsAsFactors = FALSE)
  if (length(ids) < 3) { log[[o]] <- entry; next }
  keep <- ids
  for (attempt in 1:3) {
    r <- post("/tree_of_life/induced_subtree", list(ott_ids = as.list(unname(keep)), label_format = "id"))
    if (r$status == 200) break
    bad <- unlist(r$body$unknown)   # ids not in the synthetic tree are reported back; drop them and ask again
    if (is.null(bad)) break
    keep <- keep[!(paste0("ott", keep) %in% names(bad))]
  }
  if (r$status != 200 || is.null(r$body$newick)) { entry$note <- "no induced subtree"; log[[o]] <- entry; next }
  # tips come back as ott ids; a family the synthesis splits ("broken") comes back as the mrca node standing in for it
  id2fam <- setNames(names(keep), paste0("ott", keep))
  br <- r$body$broken; if (length(br)) for (k in names(br)) if (!is.null(id2fam[k]) && !is.na(id2fam[k])) id2fam[br[[k]]] <- id2fam[k]
  tr <- read.tree(text = r$body$newick)
  tr$tip.label <- ifelse(tr$tip.label %in% names(id2fam), id2fam[tr$tip.label], NA)
  tr <- drop.tip(tr, which(is.na(tr$tip.label)))
  if (is.null(tr) || length(tr$tip.label) < 2) { entry$note <- "too few tips"; log[[o]] <- entry; next }
  tr <- collapse.singles(tr)
  tips <- tr$tip.label
  entry$in_tree <- length(tips)
  out[[o]] <- nest(tr)
  log[[o]] <- entry
  Sys.sleep(0.3)
}

write_json(list(source = paste0("Open Tree of Life synthetic tree (", synth, "), induced subtree of each order's families; fetched ", Sys.Date()),
                stand_ins = as.list(stand_in), orders = out), "data/angiosperm_family_topology.json", auto_unbox = TRUE, pretty = FALSE)
write.csv(do.call(rbind, log), "data/angiosperm_family_topology_log.csv", row.names = FALSE)
message("orders resolved: ", length(out), " of ", length(unique(of$order)), "; synthesis ", synth)
