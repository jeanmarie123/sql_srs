import streamlit as st
import pandas as pd 
import duckdb  

st.write(""" 
         # SQL SRS
         SPaced repetition SQL practice """)

# Ici on crée un selecteur qui va permettre à l utilisateur de faire son choix
option = st.selectbox( 
    'What would you like review?',
    ('Joins', 'Group by', 'Windows function'),
    index=None,
    placeholder="Select a them...",
    )

st.write('You selected:', option)

data = {'a': [1, 2, 3],
        'b': [4, 5, 6]}


df = pd.DataFrame(data)


tab1, tab2, tab3 = st.tabs(['Cat', 'Dog', 'Owl'])
with tab1:
    # On demande a l utilisateur d entrer sa requette sql
    sql_query = st.text_area(label = "entrer votre input")
    resulte = duckdb.query(sql_query).df()
    st.write(f"Vous avez entrer la variable suivante : {sql_query}")
    # pour affichier le dataframe
    st.dataframe(resulte)  

    #st.header("A Cat")
    #st.image("https://static.streamlit.io/examples/cat.jpg", width = 200)

with tab2:
    st.header("A Dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width = 200)

with tab3:
    st.header("A Owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width = 200)