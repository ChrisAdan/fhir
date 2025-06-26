{{ config(
    materialized='view',
    persist_docs={'relation': True, 'columns': True}) }}

select
    base.id as observation_id,
    split_part(base.raw_response:subject.reference::string, '/', 2) as patient_id,
    split_part(base.raw_response:encounter.reference::string, '/', 2) as encounter_id,
    base.raw_response:code.coding[0].code::string as loinc_code,
    name.consumername as consumer_name, 
    base.raw_response:effectiveDateTime::timestamp_ntz as observation_time,
    base.raw_response:valueQuantity.value::float as result_value,
    base.raw_response:valueQuantity.unit::string as unit
from {{ source('raw', 'raw_observation' ) }} as base
left join {{ ref('dim_loinc_consumer_name') }} as name
on name.loincnumber = base.raw_response:code.coding[0].code::string
where raw_response:code.coding[0].system = 'http://loinc.org'
and name.consumername is not null
having loinc_code is not null
and observation_time is not null