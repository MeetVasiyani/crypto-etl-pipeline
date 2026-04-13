import requests
import time
import logging

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_crypto_data(page : int,per_page : int = 50,retries : int = 3):
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page
    }
    
    for attempt in range(retries):
        
        try:
            response = requests.get(BASE_URL,params=params,timeout=10)
            
            if(response.status_code == 200):
                return response.json()
            
            logging.warning(f"Attempt {attempt+1}: Failed with status {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt+1}: Request failed : {e}")
        
        time.sleep(2)
        
    logging.error("Max retries reached. Returning empty list.")
    
    return []


def fetch_all_crypto_data(pages : int = 2):
    all_data = []
    
    for page in range(1,pages+1):
        logging.info(f"Fetching page {page}")
        
        data = fetch_crypto_data(page)
        
        if not data:
            logging.warning(f"No data returned for the page {page}")
            continue
        
        all_data.extend(data)
        
        time.sleep(1)
    
    return all_data
