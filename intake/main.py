import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from intake.schemas import FieldObservationInput
from pipeline.mapper import map_input_to_fhir
from pipeline.client import HapiFhirClient

app = FastAPI(title="OAH-Lagos Field Logger & FHIR Bridge")
fhir_client = HapiFhirClient()
os.makedirs("intake/data/samples", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def root():
    with open("intake/web/index.html", "r") as f:
        return f.read()

@app.get("/sw.js")
def service_worker():
    return FileResponse("intake/web/sw.js", media_type="application/javascript")

@app.get("/manifest.json")
def manifest():
    return FileResponse("intake/web/manifest.json", media_type="application/json")

@app.post("/api/v1/observations")
def log_observation(obs_input: FieldObservationInput):
    fname = f"intake/data/samples/{obs_input.site_id}_{int(obs_input.timestamp.timestamp())}.json"
    with open(fname, "w") as f:
        f.write(obs_input.model_dump_json(indent=2))

    try:
        loc_res, obs_res = map_input_to_fhir(obs_input)
        loc_id = fhir_client.upsert_location(loc_res)
        obs_id = fhir_client.create_observation(obs_res, location_id=loc_id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"status": "success", "fhir_location_id": loc_id, "fhir_observation_id": obs_id}

@app.post("/api/v1/observations/bundle")
def sync_offline_bundle(inputs: List[FieldObservationInput]):
    """Receives buffered offline records, generates a FHIR R4 Transaction Bundle, and posts to HAPI."""
    if not inputs:
        return {"status": "empty", "synced_count": 0}

    bundle_entries = []
    synced_obs_ids = []

    for item in inputs:
        # Save raw backup locally on disk
        fname = f"intake/data/samples/{item.site_id}_{int(item.timestamp.timestamp())}_offline.json"
        with open(fname, "w") as f:
            f.write(item.model_dump_json(indent=2))

        loc_res, obs_res = map_input_to_fhir(item)
        loc_id = fhir_client.upsert_location(loc_res)
        
        obs_res.subject = {"reference": f"Location/{loc_id}"}
        fhir_client.validate_locally(obs_res)

        # Build FHIR Transaction Entry
        bundle_entries.append(BundleEntry(
            resource=obs_res,
            request=BundleEntryRequest(method="POST", url="Observation")
        ))
        synced_obs_ids.append(obs_res.id)

    # Wrap into FHIR Transaction Bundle
    transaction_bundle = Bundle(
        type="transaction",
        entry=bundle_entries
    )

    # Dispatch to local HAPI FHIR server
    import requests
    resp = requests.post(
        f"{fhir_client.base_url}",
        data=transaction_bundle.model_dump_json(),
        headers={"Content-Type": "application/fhir+json"}
    )

    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"HAPI rejected transaction bundle: {resp.text}")

    return {
        "status": "success",
        "synced_count": len(inputs),
        "synced_observation_ids": synced_obs_ids
    }
