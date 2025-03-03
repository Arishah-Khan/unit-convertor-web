import streamlit as st
import time

conversion_factors = {
    "Length": {
        "Kilometer": 1000, "Meter": 1, "Centimeter": 0.01, "Millimeter": 0.001,
        "Mile": 1609.34, "Yard": 0.9144, "Foot": 0.3048, "Inch": 0.0254
    },
    "Mass": {
        "Kilogram": 1, "Gram": 0.001, "Milligram": 0.000001, "Metric Ton": 1000,
        "Pound": 0.453592, "Ounce": 0.0283495
    },
    "Temperature": "Special",
    "Area": {
        "Square Meter": 1, "Square Kilometer": 1e6, "Square Centimeter": 0.0001, "Square Millimeter": 0.000001,
        "Hectare": 10000, "Acre": 4046.86
    },
    "Volume": {
        "Cubic Meter": 1, "Liter": 0.001, "Milliliter": 1e-6, "Cubic Centimeter": 1e-6,
        "Gallon": 3.78541, "Pint": 0.473176
    },
    "Speed": {
        "Meter per second": 1, "Kilometer per hour": 0.277778, "Mile per hour": 0.44704,
        "Foot per second": 0.3048, "Knot": 0.514444
    },
    "Time": {
        "Second": 1, "Minute": 60, "Hour": 3600, "Day": 86400,
        "Week": 604800, "Year": 31536000
    },
    "Pressure": {
        "Pascal": 1, "Bar": 100000, "Atmosphere": 101325, "Torr": 133.322,
        "Pound per square inch": 6894.76
    },
    "Energy": {
        "Joule": 1, "Kilojoule": 1000, "Calorie": 4.184, "Kilocalorie": 4184,
        "Watt-hour": 3600, "Kilowatt-hour": 3.6e6
    },
    "Power": {
        "Watt": 1, "Kilowatt": 1000, "Horsepower": 745.7
    },
    "Data Storage": {
        "Bit": 1, "Byte": 8, "Kilobyte": 8192, "Megabyte": 8.38861e6,
        "Gigabyte": 8.59e9, "Terabyte": 8.796e12
    },
    "Angle": {
        "Degree": 1, "Radian": 57.2958
    },
    "Fuel Efficiency": {
        "Kilometer per liter": 1, "Miles per gallon": 0.425144
    },
    "Force": {
        "Newton": 1, "Kilonewton": 1000, "Pound-force": 4.44822
    }
}


def convert_units(category, from_unit, to_unit, value):
    if category == "Temperature":
        conversions = {
            ("Celsius", "Fahrenheit"): lambda v: (v * 9/5) + 32,
            ("Celsius", "Kelvin"): lambda v: v + 273.15,
            ("Fahrenheit", "Celsius"): lambda v: (v - 32) * 5/9,
        }
        return conversions.get((from_unit, to_unit), lambda v: v)(value)
    else:
        return (value * conversion_factors[category][from_unit]) / conversion_factors[category][to_unit]

st.set_page_config(page_title="Smart Unit Converter", page_icon="🔄")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Smart Unit Converter")
st.markdown("### 🔹 Convert units instantly with a sleek interface and history tracking!")

category = st.selectbox("📌 Select Conversion Category", list(conversion_factors.keys()))

if category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
else:
    units = list(conversion_factors[category].keys())

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("📍 From Unit", units)
with col2:
    to_unit = st.selectbox("🎯 To Unit", units)

from_value = st.number_input("✏️ Enter Value", value=1.0, format="%f")

if st.button("🔄 Reverse Conversion"):
    from_unit, to_unit = to_unit, from_unit

if from_unit and to_unit:
    with st.spinner("🔄 Converting... Please wait..."):
        time.sleep(1)
        try:
            to_value = convert_units(category, from_unit, to_unit, from_value)
            st.success(f"✅ Converted Value: **{to_value:.5f} {to_unit}**")
            st.session_state.history.append(f"{from_value} {from_unit} → {to_value:.5f} {to_unit}")
            st.session_state.history = st.session_state.history[-5:]
            st.code(f"{to_value:.5f} {to_unit}", language='text')
        except Exception as e:
            st.error(f"⚠️ Conversion Error: {str(e)}")

if st.session_state.history:
    st.subheader("📜 Conversion History")
    for item in reversed(st.session_state.history):
        st.write(item)

if st.button("🗑️ Clear History"):
    st.session_state.history.clear()
    st.rerun()