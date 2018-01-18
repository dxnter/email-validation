import re, os
from flask import Flask, render_template, redirect, request, session, flash, url_for
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = os.urandom(24)
mysql = MySQLConnector(app, 'emails')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', request.form['email'])
    
    if match == None:
        flash("Email is not valid!")
        return redirect('/')
    session['email'] = request.form['email']
    query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
    data = {
        'email': session['email']
    }
    mysql.query_db(query, data)
    return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT * FROM emails ORDER BY created_at DESC"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails=emails)
app.run(debug=True)