# --- import necessary files ---
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

# --- Load Model ---
with open("best_model.pkl", "rb") as file:
    model = pickle.load(file)
    
# --- Page Config ---
st.set_page_config(page_title="Medical Insurance Premium Predictor", layout="wide")


# --- Custom CSS Styling ---
st.markdown("""
    <style>
     [data-testid="stAppViewContainer"] {
        background-color: #cce6ff !important;
    }
    .reportview-container .main .block-container {
        background-image: linear-gradient(to bottom right, #ffffff, #e6f0ff);
        padding: 2rem;
        border-radius: 10px;
    }
    header {
        background-size: cover;
        color: white;
    }
    .css-1d391kg, .css-1avcm0n {
        background-size: cover;
        color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 47, 95, 0.9) !important;
        color: white;
        border-radius: 10px;
        padding: 20px;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    .card {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        text-align: center;
        width: 250px;
    }
    .card-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        margin-top: 20px;
    }
    .prediction-section {
        background-size: cover;
        background-repeat: no-repeat;
        padding: 30px;
        border-radius: 15px;
        position: relative;
    }
    .prediction-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 50%;
        background: linear-gradient(rgba(0, 123, 255, 0.25), rgba(255, 255, 255, 0.8));
        border-radius: 15px;
        z-index: 0;
    }
    .prediction-section * {
        position: relative;
        z-index: 1;
    }
    /* Form box styling */
    div[data-testid="stForm"] {
        background-color: rgba(229, 247, 255, 0.6); /* Soft aqua tone */
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.2);
        margin-top: 20px;
        border: 1px solid #b3e0ff;
    }
    </style>

""", unsafe_allow_html=True)
    
# --- Custom Header Section ---
st.markdown("""
    <div style='background-color:#ccccff; padding:15px 20px; border-radius:12px; margin-bottom:20px;'>
        <h1 style='color:#1a237e; font-size:2.5rem; text-align:center;'>Medical Insurance Premium Predictor</h1>
        <p style='color:#333366; font-size:1.1rem; text-align:center;'><i>Predicting future medical expenses to help insurers make smarter decisions on premiums.</i></p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Navigation with Style ---
with st.sidebar:
    st.markdown("## 🌐 Main Menu")
    
    nav_option = st.radio("", ["Predict Premium","About Us"], index=0)

    st.markdown("---")

if nav_option == "About Us":
    st.markdown("### 📘 About This Project")
    st.markdown("""
    This application is designed to **predict annual medical insurance premiums** based on an individual's demographic and health-related factors.

    #### 🧠 Project Objective:
    The goal is to analyze how various features — like **age**, **BMI**, **number of children**, **smoking status**, **gender**, and **region** — influence medical costs. These insights are then used to train a **multiple linear regression model** that predicts future medical expenses.


    #### 🏥 Real-World Use:
    This tool helps **insurance providers** estimate personalized premiums using data-driven predictions, enabling **fairer pricing** based on individual risk profiles.

    ---
    """)
# --- Prediction Tab ---
elif nav_option == "Predict Premium":
    st.info('Enter User Details', icon="🧾")
    with st.form("prediction_form"):
        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
            bmi = st.number_input("BMI (Body Mass Index)", 10.0, 50.0, 25.0, step=0.1)
            children = st.number_input("Number of Children", 0, 10, 0)

        with c2:
            sex = st.selectbox("Sex", ["male", "female"])
            smoker = st.selectbox("Does user Smoke?", ["yes", "no"])
            region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

        submitted = st.form_submit_button("🔍 Predict Premium")

    if submitted:
        input_df = pd.DataFrame.from_dict({
            "age": [age],
            "sex": [sex],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })

        try:
            
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Estimated Annual Premium: $ {prediction:,.2f}")

            # Determine tier
            tier = 'High' if prediction > 15000 else 'Mid' if prediction > 8000 else 'Low'

            # Define styles per tier
            card_styles = {
                'Low': {
                    'bg': '#e3fceb',
                    'border': '#43a047',
                    'text': '#2e7d32',
                    'desc': 'You fall under the <strong>Low-Tier Premium Plan</strong> with great health and non-smoking status.'
                },
                'Mid': {
                    'bg': '#fff8e1',
                    'border': '#f9a825',
                    'text': '#f57f17',
                    'desc': 'You fall under the <strong>Mid-Tier Premium Plan</strong> based on your health and lifestyle indicators.'
                },
                'High': {
                    'bg': '#ffebee',
                    'border': '#c62828',
                    'text': '#b71c1c',
                    'desc': 'You fall under the <strong>High-Tier Premium Plan</strong> due to higher risk factors like smoking or high BMI.'
                }
            }

            style = card_styles[tier]

            st.markdown(f"""
                <div style='background-color:{style['bg']}; border-left: 5px solid {style['border']}; padding: 10px 20px; border-radius: 10px; margin-top: 20px;'>
                    <h4 style='color:{style['text']};'>Your Predicted Premium</h4>
                    <p style='color:{style['text']}; font-size: 1.1rem;'>{style['desc']}</p>
                    <p style='font-size: 0.95rem; color:{style['text']};'>This estimate is calculated using advanced machine learning techniques and helps you anticipate future insurance costs more accurately.</p>
                </div>
            """, unsafe_allow_html=True)

            # --- Generate PDF Report ---
            from fpdf import FPDF
            class PDFReport(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 14)
                    self.cell(0, 10, "Medical Insurance Premium Report", ln=True, align="C")
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Arial", "I", 8)
                    self.cell(0, 10, f"Page {self.page_no()}", align="C")

                def generate(self, data: dict, prediction: float) -> str:
                    self.add_page()
                    self.set_font("Arial", "", 12)
                    self.multi_cell(0, 10, """Dear Sir/Madam,

Thank you for using the Medical Insurance Premium Predictor. Based on the information you provided, your predicted annual premium falls into the following range:
""")
                    self.set_font("Arial", "B", 12)
                    self.cell(0, 10, "User Details:", ln=True)
                    self.set_font("Arial", "", 12)
                    for key, value in data.items():
                        self.cell(0, 10, f"- {key}: {value}", ln=True)
                    self.ln(5)
                    self.set_font("Arial", "B", 12)
                    self.cell(0, 10, "Prediction Insight:", ln=True)
                    self.set_font("Arial", "", 12)
                    self.multi_cell(0, 10, f"""Based on our trained machine learning model, your expected premium is:

USD ${prediction:,.2f} per year

This prediction considers your physical and lifestyle characteristics, as well as regional factors, to help insurance providers assess premium rates accurately. Please consult your insurer for detailed breakdowns and eligibility terms.

Warm regards,
The InsureSmart Team""")
                    
                    path = "Insurance_Premium_Report.pdf"
                    self.output(path)
                    return path

            user_data = {
                "Age": age,
                "Sex": sex.capitalize(),
                "BMI": bmi,
                "Children": children,
                "Smoker": smoker.capitalize(),
                "Region": region.capitalize()
            }

            pdf = PDFReport()
            pdf_path = pdf.generate(user_data, prediction)
            
            with open(pdf_path, "rb") as f:
                st.markdown("<div style='margin-top: 25px; text-align: center;'>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f,
                    file_name="Insurance_Premium_Report.pdf",
                    mime="application/pdf"
                )
                st.markdown("</div>", unsafe_allow_html=True)            

        except Exception as e:
            st.error(f"⚠️ Error during prediction: {e}")

