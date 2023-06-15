import random
import time
from multiprocessing import Process, Pipe
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
    return "dummy response " + str(random.randrange(1000))



def do_wait_info_dots(current_wait_info: str) -> str:
    time.sleep(0.5)
    return current_wait_info + '.'


def clean_query(query: str) -> str:
    if query[-1] == ',':
        query = query[:-1]
    if "\"\"" in query:
        query = query.replace("\"\"",'')

    return bytes(query, "utf-8").decode("utf-8", "ignore")


query_tab, database_tab = st.tabs(["Query", "Database"])

response = "Ask me a question..."
wait_info = "Thinking"
accepting_responses = False

with query_tab:
    st.title("School Work Showcase")
    st.text("A.I. Analysis of Our Writing: Query over the deliverables from the past four years \nusing a language learning model.")

    with st.form("query"):
        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("### Creativity")
            temperature_selection = st.slider(
                "temperature",0,100,
                value=70,step=10,
                help="How strictly you want the model to adhere to your query")
            
        with right_column:
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

        response_box = st.code(response)

        if generated:
            
            response_box.code(wait_info)
            
            connection = Pipe()

            def get_response(response_pipe: Pipe) -> None:
                # input response function here \/
                response_pipe.send(get_dummy_response())
                # state check
                if accepting_responses:
                    response_pipe.send(make_query(
                        query=st.session_state.query,
                        dataset=parse_dataset(dataset_selection),
                        temperature=get_scaled_temperature(temperature_selection),
                    ))

            response_process = Process(
                target=get_response, 
                args=(connection[1],))
            response_process.start()
            while response_process.is_alive():
                wait_info = do_wait_info_dots(wait_info)
                response_box.code(wait_info)

            response_process.join()
            response = connection[0].recv()

            response_box.code(response)
           
            write_output(Entry(
                parse_dataset(dataset_selection),
                get_scaled_temperature(temperature_selection),
                Defaults.model,
                clean_query(st.session_state.query),
                response).parse_to_csv())
        
   
     

# dataset, temperature, model_type, query, response
df = pd.read_csv(OUTPUT_FILE)
df = df.drop(columns=["model_type"])

with database_tab:

    st.table(df)

    # st.dataframe(
    #     df,
    #     column_config={
    #         "dataset": "Set",
    #         "temperature": "Temp",
    #         "query":"Query",
    #         "response":"Response"
    #     },
    #     hide_index=True,
    #     use_container_width=True
    # )


    st.download_button(
        "Download Responses",
        OUTPUT_FILE, # df.to_csv(index=False).encode("utf-8"),
        "responses.csv",
        "text/csv",
        "download-csv",
        "Download this table as a csv"
    )

