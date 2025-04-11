import streamlit as st
import datetime
import urllib.parse
import random

# Sample attractions in Ras Al Khaimah
attractions = {
    "Jebel Jais": "Famous for its mountain views and zipline adventure.",
    "Al Hamra Mall": "Great for budget shopping and quick meals.",
    "RAK National Museum": "Explore history on a budget.",
    "Al Marjan Island": "Scenic beaches perfect for relaxing.",
    "Dhayah Fort": "A historic fort with a panoramic view."
}

st.title("🌍 Ras Al Khaimah Budget Tour Planner")

st.sidebar.header("🌐 Trip Settings")
budget = st.sidebar.number_input("Enter your budget (AED):", min_value=50, step=10)
trip_date = st.sidebar.date_input("Select trip date:", datetime.date.today())
start_time = st.sidebar.time_input("Trip start time:", datetime.time(9, 0))

mode = st.radio("Choose how to plan your trip:", ["I want to choose attractions", "Surprise Me!"])

selected_attractions = []
reasons = {}

if mode == "I want to choose attractions":
    selected_attractions = st.multiselect("Select attractions to visit:", list(attractions.keys()))
    for place in selected_attractions:
        duration = st.number_input(f"How many minutes at {place}?", min_value=15, max_value=300, step=15, key=place)
        reasons[place] = attractions[place]
else:
    surprise_count = st.slider("How many places should we surprise you with?", min_value=1, max_value=5, value=3)
    selected_attractions = random.sample(list(attractions.keys()), surprise_count)
    for place in selected_attractions:
        duration = random.choice([30, 60, 90, 120])
        st.markdown(f"**{place}** - {duration} mins  → {attractions[place]}")
        st.session_state[place] = duration
        reasons[place] = attractions[place]

if selected_attractions:
    st.subheader("🕒 Trip Schedule")
    current_time = datetime.datetime.combine(trip_date, start_time)
    schedule = []
    for place in selected_attractions:
        duration = st.session_state.get(place) if mode == "Surprise Me!" else st.number_input(f"Reconfirm minutes at {place}:", value=60, min_value=15, max_value=300, step=15, key=f"confirm_{place}")
        arrive = current_time.strftime("%I:%M %p")
        leave = (current_time + datetime.timedelta(minutes=duration)).strftime("%I:%M %p")
        schedule.append((place, arrive, leave))
        current_time += datetime.timedelta(minutes=duration + 15)  # 15 mins buffer for travel

    for place, arrive, leave in schedule:
        st.write(f"**{place}** → Arrive: {arrive} | Leave: {leave}")

    st.subheader("🚗 Google Maps Route")
    base_url = "https://www.google.com/maps/dir/"
    places_encoded = [urllib.parse.quote_plus(place + ", Ras Al Khaimah") for place in selected_attractions]
    route_url = base_url + "/".join(places_encoded)
    st.markdown(f"[Click to view route in Google Maps]({route_url})")

    st.subheader("🔍 Why These Places?")
    for place in selected_attractions:
        st.write(f"**{place}** → {reasons[place]}")
