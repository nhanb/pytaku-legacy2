import webapp2
from handlers.auth import Otaku
import sites
import json
import helpers.dropbox as dbx
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
            handler.dbx_token = otaku.dropbox_access_token
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

        html = s.fetch_manga_seed_page(url)
        info = s.manga_info(html)

        result = json.dumps(info)
        self.response.write(result)


class FetchHandler(webapp2.RequestHandler):

    @auth
    def put(self):
        # Sample request path: /api/fetch/Naruto/Chapter-1169
        # body: json list of chapter objects: [ {url:..., name:...} . {}, ...]
        path = self.request.path.split('/')[1:]  # cut out empty first elem
        if len(path) <= 2:  # only ['api', 'fetch']
            return

        path = path[2:]  # cut out api/fetch
        path = '/'.join(path)  # now we have 'path/to/our/chapter/folder'

        in_payload = self.request.body
        chapters = json.loads(in_payload)

        # Call appropriate site instance. This assumes all chapters are from
        # the same manga page
        s = sites.get_site(chapters[0]['url'])

        # Fetch chapters one by one
        for chapter in chapters:
            html = urlfetch.fetch(chapter['url']).content
            pages = s.chapter_pages(html)
            chapter_path = path + '/' + chapter['name']

            # Transfer pages to dropbox
            for page in pages:
                file_path = chapter_path + '/' + page['filename']
                page_content = urlfetch.fetch(page['url']).content
                dbx.upload(file_path, page_content, self.dbx_token)
