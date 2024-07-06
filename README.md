<p align="center">
<img height="150" width="150" src="https://cdn.simpleicons.org/apacheairflow/gray"/>
</p>

<h1 align="center">Coinbase Airflow Pipeline (README FILE IN PROGRESS)</h1>
</p>

This repository contains an Airflow DAG (coinbase_elt_dag_s3_postgres) designed to automate the extraction, loading to Minio S3 with versioning, and transformation of data from the Coinbase API into PostgreSQL. The DAG fetches spot prices for BTC-USD, ETH-USD, and LTC-USD on a daily basis, storing them first in a Minio S3 bucket and then transforming them into a PostgreSQL database. It includes error handling, retry mechanisms, and email alerts for failures, ensuring reliable data processing and storage.

---

## Table of Contents

1. [Architecture Diagram](#architecture-diagram)
2. [DAG Run](#dag-run)
3. [S3 Bucket](#s3-bucket)
4. [PostgreSQL Database](#postgresql-database)
5. [Visualization](#visualization)
6. [Setup Instructions](#setup-instructions)
7. [Usage](#usage)

---

## Architecture Diagram

![1_S3VwV6_Gr5IzCSWUgarX4A](https://github.com/narwhalhorned/coinbase-data-pipeline/assets/94519064/7fa81f5e-4fee-411e-a541-ed9b852337b5)

### Key Features:
- Automated extraction of cryptocurrency spot prices from Coinbase API.
- Versioned storage of data in Minio S3 to manage updates and revisions.
- Transformation of JSON data into PostgreSQL tables for analytics and reporting.
- Error handling and retry mechanisms to ensure data reliability.
- Email alerts on task failures for proactive monitoring and maintenance.


#### Example:
