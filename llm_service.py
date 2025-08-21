import openai
import os
import json
import re
from typing import Dict, List, Any

class LLMService:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            self.client = None
            print("Warning: No OpenAI API key found. LLM features will use fallback analysis.")
    
    def analyze_user_input(self, user_message: str) -> Dict[str, Any]:
        """Analyze user input to extract needs, budget, emotions, and preferences"""
        
        system_prompt = """
        You are a car recommendation expert AI. Analyze the user's message to extract:
        1. Budget information (extract numeric values for min/max budget)
        2. Car preferences (size, type, features needed)
        3. Emotional indicators (what feelings they want from the car)
        4. Usage patterns (commuting, family, sports, off-road, etc.)
        5. Specific requirements (fuel efficiency, luxury, performance, etc.)
        
        Return your analysis as a JSON object with these keys:
        - budget_min: minimum budget in USD (number or null)
        - budget_max: maximum budget in USD (number or null)
        - car_type: preferred car type (sedan, suv, sports_car, truck, hatchback, etc.)
        - emotions: array of emotional desires (excitement, luxury, reliability, adventure, etc.)
        - usage: primary usage pattern (family, commuting, sports, off_road, luxury, work)
        - fuel_preference: fuel type preference (gasoline, electric, hybrid, any)
        - features: array of desired features
        - brand_preference: any specific brand mentioned
        - priorities: array of top priorities (budget, performance, efficiency, luxury, etc.)
        """
        
        user_prompt = f"Analyze this car buying request: '{user_message}'"
        
        try:
            if not self.client:
                # Use fallback if no API key available
                return self._fallback_analysis(user_message)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                # Fallback parsing if no JSON found
                analysis = self._fallback_analysis(user_message)
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing user input: {e}")
            return self._fallback_analysis(user_message)
    
    def _fallback_analysis(self, user_message: str) -> Dict[str, Any]:
        """Fallback analysis using simple keyword matching"""
        message_lower = user_message.lower()
        
        # Extract budget using regex
        budget_matches = re.findall(r'\$?(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)', user_message)
        budgets = [int(match.replace(',', '')) for match in budget_matches if len(match.replace(',', '')) >= 4]
        
        budget_min = min(budgets) if budgets else None
        budget_max = max(budgets) if budgets else None
        
        # Simple keyword matching for car types
        car_type = "sedan"  # default
        if any(word in message_lower for word in ['suv', 'suv']):
            car_type = "suv"
        elif any(word in message_lower for word in ['sports', 'sport', 'fast', 'performance']):
            car_type = "sports_car"
        elif any(word in message_lower for word in ['truck', 'pickup']):
            car_type = "truck"
        
        # Emotion detection
        emotions = []
        if any(word in message_lower for word in ['luxury', 'premium', 'elegant']):
            emotions.append("luxury")
        if any(word in message_lower for word in ['reliable', 'dependable']):
            emotions.append("reliability")
        if any(word in message_lower for word in ['exciting', 'fun', 'thrilling']):
            emotions.append("excitement")
        if any(word in message_lower for word in ['adventure', 'outdoor', 'off-road']):
            emotions.append("adventure")
        
        # Usage pattern detection
        usage = "commuting"  # default
        if any(word in message_lower for word in ['family', 'kids', 'children']):
            usage = "family"
        elif any(word in message_lower for word in ['work', 'business', 'professional']):
            usage = "work"
        elif any(word in message_lower for word in ['sports', 'track', 'racing']):
            usage = "sports"
        
        # Fuel preference
        fuel_preference = "any"
        if any(word in message_lower for word in ['electric', 'ev', 'tesla']):
            fuel_preference = "electric"
        elif any(word in message_lower for word in ['hybrid']):
            fuel_preference = "hybrid"
        
        return {
            "budget_min": budget_min,
            "budget_max": budget_max,
            "car_type": car_type,
            "emotions": emotions,
            "usage": usage,
            "fuel_preference": fuel_preference,
            "features": [],
            "brand_preference": None,
            "priorities": ["budget"] if budget_min else ["reliability"]
        }
    
    def generate_recommendation_explanation(self, recommended_cars: List[Dict], user_analysis: Dict) -> str:
        """Generate a natural language explanation for the recommendations"""
        
        if not recommended_cars:
            return "I couldn't find any cars that match your specific criteria. Could you please provide more details about your budget or preferences?"
        
        system_prompt = """
        You are a friendly and knowledgeable car expert. Generate a personalized explanation for why these cars are recommended to the user. 
        Be enthusiastic but honest, mention specific features that match their needs, and explain why each car fits their emotional and practical requirements.
        Keep the tone conversational and helpful, like talking to a friend who knows cars.
        """
        
        cars_info = []
        for car in recommended_cars[:3]:  # Limit to top 3 recommendations
            cars_info.append({
                "brand": car["brand"],
                "model": car["model"],
                "price_range": car["price_range"],
                "features": car["features"],
                "emotions": car["emotions"],
                "description": car["description"]
            })
        
        user_prompt = f"""
        User analysis: {json.dumps(user_analysis, indent=2)}
        
        Recommended cars: {json.dumps(cars_info, indent=2)}
        
        Write a personalized recommendation explanation that connects the user's needs with why these cars are perfect for them.
        """
        
        try:
            if not self.client:
                # Use fallback if no API key available
                return self._fallback_explanation(recommended_cars, user_analysis)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return self._fallback_explanation(recommended_cars, user_analysis)
    
    def _fallback_explanation(self, recommended_cars: List[Dict], user_analysis: Dict) -> str:
        """Fallback explanation generation"""
        if not recommended_cars:
            return "I couldn't find any cars that match your criteria. Please adjust your budget or preferences."
        
        explanation = f"Based on your requirements, I found {len(recommended_cars)} great options for you:\n\n"
        
        for i, car in enumerate(recommended_cars[:3], 1):
            price_range = f"${car['price_range']['min']:,} - ${car['price_range']['max']:,}"
            explanation += f"{i}. **{car['brand']} {car['model']}** ({price_range})\n"
            explanation += f"   {car['description']}\n\n"
        
        return explanation