import sqlite3
from flask import Flask, render_template, g

PATH = 'db/jobs.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connecttion = g._connection = sqlite3.connect(PATH)
        
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.exexute(sql, values)
    if commit == True:
        result = connection.commit()
    else:
        result = cursor.fetchone() if single else cursor.fetchall()
    
    cursor.close()
    return result

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close() 
        
    
@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')  