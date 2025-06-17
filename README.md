# Patient Risk Simulation Pipeline

## With Public FHIR Data

The objective of this repository is to simulate a data pipeline for predictive modeling of patient deterioration risk.

This project draws conceptual inspiration from the Electronic Cardiac Arrest Risk Triage (eCART) model, a proprietary clinical risk scoring system developed and owned by [AgileMD](https://www.agilemd.com/).
No proprietary code, data, or intellectual property from AgileMD is accessed, used, or replicated here.

This implementation is an educational approximation built on publicly available data out of personal interest by the author.

The project will consume sample FHIR patient data from a public API to store raw Vitals, Labs, Patient Data, and Historical Trends. The pipeline will clean, map, and build eCART-like Machine Learning training and testing data, and a Logistic Regression model will be built to predict patient deterioration risks.

Raw FHIR data is stored temporarily in scripts/data/raw_json during extraction, organized by Resource Type. This directory is excluded from version control, regenerate using scripts/extract_fhir.py.

Public metadata from major clinical coding systems is ingested to enable dimensional modeling and semantically enrich FHIR resource data including:

- LOINC (Logical Observation Identifiers Names and Codes) for lab test and clinical observation standardization

[Find me on Linkedin](https://www.linkedin.com/in/chrisadan/)

## Acknowledgements

[HAPI FHIR Test/Demo Server R4 Endpoint](https://hapi.fhir.org/baseR4/swagger-ui/?page=All)
This project includes code from the HAPI FHIR project, licensed under the Apache 2.0 License.
