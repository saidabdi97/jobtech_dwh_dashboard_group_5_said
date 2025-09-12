with job_ads as (select * from {{ ref('src_job_ads') }})

select
    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as occupation_id,
    {{ dbt_utils.generate_surrogate_key(['HEADLINE']) }} AS job_details_id,
    {{ dbt_utils.generate_surrogate_key(['WORKPLACE_ADDRESS__REGION_CONCEPT_ID']) }} AS employer_id,
    {{ dbt_utils.generate_surrogate_key(['experience_required', 'access_to_own_car','driving_license_required']) }} as auxilliary_attributes_id,
    vacancies,
    relevance,
    application_deadline
from job_ads