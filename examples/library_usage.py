#!/usr/bin/env python3
"""
Simple example showing how to use GeoSpy as a library
"""

from geospyer import GeoSpy
import os 
import pathlib
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize GeoSpy with API key from environment variable
# You can also pass the API key directly: GeoSpy(api_key="your_api_key_here")
geospy = GeoSpy()  # Will automatically use GEMINI_API_KEY from environment

# Analyze a local image
image_path = os.path.join(pathlib.Path(__file__).parent.parent, "kule.jpg")
result = geospy.locate(image_path=image_path)

# For this example, let's show how to access the data
if "error" in result:
    print(f"Error: {result['error']}")
    exit(1)

# Example 1: Save the raw JSON to a file
with open("geospy_result.json", "w") as f:
    json.dump(result, f, indent=2)
    
# Example 2: Access specific data from the result
if "locations" in result and result["locations"]:
    # Get the first (most likely) location
    location = result["locations"][0]
    
    # Location details
    city = location.get("city", "Unknown")
    country = location.get("country", "Unknown")
    confidence = location.get("confidence", "Unknown")
    
    # Coordinates for Google Maps
    if "coordinates" in location:
        lat = location["coordinates"].get("latitude", 0)
        lng = location["coordinates"].get("longitude", 0)
        maps_url = f"https://www.google.com/maps?q={lat},{lng}"

# Example 3: Return just the result object for programmatic use
# When using in your own application, you would typically just return this result
# and process it according to your needs
# return result  # Uncomment this in your actual application 