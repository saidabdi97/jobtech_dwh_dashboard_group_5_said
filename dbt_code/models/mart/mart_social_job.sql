with
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }}),
    dim_job_details as (select * from {{ ref('dim_job_details') }}),
    dim_employer as (select * from {{ ref('dim_employer') }})
select
    f.vacancies,
    f.relevance,
    e.employer__name,
    o.occupation,
    j.headline, 
    o.occupation_group,
    o.occupation_field,
    j.description,
    e.workplace_region,
    f.application_deadline
from fct_job_ads f
left join dim_occupation o on f.occupation_id = o.occupation_id
left join dim_job_details j on f.job_details_id = j.job_details_id 
left join dim_employer e on f.employer_id = e.employer_id 
where o.occupation_field = 'Yrken med social inriktning';
