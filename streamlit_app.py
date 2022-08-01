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

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else: 
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  with cnx.cursor() as cur:
    cur.execute("select * from fruit_load_list")
    return cur.fetchall()

if streamlit.button("Get Fruit Load List"):
  cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  data_row = get_fruit_load_list()
  streamlit.dataframe(data_row)

def insert_row_snowflake(new_fruit):
  with cns.cursor() as cur:
    cur.execute("insert into fruit_load_list values('from streamlit')")
    return "Thanks for adding" + new_fruit

add_fruit = streamlit.text_input("What fruit would you like to add ?")
if streamlit.button("Add a fruit to the list"):
  cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_snowflake(add_fruit))


