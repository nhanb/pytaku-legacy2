#!/usr/bin/env python
import webapp2
import os
import sys

# Add project root to PATH
path = os.path.dirname(__file__)
sys.path.append(path)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
