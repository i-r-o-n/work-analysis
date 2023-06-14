import math
import random
import time
import pandas as pd

import streamlit as st

from utils.data_types import Dataset 
from utils.text_analyzer import Defaults, make_query
from utils.file_manager import write_output, Entry, OUTPUT_FILE


# def temperature_sanitizer(temperature: str) -> float:
#     try:
#         temperature = float(temperature)
#         # return the value scaled between zero and one
#         # return round(temperature / math.pow(10, math.floor(math.log(temperature, 10)) + 1, 2))
#         # return the value of the decimal only
#         # return round(temperature % 1.0, 2)
#         return temperature
#     except:
#         return Defaults.temperature
    


def get_scaled_temperature(temperature_selection: int) -> float:
   return round(temperature_selection / 100, 1)


def parse_dataset(dataset_selection: str) -> Dataset:
    # [!] dataset_options order must match enum order for this to work
    return Dataset(dataset_options.index(dataset_selection))


def get_dummy_response() -> str:
    # wait time to simulate long query
    time.sleep(3)
    return "temporary dummy response " + str(random.randrange(1000))


query_tab, database_tab = st.tabs(["Query", "Database"])

response = "Ask me a question..."
accepting_responses = False

with query_tab:
    st.title("School Work Showcase")
    st.text("A.I. Analysis of Our Writing: Query over the deliverables from the past four years \nusing a language learning model.")

    with st.form("query"):
        st.markdown("### Creativity")
        temperature_selection = st.slider(
            "temperature",0,100,
            value=70,step=10,
            help="How strictly you want the model to adhere to your query")

        st.markdown("### Data")
        dataset_options = [
            "all years",
            "freshman",
            "sophomore",
            "junior",
            "senior"
        ]
        dataset_selection = st.selectbox(
            "Which school year would you like to look at?",
            dataset_options)

        st.markdown("### Query")
        st.text_input("What would you like to know?", key="query")

        generated = st.form_submit_button("Generate response")
        if generated:
            response = get_dummy_response()
            dataset = parse_dataset(dataset_selection)
            if accepting_responses:
                response = make_query(
                    query=st.session_state.query,
                    dataset=dataset,
                    temperature=get_scaled_temperature(temperature_selection),
                )
            write_output(Entry(
                dataset,
                get_scaled_temperature(temperature_selection),
                Defaults.model,
                st.session_state.query,
                response).parse_to_csv())

        
    st.code(response)

# dataset, temperature, model_type, query, response
df = pd.read_csv(OUTPUT_FILE)
df = df.drop(columns=["model_type"])
with database_tab:

    st.dataframe(
        df,
        column_config={
            "dataset": "Set",
            "temperature": "Temp",
            "query":"Query",
            "response":"Response"
        },
        hide_index=True,
        use_container_width=True
    )

