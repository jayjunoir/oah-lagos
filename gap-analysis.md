# OAH-Lagos Portability Audit & Gap Analysis

**Project:** OAH-Lagos (Track 7: Digital Health Standards)  
**Target:** OneAquaHealth (OAH) European Stream Health Toolchain  
**Test Location:** Lagos, Nigeria (Sub-Saharan Urban Coastal Wetland)

---

## 1. Executive Summary
The OneAquaHealth (OAH) platform standardizes urban stream health indicators across five European pilot sites (Benevento, Coimbra, Ghent, Oslo, Toulouse) using an HL7 FHIR R4 Implementation Guide, Citizen Science mobile intake, and a Decision Support System (DSS).

This audit evaluates the portability of the OAH toolchain when subjected to field conditions in Lagos, Nigeria. The audit identifies structural ontology gaps, mismatched epidemiological priorities (disease vector risk), and non-viable DSS remediation assumptions.

---

## 2. Structured Gap Matrix

| OAH Component | Lagos Field Input / Test Case | Point of Failure / Incompatibility | Root Cause in European Baseline | Proposed Extension / Fix |
| :--- | :--- | :--- | :--- | :--- |
| **FHIR Profile: LocationOah** | Somolu secondary stormwater drain (`lagos-somolu-drain-01`) | Cannot classify concrete trapezoidal/rectangular open drains without misrepresenting them as natural streams or piped sewers. | European pilots focus on daylighted or natural riverine corridors; Lagos relies on surface-level concrete U-drains. | Defined `ChannelMorphologyCS` containing `#open_concrete_drain`, `#concrete_channel`, `#covered_slab`, and `#lagoon_adjacent`. |
| **FHIR Profile: ObservationIndicatorsOah** | Somolu & Makoko sites with stagnant pools holding >10 mosquito larvae per dip | No LOINC or OAH indicator exists for vector breeding larval density. | European urban stream health prioritizes macroinvertebrate biodiversity (EPT taxa) rather than vector-borne disease reservoirs. | Added component `larvae-density` referencing `LarvaeDensityCS` (`#none`, `#low_1_10_per_dip`, `#high_over_10_per_dip`) as an environmental indicator. |
| **FHIR Profile: ObservationIndicatorsOah** | Makoko tidal outfall (`lagos-makoko-lagoon-02`) choked with PET bottles and styrofoam | European OAH indicators track dissolved chemical contaminants and microplastics, lacking a macroscopic debris blockage scale. | Solid waste collection failures in dense informal settlements cause direct hydraulic stagnation and localized flooding. | Added component `waste-clogging` referencing `WasteSeverityCS` (`#none`, `#moderate_bank_litter`, `#choked_flow_obstructed`). |
| **FHIR Semantic Mapping** | Interoperability between European and African hydrological taxonomies | Standard OAH terminology lacks translation to tropical open-channel networks. | OAH taxonomy assumes temperate European hydromorphology (WFD guidelines). | Encoded `ConceptMap/oah-morphology-gap-map` mapping OAH concepts to tropical channel classes with explicit `equivalence` tags. |
| **Decision Support System (DSS)** | Remediation query for urban open concrete drain | DSS recommends "riparian buffer planting", "meander restoration", and "gravel bed installation". | DSS decision trees assume rehabilitatable natural geomorphology; these measures would block urban drainage and worsen flash floods. | Authored `pipeline/dss_lagos_rules.json` detailing urban channel triage: mechanical desilting and vector source reduction before riparian bio-restoration. |
| **Citizen Science App** | Water sampling during heavy monsoon downpour vs. dry season stagnation | Fixed indicator thresholds flag extreme variance as sensor error. | Tropical monsoon climates experience acute flood-pulse dilution followed by hyper-eutrophic dry-season pooling. | Propose seasonal context metadata (`monsoon_surge` vs. `dry_stagnant`) in observation intake. |

---

## 3. Provenance & Interoperability
All Lagos observations were validated against FHIR R4 constraints using `fhir.resources`, mapped to LOINC codes for physico-chemical parameters, and persisted in a local PostgreSQL-backed HAPI FHIR server (`http://localhost:8080/fhir`). The formal extensions are compiled into standard FHIR JSON via FSH/SUSHI under `ig-tropical-extension/`.
