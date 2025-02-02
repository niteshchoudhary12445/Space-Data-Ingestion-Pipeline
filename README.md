# ETL Pipeline for NASA APOD Data using Apache Airflow

## Overview
This ETL pipeline fetches data from NASA's Astronomy Picture of the Day (APOD) API, transforms it, and stores it in a PostgreSQL database. The pipeline is managed using Apache Airflow and can be deployed on Astronomer.

## Features
- **Extract**: Fetches data from NASA's APOD API.  
- **Transform**: Cleans and formats the data.  
- **Load**: Stores data in a PostgreSQL database.  
- **Automated Scheduling**: Runs daily using Apache Airflow.  
- **Idempotent Storage**: Avoids duplicate entries based on the date field.  

## Prerequisites
- Docker & Docker Compose  
- Apache Airflow (Managed via Astronomer)  
- PostgreSQL Database  
- Astronomer CLI  

## Installation & Setup

### 1. Install Astronomer CLI
```sh
winget install -e --id Astronomer.Astro
```

### 2. Initialize an Astronomer Project
```sh
astro dev init
```

### 3. Start the Local Airflow Instance
```sh
astro dev start
```

### 4. Stop the Local Airflow Instance
```sh
astro dev stop
```

## Airflow DAG Breakdown

### **DAG File:** `etl_pipeline.py`
- **`create_table`**: Ensures the `apod_data` table exists in PostgreSQL.  
- **`extract_apod`**: Fetches data from NASA's APOD API.  
- **`transform_apod_data`**: Extracts required fields from the API response.  
- **`load_data_to_postgres`**: Inserts transformed data into the PostgreSQL database, ensuring no duplicate entries.  

## Airflow Connection Setup

Ensure you have the following Airflow connections set up:

### **PostgreSQL Connection (`my_postgres_connection`)**
- **Connection ID**: `my_postgres_connection`  
- **Host**: `<your_db_host>`  
- **Schema**: `<your_db_name>`  
- **Login**: `<your_db_user>`  
- **Password**: `<your_db_password>`  

### **NASA API Connection (`nasa_api`)**
- **Connection ID**: `nasa_api`  
- **Extra JSON**:  
```json
{
  "api_key": "your_nasa_api_key"
}
```

## Deploying on Astronomer

### 1. Login to Astronomer
```sh
astro login
```

### 2. Deploy to Astronomer
```sh
astro deploy
```

## Running the DAG
1. Navigate to the Airflow UI: [http://localhost:8080](http://localhost:8080).  
2. Enable and trigger the `etl_pipeline` DAG.  

## Troubleshooting
- Ensure **Docker** is running.  
- Verify **Airflow connections** (`Admin -> Connections`).  
- Check **Airflow logs** if a task fails.  
