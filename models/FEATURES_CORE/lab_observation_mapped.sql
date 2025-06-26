select
    obvs.patient_id,
    obvs.observation_time,
    obvs.loinc_code,
    loinc.consumername as feature_name,
    obvs.result_value
from {{ ref('stage_observation') }} obvs
left join {{ source('dim', 'dim_loinc_consumer_name') }} loinc
    on obvs.loinc_code = loinc.loincnumber
where obvs.result_value is not null