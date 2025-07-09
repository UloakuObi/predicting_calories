# This is for building the frontend of the Streamlit app
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
from load_predict import predict_calories
from streamlit_extras.card import card
from streamlit_extras.stylable_container import stylable_container


# --- PAGE CONFIG ---
st.set_page_config(page_title="Calorie Burn Estimator", layout="wide")

# --- Force light mode visually with custom CSS ---
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: white !important;
            color: black !important;
        }

        [data-testid="stSidebar"] {
            background-color: #f8f8f8 !important;
        }
            
         /* Make input boxes white with black text */
        input, select, textarea {
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
        }

        /* Adjust Streamlit's styled input containers */
        [data-baseweb="input"] {
            background-color: white !important;
        }

        /* Adjust dropdowns and slider text color */
        .stSelectbox div, .stNumberInput div {
            background-color: white !important;
            color: black !important;
        }

        h1, h2, h3, h4, h5, h6, p, span, div {
            color: black !important;
        }

        .stButton > button {
            background-color: #6ec071 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Compact layout settings ---
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        html, body, [data-testid="stAppViewContainer"] {
            height: 100vh;
            overflow: hidden;
        }

        [data-testid="stVerticalBlock"] {
            max-height: 100vh;
            overflow-y: auto;
        }

        h1, h2, h3 {
            margin-bottom: 0.3rem;
        }

        .stButton > button {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)
##---
# --- Custom CSS for button styling ---
st.markdown("""
    <style>
        button[kind="secondary"] {
            padding: 0.5em 1.5em;
            font-size: 1.1em;
            border-radius: 8px;
            background-color: #6ec071;
            color: white;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)



# --- HEADER ROW ---
st.markdown("## 🔥 Calorie Burn Estimator")
st.markdown(
    "<p style='font-size:20px; font-weight:400; color:#555;'>Estimate calories burned based on your workout details</p>",
    unsafe_allow_html=True
)


# --- MAIN CONTENT AREA: Two Columns ---
left_col, right_col = st.columns([2, 1])

# --- LEFT COLUMN: Inputs and Prediction ---
with left_col:
    # --- INPUT CARD ---
    with stylable_container(
            key="input_card",
            css_styles="""
                {
                    background-color: #f8f8f8;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
                    margin-bottom: 0.3rem;
                }
            """,
    ):
        #st.markdown("### 🔧 Input Features")
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("👤Age", min_value=18, max_value=80, step=1)
            weight = st.number_input("⚖️Weight (kg)", min_value=30.0, max_value=140.0, step=0.5)
            height = st.number_input("⬆️Height (cm)", min_value=120.0, max_value=250.0, step=0.5)
        with col2:
            gender = st.selectbox("♀♂ Gender", ["Male", "Female"])
            heart_rate = st.number_input("❤️Heart Rate (bpm)", min_value=60, max_value=130, step=1)
            duration = st.number_input("🏃Duration (min)", min_value=1, max_value=30, step=1)

        # Add spacing to separate from last row
        st.markdown("")

        # --- Centered Predict Button ---
        col_a, col_b, col_c = st.columns([1, 1, 1])

        with col_b:
            # Streamlit button with inline custom style
            predict_clicked = st.button(
            "Predict Calories Burned"
            )

        # Create a dictionary to hold input features
        input_features = {
            "age": age,
            "weight": weight,
            "height": height,
            "duration": duration,
            "gender": gender,    # male or female
            "heart_rate": heart_rate
            }


    # --- PREDICTION CARD ---
    with stylable_container(
        key="prediction_card",
        css_styles="""
            {
                background-color: #f8f8f8;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
        """,
    ):
        #st.markdown("#### 🎯 Prediction")
        # --- PREDICTION LOGIC ---
        if predict_clicked:
            prediction = predict_calories(input_features)
            st.success(f"🔥 Estimated Calories Burned: **{round(prediction, 2)} kcal**")
    


# --- RIGHT COLUMN: Running Boy Image ---
with right_col:
    with stylable_container(
            key="image_card",
            css_styles="""
                    {
                        background-color: #f8f8f8;
                        padding: 20px;
                        border-radius: 10px;
                        #box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                        height: 450px;  /* You can adjust this value */
                        display: flex;
                        justify-content: center;
                        align-items: flex-start;
                    }
                """,
    ):
        # Move the image a little higher
        st.markdown("<div style='margin-top: -10px'></div>", unsafe_allow_html=True)
        
        # Get current directory and full path
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, "running_boy_no_background.png")
        # Load and display the image
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


