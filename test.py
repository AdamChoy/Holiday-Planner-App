import streamlit as st

st.title("Holiday Planner")
st.write("Test")

# Budget slider
budget = st.slider(
    "What is your max budget? (£)",
    min_value=0,
    max_value=10000,
    value=1000,
    step=50
)

days = st.number_input("Number of days", min_value=1, value=7)
daily_budget = budget / days
st.write("Your daily budget is",daily_budget)

origin_airport = st.text_input("Origin airport")
start_date, end_date = st.date_input(
    "Select your travel dates",
    value=()
)

st.write("Start date:", start_date)
st.write("End date:", end_date)