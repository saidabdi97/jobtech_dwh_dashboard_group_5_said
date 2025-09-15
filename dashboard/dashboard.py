import streamlit as st
from connect_data_warehouse import query_job_listings


def layout():
    df = query_job_listings()

    st.title("Data engineering job ads")
    st.write("This data shows data engineering job ads from arbetsförmedlingens API")

    st.dataframe(df)

if __name__ == "__main__":
    layout()