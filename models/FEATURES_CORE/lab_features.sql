select
    patient_id,
    max(case when feature_name = 'WBC' then result_value end) as wbc,
    max(case when feature_name = 'Lactate' then result_value end) as lactate
from {{ ref('lab_observation_mapped') }}
group by 1