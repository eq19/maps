from flask import render_template, flash, redirect
from app import app

@app.route('/')
@app.route('/index')
def index():
    api_data = [{'name': 'GDAX', "last_fetched":"tbd"}]
    
    return render_template('index.html', api_data=api_data)
