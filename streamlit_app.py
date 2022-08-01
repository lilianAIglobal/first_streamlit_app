import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

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

streamlit.stop()

cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
cur = cnx.cursor()
cur.execute("SELECT * from fruit_load_list")
data_row = cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(data_row)

add_fruit = streamlit.text_input("What fruit would you like to add ?")
streamlit.write("Thanks for adding", add_fruit)

cur.execute("insert into fruit_load_list values('from streamlit')");

