output:
<img width="1741" height="801" alt="image" src="https://github.com/user-attachments/assets/c689bdba-1005-4f75-b12f-cc272990d9d1" />

# 🚗 LLM-Powered Car Recommendation Chat Assistant

An intelligent car recommendation system that uses Large Language Models (LLM) to understand user needs, emotions, and budget to recommend the perfect car. The system analyzes user input in natural language and provides personalized car recommendations with comprehensive online data and beautiful car images.

## ✨ Enhanced Features

### 🎨 **Modern Frontend Design**
- **Beautiful gradient UI** with professional styling
- **Responsive design** that works on all devices
- **Enhanced car recommendation cards** with images and detailed information
- **Smooth animations** and hover effects
- **Mobile-first approach** with optimized layouts

### 🌐 **Online Car Data Integration**
- **Comprehensive car database** with realistic online-like features
- **Real-time car information** including:
  - Customer reviews and ratings
  - Safety ratings (NHTSA)
  - Fuel cost calculations
  - Financing estimates
  - Dealer information
  - Market trends
  - Reliability scores
  - Awards and recognition
- **Fallback system** to static database

### 🖼️ **Car Images & Visual Elements**
- **Car images** displayed with each recommendation
- **Professional placeholder images** for visual appeal
- **Image hover effects** and loading states
- **Visual car representation** for better user experience

### 🧠 **Enhanced Recommendation Engine**
- **Sophisticated scoring algorithms** using comprehensive data
- **Multi-factor analysis** including budget, usage, preferences
- **Detailed matching reasons** explaining why each car fits
- **Professional recommendation format** with scores and details

- **Natural Language Understanding**: Powered by OpenAI's GPT models to understand user requirements
- **Emotion Detection**: Analyzes emotional preferences (luxury, excitement, reliability, adventure, etc.)
- **Budget Analysis**: Intelligently extracts and works with user budget constraints
- **Comprehensive Car Database**: Includes cars from multiple categories and price ranges
- **Intelligent Matching**: Sophisticated recommendation engine that scores cars based on user preferences
- **Interactive Chat Interface**: User-friendly web interface with real-time recommendations
- **Detailed Explanations**: Provides reasoning for each recommendation

## 🏗️ Enhanced Architecture

The application consists of several key components:

1. **Flask Web Application** (`app.py`) - Main web server and API endpoints
2. **LLM Service** (`llm_service.py`) - OpenAI integration for natural language processing
3. **External Car Service** (`external_car_service.py`) - **NEW**: Comprehensive online car data with realistic features
4. **Car Image Service** (`car_image_service.py`) - **NEW**: Car image management and placeholder system
5. **Car Database** (`car_database.py`) - Static fallback car information
6. **Recommendation Engine** (`recommendation_engine.py`) - Enhanced intelligent matching and scoring system
7. **Web Interface** (`templates/index.html`) - **ENHANCED**: Modern responsive chat interface with images

### **New Services Added:**

- **🌐 External Car Service**: Simulates real automotive data sources with reviews, ratings, financing info
- **🖼️ Car Image Service**: Manages car images with beautiful SVG placeholders 
- **📊 Enhanced Data**: Comprehensive car information including safety, costs, dealer details

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/copilot-llm-chat-application-for-car-recommendation.git
   cd copilot-llm-chat-application-for-car-recommendation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 💬 Usage Examples

Here are some example queries you can try:

- **Budget-focused**: "I need a reliable family car under $35,000 for daily commuting"
- **Luxury seeker**: "I want a luxury sedan that shows sophistication and has premium features"
- **Sports enthusiast**: "Looking for an exciting sports car under $80,000 for weekend driving"
- **Eco-conscious**: "I want an electric car for city driving with good technology features"
- **Adventure seeker**: "Need a rugged SUV for off-road adventures and outdoor activities"

## 🎯 How It Works

### 1. Natural Language Processing
The system uses OpenAI's GPT models to analyze user input and extract:
- Budget constraints (min/max prices)
- Car type preferences (sedan, SUV, sports car, etc.)
- Emotional desires (luxury, excitement, reliability, adventure)
- Usage patterns (family, commuting, sports, work)
- Specific features and requirements

