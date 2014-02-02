import webapp2
from handlers.auth import Otaku
import sites
import json
import helpers.dropbox
from google.appengine.api import urlfetch


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
        path = self.request.path.split('/')
        if len(path) == 3:  # that is just plain /api/manga
            self.get_manga_list()
        elif len(path) == 4:  # basically anything: /api/manga/crap?url=...
            self.get_manga_info()

    def get_manga_list(self):
        keyword = self.request.get('keyword')
        s = sites.available_sites('')
        titles = []

        for site in s:
            titles.extend(site.search_titles(keyword))

        result = json.dumps(titles)
        self.response.write(result)

    def get_manga_info(self):
        url = self.request.get('url')
        s = sites.get_site(url)

        html = sites.get_html(url)
        info = s.manga_info(html)

        result = json.dumps(info)
        self.response.write(result)


class FetchHandler(webapp2.RequestHandler):

    @auth
    def put(self):
        # Sample request path: /api/fetch/Naruto/Chapter-1169
        # params:   url (chapter seed page URL)
        #           options (maybe add stuff later, like auto zip)
        path = self.request.path.split('/')[1:]  # cut out empty first elem
        if len(path) <= 2:  # only ['api', 'fetch']
            return

        path = path[2:]  # cut out api/fetch
        path = '/'.join(path)  # now we have 'path/to/our/chapter/folder'

        url = self.request.get('url')
        html = sites.get_html(url)

        s = sites.get_site(url)
        pages_urls = s.chapter_pages_urls(html)
        self.response.write(str(pages_urls))
