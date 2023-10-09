import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My Parents New Healthy Dinner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
#write data to the screen with text
# streamlit.text(fruityvice_response.json()) 
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try :
  # Input by textbox
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    # streamlit.write('The user entered ', fruit_choice)
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # normalize json response
    # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # use function
    back_from_function = get_fruityvice_data(fruit_choice)
    # output to screen table
    # streamlit.dataframe(fruityvice_normalized)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

def get_fuit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fuit_load_list()
  streamlit.dataframe(my_data_rows)



def insert_fruit_load_list(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
    return "thanks to adding"+new_fruit
# add button to load fruit
add_new_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button('add a fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_fruit_load_list(add_new_fruit)
  streamlit.text(back_from_function)

  

streamlit.stop()
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
# select firts row
# my_data_row = my_cur.fetchone()
# select all row
# my_data_rows = my_cur.fetchall()
# streamlit.header("The Fruit Load List Contains:")
# streamlit.dataframe(my_data_rows)

snowflake_choice = streamlit.text_input('What fruit would you like information about?','Jackfruit')
streamlit.write('thanks to add', snowflake_choice)
snowflake_response = requests.get("https://fruityvice.com/api/fruit/"+snowflake_choice)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
