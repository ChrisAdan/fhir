{{ config(
    materialized='view',
    persist_docs={'relation': True, 'columns': True}) }}

select
    base.id as patient_id,
    base.raw_response:id::string as encounter_id,
    base.raw_response:period.start::timestamp_ntz as encounter_start,
    base.raw_response:period.end::timestamp_ntz as encounter_end,
    base.raw_response:class.code::string as encounter_class,
    base.raw_response:serviceType.coding[0].code::string as service_code
from {{ source('raw', 'raw_encounter')}} as base