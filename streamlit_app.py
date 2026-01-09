import streamlit as st
import requests

st.set_page_config(page_title="Location Travel Directory", layout="wide")

st.title("🌍 Location Travel Directory")

# ---------------- FUNCTIONS ----------------

def search_places(query, limit=20):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "extratags": 1,
        "limit": limit
    }
    headers = {"User-Agent": "Location-Travel-App"}
    return requests.get(url, params=params, headers=headers).json()

def safe_tags(item):
    return item["extratags"] if isinstance(item.get("extratags"), dict) else {}

def get_image(name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": name,
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
    return "https://via.placeholder.com/300x200?text=No+Image"

def show_card(title, phone, website, map_link, image):
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:14px;
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.1);
        margin-bottom:18px;
        display:flex;
        gap:16px;
    ">
        <img src="{image}" style="width:160px;height:120px;border-radius:10px;object-fit:cover;">
        <div style="color:#111">
            <h4>{title}</h4>
            📞 {phone}<br>
            🌐 {website}<br>
            📍 <a href="{map_link}" target="_blank">View location</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- USER INPUT ----------------

location = st.text_input("📍 Enter Location")

tabs = st.tabs(["🏨 Room Stays", "🚗 Car Rentals", "🏍️ Bike Rentals"])

# ---------------- ROOM STAYS ----------------
with tabs[0]:
    if location:
        hotels = search_places(f"hotel in {location}")
        for h in hotels:
            tags = safe_tags(h)
            show_card(
                title=h["display_name"].split(",")[0],
                phone=tags.get("phone", "Not available"),
                website=tags.get("website", "Not available"),
                map_link=f"https://www.openstreetmap.org/{h['osm_type']}/{h['osm_id']}",
                image=get_image(h["display_name"])
            )

# ---------------- CAR RENTALS ----------------
with tabs[1]:
    if location:
        cars = search_places(f"car rental in {location}")
        for c in cars:
            tags = safe_tags(c)
            show_card(
                title=c["display_name"].split(",")[0],
                phone=tags.get("phone", "Not available"),
                website=tags.get("website", "Not available"),
                map_link=f"https://www.openstreetmap.org/{c['osm_type']}/{c['osm_id']}",
                image=get_image(c["display_name"])
            )

# ---------------- BIKE RENTALS ----------------
with tabs[2]:
    if location:
        bikes = search_places(f"bike rental in {location}")
        for b in bikes:
            tags = safe_tags(b)
            show_card(
                title=b["display_name"].split(",")[0],
                phone=tags.get("phone", "Not available"),
                website=tags.get("website", "Not available"),
                map_link=f"https://www.openstreetmap.org/{b['osm_type']}/{b['osm_id']}",
                image=get_image(b["display_name"])
            )
