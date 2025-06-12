# eCART Simulation Pipeline

## With Public FHIR Data

The objective of this repository is to simulate a data pipeline for predictive modeling of patient deterioration risk.

Electronic Cardiac Arrest Risk Triage (eCART) is a clinical early warning system that uses Machine Learning to output a patient risk score, indicating their likelihood of deterioration, resulting in outcomes such as ICU transfer, or an imminent code event.

This project will consume sample FHIR patient data from a public API to store raw Vitals, Labs, Patient Data, and Historical Trends. The pipeline will clean, map, and build eCART-like Machine Learning training and testing data, and a Logistic Regression model will be built to predict patient deterioration risks.

[Find me on Linkedin](https://www.linkedin.com/in/chrisadan/)
[HAPI FHIR Test/Demo Server R4 Endpoint](https://hapi.fhir.org/baseR4/swagger-ui/?page=All)
This project includes code from the HAPI FHIR project, licensed under the Apache 2.0 License.
