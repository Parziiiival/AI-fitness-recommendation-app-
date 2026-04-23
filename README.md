# AI Fitness Recommendation System

An intelligent, full-stack web application that uses Machine Learning to provide highly personalized workout and diet recommendations based on user metrics.

![App Demo](https://via.placeholder.com/800x400?text=AI+Fitness+Recommendation+System)

## 🚀 Features

- **Machine Learning Recommendations**: Utilizes Scikit-Learn models trained on fitness datasets to predict optimal workout styles (Cardio, HIIT, Strength Training, Weight Training, Yoga) and diet plans (Balanced, Calorie Deficit, High Protein, Low Carb).
- **Personalized 7-Day Workout Plans**: Dynamically generates day-by-day workout splits complete with specific exercises, sets, and reps tailored to the AI's predicted workout category and the user's experience level.
- **Comprehensive Health Insights**: Calculates and visualizes BMI, BMR, TDEE, optimal macronutrient splits, hydration targets, and an overall health score.
- **Progress Tracking**: Securely saves user history using session tracking to monitor fitness journey progress over time.
- **Modern, Premium UI**: A highly responsive, glassmorphic React frontend featuring modern typography, curated color palettes, and smooth micro-animations.

## 🛠️ Technology Stack

### Backend
- **Django**: High-level Python web framework.
- **Django REST Framework (DRF)**: For building the robust JSON API.
- **SQLite3**: Lightweight database for storing user session tracking and recommendation history.

### Machine Learning
- **Scikit-Learn**: For training and utilizing the Random Forest classifiers.
- **Pandas**: For data manipulation and preprocessing.
- **Joblib**: For serializing and loading the trained `.pkl` models.

### Frontend
- **React**: Component-based JavaScript library for building the user interface.
- **Vanilla CSS**: Custom styling leveraging CSS variables, Flexbox/Grid, and modern glassmorphism aesthetics.
- **Fetch API**: For seamless communication with the Django backend.

---

## 📖 How This Project Was Built (Step-by-Step)

### Phase 1: Machine Learning Core
1. **Dataset Generation**: Created a robust script (`generate_dataset.py`) to simulate thousands of realistic user profiles (age, gender, height, weight, goals, activity level) mapped to optimal workout and diet strategies.
2. **Model Training**: Developed `train.py` to preprocess the dataset (label encoding) and train two classification models (Workout Model and Diet Model) using Scikit-Learn. The models were exported as `.pkl` files using `joblib`.
3. **Prediction Interface**: Built `predict.py` to take raw user input, encode it, feed it through the models, and map the numeric predictions back to human-readable categories. Later expanded this module to generate detailed 7-day workout splits based on the prediction.

### Phase 2: Django Backend & API
1. **Project Setup**: Initialized the Django project (`ai_fitness_project`) and created the `recommendations` app.
2. **Database Models**: Defined the `FitnessRecord` model to store user metrics, goals, and the resulting AI predictions.
3. **API Endpoints**: 
   - `POST /api/predict/`: Validates incoming user data, queries the ML model, saves the result to the DB via session keys, and returns the recommendation alongside the detailed 7-day plan.
   - `POST /api/insights/`: Processes user metrics to calculate BMI, TDEE, macro splits, and a dynamic health score.
   - `GET /api/history/`: Retrieves past recommendations for progress tracking.

### Phase 3: React Frontend & UI/UX
1. **Frontend Scaffolding**: Initialized a React app within the project directory.
2. **Component Architecture**: 
   - `Form.js`: Captures user metrics with auto-calculating BMI fields.
   - `Result.js`: Displays the AI's top-level recommendations and the detailed day-by-day workout split.
   - `HealthInsights.js`: Visualizes the mathematical health calculations (macros, hydration, BMR).
   - `ProgressTracker.js`: Shows historical data to the user.
3. **Styling**: Implemented a global `App.css` utilizing modern web design best practices—vibrant colors, glassmorphic cards, responsive grid layouts, and subtle hover animations to create a premium feel.

### Phase 4: Integration & Polish
1. **Connecting the Stack**: Configured Django to handle API requests from the React development server.
2. **Refining the Output**: Upgraded the prediction engine to not just recommend "Weight Training", but to actually provide the exercises (e.g., "Squats 3x10") based on the user's specific experience level.

---

## 💻 Getting Started (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/Parziiiival/AI-fitness-recommendation-app-.git
cd AI-fitness-recommendation-app-/ai_fitness_project
```

### 2. Setup the Backend (Django)
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework pandas scikit-learn joblib

# Run migrations and start the server
python manage.py migrate
python manage.py runserver
```

### 3. Setup the Frontend (React)
```bash
# Open a new terminal and navigate to the frontend folder
cd frontend

# Install Node dependencies
npm install

# Start the React development server
npm start
```

### 4. Access the App
Open your browser and navigate to `http://localhost:3000`. The frontend will communicate with the Django server running on port `8000`.
