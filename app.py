import streamlit as st
import pandas as pd

st.title("My First Streamlit App 🚀")
st.write("Welcome! This app displays a simple table.")

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [24, 30, 22]
})

st.table(data)
