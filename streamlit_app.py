import streamlit as st
import requests
import random

st.set_page_config(page_title="Hotel Finder with Filters", layout="wide")

# ---------------- CSS FIX ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.card {
    background: #ffffff;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 18px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    display: flex;
    gap: 16px;
}
.card img {
    width: 160px;
    height: 120px;
    object-fit: cover;
    border-radius: 10px;
}
.card h4 {
    color: #111;
    margin: 0;
}
.card p, .card span, .card a {
    color: #333;
    font-size: 14px;
}
.price {
    color: #2b7cff;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def search_hotels(location, limit=15):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"hotel in {location}",
        "format": "json",
        "extratags": 1,
        "limit": limit
    }
    headers = {"User-Agent": "Hotel-App"}
    return requests.get(url, params=params, headers=headers).json()

def safe_tags(item):
    return item["extratags"] if isinstance(item.get("extratags"), dict) else {}

def get_image(name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": name + " hotel",
        "gsrlimit": 1,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params).json()
        pages = r.get("query", {}).get("pages", {})
        for p in pages.values():
            return p["imageinfo"][0]["url"]
    except:
        pass
    return "https://via.placeholder.com/300x200?text=Hotel+Image"

def ai_price_rating():
    price = random.randint(1500, 5000)
    rating = round(random.uniform(3.0, 4.8), 1)
    stars = int(round(rating))
    available = random.choice([True, True, False])
    return price, rating, stars, available

# ---------------- HEADER ----------------
st.title("🏨 Hotel Finder with Filters")
location = st.text_input("📍 Enter Location")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filter by")

only_available = st.sidebar.checkbox("Only show available")

budget = st.sidebar.slider(
    "Your Budget (per night)",
    1000, 6000, (1500, 5000)
)

st.sidebar.subheader("Star Rating")
star_3 = st.sidebar.checkbox("3 ⭐")
star_4 = st.sidebar.checkbox("4 ⭐")
star_5 = st.sidebar.checkbox("5 ⭐")

selected_stars = []
if star_3: selected_stars.append(3)
if star_4: selected_stars.append(4)
if star_5: selected_stars.append(5)

# ---------------- RESULTS ----------------
if location:
    hotels = search_hotels(location)

    if not hotels:
        st.warning("No hotels found")
    else:
        for h in hotels:
            price, rating, stars, available = ai_price_rating()

            if only_available and not available:
                continue
            if not (budget[0] <= price <= budget[1]):
                continue
            if selected_stars and stars not in selected_stars:
                continue

            tags = safe_tags(h)
            image = get_image(h["display_name"])

            st.markdown(f"""
            <div class="card">
                <img src="{image}">
                <div>
                    <h4>{h['display_name'].split(',')[0]}</h4>
                    <span>⭐ {rating} ({stars}★)</span><br>
                    <span class="price">₹{price} / night</span><br>
                    <span>📞 {tags.get('phone','Not available')}</span><br>
                    <span>🌐 {tags.get('website','Not available')}</span><br>
                    <a href="https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']}" target="_blank">
                        📍 View location
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
