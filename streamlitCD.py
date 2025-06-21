import openpyxl # type: ignore
import pandas as pd
import joblib # type: ignore
import streamlit as st # type: ignore

# Load the saved model and encoded columns
model = joblib.load(r"D:\streamlit_pp3\card\Scripts\xgboost_ml_model.pkl")
encoded_columns = joblib.load(r"D:\streamlit_pp3\card\Scripts\encoded_columns.pkl")

# Load dataset from Excel to extract unique values for dropdown options
df_cars = pd.read_excel(r"D:\streamlit_pp3\card\Scripts\Preprocessed_data.xlsx")

# Define categorical columns and extract unique values
categorical_columns = ['ft', 'bt', 'transmission', 'company', 'model', 
                       'Insurance Validity', 'Color', 'Location', 
                       'RTO_region', 'Drive_Type_Classified']
unique_values = {col: df_cars[col].unique().tolist() for col in categorical_columns}

# Create brand-model mapping
brand_model_mapping = df_cars.groupby('company')['model'].unique().to_dict()

# Function to preprocess input data
def preprocess_input(data):
    data['Turbo Charger'] = data['Turbo Charger'].map({'True': True, 'False': False})
    data_encoded = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    return data_encoded.reindex(columns=encoded_columns, fill_value=0)

# Function to predict the price
def predict_price(input_data):
    processed_data = preprocess_input(input_data)
    prediction = model.predict(processed_data)
    return prediction[0]

# Function to format number in INR
def format_inr(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)

# Streamlit app layout
def main():
    st.set_page_config(page_title="Car Price Prediction", page_icon="clipart.png")
    st.markdown("""
        <style>
        body {
            background-color: #f0f2f5;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        .big-text {
            font-size: 48px;
            font-weight: bold;
            color: #007bff;
            text-align: center;
        }
        .stSelectbox, .stNumberInput {
            border: 2px solid orange; 
            border-radius: 5px; 
            padding: 2px; 
            width: 150px; 
            font-size: 10px; 
            margin-bottom: 5px; 
        }
        .stButton button {
            color: white; 
            border: 3px solid orange; 
            border-radius: 10px; 
            width: 100%; 
            margin-left: auto;
            margin-right: auto;
        }
        .stButton:hover {
            background-color: darkorange; 
        }
        </style>
    """, unsafe_allow_html=True)

    st.image(r"C:/Users/shalu/Downloads/WhatsApp Image 2025-04-20 at 5.59.23 PM.jpeg", width=800)
    st.write("<h1 style='text-align: center;'>Used Car Price Prediction App</h1>", unsafe_allow_html=True)

    st.sidebar.header("Enter the car details:")
    
    if st.sidebar.button("Reset Inputs"):
        st.session_state.clear()  # Clear all session states

    # Sidebar inputs for categorical features
    fuel_type = st.sidebar.selectbox('Fuel Type', unique_values['ft'], index=0)
    body_type = st.sidebar.selectbox('Body Type', unique_values['bt'], index=0)
    transmission = st.sidebar.selectbox('Transmission', unique_values['transmission'], index=0)
    company = st.sidebar.selectbox('Company', unique_values['company'], index=0)
    
    selected_model = st.sidebar.selectbox('Model', brand_model_mapping.get(company, []), index=0)

    insurance_validity = st.sidebar.selectbox('Insurance Validity', unique_values['Insurance Validity'], index=0)
    color = st.sidebar.selectbox('Color', unique_values['Color'], index=0)
    location = st.sidebar.selectbox('Location', unique_values['Location'], index=0)
    rto_region = st.sidebar.selectbox('RTO Region', unique_values['RTO_region'], index=0)
    drive_type = st.sidebar.selectbox('Drive Type', unique_values['Drive_Type_Classified'], index=0)

    # Sidebar inputs for numerical values
    owner_no = st.sidebar.number_input('Owner Number', min_value=1, max_value=5, value=1)
    model_year = st.sidebar.number_input('Model Year', min_value=2000, max_value=2024, value=2022)
    km_driven = st.sidebar.number_input('Kilometers Driven', min_value=0, value=10000)
    mileage = st.sidebar.number_input('Mileage (kmpl)', min_value=0.0, value=15.0)
    engine_cc = st.sidebar.number_input('Engine Displacement (CC)', min_value=500, max_value=5000, value=1000)
    turbo_charger = st.sidebar.selectbox('Turbo Charger', ['True', 'False'])

    # Prepare input data as a DataFrame
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

    # Prediction
    if st.sidebar.button("Predict Price"):
        predicted_price = predict_price(input_data)
        formatted_price = format_inr(predicted_price)
        
        st.write("<p style='font-size: 48px; font-weight: bold; color: orange; text-align: center;'>Predicted Price: ₹ {}</p>".format(formatted_price), unsafe_allow_html=True)

if __name__ == '__main__':
    main()