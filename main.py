import streamlit as st
import requests
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect("trip_planner.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY,
            type TEXT,
            name TEXT,
            rating REAL,
            price_level TEXT,
            description TEXT,
            reviews_count INTEGER,
            image_url TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fetch Data from Google Places API
def fetch_places_data(place_type, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={place_type}+in+Ras+Al+Khaimah&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data. Check your API key or connection.")
        return None

# Save Places to Database
def save_place_to_db(place_type, place):
    conn = sqlite3.connect("trip_planner.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO places (type, name, rating, price_level, description, reviews_count, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (place_type, place['name'], place.get('rating', 0), place.get('price_level', 'N/A'),
          place.get('formatted_address', 'No description available.'), place.get('user_ratings_total', 0),
          place.get('image_url', None)))
    conn.commit()
    conn.close()

# Display Places
def display_places(place_type):
    conn = sqlite3.connect("trip_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM places WHERE type = ?", (place_type,))
    places = cursor.fetchall()
    conn.close()
    for place in places:
        st.subheader(place[2])  # Name
        st.write(f"Rating: {place[3]} ⭐")
        st.write(f"Price Level: {place[4]}")
        st.write(place[5])  # Description
        if place[7]:  # Image URL
            st.image(place[7], width=300)

# Initialize Database
init_db()

# Streamlit UI
st.title("Ras Al Khaimah Trip Planner")

# Input API Key
api_key = st.text_input("Google Places API Key", type="password")

# Buttons for Hotels, Tourism, and Restaurants
if st.button("Fetch Hotels"):
    if not api_key:
        st.error("Please provide a valid Google Places API Key.")
    else:
        hotels_data = fetch_places_data("hotels", api_key)
        if hotels_data and "results" in hotels_data:
            for result in hotels_data["results"]:
                # Add image URL if available
                if "photos" in result:
                    photo_ref = result["photos"][0]["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={api_key}"
                    result["image_url"] = photo_url
                save_place_to_db("hotel", result)
            st.success("Hotels fetched and saved to database!")
        else:
            st.error("No data found for hotels.")

if st.button("Fetch Tourism"):
    if not api_key:
        st.error("Please provide a valid Google Places API Key.")
    else:
        tourism_data = fetch_places_data("tourist attractions", api_key)
        if tourism_data and "results" in tourism_data:
            for result in tourism_data["results"]:
                # Add image URL if available
                if "photos" in result:
                    photo_ref = result["photos"][0]["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={api_key}"
                    result["image_url"] = photo_url
                save_place_to_db("tourism", result)
            st.success("Tourist attractions fetched and saved to database!")
        else:
            st.error("No data found for tourist attractions.")

if st.button("Fetch Restaurants"):
    if not api_key:
        st.error("Please provide a valid Google Places API Key.")
    else:
        restaurants_data = fetch_places_data("restaurants", api_key)
        if restaurants_data and "results" in restaurants_data:
            for result in restaurants_data["results"]:
                # Add image URL if available
                if "photos" in result:
                    photo_ref = result["photos"][0]["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={api_key}"
                    result["image_url"] = photo_url
                save_place_to_db("restaurant", result)
            st.success("Restaurants fetched and saved to database!")
        else:
            st.error("No data found for restaurants.")

# Display Saved Data
st.header("Saved Data")
place_type = st.selectbox("Select Type to View", ["hotel", "tourism", "restaurant"])
if st.button("Show Places"):
    display_places(place_type)
