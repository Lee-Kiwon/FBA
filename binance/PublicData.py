import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class PublicData:
    def __init__(self):
        
    
    def get_data(self,symbol, start, end):
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    
    current_date = start
    while current_date <= end:
        formatted_date = current_date.strftime('%Y-%m-%d')
        url = f'https://data.binance.vision/data/futures/um/daily/klines/{symbol}/1d/{symbol}-1d-{formatted_date}.zip'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(f'{symbol}-1d-{formatted_date}.zip', 'wb') as f:
                f.write(response.content)
            print(f'Data for {symbol} on {formatted_date} saved.')
        else:
            print(f'Error downloading data for {symbol} on {formatted_date}. Status code: {response.status_code}')
        
        current_date += timedelta(days=1)
        
    def get_symbols(self):
        url = 'https://data.binance.vision/data/futures/um/daily/klines/'
        response = requests.get(url)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            symbols = []
            for a_tag in soup.find_all('a'):
                href = a_tag.get('href')
                if href and href.endswith('.zip'):
                    symbol = href.split('/')[0]
                    symbols.append(symbol)
            return symbols
        else:
            print('Failed to fetch symbols. Status code:', response.status_code)
            return []