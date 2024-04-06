import math
import streamlit as st

# Define the constants
R = 10.73  # ft3 psia/lb-moleR

# Create a function to convert temperature from °C to °R
def convert_temperature_to_rankine(temperature_celsius):
  temperature_rankine = temperature_celsius * 9/5 + 491.67
  return temperature_rankine

# Create a function to convert pressure from bar.g to psia
def convert_pressure_to_psia(pressure_barg):
  pressure_psia = (pressure_barg+1) * 14.50377377
  return pressure_psia

# Create a function to calculate the maximum velocity
def calculate_maximum_velocity(Z, T, P, G):
  umax = 100 * ((Z * R * T) / (29 * G * P))**0.5
  return umax

# Create a function to calculate the operational velocity
def calculate_operational_velocity(Z, T, P, G):
  uoperational = 0.5 * calculate_maximum_velocity(Z, T, P, G)
  return uoperational

# Create a function to convert velocity from ft/s to m/s
def convert_velocity_to_ms(velocity_ftps):
  velocity_ms = velocity_ftps * 0.3048
  return velocity_ms

# Create a function to calculate the flow rate
def calculate_flow_rate(uoperational, D):
  # Convert the diameter from inches to feet
  D_ft = D / 12

  # Calculate the cross-sectional area of the pipeline
  A = math.pi * D_ft**2 / 4

  # Calculate the volumetric flow rate in cubic feet per second
  Q_cfs = uoperational * A

  # Convert the volumetric flow rate to cubic meters per hour
  Q_m3h = Q_cfs * 101.9406477

  # Convert the volumetric flow rate to normal cubic meters per hour
  Q_nm3h = Q_m3h * Z * ( P / 14.696 ) * (493.47 / T )
  #Q_nm3h = (Q_m3h * Z * (273.15 + 0.0) * P * 14.504) / ((273.15 + T) * (14.7))
 
  # Return the flow rate in cubic meters per hour and normal cubic meters per hour
  return Q_m3h, Q_nm3h

# Create the Streamlit app
st.set_page_config(page_title="Gas Pipeline Safe Operation Velocity & Flowrate Calculator",page_icon="👩‍💻",layout="wide")
st.header("Gas Pipeline Safe Operation Velocity & Flowrate Calculator")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

input , output = st.columns(spec=2,gap="Medium")

# Create the input fields
Z = input.number_input("Compressibility factor (Z)", min_value=0.0, max_value=1.0,value=0.99)
T = input.number_input("Gas temperature (°C)", min_value=0.0,value=25.0)
P = input.number_input("Gas pressure (bar.g)", min_value=0.0,value=35.0)
G = input.number_input("Gas gravity (air = 1.00)", min_value=0.0,value=0.7)
D = input.number_input("Inner pipe diameter (inch)", min_value=0.0,value=8.0)

# Convert the input values to the units used in the equation
T = convert_temperature_to_rankine(T)
P = convert_pressure_to_psia(P)

# Calculate the maximum velocity, operational velocity, and flow rate
umax = calculate_maximum_velocity(Z, T, P, G)
uoperational = calculate_operational_velocity(Z, T, P, G)
Q_m3h, Q_nm3h = calculate_flow_rate(uoperational, D)

# Convert the velocity units to m/s
umax_ms = convert_velocity_to_ms(umax)
uoperational_ms = convert_velocity_to_ms(uoperational)

# Display the results
output.subheader('Results : 👇 ')
output.error("Erosional Velocity (m/s) : " + f"{umax_ms:,.2f}")
output.info("Safe Operation Velocity (m/s) : " + f"{uoperational_ms:,.2f}")
output.success("Safe Operation Flowrate (Nm3/h) : " + f"{Q_nm3h:,.2f}")

# Developer & Refrence
output.divider()
output.write('Developer : 👷 alias @ aliasalias85@gmail.com')
output.write('Refrence : Gas pipeline hydraulics, E.Shashi Menon, 2005 by Taylor & Francis')
