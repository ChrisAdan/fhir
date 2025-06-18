{{ config(
    materialized='view',
    persist_docs={'relation': True, 'columns': True}) }}

select
    base.id as patient_id,
    base.raw_response:gender::string as gender,
    try_cast(base.raw_response:birthDate::string as date) as birth_date 
from {{ source('raw', 'raw_patient' ) }} as base