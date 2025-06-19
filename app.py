from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        student_class TEXT,
                        email TEXT
                    )''')
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        student_class = request.form['student_class']
        email = request.form['email']

        conn = sqlite3.connect('data.db')
        conn.execute('INSERT INTO entries (name, student_class, email) VALUES (?, ?, ?)',
                     (name, student_class, email))
        conn.commit()
        conn.close()

        return "✅ Entry saved successfully!"
    
    return render_template('form.html')

@app.route('/entries')
def show_entries():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, student_class, email FROM entries')
    rows = cursor.fetchall()
    conn.close()
    return render_template('entries.html', entries=rows)

import csv
from flask import Response

@app.route('/export')
def export_csv():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, student_class, email FROM entries')
    rows = cursor.fetchall()
    conn.close()

    # Create CSV response
    def generate():
        yield 'Name,Class,Email\n'
        for row in rows:
            yield ','.join(row) + '\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=entries.csv"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
