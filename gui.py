import math

import streamlit as st

from analyzer import Defaults



def temperature_sanitizer(temperature: str) -> float:
    try:
        temperature = float(temperature)
        # return the value scaled between zero and one
        # return round(temperature / math.pow(10, math.floor(math.log(temperature, 10)) + 1, 2))
        # return the value of the decimal only
        # return round(temperature % 1.0, 2)
        return temperature
    except:
        return Defaults.temperature
    

# creativity/temperature scale slider
    # add question mark info popup explaining that, 
    # how strictly you want the model to adhere to the query
# don't do model picker, just use one model
# 
"test"
st.write("School Work Showcase")

