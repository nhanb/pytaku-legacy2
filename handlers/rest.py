import webapp2
from handlers.auth import Otaku
import sites
import json


# Decorator: check user credentials before executing real function
def auth(func):

    def wrapped(handler):
        token = handler.request.headers.get('Pytoken')
        if token is None:
            return  # no token? GTFO!
        userid = handler.request.headers.get('Userid')

        # Check token against datastore
        otaku = Otaku.query(Otaku.userid == userid,
                            Otaku.api_token == token).get()
        if otaku is not None:
            func(handler)

    return wrapped


class MangaHandler(webapp2.RequestHandler):

    @auth
    def get(self):
        keyword = self.request.get('keyword')
        s = sites.available_sites('')
        titles = []

        for site in s:
            titles.extend(site.search_titles(keyword))

        result = json.dumps(titles)
        self.response.write(result)
