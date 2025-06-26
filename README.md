# 🏥 Patient Risk Simulation Pipeline

### with Public FHIR Data

This repository simulates a modern analytics engineering pipeline for predicting patient deterioration risk, using open healthcare data.

Inspired by the **eCART** (Electronic Cardiac Arrest Risk Triage) model from [AgileMD](https://www.agilemd.com), this project **does not** use any proprietary data or code. Instead, it leverages public FHIR APIs to demonstrate how raw EHR data can be transformed into predictive insights.

> 📌 **Disclaimer:** This is a personal, educational project. It is not affiliated with AgileMD or intended for clinical use.

---

## 🔧 Pipeline Overview

The project extracts **FHIR resources** (Patient, Observation, Condition, Encounter, MedicationRequest) from a public API and processes them into a Snowflake-based data warehouse.

It follows a **Bronze → Silver → Gold** approach:

### 🔹 RAW

Ingests unprocessed FHIR JSON using:

- `scripts/extract_fhir.py`
- `scripts/load_to_snowflake.py`  
  Raw tables include `RAW_PATIENT`, `RAW_OBSERVATION`, etc., with full JSON payloads.

### 🔸 DIM

Seeded dimensional tables for semantic mapping using:

- `scripts/generate_seeds.py`  
  Focuses on:
- `DIM_LOINC_*` tables for lab and observation standardization

### 🪞 STAGE

Unpacks structured fields from raw JSON into tabular form.  
Includes:

- `stage_patient`
- `stage_encounter`
- `stage_observation`
- `stage_condition`

### 🧬 FEATURES_CORE

Transforms structured data into features for machine learning.  
Includes:

- `ecart_demographics`: Age, gender, admission type
- `ecart_lab_features`: Lab values by LOINC mapping
- `lab_observation_mapped`: Fully normalized observation data using LOINC

### 📈 ANALYTICS

Summarizes time-series and KPI metrics for business monitoring.

- `daily_retention`: Patient counts by day
- `kpi_snapshot`: Daily KPIs (volume, average vitals, etc.)
- `kpi_week_over_week`: Weekly trends and deltas in patient counts

---

## 📂 Local Setup

This repo requires:

- Python 3.9+
- dbt + Snowflake profile
- `scripts/data/raw_json/` (not version-controlled, but regenerable)

Run the pipeline:

```bash
python scripts/extract_fhir.py
python scripts/load_to_snowflake.py
dbt seed
dbt run
```

## 📚 Data Sources

- ✅ [HAPI FHIR Demo Server (R4)](https://hapi.fhir.org/baseR4/swagger-ui/?page=All)
- ✅ [LOINC Public Dataset](https://loinc.org/downloads/loinc/)

## 🙌 Acknowledgements

This project includes material from the HAPI FHIR project, licensed under the Apache 2.0 License.

## 👤 [Find Chris Adan on LinkedIn](https://www.linkedin.com/in/chrisadan/)

### [Read on Medium](https://upandtothewrite.medium.com/)
