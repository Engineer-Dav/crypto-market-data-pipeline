import requests

def get_crypto_data():
    try:
        BASE_URL = "https://api.coingecko.com/api/v3"
        ENDPOINT = "/coins/markets"
        url = BASE_URL + ENDPOINT
        params = {
            "vs_currency": "usd",
            "per_page": 20,
            "page": 1
            }
        response = requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print("API Error:",e)
        return None
    except Exception as e:
        print("Error:",e)
        return None
