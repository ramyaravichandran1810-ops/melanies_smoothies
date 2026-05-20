import streamlit as st
from snowflake.snowpark.context import get_active_session

# Snowflake session
session = get_active_session()

st.title("Customize your Smoothie")

st.write(
    """Replace this example with your own code!
And if you're new to Streamlit, check out docs.streamlit.io."""
)

# Fruit selection
option = st.selectbox(
    "choose a fruit:",
    ("Strawberry", "Banana", "Mango", "Pineapple")
)

st.write("you selected:", option)

# Name input
name_on_smoothie = st.text_input("Name on smoothie")

st.write("The name on the smoothie will be:", name_on_smoothie)

# Fetch data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Build insert logic
if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

    st.write("Selected ingredients:", ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients)
    VALUES ('{ingredients_string}')
    """

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! 🎉")
