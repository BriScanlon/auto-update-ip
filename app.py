import os
import time
import requests
import logging
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
IP_LOOKUP_URL = os.getenv('IP_LOOKUP_URL', 'https://api.ipify.org')
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4"
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
CHECK_INTERVAL_SECONDS = 3600  # 1 hour

# Function to get the external IP address
def get_external_ip():
    try:
        response = requests.get(IP_LOOKUP_URL, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except RequestException as e:
        logging.error(f"Failed to fetch external IP: {e}")
        return None

# Function to get all A records from Cloudflare
def get_a_records():
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    url = f"{CLOUDFLARE_API_URL}/zones/{ZONE_ID}/dns_records?type=A"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        records = response.json()
        if records.get('success'):
            return records.get('result', [])
        else:
            logging.error(f"Error fetching A records: {records.get('errors')}")
            return []
    except RequestException as e:
        logging.error(f"Failed to fetch A records: {e}")
        return []

# Function to update an A record
def update_a_record(record):
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    url = f"{CLOUDFLARE_API_URL}/zones/{ZONE_ID}/dns_records/{record['id']}"
    payload = {"type": "A", "name": record['name'], "content": record['content'], "ttl": 1, "proxied": record['proxied']}

    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if result.get('success'):
            logging.info(f"Successfully updated record {record['name']} to IP {record['content']}")
        else:
            logging.error(f"Error updating record {record['name']}: {result.get('errors')}")
    except RequestException as e:
        logging.error(f"Failed to update record {record['name']}: {e}")

# Main function
def main():
    last_ip = None

    while True:
        logging.info("Checking external IP...")
        current_ip = get_external_ip()

        if not current_ip:
            logging.warning("Could not determine external IP. Skipping this cycle.")
        elif current_ip != last_ip:
            logging.info(f"IP has changed to {current_ip}. Updating A records...")
            a_records = get_a_records()
            print(a_records)

            for record in a_records:
                record['content'] = current_ip  # Update the IP address
                print(f"Record: {record['content']}")
                update_a_record(record)

            last_ip = current_ip
        else:
            logging.info("IP address has not changed. No updates needed.")

        logging.info(f"Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    if not API_TOKEN or not ZONE_ID:
        logging.error("CLOUDFLARE_API_TOKEN and CLOUDFLARE_ZONE_ID must be set as environment variables.")
        exit(1)
    main()
