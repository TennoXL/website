import streamlit as st
import datetime
import urllib.parse
import random
import math

# --- Logo ---
st.image("WhatsApp Image 2025-04-17 at 16.35.32_3984a2da.jpg", width=300)  # Replace with your own logo if desired

st.title("Khaimah-Settled")

# --- Sidebar Settings ---
st.sidebar.header("🌐 Trip Settings")
budget = st.sidebar.number_input("Enter your budget (AED):", min_value=50, step=10)

# Trip start and end dates
start_date = st.sidebar.date_input("Trip start date:", datetime.date.today())
end_date = st.sidebar.date_input("Trip end date:", start_date)
start_time = st.sidebar.time_input("Daily start time:", datetime.time(9, 0))

trip_days = (end_date - start_date).days + 1
if trip_days < 1:
    st.error("End date must be the same or after the start date.")
    st.stop()

# --- Attractions Info ---
attractions = {
    "Jebel Jais": "Famous for its mountain views and zipline adventure.",
    "Al Hamra Mall": "Great for budget shopping and quick meals.",
    "RAK National Museum": "Explore history on a budget.",
    "Al Marjan Island": "Scenic beaches perfect for relaxing.",
    "Dhayah Fort": "A historic fort with a panoramic view."
}

# --- Planning Mode ---
mode = st.radio("Choose how to plan your trip:", ["I want to choose attractions", "Surprise Me!"])

selected_attractions = []
reasons = {}
durations = {}

if mode == "I want to choose attractions":
    selected_attractions = st.multiselect("Select attractions to visit:", list(attractions.keys()))
    for place in selected_attractions:
        duration = st.number_input(f"How many minutes at {place}?", min_value=15, max_value=300, step=15, key=place)
        reasons[place] = attractions[place]
        durations[place] = duration
else:
    surprise_count = st.slider("How many places should we surprise you with?", min_value=1, max_value=5, value=3)
    selected_attractions = random.sample(list(attractions.keys()), surprise_count)
    for place in selected_attractions:
        duration = random.choice([30, 60, 90, 120])
        st.markdown(f"**{place}** - {duration} mins  → {attractions[place]}")
        st.session_state[place] = duration
        reasons[place] = attractions[place]
        durations[place] = duration

# --- Generate Schedule ---
if selected_attractions:
    st.subheader("🗓️ Daily Trip Schedule")

    # Distribute attractions across trip days
    daily_plan = {start_date + datetime.timedelta(days=i): [] for i in range(trip_days)}
    for idx, place in enumerate(selected_attractions):
        day = list(daily_plan.keys())[idx % trip_days]
        daily_plan[day].append(place)

    for day, places in daily_plan.items():
        st.markdown(f"### 📅 {day.strftime('%A, %d %B %Y')}")
        current_time = datetime.datetime.combine(day, start_time)
        for place in places:
            duration = durations[place]
            arrive = current_time.strftime("%I:%M %p")
            leave = (current_time + datetime.timedelta(minutes=duration)).strftime("%I:%M %p")
            st.write(f"**{place}** → Arrive: {arrive} | Leave: {leave}")
            current_time += datetime.timedelta(minutes=duration + 15)

    st.subheader("🚗 Google Maps Route")
    base_url = "https://www.google.com/maps/dir/"
    places_encoded = [urllib.parse.quote_plus(place + ", Ras Al Khaimah") for place in selected_attractions]
    route_url = base_url + "/".join(places_encoded)
    st.markdown(f"[Click to view route in Google Maps]({route_url})")

    st.subheader("🔍 Why These Places?")
    for place in selected_attractions:
        st.write(f"**{place}** → {reasons[place]}")
