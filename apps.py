import io

import duckdb
import pandas as pd
import streamlit as st

con = duckdb.connect(database = "data/exercises_sql_table.duckdb", read_only = False)




#ANSWER_STR = """
#SELECT * FROM beverages
#CROSS JOIN food_items
#"""
# solution_df = duckdb.sql(ANSWER_STR).df()


"""
    Cette partie perme de créer un selecteur et permettrait à l'utilisateur de choisir un theme.

"""
with st.sidebar:
    theme = st.selectbox(
        "What would you like review?",
        ("cross_joins", "Groupby", "window_functions"),
        index=None,
        placeholder="Select a them...",
    )
    st.write("You selected:", theme)
    exercise = con.execute(f"SELECT * FROM memory_state_df WHERE theme = '{theme}' ").df()
    st.write(exercise)


st.header("Enter your code : ")
query = st.text_area(label="Votre code ici", key="user_input")

"""
#if query:
#    result = duckdb.query(query).df()
#    st.dataframe(result)
#
#    if len(result.columns) != len(solution_df.columns):
#        # replace with try = result[solution.columns]
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

"""