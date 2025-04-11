import streamlit as st
import requests
import pandas as pd

# Define bounding box for Ras Al Khaimah (min_lat, min_lon, max_lat, max_lon)
RAS_AL_KHAIMAH_BBOX = (25.5919, 55.7155, 25.9046, 56.0726)

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
    # Define Overpass API query
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
    
    # Extract relevant details
    locations = []
    for element in data["elements"]:
        name = element["tags"].get("name", "Unknown")
        lat = element.get("lat")
        lon = element.get("lon")
        locations.append({"name": name, "latitude": lat, "longitude": lon, "category": category})
    
    return pd.DataFrame(locations)

# Streamlit UI
st.title("Ras Al Khaimah Trip Planner")

# Buttons for Hotels, Tourism, and Restaurants
st.header("Fetch Locations")

if st.button("Fetch Hotels"):
    hotels = fetch_osm_data("hotel", RAS_AL_KHAIMAH_BBOX)
    if hotels.empty:
        st.warning("No hotels found.")
    else:
        st.success(f"Found {len(hotels)} hotels!")
        st.map(hotels)
        st.write(hotels)

if st.button("Fetch Tourism"):
    attractions = fetch_osm_data("attraction", RAS_AL_KHAIMAH_BBOX)
    if attractions.empty:
        st.warning("No attractions found.")
    else:
        st.success(f"Found {len(attractions)} attractions!")
        st.map(attractions)
        st.write(attractions)

if st.button("Fetch Restaurants"):
    restaurants = fetch_osm_data("restaurant", RAS_AL_KHAIMAH_BBOX)
    if restaurants.empty:
        st.warning("No restaurants found.")
    else:
        st.success(f"Found {len(restaurants)} restaurants!")
        st.map(restaurants)
        st.write(restaurants)
