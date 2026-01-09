import streamlit as st
import requests
import random

st.set_page_config(page_title="Hotel Finder", layout="wide")

# ---------------- FUNCTIONS ----------------
def search_hotels(location, limit=20):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"hotel in {location}",
        "format": "json",
        "extratags": 1,
        "limit": limit
    }
    headers = {"User-Agent": "Hotel-Filter-App"}
    return requests.get(url, params=params, headers=headers).json()

def safe_tags(item):
    return item["extratags"] if isinstance(item.get("extratags"), dict) else {}

def get_image(name):
    wiki = "https://en.wikipedia.org/api/rest_v1/page/summary/" + name.replace(" ", "%20")
    r = requests.get(wiki)
    if r.status_code == 200:
        return r.json().get("thumbnail", {}).get(
            "source",
            "https://via.placeholder.com/300x200?text=Hotel"
        )
    return "https://via.placeholder.com/300x200?text=Hotel"

def ai_price_rating():
    price = random.randint(1500, 5000)
    rating = round(random.uniform(3.0, 5.0), 1)
    stars = int(round(rating))
    available = random.choice([True, True, False])
    return price, rating, stars, available

# ---------------- HEADER ----------------
st.title("🏨 Hotel Finder with Filters")
location = st.text_input("📍 Enter Location")

# ---------------- FILTER SIDEBAR ----------------
st.sidebar.header("Filter by")

only_available = st.sidebar.checkbox("Only show available")

budget = st.sidebar.slider(
    "Your Budget (per night)",
    min_value=1000,
    max_value=6000,
    value=(1500, 5000)
)

st.sidebar.subheader("Star Rating")
star_3 = st.sidebar.checkbox("3 stars")
star_4 = st.sidebar.checkbox("4 stars")
star_5 = st.sidebar.checkbox("5 stars")

selected_stars = []
if star_3: selected_stars.append(3)
if star_4: selected_stars.append(4)
if star_5: selected_stars.append(5)

st.sidebar.subheader("Popular Filters")
free_cancel = st.sidebar.checkbox("Free cancellation")
breakfast = st.sidebar.checkbox("Breakfast included")

# ---------------- RESULTS ----------------
if location:
    hotels = search_hotels(location)

    if not hotels:
        st.warning("No hotels found")
    else:
        for h in hotels:
            price, rating, stars, available = ai_price_rating()

            # APPLY FILTERS
            if only_available and not available:
                continue
            if not (budget[0] <= price <= budget[1]):
                continue
            if selected_stars and stars not in selected_stars:
                continue

            tags = safe_tags(h)
            image = get_image(h["display_name"])

            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:12px;
                    border-radius:10px;
                    box-shadow:0 4px 10px rgba(0,0,0,0.08);
                    margin-bottom:15px;
                    display:flex;
                    gap:15px;
                ">
                    <img src="{image}" style="width:180px;height:130px;border-radius:8px;object-fit:cover;">
                    <div>
                        <h4>{h['display_name'].split(',')[0]}</h4>
                        ⭐ {rating} ({stars}★)<br>
                        💰 <b>₹{price} / night</b><br>
                        📞 {tags.get('phone','Not available')}<br>
                        🌐 {tags.get('website','Not available')}<br>
                        📍 <a href="https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']}" target="_blank">
                            View location
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
