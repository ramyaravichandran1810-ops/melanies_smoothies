import streamlit as st
import snowflake.connector
import pandas as pd

st.title("Customize Your Smoothie! 🍓")

# Snowflake connection (for your environment)
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

# Get ingredients
query = "SELECT INGREDIENT_NAME FROM INGREDIENTS"
ingredients_df = pd.read_sql(query, conn)

ingredients_list = ingredients_df["INGREDIENT_NAME"].tolist()

# Multi-select
selected_ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    ingredients_list,
    max_selections=5
)

# Submit
if st.button("Submit Order"):
    if name_on_smoothie and selected_ingredients:
        
        try:
            # Convert list to string
            ingredients_string = ", ".join(selected_ingredients)

            # Insert query
            insert_query = f"""
            INSERT INTO ORDERS (NAME, INGREDIENTS)
            VALUES ('{name_on_smoothie}', '{ingredients_string}')
            """

            cursor = conn.cursor()
            cursor.execute(insert_query)

            st.success(f"Your Smoothie is ordered, {name_on_smoothie}!")

        except Exception as e:
            st.error("Order failed — check table or connection")

    else:
        st.warning("Please enter name and select ingredients")
