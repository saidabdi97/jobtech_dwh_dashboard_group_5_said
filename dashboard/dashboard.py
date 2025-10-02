# dashboard.py
import streamlit as st
import plotly.express as px
import pandas as pd
from connect_data_warehouse import query_job_listings

st.set_page_config(layout="wide", page_title="HR Dashboard")

# ---------- DATA ----------
TABLE_MAP = {
    "Yrken med social inriktning": "marts.mart_social_job",
    "Yrken med teknisk inriktning": "marts.mart_technical_jobs",
    "Chefer och verksamhetsledare": "marts.mart_managers_job",
}

@st.cache_data(ttl=300)
def get_df(table_name: str) -> pd.DataFrame:
    df = query_job_listings(tabel_name=table_name)
    # Säkerställ kolumner & typer som används i UI
    needed = [
        "VACANCIES",
        "EMPLOYER__NAME",
        "OCCUPATION_GROUP",
        "WORKPLACE_ADDRESS__MUNICIPALITY",
        "DRIVING_LICENSE_REQUIRED",
    ]
    for c in needed:
        if c not in df.columns:
            df[c] = pd.NA
    df["VACANCIES"] = pd.to_numeric(df["VACANCIES"], errors="coerce").fillna(0).astype(int)
    return df

# ---------- LAYOUT ----------
st.title("HR Dashboard")
st.caption("Automatiserad analys av arbetsmarknadsdata för smartare och snabbare rekrytering.")

# SIDOPANEL (alla filter här)
with st.sidebar:
    st.header("Filter")
    table_key = st.selectbox("Tabell", list(TABLE_MAP.keys()))
    top_n = st.slider("Top N", min_value=5, max_value=50, value=10, step=5)
    st.divider()
    st.caption("Tips: Exportera data längst ned i sidan.")

df = get_df(TABLE_MAP[table_key])

# ---------- KPI-KORT ----------
k1, k2, k3 = st.columns(3)
tot = int(df["VACANCIES"].sum())
stockholm = int(df.query("WORKPLACE_ADDRESS__MUNICIPALITY == 'Stockholm'")["VACANCIES"].sum())
top_emp_ser = (
    df.groupby("EMPLOYER__NAME")["VACANCIES"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

k1.metric("Antal annonser", f"{tot:,}".replace(",", " "))
k2.metric("Totalt i Stockholm", f"{stockholm:,}".replace(",", " "))
k3.metric("Top 1 arbetsgivare", top_emp_ser.index[0] if not top_emp_ser.empty else "—")

st.divider()

# ---------- HJÄLPFUNKTION DIAGRAM ----------
def barh_plot(data: pd.DataFrame, x: str, y: str, title: str):
    fig = px.bar(data, x=x, y=y, orientation="h")
    fig.update_layout(
        height=430, title=title,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title="Antal annonser", yaxis_title=None,
    )
    fig.update_yaxes(autorange="reversed")  # störst överst
    st.plotly_chart(fig, use_container_width=True)

# ---------- TABS MED DIAGRAM ----------
tab1, tab2, tab3, tab4 = st.tabs(["Arbetsgivare", "Yrkesgrupper", "Kommuner", "Körkort"])

with tab1:
    top_emp = (
        df.groupby("EMPLOYER__NAME")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    barh_plot(top_emp, "VACANCIES", "EMPLOYER__NAME", f"Top {top_n} arbetsgivare")

with tab2:
    top_occ = (
        df.groupby("OCCUPATION_GROUP")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    barh_plot(top_occ, "VACANCIES", "OCCUPATION_GROUP", f"Top {top_n} yrkesgrupper")

with tab3:
    top_city = (
        df.groupby("WORKPLACE_ADDRESS__MUNICIPALITY")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    barh_plot(top_city, "VACANCIES", "WORKPLACE_ADDRESS__MUNICIPALITY", f"Top {top_n} kommuner")

with tab4:
    lic = df[df["DRIVING_LICENSE_REQUIRED"] == True]
    top_lic = (
        lic.groupby("OCCUPATION_GROUP")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    barh_plot(top_lic, "VACANCIES", "OCCUPATION_GROUP", f"Top {top_n} med krav på körkort")

st.subheader("Hitta jobb")
c1, c2 = st.columns(2)

with c1:
    kommun = st.selectbox(
        "Kommun",
        sorted(df["WORKPLACE_ADDRESS__MUNICIPALITY"].dropna().unique()),
        index=0 if df["WORKPLACE_ADDRESS__MUNICIPALITY"].notna().any() else None,
    )

with c2:
    emp_opts = ["Alla"] + sorted(
        df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @kommun")["EMPLOYER__NAME"]
        .dropna()
        .unique()
        .tolist()
    )
    emp = st.selectbox("Arbetsgivare", emp_opts)

df_filt = df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @kommun")
if emp != "Alla":
    df_filt = df_filt.query("EMPLOYER__NAME == @emp")

m1, m2 = st.columns([1, 2])
with m1:
    st.metric("Totalt antal jobb", f"{int(df_filt['VACANCIES'].sum()):,}".replace(",", " "))
with m2:
    top5 = (
        df_filt.groupby("OCCUPATION_GROUP")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.dataframe(top5, hide_index=True, use_container_width=True)

with st.expander("Se all data / export"):
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.download_button(
        "Ladda ned CSV",
        df.to_csv(index=False).encode("utf-8"),
        "annonser.csv",
        "text/csv",
    )

if __name__ == "__main__":
    # Tillåter körning som 'streamlit run dashboard.py'
    pass
