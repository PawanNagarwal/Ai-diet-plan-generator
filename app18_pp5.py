import streamlit as st
import openai
import os
from datetime import datetime, time, timedelta
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
import re
import time as time_module

# Set page configuration
st.set_page_config(
    page_title="AI Diet Plan Generator",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #e0bfa2 25%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0 !important;
    }
    
    /* Form sections */
    .form-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .form-section:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .section-title {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* BMI card */
    .bmi-card {
        background: linear-gradient(135deg, #bdb49b 40%, #c9c88b 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .bmi-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .bmi-category {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Loading screen */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
        background: linear-gradient(135deg, #e0bfa2 25%, #764ba2 100%);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .loading-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }
    
    .cooking-animation {
        font-size: 5rem;
        margin-bottom: 2rem;
        animation: bounce 2s infinite, rotate 4s linear infinite;
        z-index: 1;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-30px); }
        60% { transform: translateY(-15px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .loading-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        z-index: 1;
    }
    
    .loading-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 3rem;
        z-index: 1;
    }
    
    .progress-container {
        width: 100%;
        max-width: 500px;
        background-color: rgba(255,255,255,0.2);
        border-radius: 30px;
        padding: 6px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        z-index: 1;
    }
    
    .progress-bar {
        width: 0%;
        height: 25px;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 500% 500%;
        border-radius: 25px;
        animation: gradient 2s ease infinite, progress 10s linear infinite;
        box-shadow: 0 5px 15px rgba(255,255,255,0.3);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes progress {
        0% { width: 0%; }
        20% { width: 25%; }
        40% { width: 50%; }
        60% { width: 70%; }
        80% { width: 90%; }
        100% { width: 100%; }
    }
    
    .loading-steps {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        margin-top: 2rem;
        z-index: 1;
    }
    
    .step {
        opacity: 0;
        animation: fadeInOut 2.5s ease-in-out infinite;
        margin: 0.8rem 0;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 25px;
        backdrop-filter: blur(5px);
    }
    
    .step:nth-child(1) { animation-delay: 0s; }
    .step:nth-child(2) { animation-delay: 2.5s; }
    .step:nth-child(3) { animation-delay: 5s; }
    .step:nth-child(4) { animation-delay: 7.5s; }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0; transform: translateY(20px) scale(0.9); }
        20%, 80% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .spinning-utensils {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 3rem 0;
        z-index: 1;
    }
    
    .utensil {
        font-size: 2.5rem;
        animation: spin 4s linear infinite, float 3s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(255,255,255,0.3));
    }
    
    .utensil:nth-child(1) { animation-delay: 0s; }
    .utensil:nth-child(2) { animation-delay: 1s; }
    .utensil:nth-child(3) { animation-delay: 2s; }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Results page styling */
    .results-header {
        background: linear-gradient(135deg, #e0bfa2 25%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .day-header {
        background: linear-gradient(135deg, #8b678f 25%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
    }
    
    .meal-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
    }
    
    .meal-card:hover {
        box-shadow: 0 7px 25px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    .meal-header {
        background-color: #f8f9fa;
        padding: 1rem 1.5rem;
        font-weight: 600;
        color: #2d3748;
        border-bottom: 1px solid #e2e8f0;
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .meal-time {
        background: linear-gradient(135deg, #c2a388 50%, #c98ba4 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .meal-content {
        padding: 1.5rem;
        flex-grow: 1;
    }

    .meal-content p {
        color: #4a5568;
        margin-bottom: 0;
    }
    
    .meal-footer {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 1rem 1.5rem;
        background-color: #f8f9fa;
        border-top: 1px solid #e2e8f0;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
    }
    
    .nutrient-item {
        text-align: center;
        color: #4a5568;
        font-size: 0.9rem;
    }
    
    .nutrient-item strong {
        display: block;
        font-size: 1.25rem;
        font-weight: 600;
        color: #2d3748;
    }

    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .edit-form-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(252, 182, 159, 0.3);
        border: 1px solid rgba(255, 236, 210, 0.5);
    }
    
    .edit-header {
        text-align: center;
        color: #8b4513;
        margin-bottom: 2rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #76b38c 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: #2d5016;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(132, 250, 176, 0.3);
    }
    
    .sleep-schedule-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(78, 205, 196, 0.3);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem !important; }
        .loading-title { font-size: 2rem; }
        .action-buttons { flex-direction: column; }
        .spinning-utensils { gap: 1.5rem; }
        .utensil { font-size: 2rem; }
        .meal-footer { flex-wrap: wrap; gap: 1rem; }
        .nutrient-item { flex-basis: 40%; }
        .meal-header { flex-direction: column; gap: 0.5rem; text-align: center; }
    }
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* ... all your existing CSS styles ... */
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem !important; }
        .loading-title { font-size: 2rem; }
        .action-buttons { flex-direction: column; }
        .spinning-utensils { gap: 1.5rem; }
        .utensil { font-size: 2rem; }
        .meal-footer { flex-wrap: wrap; gap: 1rem; }
        .nutrient-item { flex-basis: 40%; }
        .meal-header { flex-direction: column; gap: 0.5rem; text-align: center; }
    }
    
    /* Hide Streamlit toolbar including GitHub fork icon */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    * Alternative selectors for Manage app button (try these if the above doesn't work) */
    .manage-app {
        display: none !important;
    }
    
    [data-testid="stFloatingActionButton"] {
        display: none !important;
    }
    
    .stFloatingActionButton {
        display: none !important;
    }
    
    /* Hide all floating action buttons */
    div[data-testid*="FloatingActionButton"],
    div[class*="FloatingActionButton"] {
        display: none !important;
    }
    </style>
    
    """, unsafe_allow_html=True)


def display_loading_animation():
    """Display a modern, animated loading screen"""
    st.markdown("""
    <div class="loading-container">
        <div class="cooking-animation">👩‍🍳</div>
        <div class="loading-title">Crafting Your Perfect Diet Plan</div>
        <div class="loading-subtitle">Our AI nutritionist is analyzing your profile...</div>
    </div>
    """, unsafe_allow_html=True)


class MealTimingCalculator:
    """Calculate optimal meal timing based on sleep and wake times"""
    
    @staticmethod
    def calculate_meal_times(sleep_time: time, wake_time: time, meals_per_day: int) -> Dict[str, str]:
        """
        Calculate optimal meal times based on sleep/wake schedule and number of meals
        
        Args:
            sleep_time: Time when user goes to sleep
            wake_time: Time when user wakes up  
            meals_per_day: Number of meals per day
        
        Returns:
            Dictionary mapping meal types to formatted time strings
        """
        
        # Convert times to datetime objects for easier calculation
        sleep_dt = datetime.combine(datetime.today(), sleep_time)
        wake_dt = datetime.combine(datetime.today(), wake_time)
        
        # Handle case where sleep time is after midnight
        if sleep_time < wake_time:
            sleep_dt += timedelta(days=1)
        
        meal_times = {}
        
        if meals_per_day == 2:
            meal_times['Breakfast'] = (wake_dt + timedelta(minutes=30)).strftime("%I:%M %p")
            meal_times['Dinner'] = (sleep_dt - timedelta(hours=3)).strftime("%I:%M %p")
            
        elif meals_per_day == 3:
            meal_times['Breakfast'] = (wake_dt + timedelta(hours=1)).strftime("%I:%M %p")
            meal_times['Lunch'] = (wake_dt + timedelta(hours=5.5)).strftime("%I:%M %p")
            meal_times['Dinner'] = (sleep_dt - timedelta(hours=2.5)).strftime("%I:%M %p")
            
        elif meals_per_day == 4:
            meal_times['Breakfast'] = (wake_dt + timedelta(hours=1)).strftime("%I:%M %p")
            meal_times['Lunch'] = (wake_dt + timedelta(hours=5.5)).strftime("%I:%M %p")
            meal_times['Evening Meal'] = (wake_dt + timedelta(hours=10)).strftime("%I:%M %p")
            meal_times['Dinner'] = (sleep_dt - timedelta(hours=2.5)).strftime("%I:%M %p")
            
        elif meals_per_day == 5:
            meal_times['Breakfast'] = (wake_dt + timedelta(hours=1)).strftime("%I:%M %p")
            meal_times['Mid-Morning Meal'] = (wake_dt + timedelta(hours=4)).strftime("%I:%M %p")
            meal_times['Lunch'] = (wake_dt + timedelta(hours=7)).strftime("%I:%M %p")
            meal_times['Evening Snack'] = (wake_dt + timedelta(hours=10.5)).strftime("%I:%M %p")
            meal_times['Dinner'] = (sleep_dt - timedelta(hours=2.5)).strftime("%I:%M %p")
            
        elif meals_per_day == 6:
            meal_times['Breakfast'] = (wake_dt + timedelta(hours=1)).strftime("%I:%M %p")
            meal_times['Mid-Morning Snack'] = (wake_dt + timedelta(hours=3.5)).strftime("%I:%M %p")
            meal_times['Lunch'] = (wake_dt + timedelta(hours=6)).strftime("%I:%M %p")
            meal_times['Afternoon Snack'] = (wake_dt + timedelta(hours=8.5)).strftime("%I:%M %p")
            meal_times['Evening Meal'] = (wake_dt + timedelta(hours=11)).strftime("%I:%M %p")
            meal_times['Dinner'] = (sleep_dt - timedelta(hours=2.5)).strftime("%I:%M %p")
        
        return meal_times


class DietPlanGenerator:
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai
    
    def set_api_key(self, api_key: str):
        """Set OpenAI API key"""
        openai.api_key = api_key
        self.client = openai
    
    def calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate BMI from weight (kg) and height (cm)"""
        height_m = height / 100
        return round(weight / (height_m ** 2), 1)
    
    def get_bmi_category(self, bmi: float) -> str:
        """Get BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def calculate_calories(self, weight: float, height: float, age: int, 
                          gender: str, activity_level: str) -> int:
        """Calculate estimated daily calories using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extremely_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.2)
        return int(bmr * multiplier)
    
    def create_prompt(self, user_data: Dict) -> str:
        """Create comprehensive prompt for GPT-4o focused on detailed meal plans in JSON format"""
        bmi = self.calculate_bmi(user_data['weight'], user_data['height'])
        estimated_calories = self.calculate_calories(
            user_data['weight'], user_data['height'], user_data['age'],
            user_data['gender'], user_data['activity_level']
        )
        
        prompt = f"""Create a comprehensive, personalized 7-day diet plan based on the following information:

PERSONAL INFORMATION:
- Name: {user_data['name']}
- Age: {user_data['age']} years
- Gender: {user_data['gender']}
- Weight: {user_data['weight']} kg
- Height: {user_data['height']} cm
- BMI: {bmi} ({self.get_bmi_category(bmi)})
- Estimated Daily Calories: {estimated_calories}

HEALTH GOALS & LIFESTYLE:
- Primary Goal: {user_data['health_goal']}
- Activity Level: {user_data['activity_level']}
- Meals per Day: {user_data['meals_per_day']}
- Sleep Duration: {user_data['sleep_duration']} hours
- Sleep Time: {user_data['sleep_time']}
- Wake Time: {user_data['wake_time']}

DIETARY PREFERENCES:
- Diet Type: {user_data['diet_type']}
- Food Preferences: {user_data['food_preferences'] or 'None specified'}
- Food Dislikes: {user_data['food_dislikes'] or 'None specified'}

MEDICAL & ALLERGY INFORMATION:
- Medical Conditions: {user_data['medical_conditions'] or 'None specified'}
- Allergies/Intolerances: {', '.join(user_data['allergies']) if user_data['allergies'] else 'None specified'}

ADDITIONAL INFORMATION:
{user_data['additional_info'] or 'None provided'}

Please create a detailed 7-day meal plan in JSON format. You MUST generate exactly {user_data['meals_per_day']} meals per day.

Return the response in the following JSON structure:

{{
  "diet_plan": {{
    "day_1": {{
      "day_name": "Monday",
      "meals": [
        {{
          "type": "Breakfast",
          "name": "Meal name",
          "serving_size": "Serving size with household measurements",
          "description": "Detailed description",
          "ingredients": "Ingredients with specific quantities",
          "calories": number,
          "protein": number,
          "carbs": number,
          "fats": number
        }}
        // ... more meals based on meals_per_day
      ]
    }},
    "day_2": {{
      // ... similar structure for day 2
    }},
    // ... continue for all 7 days
  }}
}}

Guidelines:
1. Provide serving sizes in both household measurements (bowls, plates, cups, pieces, slices, etc.) AND grams
2. Provide specific ingredient quantities
3. Ensure nutritional values are realistic
4. Include varied and balanced meals
5. Consider user's dietary restrictions and preferences
6. Align with caloric needs for the specified goal
7. Generate exactly {user_data['meals_per_day']} meals per day
8. Use proper meal types based on the number of meals per day

Meal types by number of meals:
- 2 meals: Breakfast, Dinner
- 3 meals: Breakfast, Lunch, Dinner
- 4 meals: Breakfast, Lunch, Evening Meal, Dinner
- 5 meals: Breakfast, Mid-Morning Meal, Lunch, Evening Snack, Dinner
- 6 meals: Breakfast, Mid-Morning Snack, Lunch, Afternoon Snack, Evening Meal, Dinner"""
        
        return prompt
    
    def generate_diet_plan(self, user_data: Dict) -> str:
        """Generate diet plan using OpenAI GPT-4o with JSON output"""
        try:
            prompt = self.create_prompt(user_data)
            
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional registered dietitian and certified nutritionist with over 15 years of experience in creating personalized diet plans. You specialize in evidence-based nutrition, medical nutrition therapy, and sustainable lifestyle changes. Always provide specific nutritional values and practical serving sizes using common household measurements. Always respond in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
            )
            print(response)
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Error generating diet plan: {str(e)}")
    
    def parse_meal_plan(self, diet_plan_json: str) -> List[Dict]:
        """Parse the JSON diet plan into structured daily meal data"""
        try:
            # Parse JSON response
            diet_data = json.loads(diet_plan_json)
            
            # Extract diet plan data
            if "diet_plan" in diet_data:
                plan_data = diet_data["diet_plan"]
            else:
                plan_data = diet_data
            
            days_data = []
            
            # Process each day
            for day_key in sorted(plan_data.keys()):
                day_info = plan_data[day_key]
                
                # Extract day number from key (e.g., "day_1" -> 1)
                day_number = int(re.findall(r'\d+', day_key)[0]) if re.findall(r'\d+', day_key) else len(days_data) + 1
                
                day_data = {
                    'day': day_number,
                    'title': f"DAY {day_number} - {day_info.get('day_name', f'Day {day_number}')}",
                    'meals': []
                }
                
                # Process meals for this day
                for meal in day_info.get('meals', []):
                    meal_data = {
                        'type': meal.get('type', ''),
                        'name': meal.get('name', ''),
                        'serving_size': meal.get('serving_size', ''),
                        'ingredients': meal.get('ingredients', ''),
                        'description': meal.get('description', ''),
                        'calories': int(meal.get('calories', 0)) if meal.get('calories') else 0,
                        'protein': float(meal.get('protein', 0)) if meal.get('protein') else 0,
                        'carbs': float(meal.get('carbs', 0)) if meal.get('carbs') else 0,
                        'fats': float(meal.get('fats', 0)) if meal.get('fats') else 0
                    }
                    
                    # Only add meal if it has required data
                    if meal_data['type'] and meal_data['name']:
                        day_data['meals'].append(meal_data)
                
                # Only add day if it has meals
                if day_data['meals']:
                    days_data.append(day_data)
            
            return days_data
            
        except json.JSONDecodeError as e:
            st.error(f"Error parsing JSON response: {str(e)}")
            return []
        except Exception as e:
            st.error(f"Error processing meal plan: {str(e)}")
            return []


