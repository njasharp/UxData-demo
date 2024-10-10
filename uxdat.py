import streamlit as st
import os
from groq import Groq
import pandas as pd
import random
from typing import Dict, Any, Optional, List

# Streamlit page configuration
st.set_page_config(layout="wide", page_title="Game User Assessment & AI ML Planning", initial_sidebar_state="expanded")

# Supported models
SUPPORTED_MODELS: Dict[str, str] = {
    "Llama 3.2 1B (Preview)": "llama-3.2-1b-preview",
    "Llama 3 70B": "llama3-70b-8192",
    "Llama 3 8B": "llama3-8b-8192",
    "Llama 3.1 70B": "llama-3.1-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
    "LLaVA 1.5 7B": "llava-v1.5-7b-4096-preview",
    "Llama 3.2 3B (Preview)": "llama-3.2-3b-preview",
    "Llama 3.2 11B Vision (Preview)": "llama-3.2-11b-vision-preview"
}

MAX_TOKENS: int = 1000

# Initialize Groq client with API key
@st.cache_resource
def get_groq_client() -> Optional[Groq]:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables. Please set it and restart the app.")
        return None
    return Groq(api_key=groq_api_key)

client = get_groq_client()

# Game Genres and Features based on the PDF
game_genres = [
    "Casual", "Hyper Casual", "Puzzle", "RPG", "Shooter", "Strategy", 
    "Sports & Driving", "Casino", "Simulation", "AR/Location-Based"
]
live_event_types = [
    "Live Events", "Seasonal Events", "Special Promotions", "Challenges", 
    "Leaderboard Tournaments", "Guild Competitions", "PvP Events"
]

