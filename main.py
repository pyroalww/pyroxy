import requests
import random
import logging
import json
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ProxyError, ConnectTimeout, SSLError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_proxies(proxy_type='https'):
    url = f'https://www.proxy-list.download/api/v1/get?type={proxy_type}'
    try:
        logging.info("Retrieving proxies...")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
        proxies = response.text.split('\r\n')
        proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
        return proxies
    except requests.exceptions.RequestException as e:
        logging.error("Failed to retrieve proxies:", e)
        return []

def validate_proxy(proxy):
    try:
        logging.info(f"Validating proxy: {proxy}")
        response = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=10)
        response.raise_for_status()
        logging.info(f"Proxy validation successful: {proxy}")
        return True
    except (ProxyError, ConnectTimeout, SSLError):
        logging.warning(f"Proxy validation failed: {proxy}")
        return False
    except requests.exceptions.RequestException as e:
        logging.error("Failed to validate proxy:", e)
        return False

def save_proxies(proxies, filename='validated_proxies.json'):
    with open(filename, 'w') as file:
        json.dump(proxies, file)
    logging.info(f"Validated proxies saved to {filename}")

def load_proxies(filename='validated_proxies.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            proxies = json.load(file)
        logging.info(f"Validated proxies loaded from {filename}")
        return proxies
    else:
        logging.warning(f"No validated proxy file found: {filename}")
        return []

def rotate_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    return random.choice(user_agents)

def make_request(url, proxies, headers=None):
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504], 
                        allowed_methods=["GET"])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # Rotate user agents
        session.headers.update({'User-Agent': rotate_user_agent()})
        
        # Make request using a random proxy
        proxy = random.choice(proxies)
        session.proxies = {'http': proxy, 'https': proxy}
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error("Failed to make request:", e)
        return None

if __name__ == "__main__":
    filename = 'validated_proxies.json'
    if os.path.exists(filename):
        proxies = load_proxies(filename)
    else:
        proxies = get_proxies(proxy_type='https')
        if proxies:
            validated_proxies = [proxy for proxy in proxies if validate_proxy(proxy)]
            if validated_proxies:
                save_proxies(validated_proxies, filename)
    
    if proxies:
        logging.info("Proxy list:")
        for proxy in proxies:
            logging.info(proxy)
        
       # Random request for testing proxy
        url = 'https://httpbin.org/ip'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
        response = make_request(url, proxies, headers=headers)
        if response:
            logging.info("Response:")
            logging.info(response)
        else:
            logging.error("Failed to make request using a proxy.")
    else:
        logging.error("No proxies available.")
