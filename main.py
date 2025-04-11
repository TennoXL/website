import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Define bounding box for Ras Al Khaimah (min_lat, min_lon, max_lat, max_lon)
RAS_AL_KHAIMAH_BBOX = (25.5919, 55.7155, 25.9046, 56.0726)

# Initialize session state for trip details and itinerary
if "trip_details" not in st.session_state:
    st.session_state["trip_details"] = {"budget": 0, "start_date": None, "end_date": None}
if "itinerary" not in st.session_state:
    st.session_state["itinerary"] = []

# Function to fetch data from OpenStreetMap using Overpass API
def fetch_osm_data(category, bbox):
    """
    Fetch data from OpenStreetMap using Overpass API.
    Args:
        category (str): Category like 'hotel', 'restaurant', or 'attraction'.
        bbox (tuple): Bounding box for Ras Al Khaimah (min_lat, min_lon, max_lat, max_lon).
    Returns:
        DataFrame: Locations data with name, latitude, longitude, and category.
    """
    category_mapping = {
        "hotel": 'node["tourism"="hotel"]',
        "restaurant": 'node["amenity"="restaurant"]',
        "attraction": 'node["tourism"="attraction"]',
    }
    query = f"""
    [out:json];
    {category_mapping[category]}({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    out body;
    """
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": query})
    if response.status_code != 200:
        return pd.DataFrame([])  # Return empty DataFrame if the request fails
    
    data = response.json()
    locations = []
    for element in data["elements"]:
        name = element["tags"].get("name", "Unknown")
        lat = element.get("lat")
        lon = element.get("lon")
        locations.append({"name": name, "latitude": lat, "longitude": lon, "category": category})
    
    return pd.DataFrame(locations)

# Streamlit UI: Trip Details
st.title("Ras Al Khaimah Trip Planner")

# Trip Details Input
st.sidebar.header("Trip Details")
trip_budget = st.sidebar.number_input("Budget (AED)", min_value=0, step=100, value=st.session_state["trip_details"]["budget"])
start_date = st.sidebar.date_input("Start Date", value=st.session_state["trip_details"]["start_date"] or datetime.today())
end_date = st.sidebar.date_input("End Date", value=st.session_state["trip_details"]["end_date"] or (datetime.today() + timedelta(days=3)))

if st.sidebar.button("Save Trip Details"):
    st.session_state["trip_details"]["budget"] = trip_budget
    st.session_state["trip_details"]["start_date"] = start_date
    st.session_state["trip_details"]["end_date"] = end_date
    st.sidebar.success("Trip details saved!")

# Fetch Locations
st.header("Fetch Locations")
if st.button("Fetch Hotels"):
    hotels = fetch_osm_data("hotel", RAS_AL_KHAIMAH_BBOX)
    if hotels.empty:
        st.warning("No hotels found.")
    else:
        st.success(f"Found {len(hotels)} hotels!")
        st.map(hotels)
        st.write(hotels)
        st.session_state["hotels"] = hotels

if st.button("Fetch Attractions"):
    attractions = fetch_osm_data("attraction", RAS_AL_KHAIMAH_BBOX)
    if attractions.empty:
        st.warning("No attractions found.")
    else:
        st.success(f"Found {len(attractions)} attractions!")
        st.map(attractions)
        st.write(attractions)
        st.session_state["attractions"] = attractions

if st.button("Fetch Restaurants"):
    restaurants = fetch_osm_data("restaurant", RAS_AL_KHAIMAH_BBOX)
    if restaurants.empty:
        st.warning("No restaurants found.")
    else:
        st.success(f"Found {len(restaurants)} restaurants!")
        st.map(restaurants)
        st.write(restaurants)
        st.session_state["restaurants"] = restaurants

# Add to Itinerary
st.header("Plan Your Itinerary")
if "hotels" in st.session_state:
    st.subheader("Select Hotels")
    selected_hotels = st.multiselect("Choose Hotels", st.session_state["hotels"]["name"].tolist())
    for name in selected_hotels:
        st.session_state["itinerary"].append({"name": name, "category": "hotel"})

if "attractions" in st.session_state:
    st.subheader("Select Attractions")
    selected_attractions = st.multiselect("Choose Attractions", st.session_state["attractions"]["name"].tolist())
    for name in selected_attractions:
        st.session_state["itinerary"].append({"name": name, "category": "attraction"})

if "restaurants" in st.session_state:
    st.subheader("Select Restaurants")
    selected_restaurants = st.multiselect("Choose Restaurants", st.session_state["restaurants"]["name"].tolist())
    for name in selected_restaurants:
        st.session_state["itinerary"].append({"name": name, "category": "restaurant"})

# Display Itinerary
st.header("Your Itinerary")
st.write(pd.DataFrame(st.session_state["itinerary"]))
