#!/usr/bin/env python
import webapp2
import sys
sys.path.insert(0, 'libs')
from handlers import index, auth, rest

app = webapp2.WSGIApplication([
    ('/', index.IndexHandler),
    ('/auth', auth.Init),
    ('/auth/callback', auth.Callback),
    ('/api/manga.*', rest.MangaHandler),
    ('/api/fetch.*', rest.FetchHandler),
], debug=True)
