import sqlite3

# create a connection to the database
connection = sqlite3.connect('jobs.db')

# create a cursor object
cursor = connection.cursor()

# create a table
table_info = '''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    if_remote BOOLEAN,
    if_onsite BOOLEAN,
    if_hybrid BOOLEAN,
    description TEXT,
    min_salary_range INTEGER,
    max_salary_range INTEGER
)
'''
cursor.execute(table_info)

# insert data into the table
cursor.execute('''INSERT INTO jobs (title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range) VALUES ('Software Engineer', 'Google', True, False, False, 'Developing and maintaining software applications', 100000, 150000)''')
cursor.execute('''INSERT INTO jobs (title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range) VALUES ('Data Scientist', 'Amazon', False, True, False, 'Analyzing and interpreting data to drive business decisions', 120000, 180000)''')
cursor.execute('''INSERT INTO jobs (title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range) VALUES ('Product Manager', 'Apple', True, False, True, 'Defining product strategy and roadmap', 110000, 160000)''')
cursor.execute('''INSERT INTO jobs (title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range) VALUES ('UX/UI Designer', 'Facebook', False, True, False, 'Creating intuitive user experiences', 90000, 140000)''')
cursor.execute('''INSERT INTO jobs (title, company, if_remote, if_onsite, if_hybrid, description, min_salary_range, max_salary_range) VALUES ('Project Manager', 'Microsoft', True, False, True, 'Overseeing project timelines and deliverables', 105000, 155000)''')

# display the data
cursor.execute('''SELECT * FROM jobs''')
data = cursor.fetchall()
print('Data inserted successfully')
for row in data:
    print(row)

# commit the changes and close the connection
connection.commit()
connection.close()