from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json

# Define the DAG
with DAG(
    dag_id='etl_pipeline',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    # Step 1: Create the table if it doesn't exist
    @task
    def create_table():
        """
        Creates the 'apod_data' table in PostgreSQL if it does not already exist.
        This ensures data consistency and prevents schema issues.
        """
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE UNIQUE,
            media_type VARCHAR(50)
        );
        """
        # Execute table creation query
        postgres_hook.run(create_table_query, autocommit=True)

    # Step 2: Extract data from NASA's APOD API
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  # Connection ID in Airflow for NASA API
        endpoint='planetary/apod',  # API endpoint for APOD
        method='GET',
        data={"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"},  # API Key retrieved from Airflow connection
        response_filter=lambda response: response.json(),  # Convert API response to JSON
    )

    # Step 3: Transform the API response to extract necessary fields
    @task
    def transform_apod_data(response):
        """
        Extracts relevant fields from the API response and formats them properly.
        Ensures missing fields do not break the pipeline.
        """
        return {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }

    # Step 4: Load transformed data into PostgreSQL
    @task
    def load_data_to_postgres(apod_data):
        """
        Inserts the transformed APOD data into PostgreSQL.
        Ensures no duplicate 'date' values exist before inserting.
        """
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')

        # Check if record with the same 'date' already exists
        check_query = "SELECT COUNT(*) FROM apod_data WHERE date = %s"
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        with postgres_hook.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(check_query, (apod_data['date'],))
                (exists,) = cursor.fetchone()

                if exists == 0:  # Only insert if no duplicate exists
                    cursor.execute(insert_query, (
                        apod_data['title'],
                        apod_data['explanation'],
                        apod_data['url'],
                        apod_data['date'],
                        apod_data['media_type']
                    ))
                    conn.commit()


    # Define Task Dependencies
    create_table() >> extract_apod  # Ensure table creation before extraction
    api_response = extract_apod.output
    transformed_data = transform_apod_data(api_response)  # Transform API response
    load_data_to_postgres(transformed_data)  # Load transformed data into DB
