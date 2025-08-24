import requests
import json
from typing import Dict, List, Optional, Any
import os
from car_database import CarDatabase

class ExternalCarDataService:
    """Service to fetch car data from external APIs and websites"""
    
    def __init__(self):
        self.static_db = CarDatabase()
        
        # API endpoints (these would be real APIs in production)
        # For now, we'll use enhanced static data with online features
        self.car_api_base = "https://api.nhtsa.gov/SafetyRatings"
        self.fuel_economy_api = "https://www.fueleconomy.gov/ws/rest"
        
        # Enhanced car data with more realistic online information
        self.enhanced_car_data = self._load_enhanced_car_data()
    
    def _load_enhanced_car_data(self) -> List[Dict]:
        """Load enhanced car database with simulated online data"""
        # Get base cars from static database
        base_cars = self.static_db.get_all_cars()
        
        # Enhance with additional online-like data
        enhanced_cars = []
        
        for car in base_cars:
            enhanced_car = car.copy()
            
            # Add online-like features
            enhanced_car.update({
                "images": self._get_car_images(car["brand"], car["model"], car["category"]),
                "reviews": self._get_mock_reviews(car["brand"], car["model"]),
                "availability": self._get_availability_info(car["brand"], car["model"]),
                "financing": self._get_financing_info(car["price_range"]),
                "dealer_info": self._get_dealer_info(car["brand"]),
                "market_trends": self._get_market_trends(car["category"]),
                "safety_rating": self._get_safety_rating(car["brand"], car["model"]),
                "reliability_score": self._get_reliability_score(car["brand"], car["model"]),
                "resale_value": self._get_resale_value(car["brand"], car["model"]),
                "fuel_costs": self._calculate_fuel_costs(car.get("mpg", {})),
                "insurance_estimate": self._estimate_insurance(car["category"], car["price_range"]),
                "similar_cars": self._get_similar_cars(car["category"], car["brand"]),
                "awards": self._get_awards(car["brand"], car["model"]),
                "recall_info": self._get_recall_info(car["brand"], car["model"]),
                "tech_features": self._get_tech_features(car["category"], car["year"]),
                "warranty": self._get_warranty_info(car["brand"]),
                "colors_available": self._get_available_colors(car["brand"], car["model"])
            })
            
            enhanced_cars.append(enhanced_car)
        
        return enhanced_cars
    
    def _get_car_images(self, brand: str, model: str, category: str) -> Dict:
        """Simulate getting car images from online sources"""
        from car_image_service import CarImageService
        image_service = CarImageService()
        return image_service.get_car_images_with_fallback(brand, model, category)
    
    def _get_mock_reviews(self, brand: str, model: str) -> Dict:
        """Generate mock review data"""
        return {
            "average_rating": round(3.5 + (hash(brand + model) % 15) / 10, 1),
            "total_reviews": (hash(brand + model) % 500) + 50,
            "expert_rating": round(4.0 + (hash(model) % 10) / 10, 1),
            "owner_rating": round(3.8 + (hash(brand) % 12) / 10, 1),
            "top_pros": ["Reliable", "Good fuel economy", "Comfortable"],
            "top_cons": ["Road noise", "Interior materials", "Price"]
        }
    
    def _get_availability_info(self, brand: str, model: str) -> Dict:
        """Get availability and inventory information"""
        return {
            "in_stock": (hash(brand + model) % 10) > 2,
            "estimated_delivery": f"{(hash(model) % 8) + 1}-{(hash(brand) % 4) + 2} weeks",
            "nearby_dealers": (hash(brand) % 15) + 5,
            "inventory_level": ["Low", "Medium", "High"][hash(model) % 3]
        }
    
    def _get_financing_info(self, price_range: Dict) -> Dict:
        """Get financing and pricing information"""
        avg_price = (price_range["min"] + price_range["max"]) / 2
        
        return {
            "starting_apr": round(2.9 + (avg_price / 100000) * 2, 1),
            "estimated_monthly": round((avg_price * 0.02), 0),
            "lease_monthly": round((avg_price * 0.008), 0),
            "down_payment_options": [0.1, 0.15, 0.2],
            "loan_terms": [36, 48, 60, 72],
            "incentives": ["$500 cash back", "0.9% APR financing"] if avg_price > 40000 else ["First-time buyer discount"]
        }
    
    def _get_dealer_info(self, brand: str) -> Dict:
        """Get dealer information"""
        return {
            "nearest_dealer": f"{brand} of Downtown",
            "dealer_rating": round(3.5 + (hash(brand) % 15) / 10, 1),
            "distance": f"{(hash(brand) % 25) + 1} miles",
            "contact": f"(555) {hash(brand) % 900 + 100}-{hash(brand) % 9000 + 1000}"
        }
    
    def _get_market_trends(self, category: str) -> Dict:
        """Get market trends for car category"""
        trends = {
            "luxury_sedan": {"trend": "stable", "demand": "medium", "price_change": "+2.1%"},
            "sports_car": {"trend": "rising", "demand": "high", "price_change": "+5.3%"},
            "family_sedan": {"trend": "declining", "demand": "medium", "price_change": "-1.2%"},
            "compact_suv": {"trend": "rising", "demand": "very high", "price_change": "+3.8%"},
            "pickup_truck": {"trend": "stable", "demand": "high", "price_change": "+1.5%"},
            "electric_luxury": {"trend": "surging", "demand": "very high", "price_change": "+8.2%"}
        }
        
        return trends.get(category, {"trend": "stable", "demand": "medium", "price_change": "0%"})
    
    def _get_safety_rating(self, brand: str, model: str) -> Dict:
        """Get safety ratings"""
        base_rating = 4 + (hash(brand + model) % 6) / 10
        return {
            "nhtsa_overall": round(min(5.0, base_rating), 1),
            "iihs_top_safety_pick": (hash(brand) % 5) == 0,
            "crash_test_score": round(min(5.0, base_rating + 0.2), 1),
            "safety_features": ["Automatic emergency braking", "Blind spot monitoring", "Lane departure warning"]
        }
    
    def _get_reliability_score(self, brand: str, model: str) -> Dict:
        """Get reliability information"""
        reliability_brands = {"Toyota": 4.8, "Honda": 4.7, "Hyundai": 4.3, "Kia": 4.2, "Nissan": 4.0}
        base_score = reliability_brands.get(brand, 4.0)
        
        return {
            "overall_score": round(base_score + (hash(model) % 5) / 10, 1),
            "predicted_reliability": "Above Average" if base_score > 4.5 else "Average",
            "maintenance_cost": "Low" if base_score > 4.5 else "Medium",
            "warranty_claims": f"{(5 - int(base_score)) * 2}% below average"
        }
    
    def _get_resale_value(self, brand: str, model: str) -> Dict:
        """Get resale value information"""
        strong_resale_brands = ["Toyota", "Honda", "Porsche", "Tesla"]
        is_strong = brand in strong_resale_brands
        
        return {
            "3_year_retention": f"{65 + (10 if is_strong else 0) + (hash(model) % 8)}%",
            "5_year_retention": f"{45 + (15 if is_strong else 0) + (hash(model) % 10)}%",
            "resale_rating": "Excellent" if is_strong else "Good",
            "market_demand": "High" if is_strong else "Medium"
        }
    
    def _calculate_fuel_costs(self, mpg: Dict) -> Dict:
        """Calculate fuel cost estimates"""
        if not mpg:
            return {"annual_cost": "N/A", "cost_per_mile": "N/A"}
        
        avg_mpg = (mpg.get("city", 25) + mpg.get("highway", 30)) / 2
        gas_price = 3.50  # Current average gas price
        annual_miles = 12000
        
        annual_cost = (annual_miles / avg_mpg) * gas_price
        cost_per_mile = annual_cost / annual_miles
        
        return {
            "annual_cost": f"${annual_cost:.0f}",
            "cost_per_mile": f"${cost_per_mile:.2f}",
            "vs_average": f"{'$' + str(int((25/avg_mpg - 1) * annual_cost))}{' more' if avg_mpg < 25 else ' less'}"
        }
    
    def _estimate_insurance(self, category: str, price_range: Dict) -> Dict:
        """Estimate insurance costs"""
        base_rates = {
            "luxury_sedan": 1800,
            "sports_car": 2500,
            "family_sedan": 1200,
            "compact_suv": 1400,
            "pickup_truck": 1300,
            "electric_luxury": 1600
        }
        
        base_rate = base_rates.get(category, 1300)
        avg_price = (price_range["min"] + price_range["max"]) / 2
        price_factor = avg_price / 50000
        
        annual_cost = base_rate * price_factor
        
        return {
            "annual_estimate": f"${annual_cost:.0f}",
            "monthly_estimate": f"${annual_cost/12:.0f}",
            "factors": ["Vehicle value", "Safety rating", "Theft rates"]
        }
    
    def _get_similar_cars(self, category: str, exclude_brand: str) -> List[Dict]:
        """Get similar cars in the same category"""
        all_cars = self.static_db.get_all_cars()
        similar = [car for car in all_cars 
                  if car["category"] == category and car["brand"] != exclude_brand]
        
        return [{"brand": car["brand"], "model": car["model"], "price_range": car["price_range"]} 
                for car in similar[:3]]
    
    def _get_awards(self, brand: str, model: str) -> List[str]:
        """Get awards and recognition"""
        awards_pool = [
            "IIHS Top Safety Pick",
            "Car and Driver 10Best",
            "MotorTrend Car of the Year",
            "KBB Best Family Car",
            "Consumer Reports Recommended",
            "JD Power Award Winner"
        ]
        
        # Deterministically assign awards based on hash
        num_awards = (hash(brand + model) % 3) + 1
        award_indices = [(hash(brand + model + str(i)) % len(awards_pool)) for i in range(num_awards)]
        
        return [awards_pool[i] for i in award_indices]
    
    def _get_recall_info(self, brand: str, model: str) -> Dict:
        """Get recall information"""
        has_recalls = (hash(brand + model) % 10) < 2  # 20% chance of recalls
        
        if has_recalls:
            return {
                "active_recalls": 1,
                "total_recalls": (hash(model) % 3) + 1,
                "last_recall": "2023-" + str((hash(brand) % 12) + 1).zfill(2),
                "severity": "Minor"
            }
        else:
            return {
                "active_recalls": 0,
                "total_recalls": 0,
                "last_recall": None,
                "severity": None
            }
    
    def _get_tech_features(self, category: str, year: int) -> List[str]:
        """Get technology features"""
        base_features = [
            "Smartphone integration",
            "Backup camera",
            "Bluetooth connectivity",
            "USB ports"
        ]
        
        premium_features = [
            "Wireless charging",
            "Premium audio system",
            "Navigation system",
            "Head-up display",
            "Adaptive cruise control",
            "Lane keeping assist"
        ]
        
        if "luxury" in category or year >= 2024:
            return base_features + premium_features[:4]
        else:
            return base_features + premium_features[:2]
    
    def _get_warranty_info(self, brand: str) -> Dict:
        """Get warranty information"""
        warranty_data = {
            "Hyundai": {"basic": "5 years/60,000 miles", "powertrain": "10 years/100,000 miles"},
            "Kia": {"basic": "5 years/60,000 miles", "powertrain": "10 years/100,000 miles"},
            "Toyota": {"basic": "3 years/36,000 miles", "powertrain": "5 years/60,000 miles"},
            "Honda": {"basic": "3 years/36,000 miles", "powertrain": "5 years/60,000 miles"}
        }
        
        return warranty_data.get(brand, {"basic": "3 years/36,000 miles", "powertrain": "5 years/60,000 miles"})
    
    def _get_available_colors(self, brand: str, model: str) -> List[Dict]:
        """Get available colors"""
        colors = [
            {"name": "Pearl White", "code": "#F8F8FF", "premium": True},
            {"name": "Jet Black", "code": "#000000", "premium": False},
            {"name": "Silver Metallic", "code": "#C0C0C0", "premium": True},
            {"name": "Deep Blue", "code": "#003366", "premium": True},
            {"name": "Crimson Red", "code": "#DC143C", "premium": True},
            {"name": "Titanium Gray", "code": "#708090", "premium": False}
        ]
        
        # Return 4-6 colors based on hash
        num_colors = (hash(brand + model) % 3) + 4
        color_indices = [(hash(brand + model + str(i)) % len(colors)) for i in range(num_colors)]
        
        return [colors[i] for i in color_indices]
    
    def get_all_cars(self) -> List[Dict]:
        """Get all enhanced car data"""
        return self.enhanced_car_data
    
    def get_car_by_id(self, brand: str, model: str) -> Optional[Dict]:
        """Get specific car with enhanced data"""
        for car in self.enhanced_car_data:
            if car["brand"].lower() == brand.lower() and car["model"].lower() == model.lower():
                return car
        return None
    
    def search_cars(self, query: Dict[str, Any]) -> List[Dict]:
        """Search cars with enhanced filtering"""
        results = self.enhanced_car_data.copy()
        
        # Apply filters
        if "budget_max" in query and query["budget_max"]:
            results = [car for car in results if car["price_range"]["min"] <= query["budget_max"]]
        
        if "category" in query and query["category"]:
            results = [car for car in results if car["category"] == query["category"]]
        
        if "fuel_type" in query and query["fuel_type"]:
            results = [car for car in results if car["fuel_type"] == query["fuel_type"]]
        
        if "brand" in query and query["brand"]:
            results = [car for car in results if car["brand"].lower() == query["brand"].lower()]
        
        return results