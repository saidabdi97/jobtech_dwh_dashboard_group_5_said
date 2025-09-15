import streamlit as st
from connect_data_warehouse import query_job_listings


def layout():

    st.title("Data engineering job ads")
    st.write("This data shows data engineering job ads from arbetsförmedlingens API")

    table = st.selectbox("Välj tabell", ["marts.mart_social_job", "marts.mart_technical_jobs" ,"marts.mart_managers_job"])

    df = query_job_listings(tabel_name=table)

    st.dataframe(df)

if __name__ == "__main__":
    layout()