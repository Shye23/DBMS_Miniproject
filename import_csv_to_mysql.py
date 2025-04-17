import pandas as pd
import mysql.connector

# Load CSV
df = pd.read_csv('IndianHealthyRecipe.csv')

# Replace NaN with None (important!)
df = df.where(pd.notnull(df), None)

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Shweta@23*',
    database='recipe'
)
cursor = conn.cursor()

# Insert data row by row
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO recipes 
        (dish_name, description, spice, prep_time, views, rating, number_of_votes, serves, dietary_info, cook_time, ingredients, instructions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            row['Dish Name'],
            row['Description'],
            row['Spice'],
            row['Prep Time'],
            None if pd.isna(row['Views']) else int(row['Views']),
            None if pd.isna(row['Rating']) else float(row['Rating']),
            None if pd.isna(row['Number of Votes']) else int(row['Number of Votes']),
            None if pd.isna(row['Serves']) else int(row['Serves']),
            row['Dietary Info'],
            row['Cook Time'],
            row['Ingredients'],
            row['Instructions']
        )
    )


conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into MySQL successfully.")
