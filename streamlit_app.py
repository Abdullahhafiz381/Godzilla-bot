"""
🔥 GODZILLERS CRYPTO TRACKER - MAIN APPLICATION
Dragon's Lair War Room Theme with Hidden Analytics
"""

import streamlit as st
import time
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import internal modules (formulas hidden)
from src.data_fetch import CryptoDataFetcher
from src.logic import SignalCalculator
from src.state_store import StateManager
from src.ui import (
    render_btc_panel, 
    render_signal_card, 
    render_error_card,
    render_header,
    render_footer
)

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🔥 GODZILLERS CRYPTO TRACKER",
    page_icon="🐲",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# ============================================================================
# GODZILLERS THEME CSS - DRAGON'S LAIR WAR ROOM
# ============================================================================
st.markdown("""
<style>
    /* Base theme - deep black → dark blood red gradient */
    .main {
        background: linear-gradient(135deg, #000000 0%, #0a0000 25%, #1a0000 50%, #330000 75%, #4d0000 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0000 25%, #1a0000 50%, #330000 75%, #4d0000 100%);
    }
    
    /* GODZILLERS Header - Orbitron */
    .godzillers-header {
        background: linear-gradient(90deg, #ff0000 0%, #ff4444 50%, #ff0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        text-align: center;
        font-size: 3.8rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 0, 0, 0.7);
        letter-spacing: 3px;
        animation: header-pulse 3s infinite;
    }
    
    @keyframes header-pulse {
        0% { text-shadow: 0 0 30px rgba(255, 0, 0, 0.7); }
        50% { text-shadow: 0 0 45px rgba(255, 0, 0, 0.9); }
        100% { text-shadow: 0 0 30px rgba(255, 0, 0, 0.7); }
    }
    
    .godzillers-subheader {
        color: #ff6666;
        font-family: 'Orbitron', monospace;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* War Room Grid Background */
    .war-room-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 0, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 0, 0, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Divider */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #ff0000 20%, #ff4444 50%, #ff0000 80%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>

<div class="war-room-grid"></div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def initialize_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.data_fetcher = CryptoDataFetcher()
        st.session_state.state_manager = StateManager()
        st.session_state.signal_calculator = SignalCalculator()
        st.session_state.last_update = None
        st.session_state.signals = {}
        st.session_state.error = None
        st.session_state.auto_refresh = True
        st.session_state.refresh_interval = 15  # seconds
        st.session_state.coins = {
            'BTC': {'symbol': 'BTCUSDT', 'name': 'BITCOIN', 'emoji': '🐲'},
            'ETH': {'symbol': 'ETHUSDT', 'name': 'ETHEREUM', 'emoji': '🔥'},
            'SUI': {'symbol': 'SUIUSDT', 'name': 'SUI', 'emoji': '💧'},
            'LINK': {'symbol': 'LINKUSDT', 'name': 'CHAINLINK', 'emoji': '🔗'},
            'SOL': {'symbol': 'SOLUSDT', 'name': 'SOLANA', 'emoji': '⚡'},
            'XRP': {'symbol': 'XRPUSDT', 'name': 'RIPPLE', 'emoji': '✖️'},
            'TAO': {'symbol': 'TAOUSDT', 'name': 'TAO', 'emoji': '🧠'},
            'ENA': {'symbol': 'ENAUSDT', 'name': 'ENA', 'emoji': '🌀'},
            'ADA': {'symbol': 'ADAUSDT', 'name': 'CARDANO', 'emoji': '🔷'},
            'DOGE': {'symbol': 'DOGEUSDT', 'name': 'DOGECOIN', 'emoji': '🐕'},
            'BRETT': {'symbol': 'BRETTUSDT', 'name': 'BRETT', 'emoji': '🤖'}
        }

# ============================================================================
# DATA REFRESH FUNCTION
# ============================================================================
def refresh_all_data():
    """Refresh all data and calculate signals"""
    try:
        # Clear previous error
        st.session_state.error = None
        
        # 1. Fetch TOR/.onion data (hidden)
        network_data = st.session_state.data_fetcher.fetch_network_data()
        if not network_data:
            st.session_state.error = "Failed to fetch network data"
            return False
        
        # 2. Update state manager with new network data
        tor_percentage = st.session_state.signal_calculator._calculate_tor_percentage(
            network_data['tor_nodes'], 
            network_data['total_nodes']
        )
        onion_percentage = st.session_state.signal_calculator._calculate_onion_percentage(
            network_data['onion_nodes'], 
            network_data['total_nodes']
        )
        
        st.session_state.state_manager.update_network_state(
            tor_percentage=tor_percentage,
            onion_percentage=onion_percentage
        )
        
        # 3. Fetch prices and order books for all coins
        signals = {}
        
        for coin_key, coin_info in st.session_state.coins.items():
            symbol = coin_info['symbol']
            
            # Fetch price and order book
            price_data = st.session_state.data_fetcher.fetch_price(symbol)
            order_book = st.session_state.data_fetcher.fetch_order_book(symbol)
            
            if not price_data or not order_book:
                continue  # Skip if data fetch failed
            
            # Calculate mid price
            mid_price = (order_book['best_bid'] + order_book['best_ask']) / 2
            
            # Calculate P_micro (hidden formula)
            p_micro = st.session_state.signal_calculator._calculate_p_micro(
                best_bid=order_book['best_bid'],
                best_ask=order_book['best_ask'],
                qbid=order_book['bid_qty'],
                qask=order_book['ask_qty']
            )
            
            # Update coin state
            st.session_state.state_manager.update_coin_state(
                coin=symbol,
                p_micro=p_micro,
                mid_price=mid_price
            )
            
            # Get previous state
            state = st.session_state.state_manager.get_state()
            
            # Calculate signal based on coin type
            if symbol == 'BTCUSDT':
                signal_data = st.session_state.signal_calculator.decide_btc_signal(
                    current_tor=state['current']['tor_percentage'],
                    previous_tor=state['previous']['tor_percentage'],
                    current_onion=state['current']['onion_percentage'],
                    previous_onion=state['previous']['onion_percentage'],
                    pmicro_btc=p_micro,
                    mid_btc=mid_price
                )
            else:
                signal_data = st.session_state.signal_calculator.decide_alt_signal(
                    coin=symbol,
                    current_tor=state['current']['tor_percentage'],
                    previous_tor=state['previous']['tor_percentage'],
                    pmicro_coin=p_micro,
                    mid_coin=mid_price
                )
            
            # Add display data
            signal_data.update({
                'coin_key': coin_key,
                'name': coin_info['name'],
                'emoji': coin_info['emoji'],
                'current_price': price_data['price'],
                'mid_price': mid_price,
                'p_micro': p_micro  # Hidden from UI, used internally
            })
            
            signals[symbol] = signal_data
        
        # Update session state
        st.session_state.signals = signals
        st.session_state.last_update = datetime.now()
        
        # Save state to persistent storage
        st.session_state.state_manager.save_state()
        
        return True
        
    except Exception as e:
        # Log error internally, show user-friendly message
        st.session_state.error = f"System error: {str(e)[:50]}..."
        return False

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # CONTROL PANEL
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown('<h2 style="font-family: Orbitron; color: #ff4444; margin: 0;">⚡ WAR ROOM CONTROL PANEL</h2>', unsafe_allow_html=True)
    
    with col2:
        # Auto-refresh toggle
        st.session_state.auto_refresh = st.checkbox(
            "🔄 AUTO REFRESH", 
            value=st.session_state.auto_refresh,
            help="Automatically refresh signals every 15 seconds"
        )
    
    with col3:
        # Refresh interval
        st.session_state.refresh_interval = st.selectbox(
            "INTERVAL",
            options=[10, 15, 30, 60],
            index=1,
            help="Refresh interval in seconds"
        )
    
    with col4:
        # Manual refresh button
        if st.button("🐉 UPDATE SIGNALS", use_container_width=True, type="primary"):
            with st.spinner("Activating dragon fire analysis..."):
                if refresh_all_data():
                    st.success("Signals updated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Update failed")
    
    # ERROR DISPLAY
    if st.session_state.error:
        render_error_card(st.session_state.error)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # BTC SECTION - ALWAYS VISIBLE
    btc_signal = st.session_state.signals.get('BTCUSDT')
    if btc_signal:
        render_btc_panel(btc_signal)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ACTIVE ALTCOIN SIGNALS - ONLY BUY/SELL
    st.markdown('<h2 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">🎯 ACTIVE BATTLEFIELD SIGNALS</h2>', unsafe_allow_html=True)
    
    # Filter for active altcoin signals (BUY/SELL only, exclude BTC and NEUTRAL)
    active_altcoins = {}
    for symbol, signal_data in st.session_state.signals.items():
        if symbol != 'BTCUSDT' and signal_data['signal'] in ['BUY', 'SELL']:
            active_altcoins[symbol] = signal_data
    
    if active_altcoins:
        st.markdown(f'<p style="color: #ff8888; font-family: Rajdhani; margin-bottom: 1rem;">Showing {len(active_altcoins)} active signals • NEUTRAL coins are hidden</p>', unsafe_allow_html=True)
        
        # Display in a responsive grid
        cols_per_row = 3
        altcoin_list = list(active_altcoins.values())
        
        for i in range(0, len(altcoin_list), cols_per_row):
            cols = st.columns(cols_per_row)
            row_items = altcoin_list[i:i + cols_per_row]
            
            for j, signal_data in enumerate(row_items):
                with cols[j]:
                    render_signal_card(signal_data)
    else:
        # No active altcoin signals
        st.markdown('''
        <div style="text-align: center; padding: 3rem; border: 1px dashed #ff4444; border-radius: 15px; margin: 2rem 0;">
            <p style="font-family: Orbitron; color: #ff8888; font-size: 1.2rem;">⚡ NO ACTIVE ALTCOIN SIGNALS</p>
            <p style="font-family: Rajdhani; color: #ff6666;">All altcoins are currently NEUTRAL or waiting for clear signals</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # FOOTER
    render_footer(st.session_state.last_update)
    
    # AUTO-REFRESH LOGIC
    if st.session_state.auto_refresh and not st.session_state.error:
        time.sleep(st.session_state.refresh_interval)
        if refresh_all_data():
            st.rerun()

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Initial data refresh on first load
    if not st.session_state.signals:
        with st.spinner("Initializing Dragon's Lair War Room..."):
            refresh_all_data()
    
    # Run main application
    main()
