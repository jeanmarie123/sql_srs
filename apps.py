import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3  
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()


# Ici on crée un selecteur qui va permettre à l utilisateur de faire son choix
with st.sidebar:
    option = st.selectbox(
        "What would you like review?",
        ("Joins", "Group by", "Windows function"),
        index=None,
        placeholder="Select a them...",
    )
    st.write("You selected:", option)


st.header("Enter your code : ")
query = st.text_area(label="Votre code ici", key="user_input")
if query:
    result = duckdb.query(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        # replace with try = result[solution.columns]
        st.write("Some columns have missing")
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns have missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(f"reslut has {n_lines_difference} lines diffrence with the solution")


tab2, tab3 = st.tabs(["Tables", "Solutions"])


with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.write(food_items)
    st.write("excepted")
    st.write(solution_df)

with tab3:
    st.write(ANSWER_STR)
