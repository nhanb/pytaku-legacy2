#!/usr/bin/env python
import webapp2
import os
from google.appengine.ext.webapp import template


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'apiSecret': 'mysecret',
            'apiPublic': 'mypublic',
            'username': 'NHAN',
        }
        path = os.path.join(os.path.dirname(__file__) + '/templates/', 'index.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug=True)
