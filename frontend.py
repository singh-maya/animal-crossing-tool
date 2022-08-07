import streamlit as st
import pandas as pd
import main


def webby():
    st.write("Animal Crossing!")
    df = pd.read_csv("Venus.csv")
    st.dataframe(df)


webby()