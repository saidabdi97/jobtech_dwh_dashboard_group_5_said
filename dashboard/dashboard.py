import streamlit as st
from connect_data_warehouse import query_job_listings
import matplotlib.pyplot as plt


def layout():
    st.set_page_config(layout="wide")
    st.title("Data engineering job ads")
    st.write("This data shows data engineering job ads from arbetsförmedlingens API")
    cols = st.columns(2)
    with cols[0]:
        tabel_options = {
            "Yrken med social inriktning": "marts.mart_social_job",
            "Yrken med teknisk inriktning": "marts.mart_technical_jobs",
            "Chefer och verksamhetsledare": "marts.mart_managers_job"
        }
        table = st.selectbox("Välj tabell", options=list(tabel_options.keys()))
        
        table = tabel_options[table]

        df = query_job_listings(tabel_name=table)

    st.write("### KPI's")
    cols = st.columns(3)

    with cols[0]:
        st.metric("Antal annonser", value=df["VACANCIES"].sum(), border=True)

    with cols[1]:
        st.metric(label="Totalt i Stockholm", value = df.query("WORKPLACE_ADDRESS__MUNICIPALITY == 'Stockholm'")["VACANCIES"].sum(), border=True)

    with cols[2]:
        top_employer = df.groupby("EMPLOYER__NAME")["VACANCIES"].sum().sort_values(ascending=False).head(1)
        st.metric(label="Top 1 Arbetsgivare", value=top_employer.index[0], border=True)

    cols = st.columns(2)
    with cols[0]:
            st.markdown("### Per yrkes grupp  topp 5")

            top_job_bar = (
                df.groupby("OCCUPATION_GROUP")["VACANCIES"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .reset_index()
            )

            plt.figure(figsize=(9, 4))
            plt.barh(top_job_bar["OCCUPATION_GROUP"], top_job_bar["VACANCIES"], color="#77a4c4")
            plt.gca().invert_yaxis()
            plt.xlabel("Antal annonser", color="white", size=14)
            plt.ylabel("Occupation Group", color="white", size=14)
            plt.xticks(color="white")
            plt.yticks(color="white")

            st.pyplot(plt,transparent=True)

    st.write("### Hitta job")
    cols = st.columns(2)
    with cols[0]:
        municipality = st.selectbox("Välj stad", options=sorted(df["WORKPLACE_ADDRESS__MUNICIPALITY"].dropna().unique()))
    
    with cols[1]:
        employer_name = st.selectbox("Välj arbetsgivare", sorted(df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @municipality")["EMPLOYER__NAME"].dropna().unique()))
        df_filtered = df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @municipality and EMPLOYER__NAME == @employer_name")

    cols = st.columns(2)
    with cols[0]:
        st.metric(label="Totalta job", value = df_filtered["VACANCIES"].sum(), border=True)
    
    with cols[1]:
        top_jobs = (
        df_filtered.groupby("OCCUPATION_GROUP")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
        st.dataframe(top_jobs,hide_index=True)


    with st.expander("Se all data"):
        st.dataframe(df)

if __name__ == "__main__":
    layout()