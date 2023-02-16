from flask import Flask, render_template, request, redirect, url_for, flash, session, g, Response
from flaskext.mysql import MySQL
from flask_session import Session
from db import insert, insert_id, select, update, delete
from datetime import timedelta
from dotenv import load_dotenv

import bcrypt
import os

load_dotenv()


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')

mysql = MySQL()
secret_key = os.urandom(24)
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)
mysql = MySQL()
mysql.init_app(app)


conn = mysql.connect()


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/home')
def home():
    if session.get('username', None) is not None:
        username = session['username'].strip()

        select_sql = 'SELECT user_id FROM users WHERE username = %s'
        data_user_name = [username]
        result = select(conn, select_sql, data_user_name)

        if len(result) > 0:
            user_id = str(result[0][0])

            select_sql = ("""
                        SELECT c.contact_id, c.fullname, c.email, c.phone
                        FROM contacts c LEFT JOIN user_contacts uc ON c.contact_id = uc.contact_id
                        LEFT JOIN users u ON uc.user_id = u.user_id
                        WHERE u.user_id = %s""")
            data_user_id = [user_id]

            contacts_result = select(conn, select_sql, data_user_id)

            return render_template('index.html', contacts=contacts_result)
        else:
            return render_template('index.html', contacts=[])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip().encode()

        select_sql = 'SELECT * FROM users WHERE username = %s'
        data = username
        print(data)
        result = select(conn, select_sql, data)
        print(result)

        if (len(result) > 0):
            user_result = result[0]
            if (bcrypt.checkpw(password, user_result[3].encode())):
                session['username'] = username
                session['password'] = password
                return redirect(url_for('home'))
            else:
                flash('There was a problem with your login.')
                return render_template('login.html')
        else:
            flash('There was a problem with your login.')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        select_sql = 'SELECT * FROM users'
        users = select(conn, select_sql, [])

        for user in users:
            if user[1] == username:
                flash('That username is already taken.')
                return redirect(url_for('register'))
            if user[2] == email:
                flash('Your email is already registered.')
                return redirect(url_for('register'))

        hashed_password = get_hashed_password(password.encode())

        insert_sql = 'INSERT INTO users (username,email,password) VALUES (%s,%s,%s)'
        data = (username, email, hashed_password)
        insert(conn, insert_sql, data)

        session['username'] = username
        session['password'] = password
        print(session['username'])
        print(session['password'])

        return redirect(url_for('home'))


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if (request.method == 'POST'):
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        insert_sql = 'INSERT INTO contacts (fullname, email, phone) VALUES (%s,%s,%s)'
        data = (fullname, email, phone)

        newTaskId = insert_id(conn, insert_sql, data)

        actualUsername = session['username']

        select_sql = 'SELECT user_id FROM users WHERE username =  %s'
        data = actualUsername
        userId = select(conn, select_sql, data)[0][0]

        insert_sql = 'INSERT INTO user_contacts (user_id, contact_id) VALUES (%s,%s)'
        data = (str(userId), str(newTaskId))
        insert(conn, insert_sql, data)

        flash('Contact Added Successfully')

        return redirect(url_for('home'))


@app.route('/edit/<id>')
def get_contact(id):
    select_SQL = 'SELECT * FROM contacts WHERE contact_id = %s'
    data = id
    result = select(conn, select_SQL, data)
    return render_template('edit-contact.html', contact=result[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        update_sql = "UPDATE contacts SET fullname = %s,email = %s, phone = %s WHERE contact_id = %s"
        data = (fullname, email, phone, id)
        update(conn, update_sql, data)

        flash('Contact Updated Successfully')
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):

    delete_sql = 'DELETE FROM contacts WHERE contact_id = %s'
    data = id
    delete(conn, delete_sql, data)

    flash('Contact Removed Successfully')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
