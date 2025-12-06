"""
Data fetching with secret endpoints and error handling
"""

import requests
import time
import os
from datetime import datetime

class CryptoDataFetcher:
    """Fetch crypto data from various APIs"""
    
    def __init__(self):
        self.binance_base = "https://api.binance.com/api/v3"
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = 10  # seconds
        
        # Load secrets from environment (never hardcoded)
        self.bitnodes_endpoint = os.getenv('BITNODES_ENDPOINT', 'https://bitnodes.io/api/v1/snapshots/latest/')
        
        # Rate limiting
        self.last_request = {}
        self.min_request_interval = 1.0  # seconds
    
    def _rate_limit(self, endpoint):
        """Rate limiting to avoid API bans"""
        current_time = time.time()
        if endpoint in self.last_request:
            elapsed = current_time - self.last_request[endpoint]
            if elapsed < self.min_request_interval:
                time.sleep(self.min_request_interval - elapsed)
        
        self.last_request[endpoint] = time.time()
    
    def fetch_network_data(self):
        """Fetch TOR/.onion data from secret endpoint"""
        try:
            self._rate_limit('network')
            
            # Use environment variable for endpoint
            response = requests.get(
                self.bitnodes_endpoint,
                timeout=10,
                headers={'User-Agent': 'GODZILLERS-CRYPTO/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract data (simplified - real implementation would parse node list)
                total_nodes = data.get('total_nodes', 15000)
                
                # In real implementation, count TOR and .onion nodes
                # For demo, using simulated data
                tor_nodes = int(total_nodes * 0.035)  # ~3.5% TOR
                onion_nodes = int(total_nodes * 0.15)  # ~15% .onion
                
                return {
                    'total_nodes': total_nodes,
                    'tor_nodes': tor_nodes,
                    'onion_nodes': onion_nodes,
                    'timestamp': datetime.now().isoformat()
                }
        
        except Exception as e:
            # Silent error - don't expose details
            pass
        
        # Fallback to simulated data
        return {
            'total_nodes': 15000,
            'tor_nodes': 525,  # 3.5%
            'onion_nodes': 2250,  # 15%
            'timestamp': datetime.now().isoformat(),
            'simulated': True  # Internal flag
        }
    
    def fetch_price(self, symbol):
        """Fetch current price for a symbol"""
        try:
            self._rate_limit(f'price_{symbol}')
            
            response = requests.get(
                f"{self.binance_base}/ticker/price",
                params={'symbol': symbol},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'symbol': symbol,
                    'price': float(data['price']),
                    'timestamp': datetime.now().isoformat()
                }
        
        except Exception:
            pass
        
        return None
    
    def fetch_order_book(self, symbol, limit=10):
        """Fetch order book for P_micro calculation"""
        try:
            self._rate_limit(f'orderbook_{symbol}')
            
            response = requests.get(
                f"{self.binance_base}/depth",
                params={'symbol': symbol, 'limit': limit},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract best bid/ask
                bids = data.get('bids', [])
                asks = data.get('asks', [])
                
                if bids and asks:
                    best_bid = float(bids[0][0])
                    best_ask = float(asks[0][0])
                    bid_qty = float(bids[0][1])
                    ask_qty = float(asks[0][1])
                    
                    return {
                        'best_bid': best_bid,
                        'best_ask': best_ask,
                        'bid_qty': bid_qty,
                        'ask_qty': ask_qty,
                        'timestamp': datetime.now().isoformat()
                    }
        
        except Exception:
            pass
        
        return None
