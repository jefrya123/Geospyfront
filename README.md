# 🌍 GeoSpy - AI-Powered Image Geolocation

[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org/)

**GeoSpy** is an advanced AI-powered image geolocation tool that uses Google's Gemini AI to analyze images and identify their geographical location with interactive maps and detailed analytics.

> **Note**: This is an enhanced version of the original [GeoSpy](https://github.com/atiilla/geospy) project by [Atilla](https://github.com/atiilla), featuring a professional Streamlit web interface, Docker containerization, and improved user experience.

## ✨ Features

- 🏛️ **Architectural Analysis** - Identifies building styles and landmarks
- 🌿 **Environmental Indicators** - Analyzes climate, vegetation, and terrain
- 🚗 **Cultural Context** - Recognizes language, vehicles, and cultural elements
- 📍 **Coordinate Estimation** - Provides precise latitude/longitude coordinates
- 🗺️ **Interactive Maps** - Satellite view with color-coded confidence markers
- 🔥 **Heatmap Visualization** - Shows multiple location predictions
- 📊 **Analytics Dashboard** - Confidence charts and detailed metrics
- 🎨 **Professional UI** - Clean, modern interface with responsive design

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/jefrya123/Geospyfront.git
   cd Geospyfront
   ```

2. **Get your API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in and create a new API key
   - Copy the generated key

3. **Set your API key**
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

5. **Open your browser**
   Navigate to `http://localhost:8502`

### Option 2: Local Development

1. **Clone and setup**
   ```bash
   git clone https://github.com/jefrya123/Geospyfront.git
   cd Geospyfront
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set environment variable**
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

3. **Run the app**
   ```bash
   streamlit run streamlit_app_clean.py
   ```

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Set it as an environment variable or enter it in the app

> **⚠️ Security Note**: Each user needs their own API key. Never share your API key publicly or commit it to version control.

## 📸 Screenshots

### API Key Setup
![API Key Setup](docs/screenshots/api-key-setup.png)
*Secure API key entry with clear instructions and validation*

### Docker Setup
![Docker Setup](docs/screenshots/docker-setup.png)
*Simple Docker Compose setup with one command*

### Main Interface
![Main Interface](docs/screenshots/main-interface.png)
*Clean, professional interface with upload area and results panel*

### Results Analysis
![Results Analysis](docs/screenshots/results-analysis.png)
*AI analysis results with uploaded image, interpretation, and metrics*

### Interactive Map & Analytics
![Interactive Map & Analytics](docs/screenshots/map-analytics.png)
*Interactive map with location markers and confidence analytics dashboard*

### Location Details
![Location Details](docs/screenshots/location-details.png)
*Detailed location information with coordinates and reasoning*

## 🎯 How to Use

### 1. Upload an Image
- Drag and drop an image file (PNG, JPG, JPEG, GIF, BMP)
- Or provide a direct image URL
- Supported file size: Up to 200MB

### 2. Configure Analysis
- Enter your Gemini API key in the sidebar
- Add optional context (time of day, weather, landmarks)
- Provide location hints if you have any

### 3. Analyze Location
- Click "🔍 Analyze Location" to start AI analysis
- Wait 5-15 seconds for processing
- View results on interactive maps and charts

### 4. Explore Results
- **Interactive Map**: See location markers with confidence levels
- **Analytics**: View confidence distribution and metrics
- **Details**: Expand location cards for coordinates and reasoning
- **Google Maps**: Click links to view locations on Google Maps

## 🏗️ Architecture

```
geospy/
├── geospyer/                 # Core GeoSpy library
│   ├── __init__.py
│   ├── geospy.py            # Main GeoSpy class
│   └── cli.py               # Command-line interface
├── streamlit_app_clean.py   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── examples/               # Usage examples
│   └── library_usage.py
└── docs/                   # Documentation
    └── screenshots/        # Screenshots for README
```

## 🛠️ Technology Stack

- **Backend**: Python 3.11+
- **AI**: Google Gemini API
- **Web Framework**: Streamlit
- **Maps**: Folium with OpenStreetMap
- **Visualization**: Plotly
- **Containerization**: Docker & Docker Compose
- **Image Processing**: Pillow

## 📊 How It Works

1. **Image Upload** - User uploads an image or provides a URL
2. **AI Analysis** - Gemini AI analyzes visual elements:
   - Architectural features and building styles
   - Environmental indicators (climate, vegetation)
   - Cultural elements (language, vehicles, signage)
   - Landmarks and distinctive features
3. **Location Prediction** - AI provides multiple location predictions with confidence levels
4. **Visualization** - Results displayed on interactive maps with analytics

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | ✅ Yes |

### Docker Configuration

The app runs on port `8502` by default. You can change this in `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"  # Change 8502 to your preferred port
```

## 📈 Performance

- **Image Size**: Supports up to 200MB per file
- **Formats**: PNG, JPG, JPEG, GIF, BMP
- **Response Time**: Typically 5-15 seconds depending on image complexity
- **Accuracy**: High confidence predictions for distinctive landmarks and locations

## 🚨 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   docker-compose logs
   docker-compose down && docker-compose up --build
   ```

2. **API key issues**
   ```bash
   echo $GEMINI_API_KEY  # Check if set
   docker-compose down && GEMINI_API_KEY="your_key" docker-compose up -d
   ```

3. **Port conflicts**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8503:8501"  # Use different host port
   ```

4. **Memory issues**
   ```bash
   # Increase memory limit
   docker run --memory=2g -p 8502:8501 geospy
   ```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/jefrya123/Geospyfront/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jefrya123/Geospyfront/discussions)
- **Email**: jefrya123@gmail.com

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Original Project**: This project is based on [GeoSpy](https://github.com/atiilla/geospy) by [Atilla](https://github.com/atiilla)
- [Google Gemini AI](https://ai.google.dev/) for the AI capabilities
- [Streamlit](https://streamlit.io/) for the web framework
- [Folium](https://python-visualization.github.io/folium/) for interactive maps
- [Plotly](https://plotly.com/) for data visualization

## 🔮 Roadmap

- [ ] Batch processing for multiple images
- [ ] Historical image analysis
- [ ] Mobile app version
- [ ] API endpoint for programmatic access
- [ ] Integration with other mapping services
- [ ] Advanced analytics and reporting

---

**Made with ❤️ by [Jeff](https://github.com/jefrya123)**

*GeoSpy - Discover the world through AI-powered image analysis*