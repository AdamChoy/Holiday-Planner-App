import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta
from PIL import Image

st.set_page_config(
    page_title="Holiday Planner",
    page_icon="🏖️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    background-color: #F5F0D8 !important;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
}

/* Sidebar stays dark */
section[data-testid="stSidebar"] {
    background-color: #1a1a1a !important;
}

/* Sidebar text stays cream */
section[data-testid="stSidebar"] * {
    color: #F5F0D8 !important;
}

/* Input boxes (date, number, text) */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #FFFFFF    !important;
    color: #1a1a1a !important;
    border-radius: 10px !important;
    border: none !important;
}

/* Selectbox + multiselect */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #F5F0D8 !important;
    color: #1a1a1a !important;
    border-radius: 10px !important;
}

/* Date picker box */
section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background-color: #F5F0D8 !important;
    border-radius: 10px !important;
}

/* Fix dropdown menu items */
section[data-testid="stSidebar"] ul {
    background-color: #F5F0D8 !important;
}
section[data-testid="stSidebar"] li {
    color: #1a1a1a !important;
}

.hp-hero {
    background: #F5F0D8;
    padding: 3rem 3rem 0;
}
.hp-logo {
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #1a1a1a;
    opacity: 0.45;
    margin-bottom: 1.5rem;
}
.hp-logo strong {
    display: inline-block;
    background: #1a1a1a;
    color: #F5F0D8 !important;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    margin-right: 6px;
}
.hp-headline {
    font-family: 'DM Serif Display', serif;
    font-size: 3.8rem;
    line-height: 1.05;
    color: #1a1a1a;
    margin: 0 0 0.8rem;
}
.hp-sub {
    font-size: 0.95rem;
    color: #1a1a1a;
    opacity: 0.95;
    font-weight: 300;
    margin-bottom: 2rem;
    line-height: 1.6;
}
.hp-stripes { display: flex; flex-direction: column; width: 100%; }
.hp-stripe  { height: 20px; width: 100%; }

.hp-section { background: #F5F0D8; padding: 2.5rem 3rem; }
.hp-section-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #1a1a1a;
    opacity: 0.38;
    margin-bottom: 6px;
}
.hp-section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #1a1a1a;
    margin: 0 0 1.5rem;
}

