import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS user (id int, username text, password text)"

cursor.execute(create_table)

user = (1,"john","abc")

insert_query = "INSERT INTO user VALUES(?,?,?)"

cursor.execute(insert_query,user)

users = [
	(2,"david","xyz"),
	(3,"rolf","pqr")
]

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM user"

list = []
for row in cursor.execute(select_query):
	list.append(row)

connection.commit()

connection.close()

print(type(list[0]))