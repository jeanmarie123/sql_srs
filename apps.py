# pylint: disable=missing-mule-docstring

import os
import logging
import duckdb
import streamlit as st
from datetime import date, timedelta, datetime

if "data" not in os.listdir():
    print("creating floder data")
    logging.error(os.listdir())
    logging.error("creating floder data")
    os.mkdir("data")

if "exercises_sql_table.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    #subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database = "data/exercises_sql_table.duckdb", read_only = False)


def check_users_solution(con, solution_df, user_query):
    """
    checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    :return:
    """

    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
    except KeyError as e:
        st.write("Some columns have missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"reslut has {n_lines_difference} lines diffrence with the solution"
        )


"""
    Cette partie perme de créer un selecteur et permettrait à l'utilisateur de choisir un theme.

"""
with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state_df").df()
    theme = st.selectbox(
        "What would you like review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a them...",
    )
    if theme:
        st.write("You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state_df WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state_df"

    
    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop = True)
    )

    st.write(exercise)
    
    # Cette partie permet d'affichier la solution de l'exercice
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df() 


st.header("Enter your code : ")
query = st.text_area(label="Votre code ici", key="user_input")


if query:
    check_users_solution(con, solution_df, query)

for n_days in [2, 7, 21]:
    if st.button(f"revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days = n_days)
        con.execute(f"UPDATE memory_state_df SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'")
        st.rerun()

if st.button('Reset'):
    con.execute(f"UPDATE memory_state_df SET last_reviewed = '1970-01-01'")
    st.rerun()




tab2, tab3 = st.tabs(["Tables", "Solutions"])


with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer) 

con.close() 
