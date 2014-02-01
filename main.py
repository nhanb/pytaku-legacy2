#!/usr/bin/env python
import webapp2
from handlers import index, auth


app = webapp2.WSGIApplication([
    ('/', index.IndexHandler),
    ('/auth', auth.Init),
    ('/auth/callback', auth.Callback),
], debug=True)