# Function to query Groq LLM for expanding strategies
def expand_strategies_with_llm(model: str, system_prompt: str, strategy: str, temperature: float = 0.7) -> str:
    user_query = f"Expand the following strategy and include recommendations for best practices:\n\nStrategy: {strategy}"
    
    try:
        response = client.chat.completions.create(
            model=SUPPORTED_MODELS[model],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=temperature,
            max_tokens=MAX_TOKENS
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            return "No expansion available for this strategy."
    except Exception as e:
        return f"Error generating strategy expansion: {str(e)}"

def create_user_profile() -> Optional[Dict[str, Any]]:
    st.header("User Assessment Questionnaire with AI-driven strategies and marketing insights.")
    with st.form(key='assessment_form'):
        age = st.slider("How old are you?", 10, 60, 25)
        gaming_frequency = st.selectbox("How often do you play mobile games?", ["Daily", "Weekly", "Monthly", "Rarely"])
        preferred_genre = st.radio("Which genre do you prefer?", game_genres)
        hours_played = st.slider("Average hours spent playing games per week?", 0, 40, 5)
        competitiveness = st.selectbox("How competitive are you in gaming?", ["Not at all", "Somewhat", "Moderately", "Very Competitive"])

        # Add Select Game Features and Event Types to the form
        st.subheader("Select Game Features")
        features = [
            "Progression", "Buildings", "Characters & Units", "Game Progression", "Items",
            "Ad Monetization", "Gacha", "IAP & Monetization", "Trading & Economy", 
            "Competition & PVP", "Social Interaction", "Appointment Mechanics", 
            "Session Length", "Live Events", "Retention"
        ]
        selected_features = st.multiselect("Choose relevant game features:", features)

        st.subheader("Select Live Event Types")
        selected_event_types = st.multiselect("Choose relevant live event types:", live_event_types)

        submit_button = st.form_submit_button(label='Submit Assessment')

    if submit_button:
        return {
            "Age": age,
            "Gaming Frequency": gaming_frequency,
            "Preferred Genre": preferred_genre,
            "Hours Played per Week": hours_played,
            "Competitiveness": competitiveness,
            "Selected Features": selected_features,
            "Selected Event Types": selected_event_types
        }
    return None

def generate_seo_aso_suggestions(user_profile: Dict[str, Any]) -> Dict[str, List[str]]:
    seo_suggestions = []
    aso_suggestions = []

    # SEO Suggestions based on user profile
    genre = user_profile['Preferred Genre']
    selected_features = user_profile['Selected Features']
    
    if genre == 'Casual':
        seo_suggestions.append("Target keywords like 'free casual games', 'best casual games', 'mobile games to relax'.")
    elif genre == 'RPG':
        seo_suggestions.append("Optimize for 'top RPG mobile games', 'best free RPGs', 'immersive RPG games'.")
    elif genre == 'Puzzle':
        seo_suggestions.append("Use keywords such as 'brain games', 'best puzzle games', 'mobile puzzle games'.")
    
    if 'Game Progression' in selected_features:
        seo_suggestions.append("Include keywords related to 'level-based games', 'game progression mechanics'.")
    
    # ASO Suggestions based on user profile
    if 'Special Promotions' in user_profile['Selected Event Types']:
        aso_suggestions.append("Utilize limited-time events in app description to encourage installs.")
        aso_suggestions.append("Highlight special promotions and seasonal events in the app’s title or subtitle.")
    
    if 'Social Interaction' in selected_features:
        aso_suggestions.append("Mention social features like multiplayer and leaderboards in the description.")

    return {
        "SEO Suggestions": seo_suggestions,
        "ASO Suggestions": aso_suggestions
    }

def generate_action_plan_with_features(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    action_plan = {
        "game_recommendations": [],
        "strategies": []
    }
    
    genre = user_profile['Preferred Genre']
    hours = user_profile['Hours Played per Week']
    competitiveness = user_profile['Competitiveness']

    # Game recommendations based on profile
    game_recommendations = {
        "Puzzle": ["Candy Crush Saga", "Two Dots", "Monument Valley"],
        "Action": ["PUBG Mobile", "Call of Duty: Mobile", "Brawl Stars"],
        "RPG": ["Genshin Impact", "Final Fantasy Brave Exvius", "Another Eden"],
        "Strategy": ["Clash Royale", "Rise of Kingdoms", "Plague Inc."],
        "Casual": ["Among Us", "Subway Surfers", "Temple Run"]
    }
    
    action_plan['game_recommendations'] = game_recommendations.get(genre, [])

    # Basic strategies
    if hours < 5:
        action_plan['strategies'].append("Set aside specific times for gaming to maintain consistency.")
    if hours > 20:
        action_plan['strategies'].append("Consider balancing gaming time with other activities for a well-rounded lifestyle.")
    if competitiveness == "Very Competitive":
        action_plan['strategies'].append("Focus on mastering one or two games rather than playing many casually.")
    
    return action_plan

def display_ai_agent_results(action_plan: Dict[str, Any], user_profile: Dict[str, Any]):
    st.write("### AI Agent: Reasoning and Planning")
    
    # Display User Profile in a more readable format
    st.subheader("User Profile")
    st.write(f"""
    **Age:** {user_profile['Age']}  
    **Gaming Frequency:** {user_profile['Gaming Frequency']}  
    **Preferred Genre:** {user_profile['Preferred Genre']}  
    **Hours Played per Week:** {user_profile['Hours Played per Week']}  
    **Competitiveness:** {user_profile['Competitiveness']}  
    **Selected Features:** {', '.join(user_profile['Selected Features']) if user_profile['Selected Features'] else 'None'}  
    **Selected Event Types:** {', '.join(user_profile['Selected Event Types']) if user_profile['Selected Event Types'] else 'None'}
    """)

    # Display game recommendations
    st.subheader("Game Recommendations")
    if action_plan["game_recommendations"]:
        st.write("\n".join([f"- {game}" for game in action_plan["game_recommendations"]]))
    else:
        st.write("*No game recommendations available based on the profile.*")

    # Display and expand strategies using Groq LLM
    st.subheader("Strategies and Best Practices")
    if action_plan["strategies"]:
        for strategy in action_plan["strategies"]:
            st.write(f"**Strategy**: {strategy}")
            # Expand strategy with best practices using LLM
            expanded_strategy = expand_strategies_with_llm("Llama 3 70B", "You are an expert in game development and strategy.", strategy)
            st.write(f"**Best Practices**: {expanded_strategy}")
    else:
        st.write("*No strategies or best practices available based on the profile.*")

    # Generate and display SEO and ASO suggestions
    seo_aso_suggestions = generate_seo_aso_suggestions(user_profile)
    st.subheader("SEO and ASO Suggestions")
    
    st.write("**SEO Suggestions**:")
    if seo_aso_suggestions["SEO Suggestions"]:
        st.write("\n".join([f"- {suggestion}" for suggestion in seo_aso_suggestions["SEO Suggestions"]]))
    else:
        st.write("*No SEO suggestions available based on the profile.*")

    st.write("**ASO Suggestions**:")
    if seo_aso_suggestions["ASO Suggestions"]:
        st.write("\n".join([f"- {suggestion}" for suggestion in seo_aso_suggestions["ASO Suggestions"]]))
    else:
        st.write("*No ASO suggestions available based on the profile.*")

    # Display the full game strategy plan in a readable format
    full_results = f"User Profile:\n{user_profile}\n\nGame Recommendations:\n{action_plan['game_recommendations']}\n\nStrategies and Best Practices:\n{action_plan['strategies']}\n\nSEO and ASO Suggestions:\n{seo_aso_suggestions}"
    
    st.subheader("Full Game Strategy Plan")
    st.write(full_results)  # Display full results on the page

    # Add a download button for the results
    st.download_button("Download Results", data=full_results, file_name="game_strategy_plan.txt", mime="text/plain")

def groq_ai_section_with_features(user_profile: Dict[str, Any]):
    with st.sidebar:
        st.header("Groq AI Configuration")
        model = st.selectbox("Select LLM Model", list(SUPPORTED_MODELS.keys()))
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

        if st.button("Generate Enhanced AI Plan with Groq"):
            system_prompt = """
            You are an AI assistant specializing in mobile game strategy and player profiling. 
            Based on the following user profile and selected game features, generate a detailed plan for enhancing their gaming experience.
            """
            
            user_query = f"""
            User Profile:
            - Age: {user_profile['Age']}
            - Gaming Frequency: {user_profile['Gaming Frequency']}
            - Preferred Genre: {user_profile['Preferred Genre']}
            - Hours Played per Week: {user_profile['Hours Played per Week']}
            - Competitiveness: {user_profile['Competitiveness']}
            - Selected Features: {', '.join(user_profile['Selected Features']) if user_profile['Selected Features'] else 'None'}
            - Selected Event Types: {', '.join(user_profile['Selected Event Types']) if user_profile['Selected Event Types'] else 'None'}

            Please provide a comprehensive gaming plan and strategy for this user, including relevant suggestions for the selected features and event types.
            """

            with st.spinner("Generating AI plan... This may take a few moments."):
                response = query_groq(model, temperature, system_prompt, user_query)

            if response.startswith("Error:"):
                st.error(response)
            else:
                st.subheader("AI-Generated Enhanced Plan")
                st.write(response)
                st.download_button(label="Download Enhanced AI Plan", data=response, file_name="enhanced_ai_game_plan.txt", mime="text/plain")

def main():
    st.image("p1.png")
    st.sidebar.image("p2.png", width=200)
    st.title("Game User Assessment and ML Personas App")
    
    # Create the user profile from the form
    user_profile = create_user_profile()

    # Only call the AI section once the user profile is created
    if user_profile:
        action_plan = generate_action_plan_with_features(user_profile)
        display_ai_agent_results(action_plan, user_profile)

        # Pass the user profile into the AI section to avoid the KeyError
        groq_ai_section_with_features(user_profile)

if __name__ == "__main__":
    main()
