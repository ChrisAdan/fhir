{{ config(
    materialized='view',
    persist_docs={'relation': True, 'columns': True}) }}

select
    base.id,
    split_part(base.raw_response:subject.reference::string, '/', 2) as patient_id,
    split_part(base.raw_response:encounter.reference::string, '/', 2) as encounter_id,
    base.raw_response:code.coding[0].code::string as condition_code,
    base.raw_response:code.coding[0].system as coding_system,
    base.raw_response:code.coding[0].display::string as condition_display,
    base.raw_response:onsetDateTime::timestamp_ntz as onset_datetime,
    base.raw_response:recordedDate::timestamp_ntz as recorded_datetime,
    base.raw_response:clinicalStatus.coding[0].code::string as clinical_status,
    base.raw_response:verificationStatus.coding[0].code::string as verification_status
from {{ source('raw', 'raw_condition') }} as base
having condition_code is not null