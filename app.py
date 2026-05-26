# app.py
import streamlit as st
import joblib
import os
import glob
import base64 # <-- NEW: We need this to encode the video
from scraper import get_live_weather

st.set_page_config(page_title="Pan-India Airport AI", page_icon="🇮🇳", layout="centered")

# --- THE UPGRADED MP4 VIDEO INJECTOR ---

# 1. We tell Streamlit to memorize this 5MB file so it doesn't cause lag!
@st.cache_data
def load_video(video_path):
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    return base64.b64encode(video_bytes).decode()

def set_video_background(video_file_path):
    """
    Reads an MP4, caches it for speed, and forces Streamlit to be transparent.
    """
    try:
        encoded_video = load_video(video_file_path)

 # 2. We add !important to force ALL Streamlit layers to be transparent
        video_html = f"""
        <style>
        #bg-video {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100vw;
            min-height: 100vh;
            z-index: -1; 
            object-fit: cover;
            filter: brightness(40%); 
        }}
        
        /* 🚨 THE FIX: Force the absolute main wrapper to be transparent! */
        [data-testid="stApp"] {{
            background: transparent !important;
        }}
        
        /* Force transparency on the inner containers */
        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        /* Keep text readable against the video */
        .stMarkdown, .stText, h1, h2, h3, p, label {{
            text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
        }}
        </style>
        
        <video id="bg-video" autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error(f"🚨 Cannot find the video file: {video_file_path}")

# --- Activate the Video ---
set_video_background("airport_bg.mp4")
# --- The rest of your app stays exactly the same! ---
st.title("🇮🇳 Pan-India Airport Weather AI")
st.write("Live data fetched via Aviation API, predicted by localized AI models.")

# (Keep your master dictionary and all the logic below here...)
# --- 1. THE MASTER DICTIONARY ---
airport_dict = {
    "VABB": "Chhatrapati Shivaji Maharaj Int'l (Mumbai)",
    "VIDP": "Indira Gandhi Int'l (New Delhi)",
    "VOBL": "Kempegowda Int'l (Bangalore)",
    "VOSH": "Rajiv Gandhi Int'l (Hyderabad)",
    "VEBS": "Biju Patnaik Int'l (Bhubaneswar)",
    "VISR": "Sheikh ul-Alam Int'l (Srinagar)",
    "VOPB": "Veer Savarkar Int'l (Port Blair)",
    "VOML": "Mangaluru Int'l (Mangalore)",
    "VIDN": "Jolly Grant Airport (Dehradun)",
    "VISM": "Shimla Airport",
    "VOPC": "Puducherry Airport",
    "VAJJ": "Juhu Aerodrome (Mumbai)",
    "VIDD": "Safdarjung Airport (New Delhi)",
    "VISP": "Sarsawa Air Force Station",
    "VORM": "INS Parundu (Ramanathapuram)",
    "VODX": "INS Kohassa (Shibpur)",
    "VOBX": "INS Baaz (Campbell Bay)",
    "VOJV": "Jindal Vijayanagar Airport (Bellary)"
}

# --- 2. AUTO-DETECT TRAINED MODELS ---
model_files = glob.glob("model_*.pkl")
available_codes = sorted([file.replace("model_", "").replace(".pkl", "") for file in model_files])

if not available_codes:
    st.error("No AI Models found! Please run train_model.py first.")
else:
    # --- 3. DYNAMIC TRANSLATION ---
    # Create a list of full names for the UI, but keep the 4-letter code attached for the backend
    ui_options = {code: f"{airport_dict.get(code, 'Unknown Airport')} [{code}]" for code in available_codes}
    
    # The user sees the beautiful full name...
    selected_name = st.selectbox("Select a Supported Airport:", list(ui_options.values()))
    
    # ...but Python secretly extracts just the 4-letter code (like 'VABB') to run the AI!
    airport_code = [code for code, name in ui_options.items() if name == selected_name][0]

    if st.button(f"Generate Forecast for {airport_code}"):
        with st.spinner(f"Fetching live data from {airport_code} sensors..."):
            
            # Fetch Live Data
            live_data_df = get_live_weather(airport_code)
            
            if live_data_df is not None:
                st.success(f"Live data secured for {airport_code}!")
                
                # Show current conditions
                st.subheader("Current Live Conditions")
                st.dataframe(live_data_df, hide_index=True)
                
                # Load the specific model for this city
                model_path = f"model_{airport_code}.pkl"
                model = joblib.load(model_path)
                
                # Make the AI Prediction
                prediction = model.predict(live_data_df)[0]
                
                # Display beautifully
                st.divider()
                st.subheader(f"🤖 AI Forecast (T+2 Hours)")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Predicted Temperature", value=f"{prediction:.1f} °C", delta="In 2 Hrs")
                with col2:
                    st.info(f"Model: {airport_code} Local AI")
                
            else:
                st.error("Failed to fetch live data from the aviation servers. Try again.")