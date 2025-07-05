# 📦 Import required libraries
import openpyxl  # To work with Excel files
import pandas as pd  # For data manipulation
import joblib  # To load the pre-trained ML model and columns
import streamlit as st  # Streamlit framework to create the web app

# 🚀 Load ML model and column encoder
model = joblib.load(r"D:\streamlit_pp3\card\Scripts\xgboost_ml_model.pkl")  # Pre-trained XGBoost model
encoded_columns = joblib.load(r"D:\streamlit_pp3\card\Scripts\encoded_columns.pkl")  # Expected column format

# 📊 Load dataset to extract dropdown options for form inputs
df_cars = pd.read_excel(r"D:\streamlit_pp3\card\Scripts\Preprocessed_data.xlsx")

# 🔠 Categorical features that need encoding
categorical_columns = ['ft', 'bt', 'transmission', 'company', 'model',
                       'Insurance Validity', 'Color', 'Location',
                       'RTO_region', 'Drive_Type_Classified']

# 🔄 Create dictionary of unique values for dropdowns
unique_values = {col: df_cars[col].unique().tolist() for col in categorical_columns}
brand_model_mapping = df_cars.groupby('company')['model'].unique().to_dict()

# 🔧 Function to preprocess user input before sending to the model
def preprocess_input(data):
    # ✅ Convert string values 'True'/'False' into actual Boolean values
    data['Turbo Charger'] = data['Turbo Charger'].map({'True': True, 'False': False})
    
    # 🔄 Apply one-hot encoding to categorical columns
    data_encoded = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    
    # 📏 Reindex the columns to match training set, filling missing columns with 0
    return data_encoded.reindex(columns=encoded_columns, fill_value=0)

# 💡 Function to predict price
def predict_price(input_data):
    processed_data = preprocess_input(input_data)  # Clean and encode the data
    prediction = model.predict(processed_data)  # Predict using ML model
    return prediction[0]  # Return the predicted price

# 💸 Format price to INR format: Rs.13,58,679.00
def format_inr(amount):
    s = f"{amount:,.2f}".split(".")[0].replace(",", "")
    if len(s) > 3:
        s_main = s[:-3]
        s_last = s[-3:]
        s_main_rev = s_main[::-1]
        s_chunks = [s_main_rev[i:i+2] for i in range(0, len(s_main_rev), 2)]
        s_indian = ",".join(chunk[::-1] for chunk in s_chunks[::-1])
        formatted = f"{s_indian},{s_last}"
    else:
        formatted = s
    return f"Rs.{formatted}.{str(amount).split('.')[-1][:2]}"

# 🖥️ Main web app logic
def main():
    # 📌 Set page title and icon
    st.set_page_config(page_title="Used Car Price Prediction", page_icon="🚗")

    # 🎨 Add custom CSS for better appearance
    st.markdown("""
        <style>
        body {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #007bff;
        }
        .stButton > button {
            background-color: orange;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🖼️ Display logo or car image
    st.image(r"C:/Users/shalu/Downloads/WhatsApp Image 2025-04-20 at 5.59.23 PM.jpeg", width=800)
    
    # 🏷️ Title of the app
    st.markdown("<h1>Used Car Price Prediction App</h1>", unsafe_allow_html=True)

    # 📥 Sidebar input form
    st.sidebar.header("Enter Car Details")

    # 🔄 Reset form if button clicked
    if st.sidebar.button("Reset Inputs"):
        st.session_state.clear()

    # 🧾 Dropdowns and number inputs (all user inputs)
    fuel_type = st.sidebar.selectbox('Fuel Type', unique_values['ft'])
    body_type = st.sidebar.selectbox('Body Type', unique_values['bt'])
    transmission = st.sidebar.selectbox('Transmission', unique_values['transmission'])
    company = st.sidebar.selectbox('Company', unique_values['company'])
    selected_model = st.sidebar.selectbox('Model', brand_model_mapping.get(company, []))
    insurance_validity = st.sidebar.selectbox('Insurance Validity', unique_values['Insurance Validity'])
    color = st.sidebar.selectbox('Color', unique_values['Color'])
    location = st.sidebar.selectbox('Location', unique_values['Location'])
    rto_region = st.sidebar.selectbox('RTO Region', unique_values['RTO_region'])
    drive_type = st.sidebar.selectbox('Drive Type', unique_values['Drive_Type_Classified'])
    owner_no = st.sidebar.number_input('Owner Number', min_value=1, max_value=5, value=1)
    model_year = st.sidebar.number_input('Model Year', min_value=2000, max_value=2024, value=2022)
    km_driven = st.sidebar.number_input('Kilometers Driven', min_value=0, value=10000)
    mileage = st.sidebar.number_input('Mileage (kmpl)', min_value=0.0, value=15.0)
    engine_cc = st.sidebar.number_input('Engine Displacement (CC)', min_value=500, max_value=5000, value=1000)
    turbo_charger = st.sidebar.selectbox('Turbo Charger', ['True', 'False'])

    # 📋 Create DataFrame from input
    input_data = pd.DataFrame({
        'ft': [fuel_type],
        'bt': [body_type],
        'transmission': [transmission],
        'company': [company],
        'model': [selected_model],
        'modelYear': [model_year],
        'km': [km_driven],
        'Insurance Validity': [insurance_validity],
        'Mileage': [mileage],
        'Color': [color],
        'Displacement': [engine_cc],
        'Turbo Charger': [turbo_charger],
        'Location': [location],
        'RTO_region': [rto_region],
        'Drive_Type_Classified': [drive_type],
        'ownerNo': [owner_no]
    })

    # 🧠 Predict button
    if st.sidebar.button("Predict Price"):
        predicted_price = predict_price(input_data)  # ML prediction

        # 🎯 Business logic for price adjustment
        adjustment = 0
        if km_driven > 100000:
            adjustment -= 0.10 * predicted_price
        elif km_driven > 50000:
            adjustment -= 0.05 * predicted_price
        elif km_driven < 20000:
            adjustment += 0.05 * predicted_price

        if mileage > 20:
            adjustment -= 0.05 * predicted_price
        elif mileage < 10:
            adjustment += 0.05 * predicted_price

        if model_year >= 2022:
            adjustment += 0.10 * predicted_price
        elif model_year <= 2010:
            adjustment -= 0.10 * predicted_price

        # 🧾 Apply adjustment
        final_price = predicted_price + adjustment
        formatted_price = format_inr(final_price)

        # 📣 Display the final output
        st.markdown(
            f"<h2 style='text-align:center; color: orange;'>Predicted Price: {formatted_price}</h2>",
            unsafe_allow_html=True
        )

# ▶️ Run the app
if __name__ == '__main__':
    main()
