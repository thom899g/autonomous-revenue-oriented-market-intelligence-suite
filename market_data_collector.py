import logging
from typing import Dict, Any
import requests

class MarketDataCollector:
    def __init__(self, api_keys: Dict[str, str], data_sources: Dict[str, str]):
        self.api_keys = api_keys
        self.data_sources = data_sources
        self.session = requests.Session()
        logging.basicConfig(
            filename='market_data_collector.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def fetch_data(self, source: str) -> Dict[str, Any]:
        """
        Fetches market data from a specified source.
        
        Args:
            source: Name of the data provider
            
        Returns:
            Dictionary containing the fetched data
        Raises:
            ConnectionError if API call fails
            ValueError if data parsing fails
        """
        try:
            api_key = self.api_keys.get(source, None)
            if not api_key:
                raise ValueError(f"No API key found for source: {source}")
            
            response = self.session.get(self.data_sources[source], headers={'Authorization': f'Bearer {api_key}'})
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed to {source}: {str(e)}")
            raise ConnectionError(f"Failed to fetch data from {source}")
        except ValueError as e:
            logging.error(f"Data parsing error: {str(e)}")
            raise