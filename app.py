from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from llm_service import LLMService
from recommendation_engine import RecommendationEngine
from car_database import CarDatabase

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize services
llm_service = LLMService()
recommendation_engine = RecommendationEngine()
car_database = CarDatabase()

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return car recommendations"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Analyze user input using LLM
        user_analysis = llm_service.analyze_user_input(user_message)
        
        # Get car recommendations
        recommended_cars = recommendation_engine.recommend_cars(user_analysis)
        
        # Generate explanation
        explanation = llm_service.generate_recommendation_explanation(
            recommended_cars[:3], user_analysis
        )
        
        # Format response
        response = {
            'message': explanation,
            'recommendations': [
                {
                    'brand': car['brand'],
                    'model': car['model'],
                    'year': car['year'],
                    'price_range': car['price_range'],
                    'description': car['description'],
                    'features': car['features'][:5],  # Limit features shown
                    'mpg': car['mpg'],
                    'category': car['category'],
                    'score': round(car['recommendation_score'], 1),
                    'match_reasons': car['match_reasons']
                }
                for car in recommended_cars[:5]  # Top 5 recommendations
            ],
            'user_analysis': user_analysis
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'Sorry, I encountered an error processing your request. Please try again.',
            'message': 'I apologize, but I\'m having trouble understanding your request right now. Could you please rephrase what kind of car you\'re looking for?'
        }), 500

@app.route('/api/cars')
def get_all_cars():
    """Get all cars in database for browsing"""
    try:
        cars = car_database.get_all_cars()
        return jsonify({
            'cars': [
                {
                    'brand': car['brand'],
                    'model': car['model'],
                    'year': car['year'],
                    'price_range': car['price_range'],
                    'category': car['category'],
                    'fuel_type': car['fuel_type'],
                    'description': car['description']
                }
                for car in cars
            ]
        })
    except Exception as e:
        print(f"Error getting cars: {e}")
        return jsonify({'error': 'Failed to retrieve cars'}), 500

@app.route('/api/car/<brand>/<model>')
def get_car_details(brand, model):
    """Get detailed information about a specific car"""
    try:
        car = car_database.get_car_by_id(brand, model)
        if car:
            return jsonify(car)
        else:
            return jsonify({'error': 'Car not found'}), 404
    except Exception as e:
        print(f"Error getting car details: {e}")
        return jsonify({'error': 'Failed to retrieve car details'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Car Recommendation System'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)