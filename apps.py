# pylint: disable=missing-mule-docstring

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating floder data")
    logging.error(os.listdir())
    logging.error("creating floder data")
    os.mkdir("data")

if "exercises_sql_table.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    #subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database = "data/exercises_sql_table.duckdb", read_only = False)


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
    result = con.execute(query).df()
    st.dataframe(result)
 
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer) 

con.close() 
