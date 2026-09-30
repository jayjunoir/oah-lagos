# OAH-Lagos: Portability Audit & Tropical Extension of the OneAquaHealth Toolchain

An empirical portability audit and formal HL7 FHIR extension of the European **OneAquaHealth (OAH)** urban stream health toolchain for Lagos, Nigeria.

Submitted to the **OneAquaHealth IEEE Global Hackathon 2026** under **Track 7: Digital Health Standards**.

---

## Architecture Overview
[Offline PWA Intake Form] (IndexedDB + ServiceWorker)
│
▼ HTTP POST /api/v1/observations/bundle (FHIR Transaction Bundle)
[FastAPI Bridge] (intake/main.py)
├── Local Validation (fhir.resources Pydantic V2)
├── Dual-Coding Pipeline (LOINC + Tropical Extensions)
└── Anomaly Engine (pipeline/anomaly.py)
│
▼ HTTP PUT / POST (application/fhir+json)
[HAPI FHIR JPA Server R4] ───► [PostgreSQL 15] (Docker Compose)
▲
│ Formal Definitions & ConceptMap
[Tropical Extension FHIR IG] (FSH / SUSHI)
├── CodeSystems: Channel Morphology, Larvae Density, Waste Severity
└── ConceptMap: OAH European to Tropical Morphology Alignment
---

## Key Differentiators

1. **Offline-First PWA Intake:** Built for low-connectivity field environments in West Africa. Caches observations in browser IndexedDB and syncs as a formal FHIR R4 Transaction Bundle upon reconnection.
2. **The Transfer Test (Honest ML Evaluation):** Evaluates a classifier trained on European pilot data (Benevento, Coimbra, Ghent) against Lagos observations. Documents the 33.3% drop in accuracy caused by climate and morphology covariate shift (28–32°C water temps vs 12–20°C in Europe).
3. **MCP Agent with FHIR Provenance:** Plain-language metric explanation grounded in OAH Zenodo Factsheets (DOI: 10.5281/zenodo.20345207), generating a formal `FHIR Provenance` audit trail requiring human-in-the-loop review.
4. **Tropical DSS Rule Proposal:** Formulates an actionable decision-rule matrix for concrete drains and tidal lagoons, replacing inapplicable European bio-meander restoration with desilting, trash grids, and biological larviciding.

---

## Quickstart (Fedora / Linux)

### 1. Launch FHIR Infrastructure
```bash
docker compose up -d
# Verify HAPI FHIR:
curl -s http://localhost:8080/fhir/metadata | grep "fhirVersion"
source .venv/bin/activate
uvicorn intake.main:app --host 0.0.0.0 --port 8000 --reload
python pipeline/ml/transfer_test.py
python pipeline/anomaly.py
python pipeline/mcp_server.py
cd ig-tropical-extension
sushi .
