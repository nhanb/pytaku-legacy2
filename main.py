#!/usr/bin/env python
import webapp2
from handlers import index


app = webapp2.WSGIApplication([
    ('/', index.IndexHandler)
], debug=True)
