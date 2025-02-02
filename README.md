NASA APOD ETL Pipeline

Overview

This Airflow ETL pipeline extracts data from NASA's Astronomy Picture of the Day (APOD) API, transforms the data, and loads it into a PostgreSQL database. The pipeline ensures that duplicate records are not inserted by checking for existing entries based on the date field.

Features

Extracts daily APOD data from NASA's API.

Transforms data to retain only essential fields.

Loads data into a PostgreSQL database, avoiding duplicates.

Uses Airflow tasks for automation and scheduling.

Prerequisites

Apache Airflow installed and running.

PostgreSQL database configured.

Airflow Connections:

nasa_api: Configured with NASA API key.

my_postgres_connection: Configured PostgreSQL connection.

Python packages:

pip install apache-airflow apache-airflow-providers-postgres apache-airflow-providers-http psycopg2

Setup Instructions

1. Configure Airflow Connections

NASA API Connection (nasa_api)

Navigate to Airflow UI → Admin → Connections → Create

Set Connection Id = nasa_api

Set Connection Type = HTTP

In Extra, add:

{"api_key": "your_nasa_api_key"}

PostgreSQL Connection (my_postgres_connection)

Navigate to Airflow UI → Admin → Connections → Create

Set Connection Id = my_postgres_connection

Set Connection Type = Postgres

Fill in:

Host: localhost (or your PostgreSQL server IP)

Schema: Your database name

Login: Your database username

Password: Your database password

Port: 5432

2. Deploy the DAG

Save the pipeline script as etl_pipeline.py in the Airflow DAGs folder (~/airflow/dags/):

mv etl_pipeline.py ~/airflow/dags/

Restart Airflow services:

airflow scheduler restart
airflow webserver restart

Navigate to Airflow UI and enable the DAG etl_pipeline.

Pipeline Structure

1. Create Table (create_table task)

Ensures the apod_data table exists in PostgreSQL.

Defines schema with a unique date column to prevent duplicates.

2. Extract APOD Data (extract_apod task)

Calls NASA's APOD API to fetch the latest astronomy picture details.

Uses Airflow’s SimpleHttpOperator to extract JSON data.

3. Transform Data (transform_apod_data task)

Extracts essential fields (title, explanation, url, date, media_type).

Ensures missing fields do not cause errors.

4. Load Data into PostgreSQL (load_data_to_postgres task)

Checks if the date already exists in the database.

Inserts new data only if it's not a duplicate.

DAG Workflow

(create_table) → (extract_apod) → (transform_apod_data) → (load_data_to_postgres)

Monitoring and Debugging

Check logs for errors:

airflow tasks logs -d etl_pipeline load_data_to_postgres

Verify database entries:

SELECT * FROM apod_data;

Restart a failed task manually:

airflow tasks run etl_pipeline load_data_to_postgres <dag_run_id>

Future Enhancements

Implement notifications for failures (e.g., via Slack or email).

Extend data storage to cloud-based solutions.

Add error handling for API failures.

This ETL pipeline provides a reliable method for automating NASA APOD data collection and storage. 🚀

