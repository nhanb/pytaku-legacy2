import urllib
from google.appengine.api import urlfetch
from sites import Site
from bs4 import BeautifulSoup


class Batoto(Site):

    def search_titles(self, keyword):
        url = 'http://www.batoto.net/search?'
        params = {
            'name_cond': 'c',  # "title contains keyword"
            'name': keyword
        }

        url += urllib.urlencode(params)
        resp = urlfetch.fetch(url, method='GET')

        if resp.status_code != 200:
            return 'screwed'

        soup = BeautifulSoup(resp.content)
        table = soup.find('table', class_='chapters_list')
        strongs = table.find_all('strong')
        titles = []
        for strong in strongs:
            a = strong.find('a')
            url = a['href']
            title = a.contents[1].strip()
            titles.append({
                'url': url,
                'title': title,
                'site': 'batoto'
            })
        return titles

    def manga_info(self, html):
        soup = BeautifulSoup(html)
