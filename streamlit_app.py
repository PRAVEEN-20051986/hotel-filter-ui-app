import streamlit as st
import requests
from openai import OpenAI
from datetime import date

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Travel Finder", layout="wide")
st.title("🏨 AI Travel Finder")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- FUNCTIONS ----------------

def ai_fix_query(text):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": f"Correct hotel or place name: {text}"}
        ]
    )
    return res.choices[0].message.content.strip()

def ai_description(place):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Describe {place} in simple Tamil + English mix for travel app"
            }
        ]
    )
    return res.choices[0].message.content

def google_places_search(query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }
    return requests.get(url, params=params).json()

def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,website",
        "key": GOOGLE_API_KEY
    }
    return requests.get(url, params=params).json()

def get_photo(photo_ref):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_ref}&key={GOOGLE_API_KEY}"

def show_card(name, image, phone, website, desc):
    st.markdown(f"""
    <div style="background:#fff;padding:16px;border-radius:14px;
    box-shadow:0 6px 14px rgba(0,0,0,.1);margin-bottom:20px;display:flex;gap:16px">
        <img src="{image}" style="width:180px;height:130px;border-radius:12px;object-fit:cover">
        <div>
            <h4>{name}</h4>
            <p>{desc}</p>
            📞 {phone}<br>
            🌐 <a href="{website}" target="_blank">{website}</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- INPUT ----------------

location = st.text_input("📍 Enter location or hotel name")

col1, col2 = st.columns(2)
with col1:
    check_in = st.date_input("Check-in", min_value=date.today())
with col2:
    check_out = st.date_input("Check-out", min_value=check_in)

# ---------------- MAIN LOGIC ----------------

if location:
    with st.spinner("AI thinking..."):
        fixed_query = ai_fix_query(location)

    st.success(f"🔍 Showing results for: {fixed_query}")

    data = google_places_search(f"hotel in {fixed_query}")

    if "results" in data:
        for h in data["results"][:5]:
            name = h["name"]
            photo = get_photo(h["photos"][0]["photo_reference"]) if "photos" in h else "https://via.placeholder.com/300"
            place_id = h["place_id"]

            details = get_place_details(place_id)
            phone = details.get("result", {}).get("formatted_phone_number", "Not available")
            website = details.get("result", {}).get("website", "Not available")

            desc = ai_description(name)

            show_card(name, photo, phone, website, desc)
