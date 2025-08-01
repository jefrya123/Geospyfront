"""
GeoSpy Library Package

A Python library for AI-powered image geolocation using Google's Gemini AI.
This package provides the core functionality for analyzing images and identifying
geographical locations based on visual elements.

Main Components:
    - GeoSpy: Main class for image analysis and location prediction
    - CLI: Command-line interface for batch processing
    - Core AI integration with Gemini API

Author: Atilla (Original), Enhanced version
License: MIT
"""

from .geospy import GeoSpy

__version__ = "0.1.9"
__all__ = ["GeoSpy"]