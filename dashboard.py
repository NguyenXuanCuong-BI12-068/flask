from flask import Flask,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy


def Dashboard(username):

    return render_template('dashboard.html', username= username)