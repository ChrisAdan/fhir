select
    patient_id,
    gender,
    datediff('year', birth_date, current_date) as age
from {{ ref('stage_patient') }}
