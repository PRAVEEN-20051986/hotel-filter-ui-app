import streamlit as st
from datetime import date

st.set_page_config(page_title="AI Travel Finder", layout="wide")

st.title("🏨 AI Travel Finder")
st.caption("Demo version – No API | UI + Flow Test")

# ---------------- DEMO DATA ----------------

DEMO_HOTELS = [
    {
        "name": "Blue Hills International",
        "location": "Ooty, Tamil Nadu",
        "phone": "+91 98765 43210",
        "website": "https://bluehillsinternational.com",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
        "desc": "Ooty-la irukkura comfortable hotel. Family & couples-ku suitable. Budget + clean rooms."
    },
    {
        "name": "Hill View Residency",
        "location": "Ooty, Tamil Nadu",
        "phone": "+91 91234 56789",
        "website": "https://hillviewresidency.com",
        "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b",
        "desc": "Hill view rooms with peaceful atmosphere. Tourist places-ku near-la irukkum."
    },
    {
        "name": "Lake Side Inn",
        "location": "Ooty, Tamil Nadu",
        "phone": "+91 99887 66554",
        "website": "https://lakesideinn.com",
        "image": "https://images.unsplash.com/photo-1501117716987-c8e1ecb210d1",
        "desc": "Lake view stay. Couples-ku romba popular. Morning view super-aa irukkum."
    }
]

# ---------------- UI FUNCTIONS ----------------

def show_card(hotel):
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:18px;
        border-radius:16px;
        box-shadow:0 6px 16px rgba(0,0,0,0.12);
        margin-bottom:20px;
        display:flex;
        gap:18px;
        align-items:flex-start;
    ">
        <img src="{hotel['image']}" style="
            width:200px;
            height:140px;
            border-radius:14px;
            object-fit:cover;
        ">
        <div style="color:#111">
            <h3 style="margin:0">{hotel['name']}</h3>
            <p style="margin:4px 0;color:#555">{hotel['location']}</p>
            <p>{hotel['desc']}</p>
            📞 {hotel['phone']}<br>
            🌐 <a href="{hotel['website']}" target="_blank">{hotel['website']}</a><br><br>
            <button style="
                padding:8px 16px;
                background:#ff4b4b;
                color:#fff;
                border:none;
                border-radius:8px;
                cursor:pointer;
            ">Book Now</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SEARCH BAR ----------------

location = st.text_input("📍 Enter location or hotel name (eg: Ooty, Blue Hills)")

col1, col2 = st.columns(2)
with col1:
    check_in = st.date_input("Check-in", min_value=date.today())
with col2:
    check_out = st.date_input("Check-out", min_value=check_in)

tabs = st.tabs(["🏨 Room Stays", "🚗 Car Rentals", "🏍️ Bike Rentals"])

# ---------------- ROOM STAYS ----------------
with tabs[0]:
    if location:
        st.subheader("Available Room Stays")
        for h in DEMO_HOTELS:
            show_card(h)
    else:
        st.info("👆 Location enter panninaa room stays kaattum")

# ---------------- CAR RENTALS ----------------
with tabs[1]:
    if location:
        st.success("🚗 Car rentals coming soon (Demo)")
        show_card({
            "name": "Ooty Car Rentals",
            "location": "Ooty",
            "phone": "+91 90000 11111",
            "website": "https://ootycars.com",
            "image": "https://images.unsplash.com/photo-1549924231-f129b911e442",
            "desc": "Innova, Swift, Etios available. Driver option irukku."
        })

# ---------------- BIKE RENTALS ----------------
with tabs[2]:
    if location:
        st.success("🏍️ Bike rentals coming soon (Demo)")
        show_card({
            "name": "Hill Ride Bikes",
            "location": "Ooty",
            "phone": "+91
