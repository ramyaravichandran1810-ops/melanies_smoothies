import streamlit as st

# Snowflake connection (Streamlit managed)
conn = st.connection("snowflake")
session = conn.session()

st.title("Customize your Smoothie 🍓")

# Fruit selection
option = st.selectbox(
    "Choose a fruit:",
    ("Strawberry", "Banana", "Mango", "Pineapple")
)
st.write("You selected:", option)

# Name input
name_on_smoothie = st.text_input("Name on Smoothie")
st.write("Name on your smoothie:", name_on_smoothie)

# Load Snowflake table
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select("FRUIT_NAME")
st.dataframe(my_dataframe)

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Insert order
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)

    if st.button("Submit Order"):
        session.sql(f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS)
            VALUES ('{ingredients_string}')
        """).collect()

        st.success("Your Smoothie Order is Placed! 🎉")
