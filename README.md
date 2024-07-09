<p align="center">
<img height="150" width="150" src="https://cdn.simpleicons.org/apacheairflow/gray"/>
</p>

<h1 align="center">Coinbase Airflow Pipeline (README FILE IN PROGRESS)</h1>

This repository contains an Airflow DAG designed to automate the extraction, loading to Minio S3 with versioning, and transformation of data from the Coinbase API into PostgreSQL. The DAG fetches spot prices for BTC-USD, ETH-USD, and LTC-USD on a daily basis, storing them first in a Minio S3 bucket and then transforming them into a PostgreSQL database. It includes error handling, retry mechanisms, and email alerts for failures, ensuring reliable data processing and storage.

---

## Table of Contents

1. [Data Pipeline Diagram](#data-pipeline-diagram)
2. [DAG Run](#dag-run)
3. [S3 Bucket](#s3-bucket)
4. [PostgreSQL Database](#postgresql-database)
5. [Visualization](#visualization)
6. [Setup Instructions](#setup-instructions)
7. [Usage](#usage)
8. [Contact](#contact)

---

## Data Pipeline Diagram

![diagram1](https://github.com/narwhalhorned/coinbase-data-pipeline/assets/94519064/47623b58-bb4d-4440-bb2d-2b923237f654)

### Key Features:
- **Automated Data Extraction**: Fetches cryptocurrency spot prices from Coinbase API daily.
- **Versioned Storage in Minio S3**: Stores multiple versions of data files, managing updates and revisions.
- **Data Transformation**: Converts JSON data into structured PostgreSQL tables.
- **Error Handling**: Incorporates retry mechanisms and error alerts to maintain data integrity.
- **Email Alerts**: Notifies users of task failures or task retries for proactive monitoring.

---

## DAG Run

### Overview:
The DAG runs daily at midnight UTC, ensuring fresh data is available for analysis every day.

#### Screenshot:
![DAG Run](https://path/to/your/dag_run_image.png)

---

## S3 Bucket

### Overview:
The Minio S3 bucket stores the JSON data files retrieved from the Coinbase API, with versioning to manage multiple data snapshots.

#### Screenshot:
![S3 Bucket](https://path/to/your/s3_bucket_image.png)

---

## PostgreSQL Database

### Overview:
Transformed data is stored in a PostgreSQL database, making it accessible for analytics and reporting.

#### Schema:
- **Table Name**: `coinbase_data`
- **Columns**:
  - `id`: Primary Key
  - `timestamp`: DateTime
  - `btc_to_usd_rate`: Float
  - `eth_to_usd_rate`: Float
  - `ltc_to_usd_rate`: Float

#### Screenshot:
![PostgreSQL Database](https://path/to/your/postgresql_database_image.png)

---

## Visualization

### Power BI Reports:
Visualizations include card charts for the latest BTC, ETH, and LTC rates, as well as a year-over-year growth chart.

#### Screenshots:
- **Card Charts**: ![Card Charts](https://path/to/your/card_charts_image.png)
- **Year-Over-Year Growth**: ![YoY Growth](https://path/to/your/yoy_growth_image.png)

---

## Setup Instructions

### Prerequisites:
- Docker
- Docker Compose

### Installation Steps:
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/narwhalhorned/coinbase-data-pipeline.git
    cd coinbase-data-pipeline
    ```

2. **Start Docker Containers**:
    - Make sure Docker is running on your machine.
    - Build and start the Docker containers using Docker Compose:
    ```sh
    docker-compose up --build
    ```

3. **Configure Airflow**:
    - Access the Airflow web interface at `http://localhost:8081`.
    - Set up the necessary connections and variables in Airflow using `airflow.cfg`.

4. **Set Up Minio**:
    - Access Minio at `http://localhost:9001`.
    - Follow Minio's documentation to create your S3 bucket.

5. **Initialize PostgreSQL**:
    - Access the PostgreSQL database using your preferred client. For this project I used `DBeaver`.
    - Create the necessary database and tables.

---

## Usage

### Triggering the DAG:
- The DAG is scheduled to run daily at midnight UTC.

### Monitoring:
- Check the status of the DAG and its tasks via the Airflow web interface.
- Receive email alerts on task failures or on task retries for quick issue resolution.

---

## Data Access

### For Data Analysts:
- An Excel workbook is included for data analysts to easily access and analyze the data.
- Data analysts can also connect directly to the PostgreSQL database for more advanced queries and analysis.

### For Data Scientists:
- Data scientists can directly access the data stored in the S3 bucket or PostgreSQL database for advanced analytics and modeling.

---

## Contact

For questions or issues, please open an issue in this repository or contact me personally.

---
