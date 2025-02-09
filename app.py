import streamlit as st
from main import setup_query_engine

# Setup the query engine
st.title("Interactive Query Engine with Streamlit")
st.sidebar.header("Query Engine Setup")
st.sidebar.write("Loading query engine, please wait...")

# Initialize the query engine
query_engine = setup_query_engine()

# Streamlit user interface
query = st.text_input("Enter your query:")
if query:
    with st.spinner("Querying the engine..."):
        response = query_engine.query(query)
    st.write(f"**Answer:** {response}")