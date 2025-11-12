import streamlit as st
import os
import time
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini

# -------------------------------
# Load Gemini API Key
# -------------------------------
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Missing Gemini API key! Please add GEMINI_API_KEY in .streamlit/secrets.toml or as an environment variable.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title("AI Travel Planner")

# -------------------------------
# User Input Section
# -------------------------------
st.subheader("Trip Details")

source = st.text_input("Departure City:", "")
destination = st.text_input("Destination:", "")
num_days = st.slider("Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox(
    "Travel Theme:",
    ["", "Couple Getaway", "Family Vacation", "Adventure Trip", "Solo Exploration"],
    index=0
)
activity_preferences = st.text_area("What activities do you enjoy?", "")
departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")

st.markdown("---")

# -------------------------------
# Sidebar Preferences
# -------------------------------
st.sidebar.header("Travel Preferences")

budget = st.sidebar.radio("Budget:", ["Economy", "Standard", "Luxury"], index=0)
hotel_rating = st.sidebar.selectbox("Preferred Hotel Rating:", ["Any", "3⭐", "4⭐", "5⭐"], index=0)
flight_class = st.sidebar.radio("Flight Class:", ["Economy", "Business", "First Class"], index=0)
visa_required = st.sidebar.checkbox("Visa Required?")
travel_insurance = st.sidebar.checkbox("Travel Insurance?")
currency_converter = st.sidebar.checkbox("Currency Exchange Info?")

# -------------------------------
# Define Gemini AI Agent
# -------------------------------
planner = Agent(
    name="Travel Planner",
    instructions=[
        "You are an AI travel planner.",
        "Given user inputs, create a complete travel plan with:",
        "1. Destination overview (climate, culture, safety)",
        "2. Recommended attractions and activities",
        "3. Hotel and restaurant suggestions",
        "4. A detailed day-by-day itinerary"
    ],
    model=Gemini(id="models/gemini-2.0-flash"),
)

# -------------------------------
# Function: Safe Run (robust retries)
# -------------------------------
def safe_run(agent, prompt, retries=5):
    """Executes the Gemini agent with automatic retry on API errors."""
    for i in range(retries):
        try:
            return agent.run(prompt, stream=False)
        except Exception as e:
            err = str(e)
            if "503" in err:
                wait = (i + 1) * 8
                st.warning(f"Gemini service temporarily unavailable (503). Retrying in {wait}s...")
                time.sleep(wait)
            elif "404" in err:
                st.error("Model not found. Please check your model name (try 'models/gemini-2.5-flash').")
                return None
            elif "429" in err or "Too Many Requests" in err:
                wait = (i + 1) * 5
                st.warning(f"Gemini rate limit hit. Retrying in {wait}s...")
                time.sleep(wait)
            elif "API key" in err or "Invalid" in err:
                st.error("Invalid or expired Gemini API key. Please verify your key in secrets.toml.")
                return None
            else:
                st.error(f"Unexpected error: {err}")
                return None

    st.error("Gemini API unavailable after multiple retries. Please try again later.")
    return None

# -------------------------------
# Generate Travel Plan
# -------------------------------
if st.button("Generate My Travel Plan"):
    if not destination.strip():
        st.warning("Please enter your destination before generating a plan.")
    else:
        with st.spinner("Generating your personalized itinerary..."):
            prompt = f"""
            Create a {num_days}-day {travel_theme.lower() if travel_theme else "custom"} travel plan
            from {source or "your departure city"} to {destination}.
            Include:
            - Destination introduction (climate, safety, travel tips)
            - Top attractions, hidden gems, and local experiences
            - Suggested hotels and restaurants (matching {hotel_rating} rating, {budget} budget)
            - Day-by-day itinerary (activities, rest time, travel between spots)
            Traveler preferences: {activity_preferences or "Not specified"}.
            Departure date: {departure_date}, Return date: {return_date}.
            Visa required: {visa_required}, Travel insurance: {travel_insurance}.
            Output the plan in a clear, structured, professional format.
            """

            response = safe_run(planner, prompt)

        if response:
            result_text = getattr(response, "content", str(response))
            st.subheader("Your AI-Generated Travel Plan")
            st.write(result_text)
            st.success("Travel plan created successfully.")
        else:
            st.error("Failed to generate travel plan. Please try again later.")

# -------------------------------
# App Ready
# -------------------------------
if __name__ == "__main__":
    st.write("App loaded successfully!")
