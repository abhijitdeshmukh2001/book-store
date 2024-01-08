
import sqlite3
#open database
conn = sqlite3.connect('books.db')
cursor = conn.execute("SELECT * from books")
print("ID\tBOOKNAME\tWRITER\t\tPAGES\t")
for row in cursor.fetchall():
   print(row)
conn.close()





