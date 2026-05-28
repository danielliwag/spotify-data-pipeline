# Spotify ETL Data Pipeline

An end-to-end, production-grade data pipeline that extracts a user's recent listening history from the Spotify Web API, loads the data incrementally into a local PostgreSQL instance, and cleanses/transforms it using dbt (Data Build Tool). The entire workflow is fully containerized and orchestrated using Apache Airflow via Astronomer Cosmos.

## Architecture Overview
<img width="7116" height="2806" alt="SP_diagram" src="https://github.com/user-attachments/assets/29c72f42-a7c6-46a9-aedb-cb4d35bc24cd" /><br>

**Extract and Load (E-L)**: A Python script uses the spotipy library to authenticate via OAuth2 (user-read-recently-played scope). It handles data ingestion using native cursor-based pagination, extracting the after cursor token directly from the Spotify API response metadata to sequentially fetch upcoming pages of listening history. The net-new records are then appended to the staging table in PostgreSQL via psycopg2.

**Transform (T)**: dbt runs modular SQL transformations and generic data test on the raw data to generate clean, analytics-ready dimensional and fact tables back inside PostgreSQL.

**Orchestration**: Apache Airflow handles the workflow scheduling. Astronomer Cosmos dynamically renders the dbt project as native Airflow task groups.

## Tech Stack
- **Orchestration**: Apache Airflow, Astronomer Cosmos
- **Transformation**: dbt-core, dbt-postgres
- **Language/Libraries**: Python 3, Spotipy, Psycopg2
- **Containerization**: Docker


