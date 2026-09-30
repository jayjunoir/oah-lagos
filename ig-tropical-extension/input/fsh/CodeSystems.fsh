CodeSystem: TropicalWaterwayIndicatorsCS
Id: tropical-waterway-indicators-cs
Title: "Tropical Urban Waterway Indicators"
Description: "Indicators specific to tropical urban waterways, disease vector habitats, and anthropogenic channel morphologies absent from temperate European baselines."
* ^status = #draft
* ^experimental = true
* #larvae-density "Mosquito Larvae Density" "Visual count or density bracket of mosquito larvae per standard dip (vector breeding risk indicator, non-diagnostic)"
* #waste-clogging "Informal Waste Blockage Severity" "Degree to which anthropogenic solid waste obstructs waterway discharge and creates stagnation"
* #channel-morphology "Channel Structural Morphology" "Engineered or natural structural configuration of urban water conveyance"

CodeSystem: LarvaeDensityCS
Id: larvae-density-cs
Title: "Mosquito Larvae Density Categories"
Description: "Semi-quantitative categories for larvae counts."
* ^status = #draft
* ^experimental = true
* #none "None Detected" "Zero mosquito larvae identified in sampling scoop"
* #low_1_10_per_dip "Low (1-10 per dip)" "Sparse larval activity"
* #high_over_10_per_dip "High (>10 per dip)" "Dense breeding cluster indicating acute stagnation and vector habitat"

CodeSystem: ChannelMorphologyCS
Id: channel-morphology-cs
Title: "Tropical Urban Drainage Morphology"
Description: "Structural channel typologies common in West African urban environments."
* ^status = #draft
* ^experimental = true
* #open_concrete_drain "Open Concrete U-Drain" "Engineered open roadside or neighborhood storm drain"
* #concrete_channel "Engineered Concrete Canal" "High-capacity concrete trapezoidal or rectangular flood canal"
* #natural_stream "Natural Stream" "Unlined native soil or sand stream bed"
* #lagoon_adjacent "Lagoon Adjacent" "Low-energy brackish littoral or mangrove margin subject to tidal exchange"

CodeSystem: WasteSeverityCS
Id: waste-severity-cs
Title: "Solid Waste Obstruction Severity"
Description: "Qualitative assessment of solid waste flow impedance."
* ^status = #draft
* ^experimental = true
* #none "Clean" "Unimpeded hydraulic flow with minimal or no debris"
* #moderate_bank_litter "Moderate Litter on Bank" "Litter visible along shoreline/banks without complete hydraulic obstruction"
* #choked_flow_obstructed "Choked / Stagnated by Waste" "Channel bed choked with PET, single-use plastics, or silt causing active water pooling"
