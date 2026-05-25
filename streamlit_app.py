import streamlit as st
import snowflake.connector
import pandas as pd

st.title("Customize Your Smoothie! 🍓")

# Create Snowflake connection
conn = snowflake.connector.connect(
    user="ACME_ADMIN",
    password="YOUR_PASSWORD",
    account="atxug04702.australia-southeast2.gcp",
    warehouse="COMPUTE_WH",
    database="SMOOTHIES",
    schema="PUBLIC"
)

# Name input
name_on_smoothie = st.text_input("Name on Smoothie:")

if name_on_smoothie:
    st.write("The name on your Smoothie will be:", name_on_smoothie)

# Fetch ingredients
query = "SELECT INGREDIENT_NAME FROM INGREDIENTS"
ingredients_df = pd.read_sql(query, conn)

ingredients_list = ingredients_df["INGREDIENT_NAME"].tolist()

# Multi-select (max 5)
selected_ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    ingredients_list,
    max_selections=5
)

# Show selection
if selected_ingredients:
    st.write("You selected:", selected_ingredients)

# Button
if st.button("Create Smoothie"):
    if name_on_smoothie and selected_ingredients:
        st.success(f"Smoothie for {name_on_smoothie} created with {selected_ingredients}")
    else:
        st.warning("Please enter name and select ingredients")
