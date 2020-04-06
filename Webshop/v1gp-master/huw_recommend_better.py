from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
import random

app = Flask(name)
api = Api(app)
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# We define these variables to (optionally) connect to an external MongoDB
# instance.
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop


# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the
# Recom class.
load_dotenv()
try:
    conn = psycopg2.connect("dbname=AI_gr user=postgres password=1")
    cur = conn.cursor()
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count, type, productid):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        if type == 5:
            cur.execute("SELECT id FROM populair; ")
            rows = cur.fetchall()
            res = [item[0] for item in rows]
            res = random.sample(res, count)
            return res, 200
        elif type == 1:
            return [], 200
        elif type == 2:
            return [], 200
        elif type == 3:
            return [], 200
        elif type == 4:
            return [], 200
        else:
            return [], 200


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<int:type>/<int:productid>")
