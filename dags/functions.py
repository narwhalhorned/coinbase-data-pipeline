import json
import logging
from datetime import datetime
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def extract_data(date_for_spot_price):
    url_spot_btc_usd = f"https://api.coinbase.com/v2/prices/BTC-USD/spot?date={date_for_spot_price}"
    url_spot_eth_usd = f"https://api.coinbase.com/v2/prices/ETH-USD/spot?date={date_for_spot_price}"
    url_spot_ltc_usd = f"https://api.coinbase.com/v2/prices/LTC-USD/spot?date={date_for_spot_price}"

    response_spot_btc_usd = requests.get(url_spot_btc_usd)
    response_spot_eth_usd = requests.get(url_spot_eth_usd)
    response_spot_ltc_usd = requests.get(url_spot_ltc_usd)
    
    spot_data_btc_usd = response_spot_btc_usd.json()
    spot_data_eth_usd = response_spot_eth_usd.json()
    spot_data_ltc_usd = response_spot_ltc_usd.json()
    
    btc_to_usd_rate = float(spot_data_btc_usd['data']['amount'])
    eth_to_usd_rate = float(spot_data_eth_usd['data']['amount'])
    ltc_to_usd_rate = float(spot_data_ltc_usd['data']['amount'])
    
    data = {
        'btc_to_usd_rate': btc_to_usd_rate,
        'eth_to_usd_rate': eth_to_usd_rate,
        'ltc_to_usd_rate': ltc_to_usd_rate,
        'data_date': date_for_spot_price
    }
    
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    filename = f"/tmp/coinbase_data_{date_for_spot_price}_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f)
    
    logging.info(f"Extracted data from Coinbase and saved to file: {filename}")
    return filename

def load_data_to_s3(filename, current_date):
    s3_hook = S3Hook(aws_conn_id="minio_conn")
    
    s3_prefix = f"coinbase-data/{current_date}"
    s3_key_original = f"{s3_prefix}/{filename.split('/')[-1]}"
    
    if not s3_hook.check_for_key(key=s3_key_original, bucket_name="airflow"):
        s3_hook.load_file(
            filename=filename,
            key=s3_key_original,
            bucket_name="airflow",
            replace=True
        )
        logging.info(f"Uploaded data to S3: {s3_key_original.split('/')[-1]}")
        return s3_key_original
    
    existing_folders = s3_hook.list_keys(bucket_name="airflow", prefix=s3_prefix + '_v')
    
    version_numbers = []
    
    if existing_folders:
        logging.info(f"Existing versioned folders in S3: {existing_folders}")
        
        for folder in existing_folders:
            folder_name = folder.split('/')[-1] 
            if folder_name.startswith(f"{current_date}_v"):
                try:
                    version_number_str = folder_name.split('_v')[-1]
                    version_numbers.append(int(version_number_str))
                except ValueError:
                    logging.warning(f"Skipping folder {folder} due to invalid version number format.")
    
    latest_version = max(version_numbers) if version_numbers else 0
    version_suffix = f'_v{latest_version + 1}'
    
    s3_key_new_version = f"{s3_prefix}{version_suffix}/{filename.split('/')[-1]}"
    
    s3_hook.load_file(
        filename=filename,
        key=s3_key_new_version,
        bucket_name="airflow",
        replace=True
    )
    
    logging.info(f"Uploaded data to new versioned S3 folder: {s3_key_new_version.split('/')[-1]}")
    return s3_key_new_version

def transform_data_to_postgres(s3_key):
    filename = f"/tmp/{s3_key.split('/')[-1]}"
    
    s3_hook = S3Hook(aws_conn_id="minio_conn")
    s3_hook.get_key(
        key=s3_key,
        bucket_name="airflow"
    ).download_file(filename)

    with open(filename, "r") as f:
        data = json.load(f)

    logging.info(f"Transformed data from file: {filename}. Data: {data}")

    hook = PostgresHook(postgres_conn_id="postgres_localhost")  # Check connection ID
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.coinbase_data (
        id SERIAL PRIMARY KEY,
        btc_to_usd_rate FLOAT,
        eth_to_usd_rate FLOAT,
        ltc_to_usd_rate FLOAT,
        data_date DATE UNIQUE,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    try:
        cursor.execute("""
        INSERT INTO public.coinbase_data (btc_to_usd_rate, eth_to_usd_rate, ltc_to_usd_rate, data_date, ts)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (data_date) DO NOTHING;
        """, (data['btc_to_usd_rate'], data['eth_to_usd_rate'], data['ltc_to_usd_rate'], data['data_date'], datetime.utcnow()))

        conn.commit()
        logging.info(f"Transformed and loaded data to PostgreSQL from file: {filename}")
    except Exception as e:
        logging.error(f"Error inserting data into PostgreSQL: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
