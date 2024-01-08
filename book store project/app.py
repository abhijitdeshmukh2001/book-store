from flask import Flask, render_template, request,request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'books.db'

def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   bookname TEXT NOT NULL,
                   writer TEXT NOT NULL,
                   pages INTEGER NOT NULL
                    )''')
    connection.commit()
    connection.close()

@app.route("/")
def index():
    
      conn = sqlite3.connect('books.db')
      cursor = conn.cursor()

      cursor.execute("SELECT * from books")
      data = cursor.fetchall()
       
      conn.close()
      return render_template('allbooks.html', data=data)

@app.route("/add", methods=['GET', 'POST'])
def addbook():
     if request.method == 'POST':
        try:
            bookname = request.form['bookname']
            writer = request.form['writer']
            pages = request.form['pages']
            # Perform server-side validation
            if not bookname or not writer or not pages :
                return "All fields are required!"
            conn = sqlite3.connect('books.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE bookname = ?', (bookname,))
            existing_book = cursor.fetchone()
            if existing_book:
                conn.close()
                return "book already exists!"
            cursor.execute('INSERT INTO books (bookname, writer, pages) VALUES (?, ?, ?)',
                           (bookname, writer, pages))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except KeyError:
            return "Error: Missing or incorrect form data!"
     return render_template('add.html')
 

@app.route("/getbook",methods=['GET', 'POST'])
def getbook():
     if request.method == 'POST':
        try:
            bookname = request.form['bookname']
            writer = request.form['writer']
            pages = request.form['pages']
            # Perform server-side validation
            if not bookname or not writer or not pages :
                return "All fields are required!"
            conn = sqlite3.connect('books.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE bookname = ? AND writer = ? AND pages = ?', (bookname, writer, pages))
            existing_book = cursor.fetchone()
            if existing_book:
                    cursor.execute('DELETE FROM books WHERE bookname = ? AND writer = ? AND pages = ?', (bookname, writer, pages))
                    conn.commit()
                    conn.close()
                    return"Book gating successfully!", "success"
            else:
                    return"Book not found!", "error"
        except KeyError:
            return "Error: Missing or incorrect form data!"           
     return render_template('get.html')
 



if __name__ == '__main__':
    app.run(debug=True)


