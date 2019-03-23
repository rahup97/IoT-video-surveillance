from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from flask_mysqldb import MySQL
from connectdb import connection
import graphPlot
 
app = Flask(__name__)
mysql = MySQL(app)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('graphs.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    c, conn = connection()
    c.execute("SELECT password FROM users WHERE user_id = (%s)", request.form['username'])
    data = c.fetchone()[0]
    print(data)
    if request.form['password'] == data: #and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout", methods = ['POST'])
def logout():
    session['logged_in'] = False
    return home()

@app.route("/graph1", methods = ['POST'])
def show_graph1():
    graphPlot.plot1()
    return home()

@app.route("/graph2", methods = ['POST'])
def show_graph2():
    graphPlot.plot2()
    return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=4000)
