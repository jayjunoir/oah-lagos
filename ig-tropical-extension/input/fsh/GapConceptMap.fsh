Instance: OAHToTropicalMorphologyMap
InstanceOf: ConceptMap
Usage: #definition
Title: "OAH Stream Morphology to Tropical Urban Morphology ConceptMap"
Description: "Formal semantic alignment highlighting structural divergence between temperate stream models and tropical drainage systems."
* url = "https://oneaquahealth.eu/fhir/ig/tropical-extension/ConceptMap/oah-morphology-gap-map"
* status = #draft
* experimental = true
* sourceUri = "http://hl7.eu/fhir/oah/CodeSystem/oah-stream-morphology"
* targetUri = "https://oneaquahealth.eu/fhir/ig/tropical-extension/CodeSystem/channel-morphology-cs"

* group[0].source = "http://hl7.eu/fhir/oah/CodeSystem/oah-stream-morphology"
* group[0].target = "https://oneaquahealth.eu/fhir/ig/tropical-extension/CodeSystem/channel-morphology-cs"

* group[0].element[0].code = #natural-stream
* group[0].element[0].target[0].code = #natural_stream
* group[0].element[0].target[0].equivalence = #equivalent

* group[0].element[1].code = #canalized-river
* group[0].element[1].target[0].code = #concrete_channel
* group[0].element[1].target[0].equivalence = #narrower
* group[0].element[1].target[0].comment = "European canalized rivers maintain perennial base flow; Lagos concrete canals alternate between high-velocity monsoon surge and completely stagnant, hyper-eutrophic pooling."

* group[0].element[2].code = #piped-conduit
* group[0].element[2].target[0].code = #open_concrete_drain
* group[0].element[2].target[0].equivalence = #unmatched
* group[0].element[2].target[0].comment = "No direct OAH equivalent. Dense open roadside U-drains act as primary urban stormwater networks in Lagos rather than enclosed subterranean sewers."

