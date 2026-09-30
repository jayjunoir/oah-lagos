import uuid
from typing import Tuple
from fhir.resources.location import Location, LocationPosition
from fhir.resources.observation import Observation, ObservationComponent
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from intake.schemas import FieldObservationInput

OAH_OBS_PROFILE = "http://hl7.eu/fhir/oah/StructureDefinition/observation-indicators-oah"
OAH_LOC_PROFILE = "http://hl7.eu/fhir/oah/StructureDefinition/LocationOah"
TROPICAL_CS_BASE = "https://oneaquahealth.eu/fhir/ig/tropical-extension/CodeSystem"

def map_input_to_fhir(data: FieldObservationInput) -> Tuple[Location, Observation]:
    # 1. Location Resource
    loc_id = f"loc-{data.site_id}"
    location = Location(
        id=loc_id,
        meta={"profile": [OAH_LOC_PROFILE]},
        status="active",
        name=data.site_name,
        position=LocationPosition(latitude=data.latitude, longitude=data.longitude)
    )

    # 2. Multi-Component Observation Resource
    components = []

    if data.water_temp_celsius is not None:
        components.append(ObservationComponent(
            code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="29662-4", display="Water temperature")]),
            valueQuantity=Quantity(value=data.water_temp_celsius, unit="Cel", system="http://unitsofmeasure.org", code="Cel")
        ))
    if data.ph is not None:
        components.append(ObservationComponent(
            code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="27466-2", display="pH of Water")]),
            valueQuantity=Quantity(value=data.ph, unit="[pH]", system="http://unitsofmeasure.org", code="[pH]")
        ))
    if data.dissolved_oxygen_mg_l is not None:
        components.append(ObservationComponent(
            code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="27449-8", display="Dissolved oxygen in Water")]),
            valueQuantity=Quantity(value=data.dissolved_oxygen_mg_l, unit="mg/L", system="http://unitsofmeasure.org", code="mg/L")
        ))
    if data.turbidity_ntu is not None:
        components.append(ObservationComponent(
            code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="42080-2", display="Turbidity of Water")]),
            valueQuantity=Quantity(value=data.turbidity_ntu, unit="NTU", system="http://unitsofmeasure.org", code="NTU")
        ))

    # Tropical Extensions
    components.append(ObservationComponent(
        code=CodeableConcept(coding=[Coding(system=f"{TROPICAL_CS_BASE}/tropical-waterway-indicators-cs", code="larvae-density", display="Mosquito Larvae Density")]),
        valueCodeableConcept=CodeableConcept(coding=[Coding(system=f"{TROPICAL_CS_BASE}/larvae-density-cs", code=data.mosquito_larvae.value, display=data.mosquito_larvae.name)])
    ))
    components.append(ObservationComponent(
        code=CodeableConcept(coding=[Coding(system=f"{TROPICAL_CS_BASE}/tropical-waterway-indicators-cs", code="waste-clogging", display="Informal Waste Blockage Severity")]),
        valueCodeableConcept=CodeableConcept(coding=[Coding(system=f"{TROPICAL_CS_BASE}/waste-severity-cs", code=data.waste_severity.value, display=data.waste_severity.name)])
    ))

    obs_id = str(uuid.uuid4())
    observation = Observation(
        id=obs_id,
        meta={"profile": [OAH_OBS_PROFILE]},
        status="final",
        category=[CodeableConcept(coding=[Coding(system="http://terminology.hl7.org/CodeSystem/observation-category", code="exam", display="Exam")])],
        code=CodeableConcept(coding=[Coding(system="http://hl7.eu/fhir/oah/CodeSystem/oah-indicators", code="environmental-stream-assessment", display="Environmental Stream Quality Assessment")]),
        effectiveDateTime=data.timestamp.isoformat(),
        component=components
    )

    return location, observation
