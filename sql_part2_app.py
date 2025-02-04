import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GEMMA_API_KEY'))

connection = sqlite3.connect('jobs.db')
cursor = connection.cursor()

st.set_page_config(page_title='Search DB Using Natural Language', page_icon=':job:')
st.title('Search DB Using Natural Language')

# function to load gemini and provide sql query as response
def get_sql_query_from_gemini(user_question):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    You are an expert in converting English questions to SQL query!
    The SQL database has the table jobs and has the following columns - 
    title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range
    
    Convert this question to a SQL query: {user_question}
    Example 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM jobs ;
    Example 2 - Tell me all the jobs that are remote?, 
    the SQL command will be something like this SELECT * FROM jobs WHERE if_remote = True;
    Example 3 - Tell me all the jobs that are paying more than 100000?,
    the SQL command will be something like this SELECT * FROM jobs WHERE min_salary_range > 100000;
    Example 4 - Tell me all the jobs that are paying more than 100000 and less than 150000?,
    the SQL command will be something like this SELECT * FROM jobs WHERE min_salary_range > 100000 AND max_salary_range < 150000;
    Example 5 - Tell me all the jobs that are about developing and maintaining software applications?,
    the SQL command will be something like this SELECT * FROM jobs WHERE description LIKE '%developing and maintaining%';
    Example 6 - How many jobs are software developer?,
    the SQL command will be something like this SELECT COUNT(*) FROM jobs WHERE title LIKE '%software developer%';
    
    Important: Return ONLY the SQL query without any markdown formatting, backticks, or 'sql' prefix.
    """
    response = model.generate_content(prompt)
    return clean_sql_query(response.text)

# Clean up any markdown formatting that might be in the gemini response
def clean_sql_query(response):
    # Remove markdown formatting, backticks, and 'sql' text
    cleaned = response.replace('```sql', '')
    cleaned = cleaned.replace('```', '')
    cleaned = cleaned.replace('`', '')
    # Remove any leading/trailing whitespace and newlines
    cleaned = cleaned.strip()
    return cleaned

# function to retreive query from the sql database
def get_data_from_sql_db(sql_query):
    cursor.execute(sql_query)
    data = cursor.fetchall()
    return data

# Setup UI
user_question = st.text_input('what you want to search in the database?')

# create a button to submit the question
if user_question:   
    sql_query = get_sql_query_from_gemini(user_question)
    st.write(f"Your SQL Query: {sql_query}")
    data = get_data_from_sql_db(sql_query)
    st.write(f"Your Result:")
    for row in data:
            st.write(row)


# commit the changes and close the connection
connection.commit()
connection.close()