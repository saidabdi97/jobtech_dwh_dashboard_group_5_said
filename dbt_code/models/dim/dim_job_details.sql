with src_job_details as (select * from {{ ref('src_job_details') }})

select
    {{ dbt_utils.generate_surrogate_key(['ID']) }} AS job_details_id,
    ID,
    MAX(HEADLINE),
    MAX(DESCRIPTION), 
    MAX(DESCRIPTION__TEXT_FORMATTED),
    MAX(EMPLOYMENT_TYPE),
    MAX(DURATION),
    MAX(SALARY_TYPE),
    MAX(SCOPE_OF_WORK__MIN),
    MAX(SCOPE_OF_WORK__MAX)
from src_job_details
group by ID