### 2. Intelligent Matching
The recommendation engine scores cars based on:
- **Usage Pattern Match** (25% weight) - How well the car fits intended use
- **Emotion Alignment** (30% weight) - Matching emotional appeal
- **Type Preference** (20% weight) - Body style and category matching
- **Budget Efficiency** (15% weight) - How well the car fits within budget
- **Feature Matching** (10% weight) - Specific feature requirements

### 3. Personalized Recommendations
Each recommendation includes:
- Detailed car information and specifications
- Recommendation score (0-100)
- Specific reasons why the car matches user needs
- Price range and fuel efficiency
- Key features and benefits

## 🚗 Car Database

The system includes a comprehensive database with cars across multiple categories:

- **Luxury Sedans**: Mercedes S-Class, BMW 7 Series, Audi A8
- **Sports Cars**: Porsche 911, Chevrolet Corvette
- **Family Cars**: Toyota Camry, Honda Accord
- **SUVs**: Jeep Wrangler, Toyota RAV4
- **Electric Cars**: Tesla Model S, Nissan Leaf
- **Trucks**: Ford F-150
- **Budget Cars**: Hyundai Elantra, Kia Forte

Each car entry includes:
- Brand, model, and year
- Price range (min/max)
- Category and body type
- Fuel type and efficiency
- Key features and emotions
- Detailed description
- Target audience

## 🔧 API Endpoints

### `POST /api/chat`
Main chat endpoint for car recommendations.

**Request:**
```json
{
  "message": "I need a family car under $40,000"
}
```

**Response:**
```json
{
  "message": "Explanation of recommendations",
  "recommendations": [
    {
      "brand": "Toyota",
      "model": "Camry",
      "year": 2024,
      "price_range": {"min": 26000, "max": 38000},
      "description": "Reliable family sedan...",
      "score": 85.3,
      "match_reasons": ["Fits within your budget", "Perfect for family"]
    }
  ],
  "user_analysis": {
    "budget_min": null,
    "budget_max": 40000,
    "usage": "family"
  }
}
```

### `GET /api/cars`
Get all cars in the database.

### `GET /api/car/<brand>/<model>`
Get detailed information about a specific car.

### `GET /health`
Health check endpoint.

## 🛠️ Development

### Project Structure
```
├── app.py                    # Main Flask application
├── car_database.py          # Car database and search functionality
├── llm_service.py           # OpenAI LLM integration
├── recommendation_engine.py # Recommendation logic
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Chat interface
├── static/
│   └── style.css         # Styling
└── README.md             # This file
```

### Adding New Cars
To add new cars to the database, modify the `cars` list in `car_database.py`:

```python
{
    "brand": "Brand Name",
    "model": "Model Name",
    "year": 2024,
    "price_range": {"min": 30000, "max": 45000},
    "category": "category_name",
    "fuel_type": "gasoline",  # gasoline, electric, hybrid
    "mpg": {"city": 25, "highway": 35},
    "features": ["feature1", "feature2"],
    "emotions": ["emotion1", "emotion2"],
    "body_type": "sedan",  # sedan, suv, coupe, truck, hatchback
    "seats": 5,
    "description": "Car description",
    "suitable_for": ["target_audience"]
}
```

### Customizing Recommendations
The recommendation logic can be customized in `recommendation_engine.py`:
- Modify scoring weights in `_calculate_car_score()`
- Add new categories to `category_mapping`
- Update emotion weights in `emotion_weights`

## 🚀 Deployment

### Using Gunicorn (Production)
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Environment Variables for Production
```bash
OPENAI_API_KEY=your_api_key
FLASK_ENV=production
SECRET_KEY=your_secret_key
PORT=5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- **Multi-language support** for international markets
- **Image integration** for visual car recommendations
- **Advanced filtering** with more specific criteria
- **User profiles** to remember preferences
- **Comparison features** to compare multiple cars
- **Real-time pricing** integration with dealership APIs
- **Test drive booking** integration
- **Financing calculator** for monthly payments

## 📞 Support

For support or questions, please open an issue on GitHub or contact me.

---

**Built with ❤️ using Python, Flask, and OpenAI GPT**
