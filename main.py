#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, os, jinja2

from google.appengine.api import users
from google.appengine.ext import ndb #Cloud storage

#Say where you are keeping your HTML templates for Jinja2
template_directory = os.path.join(os.path.dirname(__file__), 'templates')
#Create a Jinja environment object by passing it the template location
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory))

class Person(ndb.Model):
    name = ndb.StringProperty() #Must specify the attribute type
    age = ndb.IntegerProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # BEGIN NDB EXAMPLE
        new_user = Person(name = "Bob") #create a Person object
        user_key = new_user.put() #put() returns a key and stores the object
        # NOTE: you must keep track of the keys
        type = user_key.kind()
        user_return = user_key.get()
        user_name = user_return.name
        # END NDB EXAMPLE

        items = ["Hello", 1, 2, "Bye"]

        # BEGIN USERS EXAMPLE
        user = users.get_current_user() #Check if logged in or not

        if user: # true if user is loggedin
            nickname = user.nickname() #In this case, email

            url = users.create_logout_url('/')
            url_text = "logout"

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(url = url, url_text = url_text, kind = type, name = user_name, items = items))

        else:
            url = users.create_login_url('/')
            url_text = "login"
        # END USERS EXAMPLE

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(url_text = url_text, url = url))

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        greeting = "Hello"
        self.response.out.write(template.render(greeting = greeting))

class OutputHandler(webapp2.RequestHandler):
    def post(self):
        data = self.request.get('userInput')

        template = jinja_environment.get_template('output.html')
        self.response.out.write(template.render(data =data))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/output', OutputHandler)
], debug=True)