.hp-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 14px;
    margin-bottom: 1.5rem;
}
.hp-card {
    background: #1a1a1a;
    border-radius: 12px;
    padding: 1.4rem;
}
.hp-card-tag  { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: #F5F0D8; opacity: 0.35; margin-bottom: 6px; }
.hp-card-name { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: #F5F0D8; margin: 0 0 3px; }
.hp-card-desc { font-size: 12px; color: #F5F0D8; opacity: 0.4; margin: 0 0 12px; line-height: 1.5; }
.hp-card-score {
    display: inline-block;
    background: #F5C800;
    color: #1a1a1a;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    margin-bottom: 10px;
}
.hp-card-meta { font-size: 11px; color: #F5F0D8; opacity: 0.5; line-height: 2; }
.hp-tag-pill  {
    display: inline-block;
    border: 1px solid rgba(245,240,216,0.18);
    border-radius: 20px;
    padding: 2px 8px;
    font-size: 10px;
    margin: 4px 3px 0 0;
    color: #F5F0D8;
    opacity: 0.45;
}
.hp-empty {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1a1a1a;
    opacity: 0.28;
    padding: 2rem 0;
    text-align: center;
}
.hp-col-pad-l { padding: 2rem 1rem 1rem 3rem; }
.hp-col-pad-r { padding: 2rem 3rem 1rem 1rem; }
.hp-footer {
    background: #F5F0D8;
    padding: 1.2rem 3rem;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid rgba(26,26,26,0.08);
    font-size: 11px;
    color: rgba(26,26,26,0.45);
}

.hp-date-banner {
    background: #1a1a1a;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.hp-date-item { display: flex; flex-direction: column; gap: 2px; }
.hp-date-label { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: #F5F0D8; opacity: 0.35; }
.hp-date-value { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: #F5F0D8; }
.hp-date-divider { color: #F5C800; font-size: 1.2rem; opacity: 0.6; }
.hp-date-nights {
    margin-left: auto;
    background: #F5C800;
    color: #1a1a1a;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 500;
}
.hp-date-error {
    background: #B41800;
    color: #F5F0D8;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 12px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


STRIPES_HTML = """
<div class="hp-stripes">
  <div class="hp-stripe" style="background:#F5C800;"></div>
  <div class="hp-stripe" style="background:#F0A800;"></div>
  <div class="hp-stripe" style="background:#E88000;"></div>
  <div class="hp-stripe" style="background:#E05800;"></div>
  <div class="hp-stripe" style="background:#CC3000;"></div>
  <div class="hp-stripe" style="background:#B41800;"></div>
</div>
"""

PIXEL_SVG = """
<svg width="80" height="64" viewBox="0 0 80 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- nose -->
  <rect x="64" y="24" width="8" height="8" fill="#1a1a1a"/>
  <!-- fuselage -->
  <rect x="48" y="24" width="8" height="8" fill="#1a1a1a"/>
  <rect x="40" y="24" width="8" height="8" fill="#1a1a1a"/>
  <rect x="32" y="24" width="8" height="8" fill="#1a1a1a"/>
  <rect x="24" y="24" width="8" height="8" fill="#1a1a1a"/>
  <rect x="16" y="24" width="8" height="8" fill="#1a1a1a"/>
  <!-- main wing top -->
  <rect x="32" y="16" width="8" height="8" fill="#1a1a1a"/>
  <rect x="24" y="8"  width="8" height="8" fill="#1a1a1a"/>
  <!-- main wing bottom -->
  <rect x="32" y="32" width="8" height="8" fill="#1a1a1a"/>
  <rect x="24" y="40" width="8" height="8" fill="#1a1a1a"/>
  <!-- tail fin top -->
  <rect x="8"  y="16" width="8" height="8" fill="#1a1a1a"/>
  <!-- tail fin bottom -->
  <rect x="8"  y="32" width="8" height="8" fill="#1a1a1a"/>
  <!-- engine under wing -->
  <rect x="24" y="32" width="8" height="8" fill="#1a1a1a"/>
</svg>
"""

DESTINATIONS = [
    {
        "name": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393,
        "temp": 27, "humidity": 60, "cloudiness": 20, "wind": 4.5,
        "hotel_avg": 95, "flight_gbp": 120, "nightlife_rating": 4.6, "restaurants": 950,
        "tags": ["Beach", "City nightlife", "Culture"],
        "desc": "Sunny coastal capital with rooftop bars, trams, and amazing food.",
        "score": 91,
    },
    {
        "name": "Barcelona", "country": "Spain", "lat": 41.3851, "lon": 2.1734,
        "temp": 29, "humidity": 65, "cloudiness": 25, "wind": 3.8,
        "hotel_avg": 130, "flight_gbp": 140, "nightlife_rating": 4.8, "restaurants": 1500,
        "tags": ["Beach", "City nightlife", "Culture"],
        "desc": "Beach city energy, late nights, incredible architecture, and tapas.",
        "score": 93,
    },
    {
        "name": "Split", "country": "Croatia", "lat": 43.5081, "lon": 16.4402,
        "temp": 30, "humidity": 58, "cloudiness": 15, "wind": 4.2,
        "hotel_avg": 110, "flight_gbp": 160, "nightlife_rating": 4.4, "restaurants": 420,
        "tags": ["Beach", "Culture"],
        "desc": "Adriatic coastline, island hopping, and buzzing summer nightlife.",
        "score": 88,
    },
    {
        "name": "Mykonos", "country": "Greece", "lat": 37.4467, "lon": 25.3289,
        "temp": 31, "humidity": 55, "cloudiness": 10, "wind": 6.0,
        "hotel_avg": 180, "flight_gbp": 190, "nightlife_rating": 4.9, "restaurants": 260,
        "tags": ["Beach", "Island", "City nightlife"],
        "desc": "Iconic Greek island with beach clubs, sunsets, and whitewashed streets.",
        "score": 90,
    },
    {
        "name": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402,
        "temp": 28, "humidity": 62, "cloudiness": 30, "wind": 3.0,
        "hotel_avg": 75, "flight_gbp": 110, "nightlife_rating": 4.7, "restaurants": 800,
        "tags": ["City nightlife", "Culture"],
        "desc": "Cheap eats, ruin bars, thermal baths, and big city vibes.",
        "score": 89,
    },
    {
        "name": "Nice", "country": "France", "lat": 43.7102, "lon": 7.2620,
        "temp": 27, "humidity": 63, "cloudiness": 20, "wind": 3.6,
        "hotel_avg": 150, "flight_gbp": 160, "nightlife_rating": 4.2, "restaurants": 650,
        "tags": ["Beach", "Culture"],
        "desc": "French Riviera beaches, pastel old town, and relaxed luxury vibes.",
        "score": 85,
    },
    {
        "name": "Ibiza", "country": "Spain", "lat": 38.9067, "lon": 1.4206,
        "temp": 30, "humidity": 60, "cloudiness": 10, "wind": 5.2,
        "hotel_avg": 170, "flight_gbp": 180, "nightlife_rating": 5.0, "restaurants": 520,
        "tags": ["Beach", "Island", "City nightlife"],
        "desc": "The nightlife capital of Europe — beach clubs, DJs, and sunsets.",
        "score": 94,
    },
    {
        "name": "Amalfi", "country": "Italy", "lat": 40.6340, "lon": 14.6027,
        "temp": 29, "humidity": 64, "cloudiness": 15, "wind": 3.4,
        "hotel_avg": 190, "flight_gbp": 170, "nightlife_rating": 3.9, "restaurants": 240,
        "tags": ["Beach", "Culture"],
        "desc": "Italian coastlines, lemon spritz, cliffs, and postcard views.",
        "score": 84,
    },
]

# FIX: Map sidebar vibe labels to destination tag values
VIBE_TAG_MAP = {
    "Beach": "Beach",
    "City": "City nightlife",
    "Mountain": "Mountain",
    "Island": "Island",
}

def filter_destinations(dests, temp_range, max_humidity, max_budget, vibe):
    # FIX: Map vibe selections to actual tag values used in destinations
    mapped_vibes = [VIBE_TAG_MAP.get(v, v) for v in vibe] if vibe else []
    results = []
    for d in dests:
        if not (temp_range[0] <= d["temp"] <= temp_range[1]):
            continue
        if d["humidity"] > max_humidity:
            continue
        if d["hotel_avg"] > max_budget:
            continue
        if mapped_vibes and not any(v in d["tags"] for v in mapped_vibes):
            continue
        results.append(d)
    return sorted(results, key=lambda x: x["score"], reverse=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:0.4;'>Your preferences</p>", unsafe_allow_html=True)

    # Travel dates
    st.markdown("Departure date")
    depart_date = st.date_input(
        "depart",
        value=date.today(),# + timedelta(weeks=4),
        min_value=date.today(),
        max_value=date.today() + timedelta(days=365),
        label_visibility="collapsed",
    )

    st.markdown("Return date")
    return_date = st.date_input(
        "return",
        value=date.today() + timedelta(weeks=1),
        min_value=date.today() + timedelta(days=1),
        max_value=date.today() + timedelta(days=366),
        label_visibility="collapsed",
    )

    # Validate dates
    dates_valid = return_date > depart_date
    if not dates_valid:
        st.markdown("<p style='color:#F5C800;font-size:12px;margin-top:4px;'>Return must be after departure.</p>", unsafe_allow_html=True)
    else:
        num_nights = (return_date - depart_date).days
        st.markdown(f"<p style='color:#F5F0D8;font-size:12px;opacity:0.5;margin-top:4px;'>You are staying for: {num_nights} night{'s' if num_nights != 1 else ''}</p>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Max budget (£)
    st.markdown("Max budget (£)")
    max_budget = st.slider("bud", 100, 5000, 1000, label_visibility="collapsed")

    # ── Travel party ─────────────────────────────────────────────
    st.markdown("Number of people")
    num_people = st.number_input(
        "people",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        label_visibility="collapsed",
    )

    st.markdown("Closest airport")
    closest_airport = st.selectbox(
        "airport",
        [
            "London Heathrow (LHR)",
            "London Gatwick (LGW)",
            "London Stansted (STN)",
            "London Luton (LTN)",
            "London City (LCY)",
        ],
        label_visibility="collapsed",
    )

    st.markdown("Temperature range (°C)")
    # FIX: Default tuple values must be within the slider's min/max range (20–40)
    temp_range = st.slider("temp", 20, 40, (20, 35), label_visibility="collapsed")

    # FIX: Added max_humidity slider so it can be passed to filter_destinations
    st.markdown("Max humidity (%)")
    max_humidity = st.slider("humidity", 0, 100, 100, label_visibility="collapsed")

    st.markdown("Type of Holiday")
    vibe = st.multiselect(
        "vibe",
        ["Beach", "City", "Mountain", "Island"],
        default=["Beach"],
        label_visibility="collapsed",
    )
    st.button("Find destinations")


# FIX: Pass all required arguments to filter_destinations
filtered = filter_destinations(DESTINATIONS, temp_range, max_humidity, max_budget, vibe)
num_nights = (return_date - depart_date).days if dates_valid else 0


# ── Hero ──────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 1])
with left:
    st.markdown(f"""
    <div class="hp-hero">
        <div class="hp-headline">Find your next holiday</div>
        <div class="hp-sub"><strong>Travel <i>anywhere</i> in Europe</strong><br>Trips that fit your wallet, the forecast, and your peace of mind.</div>
    </div>
    """, unsafe_allow_html=True)
# with right:
#     st.markdown(f"""
#     <div style="display:flex;align-items:flex-end;justify-content:flex-end;
#                 padding:2.5rem 2rem 0 0;height:100%;">
#         {PIXEL_SVG}
#     </div>
#     """, unsafe_allow_html=True)

st.markdown(STRIPES_HTML, unsafe_allow_html=True)


# ── Destination cards ─────────────────────────────────────────────────────────
# st.markdown(f"""
# <div class="hp-section">
#     <div class="hp-section-label">Top picks — {len(filtered)} found</div>
#     <div class="hp-section-title">Adventure. Sun. Nightlife.</div>
# """, unsafe_allow_html=True)

# Date summary banner
st.markdown("""
<div style="padding-top: 2rem;">
""", unsafe_allow_html=True)
if not dates_valid:
    st.markdown('<div class="hp-date-error">Please set a valid return date before searching.</div>', unsafe_allow_html=True)
elif num_nights > 0:
    airport_short = closest_airport.split("(")[-1].replace(")", "")
    st.markdown(f"""
    <div class="hp-date-banner">
        <div class="hp-date-item">
            <span class="hp-date-label">Departure</span>
            <span class="hp-date-value">{depart_date.strftime("%d %b %Y")}</span>
        </div>
        <span class="hp-date-divider">→</span>
        <div class="hp-date-item">
            <span class="hp-date-label">Return</span>
            <span class="hp-date-value">{return_date.strftime("%d %b %Y")}</span>
        </div>
        <div class="hp-date-item">
            <span class="hp-date-label">From</span>
            <span class="hp-date-value">{airport_short}</span>
        </div>
        <div class="hp-date-item">
            <span class="hp-date-label">Travellers</span>
            <span class="hp-date-value">{num_people} {"person" if num_people == 1 else "people"}</span>
        </div>
        <span class="hp-date-nights">{num_nights} night{"s" if num_nights != 1 else ""}</span>
    </div>
    """, unsafe_allow_html=True)
# ── Map ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hp-section">
    <div class="hp-section-title">Based on your preferences, here are your top destinations</div>
</div>
""", unsafe_allow_html=True)

if filtered:
    m = folium.Map(
        location=[54.5260, 15.2551],  # Europe centre
        zoom_start=4,
        tiles="CartoDB positron"
    )

    for d in filtered:
        folium.CircleMarker(
            location=[d["lat"], d["lon"]],
            radius=10 + d["score"] // 20,
            color="#B41800",
            fill=True,
            fill_color="#F5C800",
            fill_opacity=0.85,
            popup=folium.Popup(
                f"<b>{d['name']}, {d['country']}</b><br>🌡 {d['temp']}°C · 🏨 £{d['hotel_avg']}/night<br>Score: <b>{d['score']}/100</b>",
                max_width=250
            ),
            tooltip=f"{d['name']} — {d['score']}/100",
        ).add_to(m)

    st_folium(m, width=1400, height=500)

else:
    st.markdown("<div class='hp-empty'>Adjust filters to see the map.</div>", unsafe_allow_html=True)


# Destination cards
if not filtered:
    st.warning("No destinations match your filters. Try widening your preferences.")
else:
    # Use columns to create a grid layout (3 cards per row)
    cols = st.columns(3)
    
    for i, d in enumerate(filtered):
        # Calculate costs for the required cost analysis 
        total_hotel = d["hotel_avg"] * num_nights if num_nights > 0 else 0
        total_cost = (d["flight_gbp"] * 2 + total_hotel)
        
        # Determine which column to place the card in
        with cols[i % 3]:
            with st.container(border=True):
                # Header Section
                st.subheader(f"{d['name']}, {d['country']}")
                st.caption(d['desc'])
                
                # Metrics Row (Weather & Ratings) 
                m1, m2 = st.columns(2)
                m1.metric("Temperature", f"{d['temp']}°C")
                m2.metric("Nightlife", f"{d['nightlife_rating']}/5")
                
                # Detailed Cost Analysis 
                with st.expander("View Details"):
                    st.write(f"🏨 Hotel: £{d['hotel_avg']}/night")
                    st.write(f"✈ Flight: £{d['flight_gbp']} return")
                    st.divider()
                    st.write(f"**Total Est: £{total_cost:,}**")
                
                # Tags [cite: 4]
                st.write(" ".join([f"`{t}`" for t in d["tags"]]))
                



# ── Chart (below map) ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hp-section">
    <div class="hp-section-label">Cost breakdown</div>
    <div class="hp-section-title">Flights vs hotels</div>
</div>
""", unsafe_allow_html=True)

if filtered:
    df = pd.DataFrame([{
        "Destination": d["name"],
        "Hotel £/night": d["hotel_avg"],
        "Flight £ return": d["flight_gbp"],
    } for d in filtered])

    st.bar_chart(df.set_index("Destination"))

    if num_nights > 0:
        st.markdown(f"""
        <div style="padding:0 3rem 1rem 3rem;">
            <p style="font-size:11px;color:#1a1a1a;opacity:0.4;margin-top:0.5rem;">
                Hotel totals calculated over {num_nights} night{"s" if num_nights != 1 else ""} 
                ({depart_date.strftime("%d %b")} – {return_date.strftime("%d %b %Y")})
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("<div class='hp-empty'>No data.</div>", unsafe_allow_html=True)

# ── Weather table ─────────────────────────────────────────────────────────────
if filtered:
    st.markdown(STRIPES_HTML, unsafe_allow_html=True)
    st.markdown("""
    <div class="hp-section">
        <div class="hp-section-label">Full breakdown</div>
        <div class="hp-section-title">Weather &amp; data</div>
    </div>
    """, unsafe_allow_html=True)

    rows = []
    for d in filtered:
        row = {
            "Destination": f"{d['name']}, {d['country']}",
            "Temp °C": d["temp"],
            "Cloud %": d["cloudiness"],
            "Wind m/s": d["wind"],
            "Nightlife": d["nightlife_rating"],
            "Score": d["score"],
        }
        if num_nights > 0:
            row["Hotel total £"] = d["hotel_avg"] * num_nights
            row["Est. trip total £"] = d["flight_gbp"] * 2 + d["hotel_avg"] * num_nights
        rows.append(row)

    weather_df = pd.DataFrame(rows)
    st.dataframe(weather_df, use_container_width=True, hide_index=True)


# ── Footer ────────────────────────────────────────────────────────────────────
LINKEDIN_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="#000000" viewBox="0 0 24 24"><path d="M22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.72V1.72C24 .77 23.21 0 22.23 0zM7.06 20.45H3.56V9h3.5v11.45zM5.31 7.43c-1.12 0-2.03-.92-2.03-2.05 0-1.13.91-2.05 2.03-2.05 1.12 0 2.03.92 2.03 2.05 0 1.13-.91 2.05-2.03 2.05zM20.45 20.45h-3.5v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.44-2.13 2.94v5.67h-3.5V9h3.36v1.56h.05c.47-.89 1.62-1.85 3.34-1.85 3.57 0 4.23 2.35 4.23 5.41v6.33z"/></svg>'

import base64
with open("frontend/assets/plane_pixel_art2.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
FOOTER_CONTENT = f"""
<div class="hp-footer" style="display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;color:#000000 !important;">
    <div style="line-height:1.6; color:#000000 !important;">
        <div style="color:#000000 !important;">Rockborne Holiday Planner App © 2026</div>
        <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap; margin-top:4px;">
            <a href="https://www.linkedin.com/in/adam-choy-b95715190/" target="_blank"
               style="color:#000000 !important; text-decoration:none; display:flex; align-items:center; gap:6px;">
                {LINKEDIN_ICON} Adam Choy
            </a>
            <a href="https://www.linkedin.com/in/kanmani-vijay-8451a322b/" target="_blank"
               style="color:#000000 !important; text-decoration:none; display:flex; align-items:center; gap:6px;">
                {LINKEDIN_ICON} Kanmani Vijay
            </a>
        </div>
    </div>
    <div style="display:flex;align-items:center;justify-content:center;">
        <img src="data:image/png;base64,{img_b64}"
             width="64"
             style="image-rendering:pixelated; image-rendering:crisp-edges;">
    </div>
    <div style="color:#000000 !important;">
        OpenWeatherMap · Google Places · Streamlit
    </div>
</div>
"""

st.markdown(STRIPES_HTML, unsafe_allow_html=True)
st.markdown(FOOTER_CONTENT, unsafe_allow_html=True)