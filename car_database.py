import json
import os

class CarDatabase:
    def __init__(self):
        self.cars = self._load_car_data()
    
    def _load_car_data(self):
        """Load comprehensive car database"""
        return [
            # Luxury Cars
            {
                "brand": "Mercedes-Benz",
                "model": "S-Class",
                "year": 2024,
                "price_range": {"min": 110000, "max": 200000},
                "category": "luxury_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 16, "highway": 24},
                "features": ["leather_seats", "premium_audio", "advanced_safety", "autonomous_driving"],
                "emotions": ["sophistication", "prestige", "comfort"],
                "body_type": "sedan",
                "seats": 5,
                "description": "The pinnacle of luxury and technology in a sedan",
                "suitable_for": ["executives", "luxury_seekers", "comfort_prioritizers"]
            },
            {
                "brand": "BMW",
                "model": "7 Series",
                "year": 2024,
                "price_range": {"min": 95000, "max": 160000},
                "category": "luxury_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 18, "highway": 25},
                "features": ["sport_mode", "premium_interior", "advanced_tech", "massage_seats"],
                "emotions": ["sportiness", "luxury", "performance"],
                "body_type": "sedan",
                "seats": 5,
                "description": "German engineering meets luxury comfort",
                "suitable_for": ["driving_enthusiasts", "luxury_seekers", "tech_lovers"]
            },
            {
                "brand": "Audi",
                "model": "A8",
                "year": 2024,
                "price_range": {"min": 88000, "max": 140000},
                "category": "luxury_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 17, "highway": 26},
                "features": ["quattro_awd", "virtual_cockpit", "matrix_led", "air_suspension"],
                "emotions": ["sophistication", "technology", "precision"],
                "body_type": "sedan",
                "seats": 5,
                "description": "Technology-forward luxury with all-wheel drive capability",
                "suitable_for": ["tech_enthusiasts", "all_weather_drivers", "luxury_seekers"]
            },
            
            # Sports Cars
            {
                "brand": "Porsche",
                "model": "911 Carrera",
                "year": 2024,
                "price_range": {"min": 115000, "max": 250000},
                "category": "sports_car",
                "fuel_type": "gasoline",
                "mpg": {"city": 18, "highway": 24},
                "features": ["rear_engine", "sport_suspension", "track_mode", "premium_brakes"],
                "emotions": ["excitement", "performance", "heritage"],
                "body_type": "coupe",
                "seats": 4,
                "description": "Iconic sports car with unmatched driving dynamics",
                "suitable_for": ["sports_car_enthusiasts", "track_day_lovers", "collectors"]
            },
            {
                "brand": "Chevrolet",
                "model": "Corvette Stingray",
                "year": 2024,
                "price_range": {"min": 68000, "max": 85000},
                "category": "sports_car",
                "fuel_type": "gasoline",
                "mpg": {"city": 15, "highway": 27},
                "features": ["mid_engine", "removable_roof", "magnetic_suspension", "performance_exhaust"],
                "emotions": ["american_muscle", "excitement", "value"],
                "body_type": "coupe",
                "seats": 2,
                "description": "America's sports car with mid-engine layout",
                "suitable_for": ["american_car_lovers", "performance_seekers", "value_conscious"]
            },
            
            # Family Cars
            {
                "brand": "Toyota",
                "model": "Camry",
                "year": 2024,
                "price_range": {"min": 26000, "max": 38000},
                "category": "family_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 22, "highway": 32},
                "features": ["toyota_safety_sense", "spacious_interior", "reliable", "fuel_efficient"],
                "emotions": ["reliability", "practicality", "family_oriented"],
                "body_type": "sedan",
                "seats": 5,
                "description": "Reliable family sedan with excellent fuel economy",
                "suitable_for": ["families", "commuters", "reliability_seekers"]
            },
            {
                "brand": "Honda",
                "model": "Accord",
                "year": 2024,
                "price_range": {"min": 27000, "max": 40000},
                "category": "family_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 23, "highway": 34},
                "features": ["honda_sensing", "spacious_cabin", "smooth_cvt", "quality_interior"],
                "emotions": ["dependability", "comfort", "smart_choice"],
                "body_type": "sedan",
                "seats": 5,
                "description": "Well-rounded family sedan with advanced safety features",
                "suitable_for": ["families", "long_distance_drivers", "safety_conscious"]
            },
            
            # SUVs
            {
                "brand": "Jeep",
                "model": "Wrangler",
                "year": 2024,
                "price_range": {"min": 35000, "max": 65000},
                "category": "off_road_suv",
                "fuel_type": "gasoline",
                "mpg": {"city": 17, "highway": 25},
                "features": ["4x4_capability", "removable_doors", "rugged_design", "off_road_ready"],
                "emotions": ["adventure", "freedom", "ruggedness"],
                "body_type": "suv",
                "seats": 4,
                "description": "Ultimate off-road vehicle for adventure seekers",
                "suitable_for": ["outdoor_enthusiasts", "off_road_lovers", "adventure_seekers"]
            },
            {
                "brand": "Toyota",
                "model": "RAV4",
                "year": 2024,
                "price_range": {"min": 30000, "max": 42000},
                "category": "compact_suv",
                "fuel_type": "gasoline",
                "mpg": {"city": 25, "highway": 33},
                "features": ["awd_available", "cargo_space", "ground_clearance", "safety_features"],
                "emotions": ["practicality", "versatility", "reliability"],
                "body_type": "suv",
                "seats": 5,
                "description": "Practical compact SUV perfect for families",
                "suitable_for": ["families", "city_drivers", "practical_buyers"]
            },
            
            # Electric Cars
            {
                "brand": "Tesla",
                "model": "Model S",
                "year": 2024,
                "price_range": {"min": 75000, "max": 130000},
                "category": "electric_luxury",
                "fuel_type": "electric",
                "mpg": {"city": 120, "highway": 115},  # MPGe
                "features": ["autopilot", "supercharging", "over_the_air_updates", "minimalist_interior"],
                "emotions": ["innovation", "environmental_consciousness", "technology"],
                "body_type": "sedan",
                "seats": 5,
                "description": "High-performance electric luxury sedan",
                "suitable_for": ["tech_enthusiasts", "environmentally_conscious", "early_adopters"]
            },
            {
                "brand": "Nissan",
                "model": "Leaf",
                "year": 2024,
                "price_range": {"min": 32000, "max": 40000},
                "category": "electric_compact",
                "fuel_type": "electric",
                "mpg": {"city": 123, "highway": 99},  # MPGe
                "features": ["affordable_electric", "spacious_interior", "quick_charge", "eco_friendly"],
                "emotions": ["environmental_responsibility", "economy", "smart_choice"],
                "body_type": "hatchback",
                "seats": 5,
                "description": "Affordable electric car for everyday driving",
                "suitable_for": ["eco_conscious", "city_commuters", "budget_minded"]
            },
            
            # Trucks
            {
                "brand": "Ford",
                "model": "F-150",
                "year": 2024,
                "price_range": {"min": 35000, "max": 75000},
                "category": "pickup_truck",
                "fuel_type": "gasoline",
                "mpg": {"city": 19, "highway": 24},
                "features": ["towing_capacity", "cargo_space", "4x4_available", "work_ready"],
                "emotions": ["capability", "american_strength", "work_ethic"],
                "body_type": "truck",
                "seats": 6,
                "description": "America's best-selling truck for work and play",
                "suitable_for": ["workers", "outdoor_enthusiasts", "large_families"]
            },
            
            # Budget Cars
            {
                "brand": "Hyundai",
                "model": "Elantra",
                "year": 2024,
                "price_range": {"min": 22000, "max": 28000},
                "category": "budget_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 28, "highway": 37},
                "features": ["warranty", "fuel_efficient", "modern_design", "tech_features"],
                "emotions": ["value", "practicality", "smart_purchase"],
                "body_type": "sedan",
                "seats": 5,
                "description": "Stylish and affordable sedan with great warranty",
                "suitable_for": ["first_time_buyers", "budget_conscious", "young_professionals"]
            },
            {
                "brand": "Kia",
                "model": "Forte",
                "year": 2024,
                "price_range": {"min": 20000, "max": 25000},
                "category": "budget_sedan",
                "fuel_type": "gasoline",
                "mpg": {"city": 27, "highway": 37},
                "features": ["long_warranty", "spacious_interior", "modern_infotainment", "efficient"],
                "emotions": ["value", "reliability", "smart_choice"],
                "body_type": "sedan",
                "seats": 5,
                "description": "Excellent value sedan with impressive warranty",
                "suitable_for": ["budget_buyers", "practical_shoppers", "warranty_seekers"]
            }
        ]
    
    def search_by_budget(self, min_budget, max_budget):
        """Filter cars by budget range"""
        matching_cars = []
        for car in self.cars:
            car_min = car["price_range"]["min"]
            car_max = car["price_range"]["max"]
            
            # Check if there's any overlap with user's budget
            if car_min <= max_budget and car_max >= min_budget:
                matching_cars.append(car)
        
        return matching_cars
    
    def search_by_category(self, categories):
        """Filter cars by category"""
        if isinstance(categories, str):
            categories = [categories]
        
        return [car for car in self.cars if car["category"] in categories]
    
    def search_by_features(self, required_features):
        """Filter cars by required features"""
        matching_cars = []
        for car in self.cars:
            if all(feature in car["features"] for feature in required_features):
                matching_cars.append(car)
        return matching_cars
    
    def search_by_emotions(self, user_emotions):
        """Filter cars by emotional appeal"""
        matching_cars = []
        for car in self.cars:
            # Check if car emotions match user emotions
            if any(emotion in car["emotions"] for emotion in user_emotions):
                matching_cars.append(car)
        return matching_cars
    
    def get_all_cars(self):
        """Return all cars in database"""
        return self.cars
    
    def get_car_by_id(self, brand, model):
        """Get specific car by brand and model"""
        for car in self.cars:
            if car["brand"].lower() == brand.lower() and car["model"].lower() == model.lower():
                return car
        return None