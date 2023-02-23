import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = "SecondCar",
                   page_icon = ":bae_chart:",
                   layout = "wide"
)

data = pd.read_csv("SecondCar.csv")

# Missing Value Treatment

for col in data.columns:
    if data[col].dtype == "int32" or data[col].dtype == "int64" or data[col].dtype == "float32" or data[col].dtype == "float64":
        median = data[col].median()
        data[col].fillna(median, inplace = True)
    else:
        data = data.fillna(data.mode().iloc[0])

# Feature Engineering

data["company_name"] = data["name"].str.split(" ").str[0]

# Feature Engineering for KM

km_ranges = ["low", "medium", "High"]
limits = [0, 35000, 100000, 200000]
data["km_range"] = pd.cut(data["km_driven"], bins = limits, labels = km_ranges)

# Feature Engineering for Years

year_ranges = ["Junk", "Scrap", "Buy", "Best"]
limits = [1991, 2005, 2012, 2017, 2022]
data["year_range"] = pd.cut(data["year"], bins = limits, labels = year_ranges)

# Feature Engineering for ex Showroom Price

ex_range = ["Affordable", "Family", "Luxary", "Premium"]
limits = [0, 500000, 1000000, 1500000, 20000000]
data["ex_range"] = pd.cut(data["ExShowroom Price"], bins = limits, labels = ex_range)

df = data.copy()

#st.dataframe(df)

# ------------ SIDE BAR ------------
st.sidebar.header("Please Filter Here : ")

company_name = st.sidebar.multiselect(
    "Select Company Name: ",
    options = df["company_name"].unique()
)

km_range = st.sidebar.multiselect(
    "Select Kilometer Range: ",
    options = df["km_range"].unique()
)

df_selection = df.query(
    "company_name == @company_name & km_range == @km_range"
)

st.dataframe(df_selection)

#--- Hide Streamlit Style -----
hide_st_style = """ 
          <style>
          #MainMenu {visibility: hidden;}
          footer {visibility: hidden;}
          header {visibility: hidden;}
          </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)



