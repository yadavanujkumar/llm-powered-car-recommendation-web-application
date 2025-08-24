import requests
import os
from typing import Optional, List
import json
from car_placeholders import get_car_placeholder_image

class CarImageService:
    """Service to fetch car images from online sources"""
    
    def __init__(self):
        # Use local placeholder images that won't be blocked
        self.use_local_placeholders = True
        
        # Default fallback image (local base64 encoded SVG)
        self.default_image = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDQwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjBmMGYwIi8+Cjx0ZXh0IHg9IjIwMCIgeT0iMTAwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiM2Njc2ZWEiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7wn5qBIENhcjwvdGV4dD4KPC9zdmc+Cg=="

    def get_car_image_url(self, brand: str, model: str, category: str = None) -> str:
        """Get image URL for a specific car"""
        if self.use_local_placeholders:
            return get_car_placeholder_image(brand, model)
        
        # Return default car image
        return self.default_image

    def get_multiple_car_images(self, brand: str, model: str, category: str = None, count: int = 3) -> List[str]:
        """Get multiple image URLs for a car (for gallery view)"""
        primary_image = self.get_car_image_url(brand, model, category)
        
        # For placeholder images, just return the same image
        images = [primary_image] * count
        
        return images[:count]

    def is_image_url_valid(self, url: str) -> bool:
        """Check if an image URL is accessible"""
        if url.startswith("data:"):
            return True  # Base64 encoded images are always valid
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_car_images_with_fallback(self, brand: str, model: str, category: str = None) -> dict:
        """Get car images with fallback and validation"""
        primary_url = self.get_car_image_url(brand, model, category)
        gallery_urls = self.get_multiple_car_images(brand, model, category, 3)
        
        return {
            "primary": primary_url,
            "gallery": gallery_urls,
            "alt_text": f"{brand} {model}",
            "caption": f"{brand} {model}"
        }