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
    DESCRIPTION__TEXT AS DESCRIPTION,
    DESCRIPTION__TEXT_FORMATTED,
    EMPLOYMENT_TYPE__LABEL AS EMPLOYMENT_TYPE,
    DURATION__LABEL AS DURATION,
    SALARY_TYPE__LABEL AS SALARY_TYPE,
    SCOPE_OF_WORK__MIN,
    SCOPE_OF_WORK__MAX
from stg_job_ads
order by application_deadline