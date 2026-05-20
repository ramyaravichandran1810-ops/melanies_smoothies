import streamlit as st
from snowflake.snowpark import Session

# -------------------------
# SNOWFLAKE CONNECTION
# -------------------------
connection_parameters = {
    "account": "YOUR_ACCOUNT",
    "user": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "role": "YOUR_ROLE",
    "warehouse": "YOUR_WAREHOUSE",
    "database": "smoothies",
    "schema": "public"
}

session = Session.builder.configs(connection_parameters).create()

# -------------------------
# STREAMLIT UI
# -------------------------
st.title("Customize your Smoothie")

option = st.selectbox(
    "choose a fruit:",
    ("Strawberry", "Banana", "Mango", "Pineapple")
)

st.write("you selected:", option)

name_on_smoothie = st.text_input("Name on smoothie")
st.write("The name on the smoothie will be:", name_on_smoothie)

# -------------------------
# SNOWFLAKE DATA
# -------------------------
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select("FRUIT_NAME")

st.dataframe(my_dataframe)

# -------------------------
# MULTI SELECT INGREDIENTS
# -------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# -------------------------
# INSERT ORDER
# -------------------------
if ingredients_list:
    ingredients_string = ""

    for fruit in ingredients_list:
        ingredients_string += fruit + ", "

    st.write("Selected ingredients:", ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients)
    VALUES ('{ingredients_string}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! 🎉")
