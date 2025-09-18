# HR Analytics Data Warehouse - Group 5

## Project Overview

This project implements a modern data stack to solve real-world HR analytics challenges for a talent acquisition agency. Our solution automates the extraction, transformation, and analysis of job market data from Arbetsförmedlingen to help talent acquisition specialists make data-driven decisions.

## Architecture

Our data pipeline follows the modern data stack approach with these components:

```
Jobtech API → dlt → Snowflake → dbt → Streamlit Dashboard
```

- **Data Source**: Jobtech API (Arbetsförmedlingen)
- **Data Ingestion**: dlt (data load tool)
- **Data Warehouse**: Snowflake
- **Data Transformation**: dbt (data build tool)
- **Analytics Layer**: Streamlit Dashboard

## Data Model

### Dimensional Model Structure

**Fact Table:**
- `fact_job_ads` - Central fact table containing job posting metrics

**Dimension Tables:**
- `dim_occupation` - Occupation details and classifications
- `dim_employer` - Employer information
- `dim_location` - Geographic information (cities, regions)
- `dim_date` - Date dimension for time-based analysis

### Schema Organization
- **Staging Schema**: Raw data loaded by dlt
- **Data Warehouse Schema**: Cleaned and structured dimensional model
- **Mart Schema**: Business-ready views for specific occupation fields

## Getting Started

### Prerequisites
- Python 3.8+
- UV package manager
- Snowflake account
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/EfremDaniel/Data_warehouse_project_group_5.git
cd Data_warehouse_project_group_5
```

2. **Set up virtual environment**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv pip install -r requirements.txt
```

4. **Configure dbt**
```bash
dbt deps
```
Make sure your `profiles.yml` is configured with your Snowflake credentials.

5. **Set up environment variables**
Create a `.env` file with your Snowflake credentials:
```
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

## Usage

### Data Ingestion
Run the dlt pipeline to extract data from Jobtech API:
```bash
python scripts/load_job_ads.py
```

### Data Transformation
Execute dbt transformations:
```bash
dbt run
dbt test 
```

### Dashboard
Launch the Streamlit dashboard:
```bash
python dashboard/run_dashboard.py
```

## Data Quality & Testing
Run tests with:
```bash
dbt test
```

## Documentation

Generate and view dbt documentation:
```bash
dbt docs generate
dbt docs serve
```


##  Project Structure

```
Data_warehouse_project_group_5/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── scripts/
│   ├── load_job_ads.py
│   └── utils/
├── dbt_project/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   ├── warehouse/
│   │   └── marts/
│   ├── tests/
│   └── macros/
├── dashboard/
│   ├── app.py
│   ├── pages/
│   └── utils/
└── docs/
    └── project_documentation.md
```


## 👨‍💻 Team Members

- **Efrem**
- **Hampus** 
- **Said** 


## 📄 License

This project is part of an academic assignment and is for educational purposes.


**Note**: This project uses real data from Arbetsförmedlingen's Jobtech API for educational purposes. Please ensure compliance with their terms of service and data usage policies.