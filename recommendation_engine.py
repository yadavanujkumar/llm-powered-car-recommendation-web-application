from typing import List, Dict, Any
from car_database import CarDatabase

class RecommendationEngine:
    def __init__(self, external_car_service=None):
        self.car_db = CarDatabase()
        self.external_car_service = external_car_service
        
        # Mapping user preferences to car categories
        self.category_mapping = {
            "family": ["family_sedan", "compact_suv", "budget_sedan"],
            "luxury": ["luxury_sedan", "electric_luxury"],
            "sports": ["sports_car"],
            "work": ["pickup_truck"],
            "commuting": ["budget_sedan", "family_sedan", "electric_compact"],
            "off_road": ["off_road_suv"],
            "adventure": ["off_road_suv", "pickup_truck"]
        }
        
        self.emotion_weights = {
            "luxury": {"luxury_sedan": 3, "electric_luxury": 2, "sports_car": 1},
            "reliability": {"family_sedan": 3, "budget_sedan": 2, "compact_suv": 2},
            "excitement": {"sports_car": 3, "electric_luxury": 1},
            "adventure": {"off_road_suv": 3, "pickup_truck": 2},
            "practicality": {"family_sedan": 3, "compact_suv": 2, "budget_sedan": 3},
            "performance": {"sports_car": 3, "luxury_sedan": 2, "electric_luxury": 2},
            "economy": {"budget_sedan": 3, "electric_compact": 2, "family_sedan": 1}
        }
    
    def recommend_cars(self, user_analysis: Dict[str, Any]) -> List[Dict]:
        """Main recommendation function that returns scored and ranked cars"""
        
        # Use external service if available, otherwise fall back to static database
        if self.external_car_service:
            candidate_cars = self.external_car_service.get_all_cars()
        else:
            candidate_cars = self.car_db.get_all_cars()
        
        # Apply filters
        candidate_cars = self._filter_by_budget(candidate_cars, user_analysis)
        candidate_cars = self._filter_by_fuel_preference(candidate_cars, user_analysis)
        candidate_cars = self._filter_by_brand_preference(candidate_cars, user_analysis)
        
        # Score remaining cars
        scored_cars = []
        for car in candidate_cars:
            score = self._calculate_car_score(car, user_analysis)
            scored_cars.append({
                **car,
                "recommendation_score": score,
                "match_reasons": self._get_match_reasons(car, user_analysis)
            })
        
        # Sort by score (descending)
        scored_cars.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return scored_cars
    
    def _filter_by_budget(self, cars: List[Dict], user_analysis: Dict) -> List[Dict]:
        """Filter cars by budget constraints"""
        budget_min = user_analysis.get("budget_min")
        budget_max = user_analysis.get("budget_max")
        
        if not budget_min and not budget_max:
            return cars
        
        # If only one budget value is provided, make reasonable assumptions
        if budget_max and not budget_min:
            budget_min = max(15000, budget_max * 0.5)  # Assume min is 50% of max, at least $15k
        elif budget_min and not budget_max:
            budget_max = min(300000, budget_min * 2)  # Assume max is 200% of min, cap at $300k
        
        return [car for car in cars
                if car["price_range"]["min"] <= budget_max and car["price_range"]["max"] >= budget_min]
    
    def _filter_by_fuel_preference(self, cars: List[Dict], user_analysis: Dict) -> List[Dict]:
        """Filter cars by fuel preference"""
        fuel_pref = user_analysis.get("fuel_preference", "any")
        
        if fuel_pref == "any":
            return cars
        
        return [car for car in cars if car["fuel_type"] == fuel_pref]
    
    def _filter_by_brand_preference(self, cars: List[Dict], user_analysis: Dict) -> List[Dict]:
        """Filter cars by brand preference if specified"""
        brand_pref = user_analysis.get("brand_preference")
        
        if not brand_pref:
            return cars
        
        return [car for car in cars if car["brand"].lower() == brand_pref.lower()]
    
    def _calculate_car_score(self, car: Dict, user_analysis: Dict) -> float:
        """Calculate a recommendation score for a car based on user preferences"""
        score = 0.0
        
        # Usage pattern matching (25% of score)
        usage = user_analysis.get("usage", "commuting")
        if usage in self.category_mapping:
            if car["category"] in self.category_mapping[usage]:
                score += 25.0
        
        # Emotion matching (30% of score)
        user_emotions = user_analysis.get("emotions", [])
        for emotion in user_emotions:
            if emotion in self.emotion_weights:
                category_weights = self.emotion_weights[emotion]
                if car["category"] in category_weights:
                    score += 30.0 * (category_weights[car["category"]] / 3.0) / len(user_emotions)
        
        # Car type preference (20% of score)
        preferred_type = user_analysis.get("car_type")
        if preferred_type:
            if self._car_type_matches(car, preferred_type):
                score += 20.0
        
        # Budget efficiency (15% of score) - favor cars that fit well within budget
        budget_score = self._calculate_budget_score(car, user_analysis)
        score += 15.0 * budget_score
        
        # Feature matching (10% of score)
        feature_score = self._calculate_feature_score(car, user_analysis)
        score += 10.0 * feature_score
        
        return min(score, 100.0)  # Cap at 100
    
    def _car_type_matches(self, car: Dict, preferred_type: str) -> bool:
        """Check if car type matches user preference"""
        type_mapping = {
            "sedan": ["sedan"],
            "suv": ["suv"],
            "sports_car": ["coupe"],
            "truck": ["truck"],
            "hatchback": ["hatchback"]
        }
        
        if preferred_type in type_mapping:
            return car["body_type"] in type_mapping[preferred_type]
        
        return False
    
    def _calculate_budget_score(self, car: Dict, user_analysis: Dict) -> float:
        """Calculate how well the car fits within user's budget"""
        budget_min = user_analysis.get("budget_min")
        budget_max = user_analysis.get("budget_max")
        
        if not budget_min and not budget_max:
            return 0.5  # Neutral score if no budget specified
        
        car_min = car["price_range"]["min"]
        car_max = car["price_range"]["max"]
        car_avg = (car_min + car_max) / 2
        
        if budget_max and budget_min:
            user_avg = (budget_min + budget_max) / 2
            budget_range = budget_max - budget_min
            
            # Score based on how close car average price is to user's budget midpoint
            distance = abs(car_avg - user_avg)
            normalized_distance = distance / budget_range if budget_range > 0 else 1
            
            return max(0, 1 - normalized_distance)
        
        return 0.5
    
    def _calculate_feature_score(self, car: Dict, user_analysis: Dict) -> float:
        """Calculate score based on feature matching"""
        desired_features = user_analysis.get("features", [])
        
        if not desired_features:
            return 0.5  # Neutral score if no specific features requested
        
        car_features = car.get("features", [])
        matching_features = len(set(desired_features) & set(car_features))
        
        return matching_features / len(desired_features) if desired_features else 0
    
    def _get_match_reasons(self, car: Dict, user_analysis: Dict) -> List[str]:
        """Generate reasons why this car matches user preferences"""
        reasons = []
        
        # Budget match
        budget_min = user_analysis.get("budget_min")
        budget_max = user_analysis.get("budget_max")
        if budget_min or budget_max:
            car_min = car["price_range"]["min"]
            car_max = car["price_range"]["max"]
            if (not budget_min or car_max >= budget_min) and (not budget_max or car_min <= budget_max):
                reasons.append("Fits within your budget")
        
        # Usage match
        usage = user_analysis.get("usage")
        if usage and usage in self.category_mapping:
            if car["category"] in self.category_mapping[usage]:
                reasons.append(f"Perfect for {usage}")
        
        # Emotion match
        user_emotions = user_analysis.get("emotions", [])
        car_emotions = car.get("emotions", [])
        matching_emotions = set(user_emotions) & set(car_emotions)
        if matching_emotions:
            emotions_str = ", ".join(matching_emotions)
            reasons.append(f"Matches your desire for {emotions_str}")
        
        # Fuel preference
        fuel_pref = user_analysis.get("fuel_preference")
        if fuel_pref and fuel_pref != "any" and car["fuel_type"] == fuel_pref:
            reasons.append(f"Uses {fuel_pref} as preferred")
        
        # Features
        desired_features = user_analysis.get("features", [])
        car_features = car.get("features", [])
        matching_features = set(desired_features) & set(car_features)
        if matching_features:
            features_str = ", ".join(list(matching_features)[:2])  # Show up to 2 features
            reasons.append(f"Includes {features_str}")
        
        return reasons[:3]  # Limit to top 3 reasons