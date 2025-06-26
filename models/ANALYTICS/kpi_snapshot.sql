with base as(
    select
        current_date as snapshot_date,
        count(distinct patient.patient_id) as num_patients,
        count(distinct encounter.encounter_id) as num_encounters,
        count(distinct condition.condition_id) as num_conditions,
        avg(observation.result_value::float) as avg_observation_value
    from {{ ref('stage_patient') }} as patient
    left join {{ ref('stage_encounter') }} as encounter
        on patient.patient_id = encounter.patient_id
    left join {{ ref('stage_condition') }} as condition
        on patient.patient_id = condition.patient_id
    left join {{ ref('stage_observation') }} as observation
        on patient.patient_id = observation.patient_id
    group by 1
)


select * from base