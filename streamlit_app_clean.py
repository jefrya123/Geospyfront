"""
GeoSpy Streamlit Web Application

A professional web interface for AI-powered image geolocation using Google's Gemini AI.
This application provides a user-friendly way to upload images and get top 3 location
predictions with detailed AI reasoning and interactive visualizations.

Features:
- Dark theme UI with professional styling
- Image upload via file or URL
- Top 3 location predictions with AI reasoning
- Interactive maps with location markers
- Analytics dashboard with confidence distribution
- Graceful error handling for API overloads
- Responsive design with sidebar configuration

Author: Enhanced version of original GeoSpy by Atilla
License: MIT
"""

import streamlit as st
import os
from pathlib import Path
import json
from PIL import Image
import io
import base64
from dotenv import load_dotenv
from geospyer import GeoSpy
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="GeoSpy - AI Image Geolocation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Dark theme optimization */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Global text color for dark theme */
    .stMarkdown, .stText, .stTextInput, .stTextArea, .stSelectbox, .stSlider {
        color: #fafafa !important;
    }
    
    /* Ensure all text elements have proper contrast on dark theme */
    p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #fafafa !important;
    }
    
    /* Streamlit specific overrides for dark theme */
    .stMarkdown p {
        color: #fafafa !important;
    }
    
    .stTextInput > div > div > input {
        color: #fafafa !important;
        background-color: #262730 !important;
        border-color: #4a4a4a !important;
    }
    
    .stTextArea > div > div > textarea {
        color: #fafafa !important;
        background-color: #262730 !important;
        border-color: #4a4a4a !important;
    }
    
    /* Sidebar styling for dark theme */
    .css-1d391kg {
        background-color: #1f1f1f !important;
    }
    
    /* Sidebar text and elements */
    .css-1d391kg .stMarkdown,
    .css-1d391kg .stText,
    .css-1d391kg .stTextInput,
    .css-1d391kg .stTextArea,
    .css-1d391kg .stSelectbox,
    .css-1d391kg label,
    .css-1d391kg p,
    .css-1d391kg h1,
    .css-1d391kg h2,
    .css-1d391kg h3,
    .css-1d391kg h4,
    .css-1d391kg h5,
    .css-1d391kg h6,
    .css-1d391kg div {
        color: #fafafa !important;
    }
    
    /* Sidebar input fields */
    .css-1d391kg .stTextInput > div > div > input,
    .css-1d391kg .stTextArea > div > div > textarea {
        color: #fafafa !important;
        background-color: #262730 !important;
        border-color: #4a4a4a !important;
    }
    
    /* Sidebar labels and help text */
    .css-1d391kg .stMarkdown p {
        color: #fafafa !important;
    }
    
    /* Sidebar section headers */
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3 {
        color: #fafafa !important;
    }
    
    /* Sidebar list items */
    .css-1d391kg ul,
    .css-1d391kg ol,
    .css-1d391kg li {
        color: #fafafa !important;
    }
    
    /* Sidebar help icons and tooltips */
    .css-1d391kg .stTooltip,
    .css-1d391kg .stHelp {
        color: #fafafa !important;
    }
    
    /* Sidebar button styling */
    .css-1d391kg .stButton > button {
        color: #fafafa !important;
        background-color: #1f77b4 !important;
        border-color: #1f77b4 !important;
    }
    
    /* Sidebar checkbox and radio buttons */
    .css-1d391kg .stCheckbox,
    .css-1d391kg .stRadio {
        color: #fafafa !important;
    }
    
    /* Sidebar expander/collapsible sections */
    .css-1d391kg .streamlit-expanderHeader {
        color: #fafafa !important;
        background-color: #262730 !important;
    }
    
    /* Force all sidebar text to be light */
    [data-testid="stSidebar"] * {
        color: #fafafa !important;
    }
    
    /* Specific targeting for sidebar markdown content */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #fafafa !important;
    }
    
    /* Override any dark text colors in sidebar */
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #fafafa !important;
    }
    
    /* Ensure sidebar headers are visible */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6 {
        color: #fafafa !important;
    }
    
    /* Sidebar background and container styling */
    [data-testid="stSidebar"] {
        background-color: #1f1f1f !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #1f1f1f !important;
    }
    
    /* Override any inline styles that might be causing dark text */
    [data-testid="stSidebar"] *[style*="color"] {
        color: #fafafa !important;
    }
    
    /* Force light text for any remaining dark elements */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown *,
    [data-testid="stSidebar"] .stText,
    [data-testid="stSidebar"] .stText * {
        color: #fafafa !important;
    }
    
    /* Main content area text readability */
    .main .stMarkdown,
    .main .stMarkdown *,
    .main .stText,
    .main .stText *,
    .main p,
    .main h1,
    .main h2,
    .main h3,
    .main h4,
    .main h5,
    .main h6,
    .main span,
    .main div {
        color: #fafafa !important;
    }
    
    /* Location ranking cards styling */
    .ranking-card,
    .ranking-card *,
    .ranking-card p,
    .ranking-card h1,
    .ranking-card h2,
    .ranking-card h3,
    .ranking-card h4,
    .ranking-card h5,
    .ranking-card h6,
    .ranking-card span,
    .ranking-card div {
        color: #fafafa !important;
    }
    
    /* Ensure all text in main content is readable */
    .main .stMarkdown p,
    .main .stMarkdown li,
    .main .stMarkdown span,
    .main .stText p,
    .main .stText li,
    .main .stText span {
        color: #fafafa !important;
    }
    
    /* Reduce excessive padding and margins */
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 1200px !important;
    }
    
    /* Compact spacing */
    .stMarkdown {
        margin-bottom: 0.25rem !important;
    }
    
    /* Reduce blank space */
    .stButton > button {
        margin: 0.25rem 0 !important;
    }
    
    /* Reduce section header spacing */
    .section-header {
        margin: 0.5rem 0 0.25rem 0 !important;
    }
    
    /* Reduce expander spacing */
    .streamlit-expanderHeader {
        margin-bottom: 0.25rem !important;
    }
    
    /* Reduce dataframe spacing */
    .stDataFrame {
        margin: 0.25rem 0 !important;
    }
    
    /* Reduce plotly chart spacing */
    .stPlotlyChart {
        margin: 0.25rem 0 !important;
    }
    
    /* Reduce folium map spacing */
    .stFolium {
        margin: 0.25rem 0 !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: #1f77b4 !important; /* Fallback */
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #b0b0b0 !important;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        color: white !important;
    }
    .confidence-high { 
        color: #28a745 !important; 
        font-weight: bold; 
        background: rgba(40, 167, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .confidence-medium { 
        color: #ffc107 !important; 
        font-weight: bold; 
        background: rgba(255, 193, 7, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .confidence-low { 
        color: #dc3545 !important; 
        font-weight: bold; 
        background: rgba(220, 53, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .upload-area {
        border: 2px dashed #4a4a4a;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        background: #262730;
        transition: all 0.3s ease;
        color: #fafafa !important;
    }
    
    .upload-area:hover {
        border-color: #1f77b4;
        background: #2a2a3a;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0.5rem 0 0.25rem 0;
        color: #fafafa !important;
    }
    .info-box {
        background: #1a1a2e;
        border-left: 4px solid #1f77b4;
        padding: 0.75rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        color: #fafafa !important;
    }
    .ranking-card {
        background: #262730;
        border: 2px solid #4a4a4a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #fafafa !important;
    }
    
    .ranking-card * {
        color: #fafafa !important;
    }
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: #333 !important;
    }
    .ranking-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .ranking-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 1rem;
    }
    .ranking-1 { background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #333 !important; }
    .ranking-2 { background: linear-gradient(135deg, #c0c0c0 0%, #e0e0e0 100%); color: #333 !important; }
    .ranking-3 { background: linear-gradient(135deg, #cd7f32 0%, #daa520 100%); color: white !important; }
    .location-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .location-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333 !important;
        margin: 0;
    }
    .location-subtitle {
        color: #666 !important;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    .comparison-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Error message styling */
    .stAlert {
        color: #333 !important;
    }
    
    /* Success message styling */
    .stSuccess {
        color: #333 !important;
    }
    
    /* Info message styling */
    .stInfo {
        color: #333 !important;
    }
    
    /* Warning message styling */
    .stWarning {
        color: #333 !important;
    }
</style>
""", unsafe_allow_html=True)

def create_interactive_map(locations):
    """
    Create an interactive Folium map with location markers and heatmap visualization.
    
    Args:
        locations (list): List of location dictionaries containing coordinates and metadata
        
    Returns:
        folium.Map or None: Interactive map object if locations exist, None otherwise
        
    Features:
        - Satellite and street view layers
        - Ranked location markers with popups
        - Heatmap visualization for multiple locations
        - Custom styling for different ranking levels
    """
    if not locations:
        return None
    
    # Calculate center point
    lats = [loc.get("coordinates", {}).get("latitude", 0) for loc in locations if loc.get("coordinates", {}).get("latitude", 0) != 0]
    lngs = [loc.get("coordinates", {}).get("longitude", 0) for loc in locations if loc.get("coordinates", {}).get("longitude", 0) != 0]
    
    if not lats or not lngs:
        return None
    
    center_lat = sum(lats) / len(lats)
    center_lng = sum(lngs) / len(lngs)
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add satellite view option
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite View'
    ).add_to(m)
    
    # Define colors and icons for rankings
    ranking_colors = {
        1: ("gold", "star"),
        2: ("silver", "star"),
        3: ("orange", "star"),
        4: ("blue", "info-circle"),
        5: ("gray", "info-circle")
    }
    
    # Add location markers
    for i, location in enumerate(locations):
        coords = location.get("coordinates", {})
        lat = coords.get("latitude", 0)
        lng = coords.get("longitude", 0)
        
        if lat != 0 and lng != 0:
            # Get ranking color and icon
            rank = i + 1
            color, icon = ranking_colors.get(rank, ("blue", "info-circle"))
            
            # Create popup content
            popup_content = f"""
            <div style="width: 280px;">
                <h4>🏆 Rank #{rank}: {location.get('city', 'Unknown')}</h4>
                <p><strong>📍 Location:</strong> {location.get('city', 'Unknown')}, {location.get('state', 'Unknown')}</p>
                <p><strong>🌍 Country:</strong> {location.get('country', 'Unknown')}</p>
                <p><strong>🎯 Confidence:</strong> {location.get('confidence', 'Medium')}</p>
                <p><strong>📊 Coordinates:</strong> {lat:.6f}, {lng:.6f}</p>
                <hr>
                <p><strong>💡 Reasoning:</strong></p>
                <p style="font-size: 0.9em;">{location.get('explanation', 'No explanation provided')[:200]}...</p>
            </div>
            """
            
            folium.Marker(
                [lat, lng],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"#{rank}: {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}",
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
    
    # Add heatmap if multiple locations
    if len(locations) > 1:
        heatmap_data = [[loc.get("coordinates", {}).get("latitude", 0), 
                        loc.get("coordinates", {}).get("longitude", 0)] 
                       for loc in locations 
                       if loc.get("coordinates", {}).get("latitude", 0) != 0]
        
        if heatmap_data:
            folium.plugins.HeatMap(
                heatmap_data,
                radius=25,
                blur=20,
                max_zoom=15,
                gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}
            ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def create_confidence_chart(locations):
    """
    Create a Plotly bar chart showing the distribution of confidence levels.
    
    Args:
        locations (list): List of location dictionaries with confidence levels
        
    Returns:
        plotly.graph_objects.Figure or None: Bar chart figure if locations exist, None otherwise
        
    Features:
        - Color-coded confidence levels (High=Green, Medium=Yellow, Low=Red)
        - Responsive design with dark theme styling
        - Clear labels and title
    """
    if not locations:
        return None
    
    confidence_counts = {}
    for location in locations:
        confidence = location.get("confidence", "Unknown")
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
    
    fig = px.bar(
        x=list(confidence_counts.keys()),
        y=list(confidence_counts.values()),
        title="Confidence Distribution",
        labels={'x': 'Confidence Level', 'y': 'Number of Predictions'},
        color=list(confidence_counts.keys()),
        color_discrete_map={
            'High': '#28a745',
            'Medium': '#ffc107', 
            'Low': '#dc3545',
            'Unknown': '#6c757d'
        }
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_ranking_comparison(locations):
    """
    Create a pandas DataFrame for location comparison table.
    
    Args:
        locations (list): List of location dictionaries with metadata
        
    Returns:
        pandas.DataFrame or None: Comparison table if locations exist, None otherwise
        
    Features:
        - Ranked locations with city, state, country
        - Confidence levels and coordinates
        - Formatted for easy reading in Streamlit
    """
    if not locations:
        return None
    
    # Prepare data for comparison
    comparison_data = []
    for i, location in enumerate(locations):
        coords = location.get("coordinates", {})
        comparison_data.append({
            "Rank": f"#{i+1}",
            "City": location.get("city", "Unknown"),
            "State/Region": location.get("state", "Unknown"),
            "Country": location.get("country", "Unknown"),
            "Confidence": location.get("confidence", "Medium"),
            "Latitude": f"{coords.get('latitude', 0):.4f}",
            "Longitude": f"{coords.get('longitude', 0):.4f}"
        })
    
    df = pd.DataFrame(comparison_data)
    return df

def display_location_ranking(locations):
    """
    Display the top 3 location predictions in a ranked card format.
    
    Args:
        locations (list): List of location dictionaries with metadata and AI reasoning
        
    Features:
        - Gold/Silver/Bronze ranking styling
        - City, state, and country information
        - Precise coordinates display
        - Expandable AI reasoning sections
        - Professional card-based layout
    """
    if not locations:
        return
    
    st.markdown('<h3 class="section-header">🏆 Top 3 Location Predictions</h3>', unsafe_allow_html=True)
    
    # Only show top 3 locations
    top_locations = locations[:3]
    
    for i, location in enumerate(top_locations):
        rank = i + 1
        
        # Create ranking card without confidence
        st.markdown(f"""
        <div class="ranking-card">
            <div class="location-header">
                <div class="ranking-number ranking-{min(rank, 3)}">{rank}</div>
                <div>
                    <h4 class="location-title">{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}</h4>
                    <p class="location-subtitle">{location.get('state', 'Unknown')}</p>
                </div>
            </div>
            <div style="margin-left: 3.5rem;">
                <p><strong>📍 Coordinates:</strong> {location.get('coordinates', {}).get('latitude', 0):.6f}, {location.get('coordinates', {}).get('longitude', 0):.6f}</p>
                <details>
                    <summary><strong>💡 AI Reasoning</strong></summary>
                    <p style="margin-top: 0.5rem; color: #666;">{location.get('explanation', 'No explanation provided')}</p>
                </details>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main Streamlit application entry point.
    
    This function orchestrates the entire GeoSpy web application, including:
    - User interface setup with dark theme styling
    - Sidebar configuration for API key and context
    - Image upload handling (file or URL)
    - AI analysis processing with error handling
    - Results display with interactive visualizations
    
    Features:
        - Professional dark theme UI
        - Secure API key input
        - Multiple image upload methods
        - Comprehensive error handling
        - Interactive maps and analytics
        - Top 3 location predictions with AI reasoning
    """
    # Application header and branding
    st.markdown('<h1 class="main-header">🌍 GeoSpy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Image Geolocation with **Top 3 Location Predictions**</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input (hidden by default)
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key to enable image analysis.",
            placeholder="Enter your API key here..."
        )
        
        if not api_key:
            st.error("⚠️ API key required")
            st.info("""
            **Get your API key:**
            1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Create a new API key
            3. Enter it above to start analyzing images
            """)
            return
        
        st.divider()
        
        # Additional context
        context_info = st.text_area(
            "Additional Context (Optional)",
            placeholder="Any additional information that might help with location identification...",
            height=100,
            help="Provide extra context like time of day, weather, or known landmarks"
        )
        
        # Location guess
        location_guess = st.text_input(
            "Location Hint (Optional)",
            placeholder="e.g., 'This might be in Paris, France'",
            help="Provide a hint about the possible location"
        )
        
        st.divider()
        
        # About section
        st.header("ℹ️ About GeoSpy")
        st.markdown("""
        **GeoSpy** uses advanced AI to analyze images and identify their geographical location.
        
        **Features:**
        - 🏛️ Architectural analysis
        - 🌿 Environmental indicators  
        - 🚗 Cultural context
        - 📍 **Top 3 location predictions**
        - 🗺️ Interactive maps
        - 📊 AI reasoning analysis
        - 🏆 **Ranked predictions (1st, 2nd, 3rd)**
        
        **How it works:**
        1. Upload an image
        2. AI analyzes visual elements
        3. Get **top 3 location predictions** with AI reasoning
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">📸 Upload Image</h2>', unsafe_allow_html=True)
        
        # File uploader with better styling
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload an image to analyze its location"
        )
        
        # URL input as alternative
        st.markdown("---")
        st.subheader("Or enter image URL")
        image_url = st.text_input(
            "Image URL",
            placeholder="https://example.com/image.jpg",
            help="Provide a direct link to an image"
        )
        
        # Process button
        if uploaded_file or image_url:
            if st.button("🔍 Analyze Location", type="primary", use_container_width=True):
                with st.spinner("Analyzing image with AI..."):
                    try:
                        # Initialize GeoSpy
                        geospy = GeoSpy(api_key=api_key)
                        
                        # Process image
                        if uploaded_file:
                            # Save uploaded file temporarily
                            temp_path = f"temp_{uploaded_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            result = geospy.locate(
                                image_path=temp_path,
                                context_info=context_info if context_info else None,
                                location_guess=location_guess if location_guess else None
                            )
                            
                            # Clean up temp file
                            os.remove(temp_path)
                        else:
                            result = geospy.locate(
                                image_path=image_url,
                                context_info=context_info if context_info else None,
                                location_guess=location_guess if location_guess else None
                            )
                        
                        # Store result in session state
                        st.session_state.result = result
                        st.session_state.image_source = uploaded_file if uploaded_file else image_url
                        st.session_state.analysis_time = datetime.now()
                        
                    except Exception as e:
                        error_msg = str(e)
                        
                        # Handle specific API errors
                        if "503" in error_msg or "overloaded" in error_msg.lower() or "unavailable" in error_msg.lower():
                            st.error("""
                            🔄 **API Temporarily Overloaded**
                            
                            The Gemini API is experiencing high traffic right now. This is a temporary issue.
                            
                            **Solutions:**
                            - ⏱️ **Wait 1-2 minutes** and try again
                            - 🔄 **Refresh the page** and retry
                            - 🌙 **Try during off-peak hours** (late night/early morning)
                            
                            This is not a problem with your setup - it's a server-side issue.
                            """)
                        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                            st.error("""
                            📊 **API Quota Exceeded**
                            
                            You've reached your Gemini API usage limit.
                            
                            **Solutions:**
                            - 💳 **Check your API quota** at [Google AI Studio](https://makersuite.google.com/app/apikey)
                            - 🔄 **Wait for quota reset** (usually daily)
                            - 📈 **Upgrade your plan** if needed
                            """)
                        elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
                            st.error("""
                            🔑 **Invalid API Key**
                            
                            The API key you provided is not valid.
                            
                            **Solutions:**
                            - 🔑 **Check your API key** at [Google AI Studio](https://makersuite.google.com/app/apikey)
                            - 📋 **Copy the key carefully** (no extra spaces)
                            - 🔄 **Generate a new key** if needed
                            """)
                        else:
                            st.error(f"❌ **Analysis Error:** {error_msg}")
                        
                        # Show technical details in expander
                        with st.expander("🔧 Technical Details"):
                            st.code(f"Error: {error_msg}")
                            st.info("If this error persists, please check your internet connection and API key.")
    
    with col2:
        st.markdown('<h2 class="section-header">📍 Results</h2>', unsafe_allow_html=True)
        
        # Display image
        if 'image_source' in st.session_state:
            if isinstance(st.session_state.image_source, str):  # URL
                st.image(st.session_state.image_source, caption="Uploaded Image", use_container_width=True)
            else:  # Uploaded file
                st.image(st.session_state.image_source, caption="Uploaded Image", use_container_width=True)
        
        # Display results
        if 'result' in st.session_state:
            result = st.session_state.result
            
            if "error" in result:
                st.error(f"❌ Analysis failed: {result['error']}")
                if "details" in result:
                    with st.expander("Error Details"):
                        st.text(result["details"])
            else:
                # Display interpretation
                if "interpretation" in result:
                    with st.expander("🔍 Image Analysis", expanded=True):
                        st.markdown(result["interpretation"])
                
                # Display locations
                if "locations" in result and result["locations"]:
                    locations = result["locations"]
                    
                    # Create metrics row
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{len(locations)}</div>
                            <div class="metric-label">Predictions</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        high_conf = sum(1 for loc in locations if loc.get('confidence') == 'High')
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{high_conf}</div>
                            <div class="metric-label">High Confidence</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_c:
                        avg_lat = np.mean([loc.get("coordinates", {}).get("latitude", 0) for loc in locations if loc.get("coordinates", {}).get("latitude", 0) != 0])
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{avg_lat:.2f}°</div>
                            <div class="metric-label">Avg Latitude</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display location rankings
                    display_location_ranking(locations)
                    
                    # Interactive Map
                    st.markdown('<h3 class="section-header">🗺️ Interactive Map</h3>', unsafe_allow_html=True)
                    map_obj = create_interactive_map(locations)
                    if map_obj:
                        st_folium(map_obj, width=700, height=500)
                    else:
                        st.warning("⚠️ No valid coordinates found for mapping")
                    
                    # Location Comparison Table
                    st.markdown('<h3 class="section-header">📊 Location Comparison</h3>', unsafe_allow_html=True)
                    comparison_df = create_ranking_comparison(locations)
                    if comparison_df is not None:
                        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                    
                    # Analytics Charts
                    st.markdown('<h3 class="section-header">📈 Analytics</h3>', unsafe_allow_html=True)
                    
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        conf_chart = create_confidence_chart(locations)
                        if conf_chart:
                            st.plotly_chart(conf_chart, use_container_width=True)
                    
                    # Analysis timestamp
                    if 'analysis_time' in st.session_state:
                        st.caption(f"Analysis completed at: {st.session_state.analysis_time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    st.warning("⚠️ No locations identified in the analysis")

if __name__ == "__main__":
    main() 