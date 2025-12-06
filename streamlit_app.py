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
    
    /* BTC Panel Animation */
    .btc-panel-glow {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(139, 0, 0, 0.25) 100%);
        border: 2px solid rgba(255, 0, 0, 0.6);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        animation: btc-pulse 3s infinite;
    }
    
    @keyframes btc-pulse {
        0% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.4); }
        50% { box-shadow: 0 0 60px rgba(255, 0, 0, 0.6); }
        100% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.4); }
    }
    
    .btc-panel-glow::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 0, 0, 0.1), transparent);
        animation: shine 3s infinite linear;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
</style>

<div class="war-room-grid"></div>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
def initialize_session_state():
    """Initialize all session state variables"""
    # Define default coins
    coins = {
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
    
    # Initialize session state with proper defaults
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.data_fetcher = CryptoDataFetcher()
        st.session_state.state_manager = StateManager()
        st.session_state.signal_calculator = SignalCalculator()
        st.session_state.last_update = None
        st.session_state.signals = {}  # Initialize empty signals dict
        st.session_state.error = None
        st.session_state.auto_refresh = True
        st.session_state.refresh_interval = 15  # seconds
        st.session_state.coins = coins

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
                # Log internally but continue with other coins
                continue
            
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
        st.session_state.error = f"System error: Data refresh failed"
        return False

# ============================================================================
# RENDER BTC PANEL (Simplified - No custom CSS needed)
# ============================================================================
def render_btc_panel_simple(signal_data):
    """Render BTC panel with simplified styling"""
    # Determine styling based on signal
    if signal_data['signal'] == 'BUY':
        price_color = "#00ff00"
        signal_text = "🐲 DRAGON FIRE BUY 🐲"
        border_color = "#00ff00"
    elif signal_data['signal'] == 'SELL':
        price_color = "#ff0000"
        signal_text = "💀 GODZILLA SELL 💀"
        border_color = "#ff0000"
    else:
        price_color = "#ffa500"
        signal_text = "⚡ MARKET NEUTRAL ⚡"
        border_color = "#ffa500"
    
    st.markdown(f'''
    <div class="btc-panel-glow">
        <div style="position: relative; z-index: 2;">
            <div style="text-align: center;">
                <p style="color: #ff8888; font-family: Rajdhani; margin-bottom: 0.5rem; font-size: 1.1rem;">
                    BITCOIN (BTC/USDT)
                </p>
                <p style="font-family: Orbitron; font-size: 3.5rem; font-weight: 900; 
                   color: {price_color}; margin: 0.5rem 0; text-shadow: 0 0 20px {price_color}80;">
                   ${signal_data['current_price']:,.2f}
                </p>
                <p style="font-family: Orbitron; font-size: 1.8rem; margin: 1rem 0; color: {price_color};">
                    {signal_text}
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem;">
                <div style="text-align: center;">
                    <p style="color: #ff8888; font-family: Rajdhani; margin: 0;">CONFIDENCE</p>
                    <p style="font-family: Orbitron; font-size: 1.5rem; color: {price_color}; margin: 0.2rem 0;">
                        {signal_data['confidence']}%
                    </p>
                    <div style="background: #333; height: 8px; border-radius: 4px; margin-top: 0.5rem;">
                        <div style="background: {price_color}; height: 100%; width: {signal_data['confidence']}%; border-radius: 4px;"></div>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <p style="color: #ff8888; font-family: Rajdhani; margin: 0;">MID PRICE</p>
                    <p style="font-family: Orbitron; font-size: 1.5rem; color: #ffffff; margin: 0.2rem 0;">
                        ${signal_data['mid_price']:,.2f}
                    </p>
                </div>
                
                <div style="text-align: center;">
                    <p style="color: #ff8888; font-family: Rajdhani; margin: 0;">STATUS</p>
                    <p style="font-family: Orbitron; font-size: 1.5rem; color: #00ff00; margin: 0.2rem 0;">
                        🔥 LIVE
                    </p>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ============================================================================
# RENDER SIGNAL CARD (Simplified)
# ============================================================================
def render_signal_card_simple(signal_data):
    """Render signal card for altcoins with simplified styling"""
    if signal_data['signal'] == 'BUY':
        bg_gradient = "linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, rgba(0, 100, 0, 0.3) 100%)"
        border_color = "#00ff00"
        text_color = "#00ff00"
        signal_emoji = "🟢"
    else:  # SELL
        bg_gradient = "linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(100, 0, 0, 0.3) 100%)"
        border_color = "#ff0000"
        text_color = "#ff0000"
        signal_emoji = "🔴"
    
    st.markdown(f'''
    <div style="background: {bg_gradient}; 
                border: 2px solid {border_color}; 
                border-radius: 15px; 
                padding: 1.5rem; 
                margin: 1rem 0;
                animation: pulse 2s infinite;
                box-shadow: 0 0 20px {border_color}80;">
        <div style="text-align: center;">
            <h3 style="font-family: Orbitron; margin: 0.5rem 0; font-size: 1.3rem; color: {text_color};">
                {signal_data['emoji']} {signal_data['name']} {signal_emoji}
            </h3>
            <p style="font-family: Orbitron; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0; color: #ffffff;">
                ${signal_data['current_price']:,.2f}
            </p>
            <p style="font-family: Orbitron; font-size: 1.3rem; margin: 0.5rem 0; color: {text_color};">
                {signal_data['signal']} SIGNAL
            </p>
            
            <!-- Confidence bar -->
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                    <span style="color: #ff8888; font-family: Rajdhani; font-size: 0.9rem;">CONFIDENCE</span>
                    <span style="color: {text_color}; font-family: Orbitron; font-size: 0.9rem;">
                        {signal_data['confidence']}%
                    </span>
                </div>
                <div style="background: #333; height: 6px; border-radius: 3px;">
                    <div style="background: {text_color}; height: 100%; width: {signal_data['confidence']}%; border-radius: 3px;"></div>
                </div>
            </div>
            
            <p style="color: #ff8888; font-family: Rajdhani; font-size: 0.8rem; margin: 0.5rem 0 0 0;">
                {signal_data['coin_key']}
            </p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application function"""
    
    # Initialize session state FIRST
    initialize_session_state()
    
    # Render header
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS CRYPTO TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">DRAGON\'S LAIR WAR ROOM • HIDDEN ANALYTICS • ACTIVE SIGNALS ONLY</p>', unsafe_allow_html=True)
    
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
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(100, 0, 0, 0.2) 100%);
                    border: 1px solid #ff4444;
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    text-align: center;">
            <p style="font-family: Orbitron; color: #ff4444; font-size: 1.2rem; margin: 0 0 0.5rem 0;">
                ⚠️ SYSTEM ALERT
            </p>
            <p style="font-family: Rajdhani; color: #ff8888; margin: 0;">
                {st.session_state.error}
            </p>
            <p style="font-family: Rajdhani; color: #ff6666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Retrying automatically...
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # BTC SECTION - ALWAYS VISIBLE
    st.markdown('<h2 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">🐲 BITCOIN COMMAND CENTER</h2>', unsafe_allow_html=True)
    
    # Check if BTC signal exists, otherwise create default
    btc_signal = st.session_state.signals.get('BTCUSDT')
    if not btc_signal:
        # Create a default BTC display
        btc_signal = {
            'signal': 'NEUTRAL',
            'confidence': 50,
            'current_price': 0.00,
            'mid_price': 0.00,
            'coin_key': 'BTC',
            'name': 'BITCOIN',
            'emoji': '🐲'
        }
    
    # Render BTC panel
    render_btc_panel_simple(btc_signal)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ACTIVE ALTCOIN SIGNALS - ONLY BUY/SELL
    st.markdown('<h2 style="font-family: Orbitron; color: #ff4444; margin: 1rem 0;">🎯 ACTIVE BATTLEFIELD SIGNALS</h2>', unsafe_allow_html=True)
    
    # Filter for active altcoin signals (BUY/SELL only, exclude BTC and NEUTRAL)
    active_altcoins = {}
    for symbol, signal_data in st.session_state.signals.items():
        if symbol != 'BTCUSDT' and signal_data.get('signal', 'NEUTRAL') in ['BUY', 'SELL']:
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
                    render_signal_card_simple(signal_data)
    else:
        # No active altcoin signals
        st.markdown('''
        <div style="text-align: center; padding: 3rem; border: 1px dashed #ff4444; border-radius: 15px; margin: 2rem 0;">
            <p style="font-family: Orbitron; color: #ff8888; font-size: 1.2rem;">⚡ NO ACTIVE ALTCOIN SIGNALS</p>
            <p style="font-family: Rajdhani; color: #ff6666;">All altcoins are currently NEUTRAL or waiting for clear signals</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # FOOTER
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    update_time = "Never" if not st.session_state.last_update else st.session_state.last_update.strftime("%H:%M:%S")
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <p style="color: #ff6666; font-family: Rajdhani; font-size: 0.9rem; margin: 0.5rem 0;">
            <span style="display: inline-block; width: 10px; height: 10px; 
                   background-color: #00ff00; border-radius: 50%; 
                   margin-right: 8px; animation: pulse 2s infinite;"></span>
            Last Update: {update_time}
        </p>
        <p style="color: #ff4444; font-family: Orbitron; font-size: 0.8rem; letter-spacing: 1px; margin: 0.5rem 0;">
            🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥
        </p>
        <p style="color: #ff6666; font-family: Rajdhani; font-size: 0.7rem; margin: 0.5rem 0;">
            Dragon's Lair War Room • Hidden Analytics • Active Signals Only
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AUTO-REFRESH LOGIC
    if st.session_state.auto_refresh and not st.session_state.error:
        time.sleep(st.session_state.refresh_interval)
        if refresh_all_data():
            st.rerun()

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    try:
        # Initialize and run
        main()
    except Exception as e:
        # Catch any unhandled exceptions and show user-friendly error
        st.error("Application encountered an error. Please refresh the page.")
        st.info("If the error persists, check your internet connection and API access.")