USE ROLE SYSADMIN;

GRANT ROLE ACCOUNTADMIN TO USER hampus;
GRANT ROLE ACCOUNTADMIN TO USER said;

-- Ingest role
GRANT USAGE ON DATABASE hr_project_db TO ROLE ingest_role;
GRANT USAGE ON SCHEMA hr_project_db.staging TO ROLE ingest_role;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA hr_project_db.staging TO ROLE ingest_role;
GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA hr_project_db.staging TO ROLE ingest_role;


-- Transform role
GRANT USAGE ON DATABASE hr_project_db TO ROLE transform_role;
GRANT USAGE ON SCHEMA hr_project_db.staging TO ROLE transform_role;
GRANT SELECT ON ALL TABLES IN SCHEMA hr_project_db.staging TO ROLE transform_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA hr_project_db.staging TO ROLE transform_role;

GRANT USAGE ON SCHEMA hr_project_db.warehouse TO ROLE transform_role;
GRANT CREATE TABLE, CREATE VIEW ON SCHEMA hr_project_db.warehouse TO ROLE transform_role;
GRANT INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA hr_project_db.warehouse TO ROLE transform_role;

GRANT USAGE ON SCHEMA hr_project_db.marts TO ROLE transform_role;
GRANT CREATE VIEW ON SCHEMA hr_project_db.marts TO ROLE transform_role;

-- Analyst role
GRANT USAGE ON DATABASE hr_project_db TO ROLE analyst_role;
GRANT USAGE ON SCHEMA hr_project_db.marts TO ROLE analyst_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA hr_project_db.marts TO ROLE analyst_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA hr_project_db.marts TO ROLE analyst_role;

GRANT ROLE ingest_role TO ROLE SYSADMIN;
GRANT ROLE transform_role TO ROLE SYSADMIN;
GRANT ROLE analyst_role TO ROLE SYSADMIN;

-- check grants
SHOW GRANTS ON SCHEMA hr_project_db.staging;
SHOW GRANTS ON SCHEMA hr_project_db.warehouse;
SHOW GRANTS ON SCHEMA hr_project_db.marts;
SHOW FUTURE GRANTS IN SCHEMA hr_project_db.staging;
SHOW FUTURE GRANTS IN SCHEMA hr_project_db.warehouse;
SHOW FUTURE GRANTS IN SCHEMA hr_project_db.marts;

SHOW GRANTS TO ROLE ingest_role;
SHOW GRANTS TO ROLE transform_role;
SHOW GRANTS TO ROLE analyst_role;