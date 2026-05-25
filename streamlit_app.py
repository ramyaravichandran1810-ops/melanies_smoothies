import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title("Customize Your Smoothie! 🍓")

# Get Snowflake session (works ONLY inside Snowflake)
session = get_active_session()

# Name input
name_on_smoothie = st.text_input("Name on Smoothie:")

if name_on_smoothie:
    st.write("The name on your Smoothie will be:", name_on_smoothie)

# Fetch ingredients from Snowflake
ingredients_df = session.sql(
    "SELECT INGREDIENT_NAME FROM SMOOTHIES.PUBLIC.INGREDIENTS"
).to_pandas()

ingredients_list = ingredients_df["INGREDIENT_NAME"].tolist()

# Multi-select (max 5)
selected_ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    ingredients_list,
    max_selections=5
)

# Display selected
if selected_ingredients:
    st.write("You selected:", selected_ingredients)

# Button action
if st.button("Create Smoothie"):
    if name_on_smoothie and selected_ingredients:
        st.success(f"Smoothie for {name_on_smoothie} created with {selected_ingredients}")
    else:
        st.warning("Please enter name and select ingredients")
