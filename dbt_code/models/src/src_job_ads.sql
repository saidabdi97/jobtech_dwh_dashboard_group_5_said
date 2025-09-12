with stg_job_ads as (select * from {{ source('hr_project_db', 'stg_ads') }})

select 
    occupation__label,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline,
    experience_required,
    access_to_own_car,
    driving_license_required,
    HEADLINE,
    WORKPLACE_ADDRESS__REGION_CONCEPT_ID,
from stg_job_ads
order by application_deadline