def display_professional_meal_plan(days_data: List[Dict], meal_times: Dict[str, str]):
    """Display the meal plan with professional styling"""
    for day_data in days_data:
        st.markdown(f'<div class="day-header"><h2>📅 {day_data["title"]}</h2></div>', 
                   unsafe_allow_html=True)
        
        for meal in day_data['meals']:
            meal_emojis = {
                'Breakfast': '🍳', 'Mid-Morning Meal': '🍎', 'Mid-Morning Snack': '🍎',
                'Lunch': '🍽️', 'Afternoon Snack': '🥨', 'Evening Meal': '🍛',
                'Evening Snack': '🍪', 'Dinner': '🍛'
            }
            emoji = meal_emojis.get(meal['type'], '🍴')
            meal_time = meal_times.get(meal['type'], "")
            
            # Build content HTML
            content_parts = []
            if meal.get('serving_size'):
                content_parts.append(f"<p><strong>Serving Size:</strong> {meal['serving_size']}</p>")
            if meal.get('ingredients'):
                content_parts.append(f"<p><strong>Ingredients:</strong> {meal['ingredients']}</p>")
            if meal.get('description'):
                content_parts.append(f"<p><strong>Description:</strong> {meal['description']}</p>")
            
            content_html = "".join(content_parts)
            
            # Render meal card
            st.markdown(f"""
            <div class="meal-card">
                <div class="meal-header">
                    <div>{emoji} <strong>{meal['type']}:</strong> {meal['name']}</div>  
                    {f'<div class="meal-time">🕐 {meal_time}</div>' if meal_time else ''}
                </div>
                <div class="meal-content">
                    {content_html}
                </div>
                <div class="meal-footer">
                    <div class="nutrient-item"><strong>🔥 {meal['calories']}</strong><span>Calories</span></div>
                    <div class="nutrient-item"><strong>💪 {meal['protein']}g</strong><span>Protein</span></div>
                    <div class="nutrient-item"><strong>🌾 {meal['carbs']}g</strong><span>Carbs</span></div>
                    <div class="nutrient-item"><strong>🟫 {meal['fats']}g</strong><span>Fats</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)


def display_form(generator, is_edit=False):
    """Display the input form for diet plan generation"""
    
    # Pre-fill form with existing data if editing
    form_data = st.session_state.get('form_data', {}) if is_edit else {}
    
    if is_edit:
        st.markdown("""
        <div class="edit-form-container">
            <div class="edit-header">
                <h2>✏️ Edit Your Profile</h2>
                <p>Update any information and regenerate your personalized diet plan</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("diet_form", clear_on_submit=not is_edit):
        # Personal Information Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">👤 Personal Information</h3>', unsafe_allow_html=True)
        
        name = st.text_input("Name", value=form_data.get('name', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, 
                                value=form_data.get('age', None))
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, 
                                   value=form_data.get('weight', None), step=0.1)
        with col2:
            gender_options = ["Male", "Female", "Other"]
            gender_index = 0
            if is_edit and 'gender' in form_data:
                gender_value = form_data['gender'].title()
                gender_index = gender_options.index(gender_value) if gender_value in gender_options else 0
            gender = st.selectbox("Gender", gender_options, index=gender_index)
            
            height = st.number_input("Height (cm)", min_value=100, max_value=250, 
                                   value=form_data.get('height', None))
        
        # BMI Calculation and Display
        if weight and height:
            bmi = generator.calculate_bmi(weight, height)
            bmi_category = generator.get_bmi_category(bmi)
            st.markdown(f"""
            <div class="bmi-card">
                <div class="bmi-value">BMI: {bmi}</div>
                <div class="bmi-category">{bmi_category}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Health Goals & Lifestyle Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🎯 Health Goals & Lifestyle</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            goal_options = ["Weight Loss", "Weight Gain", "Muscle Building", "Weight Maintenance", "Athletic Performance", "General Health"]
            goal_index = 0
            if is_edit and 'health_goal' in form_data:
                goal_index = goal_options.index(form_data['health_goal']) if form_data['health_goal'] in goal_options else 0
            health_goal = st.selectbox("Primary Health Goal", goal_options, index=goal_index)
            
            activity_options = [
                "Sedentary (little/no exercise)",
                "Lightly Active (light exercise 1-3 days/week)",
                "Moderately Active (moderate exercise 3-5 days/week)",
                "Very Active (hard exercise 6-7 days/week)",
                "Extremely Active (physical job + exercise)"
            ]
            activity_index = 0
            if is_edit and 'activity_level' in form_data:
                activity_mapping_reverse = {
                    "sedentary": 0,
                    "lightly_active": 1,
                    "moderately_active": 2,
                    "very_active": 3,
                    "extremely_active": 4
                }
                activity_index = activity_mapping_reverse.get(form_data['activity_level'], 0)
            activity_level = st.selectbox("Activity Level", activity_options, index=activity_index)
            
        with col2:
            meals_options = [2, 3, 4, 5, 6]
            meals_index = 1
            if is_edit and 'meals_per_day' in form_data:
                meals_index = meals_options.index(form_data['meals_per_day']) if form_data['meals_per_day'] in meals_options else 1
            meals_per_day = st.selectbox("Meals per Day", meals_options, index=meals_index)
            
            sleep_duration = st.slider("Average Sleep Duration (hours)", 4.0, 12.0, 
                                     form_data.get('sleep_duration', 7.5), 0.5)

        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sleep Schedule Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🛌 Sleep Schedule</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; margin-bottom: 1rem;">Tell us your sleep and wake times to optimize meal timing for better digestion and metabolism.</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            default_sleep = time(23, 0)  # 11:00 PM
            if is_edit and 'sleep_time' in form_data:
                try:
                    sleep_str = form_data['sleep_time']
                    sleep_parts = sleep_str.replace(' AM', '').replace(' PM', '').split(':')
                    hour = int(sleep_parts[0])
                    minute = int(sleep_parts[1])
                    if 'PM' in sleep_str and hour != 12:
                        hour += 12
                    elif 'AM' in sleep_str and hour == 12:
                        hour = 0
                    default_sleep = time(hour, minute)
                except:
                    pass
            
            sleep_time_input = st.time_input("Sleep Time", value=default_sleep, 
                                           help="What time do you usually go to sleep?")
            
        with col2:
            default_wake = time(7, 0)  # 7:00 AM
            if is_edit and 'wake_time' in form_data:
                try:
                    wake_str = form_data['wake_time']
                    wake_parts = wake_str.replace(' AM', '').replace(' PM', '').split(':')
                    hour = int(wake_parts[0])
                    minute = int(wake_parts[1])
                    if 'PM' in wake_str and hour != 12:
                        hour += 12
                    elif 'AM' in wake_str and hour == 12:
                        hour = 0
                    default_wake = time(hour, minute)
                except:
                    pass
            
            wake_time_input = st.time_input("Wake Time", value=default_wake,
                                          help="What time do you usually wake up?")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Dietary Preferences Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🍽️ Dietary Preferences</h3>', unsafe_allow_html=True)
        
        diet_options = ["No specific diet", "Vegetarian", "Vegan", "Ketogenic", "Paleo", "Mediterranean", "Low Carb", "Intermittent Fasting"]
        diet_index = 0
        if is_edit and 'diet_type' in form_data:
            diet_index = diet_options.index(form_data['diet_type']) if form_data['diet_type'] in diet_options else 0
        
        diet_type = st.selectbox("Diet Type", diet_options, index=diet_index)
        
        col1, col2 = st.columns(2)
        with col1:
            food_preferences = st.text_area("Food Preferences", 
                                          value=form_data.get('food_preferences', ''),
                                          placeholder="e.g., chicken, broccoli, oatmeal")
        with col2:
            food_dislikes = st.text_area("Food Dislikes", 
                                       value=form_data.get('food_dislikes', ''),
                                       placeholder="e.g., seafood, mushrooms")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Medical & Allergy Information Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">⚕️ Medical & Allergy Information</h3>', unsafe_allow_html=True)
        
        medical_conditions = st.text_area("Medical Conditions", 
                                        value=form_data.get('medical_conditions', ''),
                                        placeholder="e.g., diabetes, hypertension")
        
        allergy_options = ["Nuts", "Dairy", "Gluten", "Eggs", "Shellfish", "Soy", "Fish", "Sesame"]
        default_allergies = form_data.get('allergies', []) if is_edit else []
        default_standard_allergies = [a for a in default_allergies if a in allergy_options]
        selected_allergies = st.multiselect("Select known allergies:", allergy_options, 
                                          default=default_standard_allergies)
        
        custom_allergies = [a for a in default_allergies if a not in allergy_options] if is_edit else []
        other_allergies = st.text_input("Other allergies or intolerances:", 
                                      value=', '.join(custom_allergies) if custom_allergies else '')
        if other_allergies:
            selected_allergies.extend([a.strip() for a in other_allergies.split(',')])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional Information Section
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">📝 Additional Information</h3>', unsafe_allow_html=True)
        
        additional_info = st.text_area("Additional Information", 
                                     value=form_data.get('additional_info', ''),
                                     placeholder="Anything else to consider...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit Button
        button_text = "🔄 Regenerate My Diet Plan" if is_edit else "🚀 Generate My Personalized Diet Plan"
        submitted = st.form_submit_button(button_text, use_container_width=True)
        
        if submitted:
            if not all([name, age, weight, height, gender, health_goal, activity_level, sleep_time_input, wake_time_input]):
                st.error("❌ Please fill in all required fields.")
            else:
                activity_mapping = {
                    "Sedentary (little/no exercise)": "sedentary",
                    "Lightly Active (light exercise 1-3 days/week)": "lightly_active",
                    "Moderately Active (moderate exercise 3-5 days/week)": "moderately_active",
                    "Very Active (hard exercise 6-7 days/week)": "very_active",
                    "Extremely Active (physical job + exercise)": "extremely_active"
                }
                
                # Format times for storage
                sleep_time_str = sleep_time_input.strftime("%I:%M %p")
                wake_time_str = wake_time_input.strftime("%I:%M %p")
                
                st.session_state.form_data = {
                    'name': name, 'age': age, 'weight': weight, 'height': height,
                    'gender': gender.lower(), 'health_goal': health_goal,
                    'activity_level': activity_mapping.get(activity_level, "sedentary"),
                    'meals_per_day': meals_per_day, 'sleep_duration': sleep_duration,
                    'sleep_time': sleep_time_str, 'wake_time': wake_time_str,
                    'diet_type': diet_type, 'food_preferences': food_preferences,
                    'food_dislikes': food_dislikes, 'medical_conditions': medical_conditions,
                    'allergies': selected_allergies, 'additional_info': additional_info
                }
                
                # Calculate meal times
                meal_timing_calc = MealTimingCalculator()
                st.session_state.meal_times = meal_timing_calc.calculate_meal_times(
                    sleep_time_input, wake_time_input, meals_per_day
                )
                
                st.session_state.page = 'generating'
                st.rerun()


def display_results():
    """Display the generated diet plan with edit functionality"""
    st.markdown("""
    <div class="results-header">
        <h1>✨ Your 7-Day Personalized Meal Plan</h1>
        <p>Crafted specifically for your health goals and dietary preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diet_plan_{timestamp}.json"
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.download_button(
            label="📥 Download Plan",
            data=st.session_state.diet_plan,
            file_name=filename,
            mime="application/json",
            use_container_width=True
        )
    with col2:
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.session_state.page = 'edit'
            st.rerun()
    with col3:
        if st.button("🆕 New Plan", use_container_width=True):
            # Clear session state
            for key in ['form_data', 'diet_plan', 'days_data', 'meal_times', 'generation_time']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.page = 'form'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display user profile summary
    if 'form_data' in st.session_state:
        user_data = st.session_state.form_data
        st.markdown(f"""
        <div class="form-section" style="margin-bottom: 2rem;">
            <h3 class="section-title">👤 Profile Summary</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div><strong>Name:</strong> {user_data['name']}</div>
                <div><strong>Goal:</strong> {user_data['health_goal']}</div>
                <div><strong>Diet Type:</strong> {user_data['diet_type']}</div>
                <div><strong>Meals/Day:</strong> {user_data['meals_per_day']}</div>
                <div><strong>Sleep:</strong> {user_data.get('sleep_time', 'N/A')} - {user_data.get('wake_time', 'N/A')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display meal plan
    if ('days_data' in st.session_state and st.session_state.days_data and 
        'meal_times' in st.session_state and st.session_state.meal_times):
        
        display_professional_meal_plan(st.session_state.days_data, st.session_state.meal_times)
        
        # Display success message with generation time
        if 'generation_time' in st.session_state:
            gen_time = st.session_state.generation_time
            st.markdown(f"""
            <div class="success-message">
                🎉 Diet plan generated successfully in {gen_time:.2f} seconds! Your personalized nutrition journey with optimized meal timing starts here.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-message">
                🎉 Diet plan generated successfully! Your personalized nutrition journey with optimized meal timing starts here.
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("❌ Could not parse the diet plan. Please try again.")
        with st.expander("View Raw Diet Plan"):
            st.text_area("Raw Diet Plan", value=st.session_state.diet_plan, height=400)


def main():
    # Load custom CSS
    load_css()
    
    generator = DietPlanGenerator()
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🥗 AI Diet Plan Generator</h1>
        <p>Get personalized nutrition plans with optimized meal timing generated by advanced AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'form'
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### 🔑 OpenAI Configuration")
        api_key_available = bool(generator.api_key)
        if api_key_available:
            st.success("✅ API key loaded from environment")
        else:
            st.warning("⚠️ OPENAI_API_KEY not found")
            api_key = st.text_input("OpenAI API Key:", type="password", 
                                  help="Enter your OpenAI API key.")
            if api_key:
                generator.set_api_key(api_key)
                api_key_available = True
                st.success("✅ API key configured")
        
        # Navigation info
        if 'form_data' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Current Session")
            st.info(f"**User:** {st.session_state.form_data.get('name', 'Unknown')}")
            if 'meal_times' in st.session_state:
                st.success("🕐 Meal timing calculated")
            if st.session_state.page == 'results':
                st.success("✅ Diet plan ready")
                
            # Display generation time in sidebar
            if 'generation_time' in st.session_state:
                st.markdown("---")
                st.markdown("### ⏱️ Generation Stats")
                st.metric("Generation Time", f"{st.session_state.generation_time:.2f}s")

    if not api_key_available:
        st.error("❌ OpenAI API key is required. Please set it in your environment variables or enter it in the sidebar.")
        return

    # Page routing
    if st.session_state.page == 'form':
        display_form(generator, is_edit=False)
    
    elif st.session_state.page == 'edit':
        display_form(generator, is_edit=True)
    
    elif st.session_state.page == 'generating':
        display_loading_animation()
        
        try:
            # Start timing for diet plan generation
            start_time = time_module.time()
            diet_plan_json = generator.generate_diet_plan(st.session_state.form_data)
            end_time = time_module.time()
            
            # Store generation time
            st.session_state.generation_time = end_time - start_time

            days_data = generator.parse_meal_plan(diet_plan_json)
            
            st.session_state.diet_plan = diet_plan_json
            st.session_state.days_data = days_data
            st.session_state.page = 'results'
            
            time_module.sleep(1)  # Brief pause to allow user to see success before rerun
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.page = 'form'
            if st.button("🔄 Try Again", use_container_width=True):
                st.rerun()

    elif st.session_state.page == 'results':
        display_results()


if __name__ == "__main__":
    main()







