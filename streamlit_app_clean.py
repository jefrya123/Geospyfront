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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GeoSpy - AI Image Geolocation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .confidence-high { 
        color: #28a745; 
        font-weight: bold; 
        background: rgba(40, 167, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .confidence-medium { 
        color: #ffc107; 
        font-weight: bold; 
        background: rgba(255, 193, 7, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .confidence-low { 
        color: #dc3545; 
        font-weight: bold; 
        background: rgba(220, 53, 69, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    .upload-area {
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #667eea;
        background: #f0f2ff;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        color: #333;
    }
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .ranking-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
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
        color: white;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 1.2rem;
        margin-right: 1rem;
    }
    .ranking-1 { background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #333; }
    .ranking-2 { background: linear-gradient(135deg, #c0c0c0 0%, #e0e0e0 100%); color: #333; }
    .ranking-3 { background: linear-gradient(135deg, #cd7f32 0%, #daa520 100%); color: white; }
    .location-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .location-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        margin: 0;
    }
    .location-subtitle {
        color: #666;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    .comparison-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def create_interactive_map(locations):
    """Create an interactive map with location markers and heatmap"""
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
    """Create a confidence distribution chart"""
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
    """Create a comparison table of all locations"""
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
    """Display locations in a ranking format"""
    if not locations:
        return
    
    st.markdown('<h3 class="section-header">🏆 Location Rankings</h3>', unsafe_allow_html=True)
    
    for i, location in enumerate(locations):
        rank = i + 1
        confidence = location.get("confidence", "Medium")
        
        # Determine confidence styling
        if confidence == "High":
            conf_class = "confidence-high"
        elif confidence == "Medium":
            conf_class = "confidence-medium"
        else:
            conf_class = "confidence-low"
        
        # Create ranking card
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
                <p><strong>🎯 Confidence:</strong> <span class="{conf_class}">{confidence}</span></p>
                <p><strong>📍 Coordinates:</strong> {location.get('coordinates', {}).get('latitude', 0):.6f}, {location.get('coordinates', {}).get('longitude', 0):.6f}</p>
                <details>
                    <summary><strong>💡 Reasoning</strong></summary>
                    <p style="margin-top: 0.5rem; color: #666;">{location.get('explanation', 'No explanation provided')}</p>
                </details>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoSpy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Image Geolocation with Multiple Location Predictions</p>', unsafe_allow_html=True)
    
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
        - 📍 Multiple location predictions
        - 🗺️ Interactive maps
        - 📊 Confidence analytics
        - 🏆 Location rankings
        
        **How it works:**
        1. Upload an image
        2. AI analyzes visual elements
        3. Get top 3-5 location predictions with confidence levels
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
                        st.error(f"❌ Error analyzing image: {str(e)}")
    
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