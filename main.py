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

from google.appengine.api import users #Google login
from google.appengine.ext import ndb #Cloud storage

#Say where you are keeping your HTML templates for Jinja2
template_directory = os.path.join(os.path.dirname(__file__), 'templates')
#Create a Jinja environment object by passing it the template location
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory))


class Person(ndb.Model): #Define a person class
    name = ndb.StringProperty() #Must specify the type the variable will be
    age = ndb.IntegerProperty() #NOTE: this does not give them a value

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # BEGIN NDB EXAMPLE
        new_user = Person(name = "Bob", age=12) #create a Person object
        other_user = Person(name = "Alice")

        user_key = new_user.put() #put() saves the object and returns a key

        type = user_key.kind() #check the class type (Person) of the key

        user_return = user_key.get() #get() will return the object

        user_name = user_return.name #get the name attribute of the Person object
        # END NDB EXAMPLE
        # NOTE: you must keep track of the keys to retrieve the object

        items = ["Hello", 1, 2, "Bye"]

        # BEGIN USERS EXAMPLE
        user = users.get_current_user() #Check if logged in or not

        if user: #true if user is logged in
            nickname = user.nickname() #nickname is email address before @

            url = users.create_logout_url('/') #url to redirect to once logged out
            url_text = "logout" #the href text that will show on index.html

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(url = url, url_text = url_text, kind = type, name = user_name, items = items))

        else:
            url = users.create_login_url('/') #url to redirect to once logged in
            url_text = "login"
        # END USERS EXAMPLE

            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(url_text = url_text, url = url))

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render())

class OutputHandler(webapp2.RequestHandler):
    def post(self): #Use post if you will be receiving information

        #'userInput' is also name in the textarea in about.html
        inputFromAbout = self.request.get('userInput')

        template = jinja_environment.get_template('output.html')
        self.response.out.write(template.render(data=inputFromAbout))

app = webapp2.WSGIApplication([ #dont forget the commas
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/output', OutputHandler)
], debug=True)
