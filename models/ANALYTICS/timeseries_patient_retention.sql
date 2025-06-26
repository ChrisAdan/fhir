with encounters as (
    select
        patient_id,
        encounter_id,
        date_trunc('day', encounter_start) as encounter_day
    from {{ ref('stage_encounter') }}
),

cohorts as (
    select 
        patient_id,
        min(encounter_day) as cohort_day
    from encounters
    group by 1
),

date_tracking as (
    select
        encs.encounter_day,
        encs.encounter_id,
        encs.patient_id,
        cohorts.cohort_day,
        datediff('day', cohorts.cohort_day, encs.encounter_day) as date_index
    from encounters as encs
    left join cohorts
        on encs.patient_id = cohorts.patient_id
),

daily_agg as (
    select
        encounter_day,
        cohort_day,
        date_index,
        case when encounter_day = cohort_day then 'New' else 'Returning' end as new_or_returning,
        count(distinct patient_id) as unique_patients,
        count(encounter_id) as total_encounters
    from date_tracking
    group by 1, 2, 3, 4
)

select * from daily_agg