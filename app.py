import streamlit as st
import requests
import pint
import pandas as pd

# Custom CSS for Stylish UI
def set_custom_style(theme):
    if theme == "Light":
        background_color = "#F0F2F6"
        text_color = "#333"
        card_bg = "rgba(255, 255, 255, 0.8)"
    else:
        background_color = "#1E1E2F"
        text_color = "#FFF"
        card_bg = "rgba(40, 40, 60, 0.8)"

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: linear-gradient(135deg, #4A90E2, {background_color});
                color: {text_color};
                font-family: 'Poppins', sans-serif;
            }}
            .main-container {{
                padding: 20px;
                border-radius: 12px;
                background: {card_bg};
                backdrop-filter: blur(10px);
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
            }}
            .stButton>button {{
                color: white;
                background: linear-gradient(90deg, #000062, #00009d);
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                transform: scale(1.05);
                text-color: white;
                background: linear-gradient(90deg, #000062, #00009d);
            }}
            .stSelectbox, .stNumberInput {{
                border-radius: 8px;
            }}
            .stSidebar {{
                background: {card_bg};
                padding: 20px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Theme selection
theme = st.sidebar.radio("🌙 Choose Theme:", ["Light", "Dark"])
set_custom_style(theme)

# Create a unit registry
ureg = pint.UnitRegistry()

# Dictionary of Common Units (Full Name + Symbol)
unit_options = {
    "Seconds (s)": "s",
    "Minutes (min)": "min",
    "Hours (h)": "hour",
    "Days (d)": "day",
    "Kilograms (kg)": "kg",
    "Grams (g)": "g",
    "Pounds (lb)": "lb",
    "Ounces (oz)": "oz",
    "Meters (m)": "m",
    "Centimeters (cm)": "cm",
    "Millimeters (mm)": "mm",
    "Feet (ft)": "ft",
    "Inches (in)": "in",
    "Celsius (°C)": "degC",
    "Fahrenheit (°F)": "degF",
    "Kelvin (K)": "kelvin",
    "Gigabytes (GB)": "GB",
    "Megabytes (MB)": "MB",
    "Kilohertz (kHz)": "kHz",
    "Hertz (Hz)": "Hz"
}

# Dictionary of Common Currencies (Full Name + Symbol)
currency_options = {
    "US Dollar (USD)": "USD",
    "Euro (EUR)": "EUR",
    "British Pound (GBP)": "GBP",
    "Pakistani Rupee (PKR)": "PKR",
    "Indian Rupee (INR)": "INR",
    "Australian Dollar (AUD)": "AUD",
    "Canadian Dollar (CAD)": "CAD",
    "Japanese Yen (JPY)": "JPY",
    "Chinese Yuan (CNY)": "CNY"
}

# Function to Convert Units
def convert_units(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return f"✅ {value} {from_unit} = {result}"
    except pint.errors.UndefinedUnitError:
        return "❌ Invalid unit. Example: 'kg', 'm', 'Celsius'"
    except pint.errors.DimensionalityError:
        return "❌ Incompatible unit types (e.g., kg to meters not possible)."

# Function for Currency Conversion
def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/993c98bc8279e4f56569e35f/pair/{from_currency}/{to_currency}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200 or "conversion_rate" not in data:
            return "❌ Error: Invalid API response."

        rate = data["conversion_rate"]
        result = amount * rate
        return f"✅ {amount} {from_currency} = {result:.2f} {to_currency}"
    
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# Streamlit UI
st.title("🔣Fast & Smart Unit & Currency Converter💱")

# Sidebar Menu
st.sidebar.header("🔍 Quick Access")
st.sidebar.markdown("- **Unit Conversion**")
st.sidebar.markdown("- **Currency Exchange**")

# Main container
with st.container():
    

    # Unit Conversion
    st.subheader("📏 Unit Conversion")
    unit_value = st.number_input("Enter value", min_value=0.0, step=0.1)
    from_unit = st.selectbox("From Unit", list(unit_options.keys()), index=0)
    to_unit = st.selectbox("To Unit", list(unit_options.keys()), index=1)
    if st.button("Convert Unit"):
        unit_result = convert_units(unit_value, unit_options[from_unit], unit_options[to_unit])
        st.success(unit_result)

    # Currency Conversion
    st.subheader("💰 Currency Conversion")
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    from_currency = st.selectbox("From Currency", list(currency_options.keys()), index=0)
    to_currency = st.selectbox("To Currency", list(currency_options.keys()), index=1)
    if st.button("Convert Currency"):
        converted_value = convert_currency(amount, currency_options[from_currency], currency_options[to_currency])
        st.success(converted_value)

    # Placeholder for Currency Trends
    st.subheader("📊 Currency Exchange Rate Trends")
    if st.button("Show Currency Trend"):
        st.write("🔍 Fetching live currency trend data...")
        st.line_chart(pd.DataFrame({"Date": ["2025-02-20", "2025-02-21", "2025-02-22"], "Rate": [275, 277, 280]}))

    st.markdown('</div>', unsafe_allow_html=True)



st.write("Made with ❤️ by Syeda Areeba")