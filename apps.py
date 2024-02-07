import streamlit as st
import pandas as pd 
import duckdb  
import io


csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3  
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution = duckdb.sql(answer).df()


# Ici on crée un selecteur qui va permettre à l utilisateur de faire son choix
with st.sidebar:
    option = st.selectbox( 
        'What would you like review?',
        ('Joins', 'Group by', 'Windows function'),
        index=None,
        placeholder="Select a them...",
        )
    st.write('You selected:', option) 


st.header("Enter your code : ")
query = st.text_area(label = "Votre code ici", key = "user_input")
if query:
    result = duckdb.query(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solutions"])


with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.write(food_items)
    st.write("excepted")
    st.write(solution)

with tab3:
    st.write(answer)


