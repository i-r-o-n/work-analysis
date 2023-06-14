import math
import random
import time

import streamlit as st

from analyzer import Defaults, make_query, Dataset
from file_manager import write_output, Entry



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
    

def parse_dataset(dataset_selection: str) -> Dataset:
    # [!] dataset_options order must match enum order for this to work
    return Dataset(dataset_options.index(dataset_selection))
# creativity/temperature scale slider
    # add question mark info popup explaining that, 
    # how strictly you want the model to adhere to the query
# don't do model picker, just use one model
# 

st.title("School Work Showcase")

st.subheader("### Creativity")
temperature_selection = st.slider(
    "temperature",0,100,
    format="%",
    value=70,
    help="How strictly you want the model to adhere to your query")

dataset_options = [
    "all years",
    "freshman",
    "sophomore",
    "junior",
    "senior"
]
dataset_selection = st.selectbox(
    "Which school year would you like to look at?",
    dataset_options
)

st.text_input("What would you like to know?", key="query")

dataset = parse_dataset(dataset_selection)
# response = make_query(
#     query=st.session_state.query,
#     dataset=dataset,
#     temperature=temperature_selection,
# )

def get_dummy_response() -> str:
    # wait time to simulate long query
    time.sleep(3)
    return "temporary dummy response " + random.randrange(1000)

response = get_dummy_response()

write_output(Entry(
    dataset,
    temperature_selection,
    Defaults.model,
    st.session_state.query,
    response).parse_to_csv())

st.write(response)

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'