"""
UI rendering components for GODZILLERS theme
"""

import streamlit as st

def render_header():
    """Render GODZILLERS header"""
    pass  # Already handled in main app

def render_btc_panel(signal_data):
    """Render BTC panel - use simplified version from main app"""
    pass

def render_signal_card(signal_data):
    """Render signal card - use simplified version from main app"""
    pass

def render_error_card(error_message):
    """Render error card"""
    st.error(f"⚠️ {error_message}")

def render_footer(last_update):
    """Render footer"""
    pass  # Already handled in main app