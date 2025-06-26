with weekly as (
    select
        date_trunc('week', encounter.encounter_start) as week,
        count(distinct patient.patient_id) as unique_patients,
        count(distinct encounter.encounter_id) as unique_encounters,
        count(distinct observation.observation_id) as unique_observations,
        count(distinct condition.condition_id) as unique_conditions
    from {{ ref('stage_encounter') }} as encounter
    join {{ ref('stage_patient') }} as patient
        on encounter.patient_id = patient.patient_id
    left join {{ ref('stage_observation') }} as observation
        on observation.encounter_id = encounter.encounter_id
    left join {{ ref('stage_condition') }} as condition
        on condition.encounter_id = encounter.encounter_id
        and condition.patient_id = patient.patient_id
    group by 1
),

change_tracking as (
    select
        week,
        unique_patients,
        lag(unique_patients) over (order by week) as prev_week_patients,
        unique_encounters,
        lag(unique_encounters) over (order by week) as prev_week_encounters,
        unique_observations,
        lag(unique_observations) over (order by week) as prev_week_observations,
        unique_conditions,
        lag(unique_conditions) over (order by week) as prev_week_conditions
    from weekly
)

select
    week,
    unique_patients,
    unique_patients - prev_week_patients as patients_vs_prev_week,

    unique_encounters,
    unique_encounters - prev_week_encounters as encounters_vs_prev_week,

    unique_observations,
    unique_observations - prev_week_observations as observations_vs_prev_week,

    unique_conditions,
    unique_conditions - prev_week_conditions as conditions_vs_prev_week
from change_tracking
