from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)   # MUST be before routes


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    search = request.args.get('search')

    if search:
        students = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR prn LIKE ? OR course LIKE ?",
            ('%' + search + '%', '%' + search + '%', '%' + search + '%')
        ).fetchall()
    else:
        students = conn.execute('SELECT * FROM students').fetchall()

    conn.close()
    return render_template('index.html', students=students)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        prn = request.form['prn']
        course = request.form['course']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO students (name, prn, course) VALUES (?, ?, ?)',
            (name, prn, course)
        )
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        prn = request.form['prn']
        course = request.form['course']

        conn.execute(
            'UPDATE students SET name = ?, prn = ?, course = ? WHERE id = ?',
            (name, prn, course, id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()

    return render_template('edit.html', student=student)


app.run(debug=True)
