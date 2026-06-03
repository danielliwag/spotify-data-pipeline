# Data Engineering Documentation: Spotify Listening History Pipeline

## 1. Document Control & Overview
- **Project Name**: Spotify Data Pipeline
- **System Architecture Pattern**: ELT (Extract, Load, Transform) via Star Schema
- **Language/Libraries**: Python 3, Spotipy, Psycopg2

### 1.1 Project Summary
The Spotify Listening History Pipeline automates the extraction of user listening history, playlist interactions, and track metadata from the Spotify Web API. This data is ingestion-loaded into a PostgreSQL data warehouse, transformed using dbt into a production-ready Star Schema, and orchestrated end-to-end using Apache Airflow (via Astronomer Cosmos in localized Docker containers).

## 2. System Architecture Overview
<img width="7116" height="2806" alt="SP_diagram" src="https://github.com/user-attachments/assets/29c72f42-a7c6-46a9-aedb-cb4d35bc24cd" /><br>

**Extract and Load (E-L)**: A Python script uses the spotipy library to authenticate via OAuth2 (user-read-recently-played scope). It handles data ingestion using native cursor-based pagination, extracting the after cursor token directly from the Spotify API response metadata to sequentially fetch upcoming pages of listening history. The net-new records are then appended to the staging table in PostgreSQL via psycopg2.

**Transform (T)**: dbt runs modular SQL transformations and generic data test on the raw data to generate clean, analytics-ready dimensional and fact tables back inside PostgreSQL.

**Orchestration**: Apache Airflow handles the workflow scheduling. Astronomer Cosmos dynamically renders the dbt project as native Airflow task groups.

## Technology Stack
- **Orchestration**: Apache Airflow, Astronomer Cosmos
- **Transformation**: dbt-core, dbt-postgres
- **Language/Libraries**: Python 3.12, Spotipy, Psycopg2
- **Containerization**: Docker

## 3. Data Architecture & Schema Design
I designed and implemented a hybrid Medallion Architecture and Star Schema framework within a single PostgreSQL instance. By utilizing this hybrid approach, I ensure that raw API data is preserved before it is cleaned, conformed, and structured into an optimized multi-dimensional model.

### 3.1 Raw / Ingestion Layer
Data is loaded with minimal transformation as append-only structures to preserve the historical API response payload.
- stg_spotify_raw: Raw JSONB/structured payload of recently played tracks.

### 3.2 Transformation / Staging Layer
Materialized as view. Cleans data types, renames columns to company conventions, flattens JSON arrays, and removes duplicates.
- **Models**: stg_spotify__recently_played.sql

### 3.3 Dimensional Model / Marts Layer
Materialized as tables. Modeled as a Star Schema optimized for high-performance BI querying.
- **Models** - fct_listens, dim_artist, dim_user, dim_track, dim_album

<img width="3744" height="2628" alt="Schema Design" src="https://github.com/user-attachments/assets/a723ca0c-f034-42b4-b515-8cf10b5f3b3d" />

## 4. Orchestration & DAG Design (Airflow + Cosmos)
The pipeline is completely automated via Airflow. I utilized Astronomer Cosmos to dynamically parse the dbt project directly into native Airflow task groups, removing the need for manifest generation workarounds.

### 4.1 Directory Structure
```
SPOTIFY-DATA-PIPELINE/
├── .venv/                            # Local Python virtual environment
├── dbt_airflow_dag/                  # Airflow Directory
│   ├── .astro/                       # Astronomer local configuration metadata
│   ├── dags/
│   │   ├── .airflowignore            # Files for Airflow scheduler to ignore
│   │   └── spotify_cosmos_pipeline.py # Main Airflow DAG orchestrating Cosmos
│   ├── include/
│   │   └── spotify_dbt/              # Core dbt project directory
│   │       ├── analyses/
│   │       ├── macros/
│   │       ├── models/
│   │       │   ├── marts/            # GOLD LAYER: Production Star Schema
│   │       │   └── staging/          # SILVER LAYER: Conformed staging views
│   │       ├── seeds/
│   │       ├── snapshots/
│   │       ├── tests/
│   │       ├── .gitignore
│   │       ├── dbt_project.yml       # dbt project configuration
│   │       ├── package-lock.yml
│   │       ├── packages.yml          # External dbt packages
│   │       └── README.md
│   ├── src/                          # Custom Python scripts / BRONZE LAYER: Insert raw API response to staging table
│   ├── plugins/                      # Custom Airflow plugins
│   └── tests/                        # CI/CD pipeline unit tests
├── .dockerignore                     # Files excluded from Docker builds
└── .env                              # Local environment credentials & tokens (git ignored)
```

### 4.2 DAG Topology & Task Flow

<img width="903" height="869" alt="airflow dag" src="https://github.com/user-attachments/assets/5c309d87-2679-458d-8eec-8a33bc0c4555" />

- ***1. extract_and_load_raw***: Custom PythonOperator running spotify_pipeline.py executing extract.py and load.py. It authenticates using the spotipy.oauth2 scope (user-read-recently-played), pulls incremental data, and writes to stg_spotify_raw table.
- ***2. transform_dbt (DbtTaskGroup)***: Cosmos dynamically translates the dbt_spotify project into a sequence of tasks:
  - stg_models runs first (upstream dependencies).
  - marts_models runs sequentially right after.
  - Data quality constraints (dbt test) are executed seamlessly at every step.

## 5. Security & Environment Configuration
Production environments must never hardcode credentials. All access tokens and database URLs are injected as runtime environment variables.

### Environment Matrix (.env)
```
AIRFLOW_CONN_MY_POSTGRES_CONNECTION="postgresql://database_user_here:database_password_here@host.docker.internal:5432/database_name_here"

CLIENT_ID='your_client_ID_here'
CLIENT_SECRET='your_client_secret_here'
REDIRECT_URI='http://127.0.0.1:8888/callback'
SCOPE='user-read-recently-played user-read-private'

DB_HOST='host.docker.internal'
DB_NAME='database_name_here'
DB_USER='database_user_here'
DB_PASS='database_password_here'
```

