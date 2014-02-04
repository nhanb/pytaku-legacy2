import webapp2
from handlers.auth import Otaku
import sites
import json
import helpers.dropbox as dbx


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

        html = s.fetch_manga_seed_page(url).content
        info = s.manga_info(html)

        result = json.dumps(info)
        self.response.write(result)


class FetchHandler(webapp2.RequestHandler):

    @auth
    def put(self):
        # body: json object of 1 chapter: {url:..., name:...}

        in_payload = self.request.body
        chapter = json.loads(in_payload)

        # Call appropriate site instance
        s = sites.get_site(chapter['url'])

        # Path to target dropbox folder
        path = chapter['name']

        # Pages urls and file names
        html = s.fetch_manga_seed_page(chapter['url']).content
        pages = s.chapter_pages(html)

        # Transfer pages to dropbox
        dropbox_rpcs = []
        for page in pages:
            file_path = path + '/' + page['filename']
            resp_code = 404
            i = 0
            while resp_code != 200 and i < 77:
                resp = s.fetch_page_image(page['url'])
                resp_code = resp.status_code
                i += 1
            page_content = resp.content
            dropbox_rpcs.append(dbx.upload(file_path, page_content,
                                           self.dbx_token))

        # Wait for all rpcs to finish
        for rpc, name, content in dropbox_rpcs:
            resp = rpc.get_result()

            # Retry later if request failed
            if resp.status_code != 200:
                dropbox_rpcs.append(dbx.upload(name, content, self.dbx_token))

        self.response.write(len(dropbox_rpcs))
