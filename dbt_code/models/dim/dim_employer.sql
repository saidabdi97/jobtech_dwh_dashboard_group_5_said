with src_employer as (select * from {{ ref('src_employer') }})


select
    {{ dbt_utils.generate_surrogate_key(['WORKPLACE_ADDRESS__REGION_CONCEPT_ID']) }} AS employer_id,
    EMPLOYER__NAME,
    EMPLOYER__WORKPLACE,
    EMPLOYER__ORGANIZATION_NUMBER,
    WORKPLACE_STREET_ADRESS,
    WORKPLACE_REGION,
    WORKPLACE_POSTCODE,
    WORKPLACE_ADDRESS__REGION_CONCEPT_ID,
    WORKPLACE_CITY,
    WORKPLACE_COUNTRY
from src_employer
