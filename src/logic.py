"""
🔥 GODZILLERS - HIDDEN FORMULA IMPLEMENTATION
All formulas are kept internal and never exposed to UI or logs
"""

import json
import os
from datetime import datetime

class SignalCalculator:
    """Internal calculator with hidden formulas - NEVER EXPOSED"""
    
    # Internal constants (never shown)
    NEUTRAL_THRESHOLD = 0.0005  # 0.05% threshold for neutral classification
    
    def __init__(self):
        # Internal tracking (not persisted)
        self._calculation_log = []
    
    # ============================================================================
    # HIDDEN FORMULA IMPLEMENTATIONS
    # ============================================================================
    
    def _calculate_tor_percentage(self, tor_nodes, total_nodes):
        """SECRET: Calculate TOR percentage - formula never displayed"""
        # Formula: tor_percentage = (tor_nodes / total_nodes) * 100
        if total_nodes == 0:
            return 0.0
        
        result = (tor_nodes / total_nodes) * 100
        
        # Internal logging (never exposed)
        self._log_calculation(
            'tor_percentage',
            {'tor_nodes': tor_nodes, 'total_nodes': total_nodes},
            result
        )
        
        return round(result, 4)
    
    def _calculate_onion_percentage(self, onion_nodes, total_nodes):
        """SECRET: Calculate .onion percentage - formula never displayed"""
        # Formula: onion_percentage = (onion_nodes / total_nodes) * 100
        if total_nodes == 0:
            return 0.0
        
        result = (onion_nodes / total_nodes) * 100
        
        # Internal logging (never exposed)
        self._log_calculation(
            'onion_percentage',
            {'onion_nodes': onion_nodes, 'total_nodes': total_nodes},
            result
        )
        
        return round(result, 4)
    
    def _calculate_p_micro(self, best_bid, best_ask, qbid, qask):
        """SECRET: Calculate P_micro - formula never displayed"""
        # Formula: P_micro = (A * Qbid + B * Qask) / (Qbid + Qask)
        # A = best_bid, B = best_ask
        if qbid + qask == 0:
            return (best_bid + best_ask) / 2
        
        result = (best_bid * qbid + best_ask * qask) / (qbid + qask)
        
        # Internal logging (never exposed)
        self._log_calculation(
            'p_micro',
            {
                'best_bid': best_bid,
                'best_ask': best_ask,
                'qbid': qbid,
                'qask': qask
            },
            result
        )
        
        return round(result, 8)
    
    # ============================================================================
    # SIGNAL DECISION LOGIC
    # ============================================================================
    
    def _interpret_pmicro_direction(self, p_micro, mid_price):
        """Determine BUY/SELL/NEUTRAL from P_micro vs mid_price"""
        diff = p_micro - mid_price
        abs_diff = abs(diff)
        
        if abs_diff < (mid_price * self.NEUTRAL_THRESHOLD):
            return 'NEUTRAL'
        elif diff > 0:
            return 'BUY'
        else:
            return 'SELL'
    
    def _get_tor_direction(self, current_tor, previous_tor):
        """Determine TOR direction (BUY/SELL/NEUTRAL)"""
        if abs(current_tor - previous_tor) < 0.01:  # Small change threshold
            return 'NEUTRAL'
        elif current_tor > previous_tor:
            return 'SELL'  # TOR rising = SELL pressure
        else:
            return 'BUY'   # TOR falling = BUY pressure
    
    def _get_onion_direction(self, current_onion, previous_onion):
        """Determine .onion direction"""
        if abs(current_onion - previous_onion) < 0.01:
            return 'NEUTRAL'
        elif current_onion > previous_onion:
            return 'SELL'  # .onion rising confirms SELL
        else:
            return 'BUY'   # .onion falling confirms BUY
    
    def _calculate_confidence(self, signals):
        """Calculate confidence percentage based on signal agreement"""
        # Count agreements
        total_signals = len(signals)
        if total_signals == 0:
            return 50  # Default neutral confidence
        
        # Weight different signals
        weights = {'TOR': 0.4, 'ONION': 0.3, 'P_MICRO': 0.3}
        agreement_score = 0
        
        for signal_name, signal_value in signals.items():
            if signal_value != 'NEUTRAL':
                # Add weighted score for non-neutral signals
                agreement_score += weights.get(signal_name, 0.33)
        
        # Convert to percentage
        confidence = int(agreement_score * 100)
        
        # Ensure bounds
        return max(30, min(99, confidence))
    
    # ============================================================================
    # PUBLIC INTERFACE (returns only signals, no formulas)
    # ============================================================================
    
    def decide_btc_signal(self, current_tor, previous_tor, 
                         current_onion, previous_onion,
                         pmicro_btc, mid_btc):
        """BTC logic with full confirmation - returns only signal data"""
        # Get individual directions
        tor_dir = self._get_tor_direction(current_tor, previous_tor)
        onion_dir = self._get_onion_direction(current_onion, previous_onion)
        pmicro_dir = self._interpret_pmicro_direction(pmicro_btc, mid_btc)
        
        # BTC BUY condition: TOR BUY AND .onion BUY AND P_micro BUY
        if (tor_dir == 'BUY' and onion_dir == 'BUY' and pmicro_dir == 'BUY'):
            signal = 'BUY'
        
        # BTC SELL condition: TOR SELL AND .onion SELL AND P_micro SELL
        elif (tor_dir == 'SELL' and onion_dir == 'SELL' and pmicro_dir == 'SELL'):
            signal = 'SELL'
        
        else:
            signal = 'NEUTRAL'
        
        # Calculate confidence
        confidence = self._calculate_confidence({
            'TOR': tor_dir,
            'ONION': onion_dir,
            'P_MICRO': pmicro_dir
        })
        
        return {
            'signal': signal,
            'confidence': confidence,
            'components': {  # Hidden from UI, used internally
                'tor_direction': tor_dir,
                'onion_direction': onion_dir,
                'pmicro_direction': pmicro_dir
            }
        }
    
    def decide_alt_signal(self, coin, current_tor, previous_tor,
                         pmicro_coin, mid_coin):
        """Altcoin logic with conflict rules - returns only signal data"""
        # Get directions
        tor_dir = self._get_tor_direction(current_tor, previous_tor)
        pmicro_dir = self._interpret_pmicro_direction(pmicro_coin, mid_coin)
        
        # Apply exact rules as specified
        signal = 'NEUTRAL'  # Default
        
        # Rule 1: P_micro SELL + TOR BUY → NEUTRAL (confused)
        if pmicro_dir == 'SELL' and tor_dir == 'BUY':
            signal = 'NEUTRAL'
        
        # Rule 2: P_micro SELL + TOR SELL → SELL
        elif pmicro_dir == 'SELL' and tor_dir == 'SELL':
            signal = 'SELL'
        
        # Rule 3: P_micro SELL + TOR NEUTRAL → SELL
        elif pmicro_dir == 'SELL' and tor_dir == 'NEUTRAL':
            signal = 'SELL'
        
        # Rule 4: P_micro BUY + TOR BUY → BUY
        elif pmicro_dir == 'BUY' and tor_dir == 'BUY':
            signal = 'BUY'
        
        # Rule 5: P_micro BUY + TOR SELL → SELL
        elif pmicro_dir == 'BUY' and tor_dir == 'SELL':
            signal = 'SELL'
        
        # Rule 6: P_micro neutral → follow TOR
        elif pmicro_dir == 'NEUTRAL':
            signal = tor_dir
        
        # Calculate confidence
        agreement = 0
        if signal != 'NEUTRAL':
            if (signal == 'BUY' and tor_dir == 'BUY') or (signal == 'SELL' and tor_dir == 'SELL'):
                agreement = 0.8
            elif tor_dir == 'NEUTRAL':
                agreement = 0.6
            else:
                agreement = 0.4
        
        confidence = int(agreement * 100)
        
        return {
            'signal': signal,
            'confidence': max(30, min(99, confidence)),
            'components': {  # Hidden from UI
                'tor_direction': tor_dir,
                'pmicro_direction': pmicro_dir
            }
        }
    
    def _log_calculation(self, formula_name, inputs, result):
        """Internal logging - never exposed to users"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'formula': formula_name,
            'inputs': inputs,
            'result': result
        }
        self._calculation_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self._calculation_log) > 1000:
            self._calculation_log = self._calculation_log[-1000:]
