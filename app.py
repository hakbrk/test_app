# Import required libraries
# import os
# from random import randint

# import plotly.plotly as py
# from plotly.graph_objs import *

# import flask
import pandas as pd
import dash
import smop
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
import dash_html_components as html
import mysql.connector
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
mydb = mysql.connector.connect(
  host="us-cdbr-east-06.cleardb.net",
  user="b299c42f0fdf61",
  passwd="fcdc6acd",
  database="heroku_826bb11c8d537f8"
)
# text = print(mydb)
# Put your Dash code here

mycursor = mydb.cursor()
query = """SELECT * FROM equity_history"""
test = pd.read_sql_query(query, mydb)
equity_list = test["ticker"].unique().tolist()
print(equity_list)



app.layout = html.Div(children=[
   


    html.Label(equity_list, id='test_text')
])


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
