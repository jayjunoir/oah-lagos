import os
import uuid
from datetime import datetime, timezone
import requests
from fhir.resources.provenance import Provenance, ProvenanceAgent
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

HAPI_BASE = os.getenv("HAPI_FHIR_URL", "http://localhost:8080/fhir")

class OAHMcpAgent:
    def __init__(self, base_url: str = HAPI_BASE):
        self.base_url = base_url.rstrip("/")

    def get_latest_observation(self):
        try:
            resp = requests.get(
                f"{self.base_url}/Observation?_count=1&_sort=-_lastUpdated",
                headers={"Accept": "application/fhir+json"}
            )
            if resp.status_code == 200 and "entry" in resp.json():
                return resp.json()["entry"][0]["resource"]
        except Exception:
            pass
        return {"id": "sample-obs-01"}

    def explain_metric(self, indicator_code: str, value: float) -> str:
        # Grounded in OAH Factsheets (DOI: 10.5281/zenodo.20345207)
        explanations = {
            "27449-8": f"Dissolved Oxygen ({value} mg/L): Levels below 2.0 mg/L represent acute hypoxia. Organic decomposition and stagnant standing water deplete oxygen, killing benthic fauna and causing foul odor.",
            "29662-4": f"Water Temperature ({value} °C): Water temperatures in tropical urban canals (28-32°C) accelerate microbial action and shorten mosquito larval development cycles.",
            "larvae-density": f"Larval Density ({value}): OAH Tropical Extension indicator tracking disease vector breeding potential. Serves as an environmental early-warning flag; non-diagnostic."
        }
        return explanations.get(indicator_code, f"Indicator {indicator_code} value: {value}.")

    def generate_provenance_audit(self, target_obs_id: str, explanation: str) -> Provenance:
        # Standard FHIR R4 Provenance using 'activity' for the trigger action
        return Provenance(
            id=str(uuid.uuid4()),
            target=[Reference(reference=f"Observation/{target_obs_id}")],
            recorded=datetime.now(timezone.utc).isoformat(),
            activity=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v3-DocumentCompletion",
                    code="DI",
                    display="Dictated"
                )],
                text="Generated via OAH-Lagos MCP Agent. Grounded in DOI 10.5281/zenodo.20345207. REQUIRES HUMAN EXPERT REVIEW."
            ),
            agent=[ProvenanceAgent(
                type=CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                        code="device",
                        display="Device/AI System"
                    )]
                ),
                who=Reference(display="OAH-Lagos MCP Agent v1.0")
            )]
        )

if __name__ == "__main__":
    agent = OAHMcpAgent()
    obs = agent.get_latest_observation()
    target_id = obs.get("id", "sample-obs-01")
    exp = agent.explain_metric("27449-8", 1.8)
    prov = agent.generate_provenance_audit(target_id, exp)
    
    print("=================================================")
    print("         OAH-LAGOS MCP AGENT RESPONSE           ")
    print("=================================================")
    print(f"Observation ID Target: {target_id}")
    print(f"Explanation: {exp}")
    print("\n--- FHIR R4 Provenance Resource Generated ---")
    print(prov.model_dump_json(indent=2))
    print("=================================================")
