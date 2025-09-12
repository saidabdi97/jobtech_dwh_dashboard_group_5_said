with src_job_details as (select * from {{ ref('src_job_details') }})

select
    {{ dbt_utils.generate_surrogate_key(['HEADLINE']) }} AS job_details_id,
    HEADLINE,
    DESCRIPTION, 
    DESCRIPTION__TEXT_FORMATTED,
    EMPLOYMENT_TYPE,
    DURATION,
    SALARY_TYPE,
    SCOPE_OF_WORK__MIN,
    SCOPE_OF_WORK__MAX
from src_job_details