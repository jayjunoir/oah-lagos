import os
import requests
from fhir.resources.location import Location
from fhir.resources.observation import Observation

HAPI_BASE = os.getenv("HAPI_FHIR_URL", "http://localhost:8080/fhir")

class HapiFhirClient:
    def __init__(self, base_url: str = HAPI_BASE):
        self.base_url = base_url.rstrip("/")

    def validate_locally(self, resource) -> bool:
        # Pydantic v2 validation via fhir.resources
        resource.__class__.model_validate(resource.model_dump())
        return True

    def upsert_location(self, location: Location) -> str:
        self.validate_locally(location)
        resp = requests.put(
            f"{self.base_url}/Location/{location.id}",
            data=location.model_dump_json(),
            headers={"Content-Type": "application/fhir+json"}
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"HAPI rejected Location: {resp.status_code} - {resp.text}")
        return location.id

    def create_observation(self, observation: Observation, location_id: str) -> str:
        # Reference the location as the subject
        observation.subject = {"reference": f"Location/{location_id}"}
        self.validate_locally(observation)
        resp = requests.post(
            f"{self.base_url}/Observation",
            data=observation.model_dump_json(),
            headers={"Content-Type": "application/fhir+json"}
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"HAPI rejected Observation: {resp.status_code} - {resp.text}")
        return resp.json()["id"]
