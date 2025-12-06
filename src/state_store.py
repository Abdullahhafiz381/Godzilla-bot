"""
State persistence for TOR/.onion/P_micro values
"""

import json
import os
from datetime import datetime

class StateManager:
    """Manage state persistence between cycles"""
    
    def __init__(self, state_file="state_data.json"):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self):
        """Load state from file or create default"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default state
        return {
            'previous': {
                'tor_percentage': 0.0,
                'onion_percentage': 0.0,
                'coins': {}
            },
            'current': {
                'tor_percentage': 0.0,
                'onion_percentage': 0.0,
                'coins': {}
            },
            'last_updated': None
        }
    
    def save_state(self):
        """Save current state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            return True
        except Exception:
            return False
    
    def update_network_state(self, tor_percentage, onion_percentage):
        """Update TOR/.onion state with shift from current to previous"""
        # Shift current to previous
        self.state['previous']['tor_percentage'] = self.state['current']['tor_percentage']
        self.state['previous']['onion_percentage'] = self.state['current']['onion_percentage']
        
        # Update current
        self.state['current']['tor_percentage'] = tor_percentage
        self.state['current']['onion_percentage'] = onion_percentage
        self.state['last_updated'] = datetime.now().isoformat()
    
    def update_coin_state(self, coin, p_micro, mid_price):
        """Update P_micro state for a specific coin"""
        # Initialize if needed
        if coin not in self.state['previous']['coins']:
            self.state['previous']['coins'][coin] = {
                'p_micro': 0.0,
                'mid_price': 0.0
            }
        if coin not in self.state['current']['coins']:
            self.state['current']['coins'][coin] = {
                'p_micro': 0.0,
                'mid_price': 0.0
            }
        
        # Shift current to previous
        self.state['previous']['coins'][coin] = self.state['current']['coins'][coin].copy()
        
        # Update current
        self.state['current']['coins'][coin] = {
            'p_micro': p_micro,
            'mid_price': mid_price
        }
    
    def get_state(self):
        """Get current state (read-only)"""
        return self.state.copy()
    
    def get_coin_previous_pmicro(self, coin):
        """Get previous P_micro for a coin"""
        return self.state['previous']['coins'].get(coin, {}).get('p_micro', 0.0)
    
    def get_coin_current_pmicro(self, coin):
        """Get current P_micro for a coin"""
        return self.state['current']['coins'].get(coin, {}).get('p_micro', 0.0)
