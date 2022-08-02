# %%
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import streamlit as st
import matplotlib.pyplot as plt

# %%
room_temperature = ctrl.Antecedent(np.arange(16, 37, 1), 'room_temperature')
temperature = ctrl.Antecedent(np.arange(16, 37, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(30, 71, 1), 'humidity')
diff_temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'diff_temperature')

# %%
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')
compressor_speed = ctrl.Consequent(np.arange(0, 101, 1), 'compressor_speed')

# %%
room_temperature['low'] = fuzz.trimf(room_temperature.universe, [16, 16, 26])
room_temperature['medium'] = fuzz.trimf(room_temperature.universe, [16, 26, 36])
room_temperature['high'] = fuzz.trimf(room_temperature.universe, [26, 36, 36])
# room_temperature.automf(3)



# %%
# room_temperature.view()

# %%
diff_temperature['high'] = fuzz.trimf(diff_temperature.universe, [25, 50, 50])
diff_temperature['medium'] = fuzz.trimf(diff_temperature.universe, [0, 25, 50])
diff_temperature['low'] = fuzz.trimf(diff_temperature.universe, [0, 0, 25])

# %%
# diff_temperature.view()

# %%
humidity['low'] = fuzz.trimf(humidity.universe, [30, 30, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [50, 70, 70])
# print("humidity", humidity.universe)

# %%
humidity.view()

# %%
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [0, 50, 100])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])
# print("fan_speed", fan_speed.universe)

# %%
fan_speed.view()

# %%
compressor_speed['low'] = fuzz.trimf(compressor_speed.universe, [0, 0, 50])
compressor_speed['medium'] = fuzz.trimf(compressor_speed.universe, [0, 50, 100])
compressor_speed['high'] = fuzz.trimf(compressor_speed.universe, [50, 100, 100])


# %%
compressor_speed.view()

# %% [markdown]
# print("compressor_speed", compressor_speed.universe)

# %%
rule1a = ctrl.Rule(diff_temperature['low'], fan_speed['low'])
rule1b = ctrl.Rule(diff_temperature['medium'], fan_speed['medium'])
rule1c = ctrl.Rule(diff_temperature['high'], fan_speed['high'])




# %%


rule2a = ctrl.Rule(diff_temperature['high'] | humidity['high'], compressor_speed['high'])
rule2b = ctrl.Rule(diff_temperature['medium'] | humidity['medium'], compressor_speed['medium'])
rule2c = ctrl.Rule(diff_temperature['low'] | humidity['low'] | room_temperature['low'], compressor_speed['low'])

# %%
ac_ctrl = ctrl.ControlSystem([rule1a, rule1b, rule1c, rule2a, rule2b, rule2c])

    

# %%
def show_predict_page():
    st.title("Fuzzy Control On HVAC Final Project")
    st.subheader(f"Durham College Student: Wenping Wang ")
    st.write("""### please key in parameter to silumate the controls""")

    # Room Temperature Input
    in_rt = st.slider("Room Temperature (°C)", 16, 36, 16 )

    

    # temperature setpoint
    in_tt = st.slider("Temperature Setpoint(°C)", 16, 36, 22 )

    # Room Humidity Temperature
    in_hd = st.slider("Room Humidity (%)", 0, 70, 50 )

    # Difference between setpoint and room temperature
    a = (in_rt - in_tt)*10
    in_diff = max(a, 0)

    speed = ctrl.ControlSystemSimulation(ac_ctrl)
    speed.input['room_temperature'] = int(in_rt)
    speed.input['diff_temperature'] = int(in_diff)
    speed.input['humidity'] = int(in_hd)
    speed.compute()
    fan_speed = max(15, speed.output['fan_speed'])
    compressor_speed = speed.output['compressor_speed']
    ok = st.button("click to calculate the speed (%)")
    if ok:
      st.subheader(f"The fan speed is {round(fan_speed)} % of full speed")
      st.subheader(f"The compressor speed is {round(compressor_speed)} % of full speed")

# %%

    
show_predict_page()
    
    


