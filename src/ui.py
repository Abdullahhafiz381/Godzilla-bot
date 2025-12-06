"""
UI rendering components for GODZILLERS theme
"""

import streamlit as st
from datetime import datetime

def render_header():
    """Render GODZILLERS header"""
    st.markdown('<h1 class="godzillers-header">🔥 GODZILLERS CRYPTO TRACKER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="godzillers-subheader">DRAGON\'S LAIR WAR ROOM • HIDDEN ANALYTICS • ACTIVE SIGNALS ONLY</p>', unsafe_allow_html=True)

def render_btc_panel(signal_data):
    """Render BTC panel with shine animation"""
    # Determine styling based on signal
    if signal_data['signal'] == 'BUY':
        price_color = "#00ff00"
        signal_text = "🐲 DRAGON FIRE BUY 🐲"
        signal_class = "buy-glow"
    elif signal_data['signal'] == 'SELL':
        price_color = "#ff0000"
        signal_text = "💀 GODZILLA SELL 💀"
        signal_class = "sell-glow"
    else:
        price_color = "#ffa500"
        signal_text = "⚡ MARKET NEUTRAL ⚡"
        signal_class = "neutral-glow"
    
    # Add custom CSS for BTC panel
    st.markdown(f"""
    <style>
        .btc-panel {{
            background: linear-gradient(135deg, rgba(20, 0, 0, 0.9) 0%, rgba(40, 0, 0, 0.95) 100%);
            border: 2px solid {price_color};
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }}
        
        .btc-panel::{signal_class} {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 30px {price_color}80; }}
            50% {{ box-shadow: 0 0 50px {price_color}; }}
            100% {{ box-shadow: 0 0 30px {price_color}80; }}
        }}
        
        .shine-overlay {{
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, {price_color}20, transparent);
            animation: shine 3s infinite linear;
        }}
    </style>
    
    <div class="btc-panel {signal_class}">
        <div class="shine-overlay"></div>
        <div style="position: relative; z-index: 2;">
            <div style="text-align: center;">
                <p style="color: #ff8888; font-family: Rajdhani; margin-bottom: 0.5rem; font-size: 1.1rem;">
                    BITCOIN (BTC/USDT)
                </p>
                <p style="font-family: Orbitron; font-size: 3.8rem; font-weight: 900; 
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
    """, unsafe_allow_html=True)

def render_signal_card(signal_data):
    """Render signal card for altcoins (BUY/SELL only)"""
    if signal_data['signal'] == 'BUY':
        bg_gradient = "linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, rgba(0, 100, 0, 0.3) 100%)"
        border_color = "#00ff00"
        text_color = "#00ff00"
        signal_emoji = "🟢"
        glow_class = "buy-pulse"
    else:  # SELL
        bg_gradient = "linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(100, 0, 0, 0.3) 100%)"
        border_color = "#ff0000"
        text_color = "#ff0000"
        signal_emoji = "🔴"
        glow_class = "sell-pulse"
    
    st.markdown(f"""
    <style>
        .signal-card {{
            background: {bg_gradient};
            border: 2px solid {border_color};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
        }}
        
        .{glow_class} {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 20px {border_color}80; }}
            50% {{ box-shadow: 0 0 35px {border_color}; }}
            100% {{ box-shadow: 0 0 20px {border_color}80; }}
        }}
    </style>
    
    <div class="signal-card {glow_class}">
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
    """, unsafe_allow_html=True)

def render_error_card(error_message):
    """Render error card (user-friendly)"""
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
            {error_message}
        </p>
        <p style="font-family: Rajdhani; color: #ff6666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
            Retrying automatically...
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_footer(last_update):
    """Render footer with last update time"""
    update_time = "Never" if not last_update else last_update.strftime("%H:%M:%S")
    
    st.markdown("""
    <div class="divider"></div>
    
    <div style="text-align: center; margin: 2rem 0;">
        <p style="color: #ff6666; font-family: Rajdhani; font-size: 0.9rem; margin: 0.5rem 0;">
            <span style="display: inline-block; width: 10px; height: 10px; 
                   background-color: #00ff00; border-radius: 50%; 
                   margin-right: 8px; animation: pulse 2s infinite;"></span>
            Last Update: """ + update_time + """
        </p>
        <p style="color: #ff4444; font-family: Orbitron; font-size: 0.8rem; letter-spacing: 1px; margin: 0.5rem 0;">
            🔥 GODZILLERS CRYPTO WARFARE SYSTEM 🔥
        </p>
        <p style="color: #ff6666; font-family: Rajdhani; font-size: 0.7rem; margin: 0.5rem 0;">
            Dragon's Lair War Room • Hidden Analytics • Active Signals Only
        </p>
    </div>
    """, unsafe_allow_html=True)
