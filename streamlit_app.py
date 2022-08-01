import streamlit
import pandas as pd
import requests
import snowflake.connector

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text("🍞🥑 Avocado toast")

streamlit.header("🍌🍓 Build your own fruit smoothie 🍉🍑")

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# put json into a table
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display the table
streamlit.dataframe(fruityvice_normalized)

cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
curr = cnx.cursor()
cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
data_row = cur.fetchone()
streamlit.text("Hello from Snowflakes")
streamlit.text(data_row)
