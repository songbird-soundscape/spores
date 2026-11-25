# Coprolite ichnotaxa from Habgood, Hass & Kerp 2004 (Rhynie chert), for the Community Paleoecology coprolite catalogue.
# Built from the paper's abstract; per-species sizes and shapes beyond the abstract still need checking against the paper.
cit <- "Habgood, K.S., Hass, H. & Kerp, H. 2004. Evidence for an early terrestrial food web: coprolites from the Early Devonian Rhynie chert. Transactions of the Royal Society of Edinburgh: Earth Sciences 94(4): 371-389 (doi 10.1017/S0263593300000754)"
common <- list(setting = "silicified in the Rhynie hot-spring cherts, among terrestrial and freshwater biota",
               locality = "Rhynie, Aberdeenshire, Scotland", unit = "Rhynie chert",
               basin_region = "Rhynie outlier, Scotland", age = "Early Devonian (Pragian)", citation = cit)
rows <- data.frame(
  id = c("HAB04-Lan-sim","HAB04-Lan-div","HAB04-Lan-mon","HAB04-Rot-agg","HAB04-Bac-con","HAB04-Bac-min"),
  type_or_name = c("Lancifaex simplex","Lancifaex divisa","Lancifaex moniliforma","Rotundafaex aggregata","Bacillafaex constipatus","Bacillafaex mina"),
  size_um_or_mm = c(rep("within 0.5-3 mm (range for the whole assemblage)", 4),
                    "within 0.5-3 mm; told apart from B. mina by size", "within 0.5-3 mm; told apart from B. constipatus by size"),
  shape = c(rep("elongate (Lancifaex); the three species differ in form", 3), "rotund", "rod-shaped", "rod-shaped"),
  contents = c(rep("particulate; spores usually not dominant, though some are spore-rich (spore-rich and spore-poor grade into each other)", 3),
               "particulate", "amorphous", "amorphous"),
  inferred_producer = c(rep("small detritivore; spore-rich examples could mean spore-eating, but comparison with modern millipede faeces favours detritivores", 3),
                        rep("one of at least four kinds of consumer (detritivores and herbivores) recognised from the coprolites", 3)),
  stringsAsFactors = FALSE)
for (k in names(common)) rows[[k]] <- common[[k]]
write.csv(rows, "data/community_paleoecology/habgood2004_coprolites.csv", row.names = FALSE)
cat(nrow(rows), "rows written\n")
