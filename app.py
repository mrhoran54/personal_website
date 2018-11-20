#!/usr/bin/python
#from flask import Flask, Response, render_template, url_for, send_from_directory, session, g

import os
import json
import pprint

from flask import url_for, session, redirect, jsonify, render_template, send_from_directory
from flask_oauthlib.client import OAuth

from flask import request as xx
import requests as yy

import urllib.parse
from urllib.parse import urlencode
import flask_login as flask_login
import argparse
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


app.config.update(
    DEBUG = True,
)

CSRF_ENABLED = True

#forms that are used
class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    fun_fact = StringField('fun fact', validators=[DataRequired()])
    #email = StringField('email', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    search_term = StringField('name', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])

    
class bar_searchForm(Form):
    drunk_level = StringField('drunk_level')
    area = StringField('area', validators=[DataRequired()])

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'
SEARCH_LIMIT = 5

#secret keys and things

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
# GOOGLEMAPS_KEY = app.config['GOOGLEMAPS_KEY'] 
# FACEBOOK_APP_ID = app.config['FACEBOOK_APP_ID']
# FACEBOOK_APP_SECRET = app.config['FACEBOOK_APP_SECRET']


#
@app.route('/')
@app.route('/index')

def index():
    return render_template('homepage.html',
                            title='Home')

#--------------------------------------
#error handling
#-------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return render_template('unauth.html')


#--------------------------------------
#views
#-------------------------------------

# @app.route('/logout')
# @flask_login.login_required
# def logout():
# #    #uid = (flask_login.current_user.id)
#     flask_login.logout_user()
#     return render_template('homepage.html')

# @app.route('/search', methods=['GET','POST'])
# @flask_login.login_required
# def search():
#      form = SearchForm()
#      # in the database
#      uid = (flask_login.current_user.id)
#      if form.validate_on_submit():
        
#         search_term = form.search_term.data
#         location = form.location.data
        
#         test1 = yelpdb.find_one({"search":search_term})
#         test2 = yelpdb.find_one({"location":location})
#         if(test1 and test2):
#             ("already in the database")
#             print(test1)
#             return render_template('index.html',
#                             search_term = search_term,
#                             results = test2)
            
#         else:
#             print("not in the database yet")
#             results = query_api(search_term, location)#query_api(search_term, location)
#             new_post = {"search": search_term,
#                             "location": location,
#                             "rest1":results[1],
#                             "rest2": results[2],
#                             "rest3": results[3],
#                             "rest4": results[4]}
#             yelpdb.insert(new_post)
#             test4 = yelpdb.find_one({"location":location})
            
#             if(test4):
#                 return render_template('index.html',
#                         search_term = search_term,
#                         results = test4)

#      return render_template('search.html',
#                             title='Search',
#                             form = form)
#
# def getuseridfromemail(email):
#     uid = users.find_one({"email":'bob.test.com'}, {'username':1})
#     return uid
#     #cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
#     #return cursor.fetchone()[0]


def isemailUnique(email):

    #use this to check if a email has already been registered
    find_user = users.find_one({"email":email})
    if find_user:
        #this means there are greater than zero entries with that email
        return False
    else:
        return True


@app.route("/photos_view")
def photos_view():

    return render_template('photos.html')



#--------------------------------------
#yelp authentication
#--------------------------------------

# import sys

# def obtain_bearer_token(host, path):
#     """Given a bearer token, send a GET request to the API.
#     """
#     url = '{0}{1}'.format(host, urllib.parse.quote(path.encode('utf8')))
#     #assert CLIENT_ID, "Please supply your client_id."
#     #assert CLIENT_SECRET, "Please supply your client_secret."
#     data = urllib.parse.urlencode({
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'grant_type': GRANT_TYPE,
#     })
#     headers = {
#         'content-type': 'application/x-www-form-urlencoded',
#     }
#     response = yy.request('POST', url, data=data, headers=headers)
#     bearer_token = response.json()['access_token']
#     return bearer_token
# #
# def request(host, path, bearer_token, url_params=None):

#     url_params = url_params or {}
#     url = '{0}{1}'.format(host, urllib.parse.quote(path.encode('utf8')))
#     headers = {
#         'Authorization': 'Bearer %s' % bearer_token,
#     }

#     print(u'Querying {0} ...'.format(url))

#     response = yy.request('GET', url, headers=headers, params=url_params)

#     return response.json()

# def search(bearer_token, term, location):

#     url_params = {
#         'term': term.replace(' ', '+'),
#         'location': location.replace(' ', '+'),
#         'limit': SEARCH_LIMIT
#     }
#     return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)

# def get_business(bearer_token, business_id):

#     """Query the Business API by a business ID.
#     Args:
#         business_id (str): The ID of the business to query.
#     Returns:
#         dict: The JSON response from the request.
#     """
#     business_path = BUSINESS_PATH + business_id
#     return request(API_HOST, business_path, bearer_token)
# #
# def query_api(term, location):

#     bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
#     response = search(bearer_token, term, location)
#     businesses = response.get('businesses')

#     if not businesses:
#         x = (u'No businesses for {0} in {1} found.'.format(term, location))
#         return x

#     business_id = businesses[0]['id']
#     array_ret = [None]*SEARCH_LIMIT

#     for i in range(SEARCH_LIMIT):

#         business_id = businesses[i]['id']
#         business_name = businesses[i]['name']
#         business_pic = businesses[i]['image_url']
#         business_price = businesses[i]['price']
#         business_rating = businesses[i]['rating']

#         array_ret[i] = (business_id,business_name,business_pic,business_price,str(business_rating))

#     print(u'{0} businesses found, querying business info ' \
#         'for the top result "{1}" ...'.format(
#             len(businesses), business_id))
#     response = get_business(bearer_token, business_id)

#     print(u'Result for business "{0}" found:'.format(business_id))
#     #pprint.pprint(response, indent=2)
#     return(array_ret)

# def search2(bearer_token, term, location):

#     url_params = {
#         'term': term.replace(' ', '+'),
#         'location': location.replace(' ', '+'),
#         'limit': 20
#     }
#     return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)

# zips = [
#     "West Roxbury","Jamaica Plain","South Boston","South End","Mission Hill","Fenway",
#     "Back Bay","Downtown","Charlestown", "Brighton", "Allston", "Cambridge","Harvard Square","Somerville","Davis Square" 
# ]
# def query_api_2():

#     bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
#     response = search2(bearer_token, "bars", "Davis Square")
#     businesses = response.get('businesses')

#     if not businesses:
#         x = (u'No businesses for {0} in {1} found.'.format(term, location))
#         return x

#     business_id = businesses[0]['id']
#     array_ret = [None]*20

#     for i in range(20):

#         business_url = businesses[i]['url']
#         business_name = businesses[i]['name']
#         business_long = businesses[i]['coordinates']['longitude']
#         business_lat = businesses[i]['coordinates']['latitude']

#         array_ret[i] = (business_url,business_name,business_long,business_lat)

#     print(u'{0} businesses found, querying business info ' \
#         'for the top result "{1}" ...'.format(
#             len(businesses), business_id))
#     response = get_business(bearer_token, business_id)

#     print(u'Result for business "{0}" found:'.format(business_id))
#     #pprint.pprint(response, indent=2)
#     return(array_ret)



if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
