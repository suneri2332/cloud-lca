import streamlit as st
import requests
import pandas as pd

# 🔗 Your EC2 API
API_URL = "http://13.53.90.69:8000/predict"

st.set_page_config(page_title="ML Dashboard", layout="wide")

# 🎨 Custom Aesthetic Theme
st.markdown("""
<style>
body {
    background-color: #fffaf0;
}

.big-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #ff8fab;
}

.card {
    padding: 20px;
    border-radius: 20px;
    background: linear-gradient(135deg, #fff3b0, #ffd6e0);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}

.stButton>button {
    background-color: #ffb6c1;
    color: black;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #ff8fab;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 🌸 Title
st.markdown('<p class="big-title">🌸 ML Prediction Dashboard</p>', unsafe_allow_html=True)
st.write("Enter feature values and get real-time predictions")

# Layout
col1, col2 = st.columns(2)

# 📥 INPUT SECTION
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 🔢 Enter Features")

    f1 = st.number_input("Feature 1")
    f2 = st.number_input("Feature 2")
    f3 = st.number_input("Feature 3")
    f4 = st.number_input("Feature 4")

    predict_btn = st.button("🚀 Predict")

    st.markdown('</div>', unsafe_allow_html=True)

# 📊 RESULT SECTION
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📈 Prediction Result")

    if "history" not in st.session_state:
        st.session_state.history = []

    if predict_btn:
        data = {"features": [f1, f2, f3, f4]}

        try:
            response = requests.post(
                API_URL,
                json=data,
                headers={"x-api-key": "123"}
            )

            result = response.json()
            prediction = result["prediction"]

            st.success(f"✅ Prediction: {prediction}")

            # Save history
            st.session_state.history.append(prediction)

        except Exception as e:
            st.error("❌ Error connecting to API")
            st.write(e)

    st.markdown('</div>', unsafe_allow_html=True)

# 📊 CHARTS SECTION
if "history" in st.session_state and st.session_state.history:

    st.markdown("## 📊 Analytics Dashboard")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📈 Prediction Trend")
        st.line_chart(st.session_state.history)

    with col4:
        st.subheader("📊 Prediction Distribution")
        df = pd.DataFrame(st.session_state.history, columns=["Prediction"])
        st.bar_chart(df["Prediction"].value_counts())

    st.subheader("📋 Prediction History")
    st.dataframe(df)