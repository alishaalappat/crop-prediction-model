import streamlit as st
import pickle
from PIL import Image

# Load scaler and model
scaler = pickle.load(open('rfcccscaler.sav', 'rb'))
model = pickle.load(open('rfcccmodel.sav', 'rb'))

# List of crop labels
labels = [
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
    'mothbeans', 'mungbean', 'blackgram', 'lentil', 'watermelon',
    'muskmelon', 'cotton', 'jute'
]

# Custom CSS for visual enhancements
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
    }
    .subheader {
        font-size: 20px;
        color: #4682B4;
        margin-top: 20px;
    }
    .predict-button {
        background-color: #2E8B57;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
    }
    .predict-button:hover {
        background-color: #3CB371;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Sidebar navigation for pages
    page = st.sidebar.radio(
        "📖 Navigation",
        ["🏠 Home", "🌿 Predict Crop", "📊 Barplot", "🔍 Conclusion"]
    )

    # Page: Home
    if page == "🏠 Home":
        st.markdown('<div class="main-title">🌾 Crop Prediction App 🌾</div>', unsafe_allow_html=True)

        # Add an image with a larger caption
        try:
            img = Image.open('crop.jpg')
            st.image(
                img,
                caption="Revolutionizing Agriculture with AI 🌟",
                use_container_width=True
            )
        except FileNotFoundError:
            st.error("Home page image not found. Please ensure 'crop.jpg' is in the correct directory.")

        # Styled content with emojis
        st.markdown(
            """
            🌟 **Welcome to the Crop Prediction App!**  
            This project is designed to assist farmers in selecting the most suitable crops based on environmental and soil conditions. 
            Using **machine learning**, the app evaluates factors such as:

            - 🌡️ **Temperature**
            - 💧 **Humidity**
            - 🌱 **Soil pH**
            - 🌊 **Water Availability**
            - 🌦️ **Season**

            With these inputs, our system ensures **better planning**, **higher yields**, and **sustainability** for modern agriculture.  
            🚀 Click on **🌿 Predict Crop** to get started!
            """
        )

    # Page: Predict Crop
    elif page == "🌿 Predict Crop":
        st.markdown('<div class="main-title">🌿 Predict Your Crop 🌿</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="subheader">Enter the environmental and soil details below to get your crop recommendation:</p>',
            unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            temperature = st.number_input('🌡️ Temperature (°C)', min_value=15.0, max_value=30.0, value=20.0, step=0.1)
            humidity = st.slider('💧 Humidity (%)', min_value=10.0, max_value=85.0, value=50.0)
            season = st.selectbox('🌦️ Season', ('Summer', 'Winter', 'Rainy', 'Spring'))
            season_mapping = {'Summer': 0, 'Winter': 1, 'Rainy': 2, 'Spring': 3}
            season_numeric = season_mapping[season]

        with col2:
            ph = st.number_input('🌱 Soil pH Level', min_value=3.0, max_value=8.0, value=7.0, step=0.1)
            wateravailability = st.slider('🌊 Water Availability (ml)', min_value=50.0, max_value=300.0, value=150.0)

        features = [temperature, humidity, season_numeric, ph, wateravailability]
        predict_button = st.button("🚜 Predict", key="predict")
        if predict_button:
            features = [float(x) for x in features]
            try:
                prediction_numeric = model.predict(scaler.transform([features]))
                crop_name = labels[int(prediction_numeric[0])]
                st.success(f"🌟 The recommended crop for the given conditions is: **{crop_name.capitalize()}**")
            except Exception as e:
                st.error(f"❌ Error during prediction: {e}")

    # Page: Barplot
    elif page == "📊 Barplot":
        st.markdown('<div class="main-title">📊 Crop Production Insights</div>', unsafe_allow_html=True)

        # Add barplot image
        try:
            barplot_img = Image.open('output_plot.png')
            st.image(barplot_img, caption="📈 Crop Production Barplot", use_container_width=True)
        except FileNotFoundError:
            st.error("Barplot image not found. Please ensure 'output_plot.png' is in the correct directory.")

        st.markdown('<p class="subheader">ROC Curve for Model Evaluation:</p>', unsafe_allow_html=True)
        # Add ROC curve image
        try:
            roc_curve_img = Image.open('roc_curves.png')
            st.image(roc_curve_img, caption="📊 ROC Curve", use_container_width=True)
        except FileNotFoundError:
            st.error("ROC curve image not found. Please ensure 'roc_curve.png' is in the correct directory.")

    # Page: Conclusion
    elif page == "🔍 Conclusion":
        st.markdown('<div class="main-title">🔍 Conclusion</div>', unsafe_allow_html=True)

        st.markdown(
            """
            🌾 **The Crop Prediction Project** harnesses the power of **machine learning** to revolutionize traditional farming.  
            By offering data-driven insights, this tool helps farmers achieve:

            - 🌟 **Higher productivity**
            - 🌟 **Sustainable practices**
            - 🌟 **Improved food security**

            🌍 Together, let's build a smarter, more resilient agricultural future!  
            Thank you for using the Crop Prediction App. 🚜
            """
        )


if __name__ == '__main__':
    main()

    #streamlit run croo.py