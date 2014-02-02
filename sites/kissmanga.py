import urllib
from google.appengine.api import urlfetch
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class Kissmanga(object):

    # Return a list of dictionaries that store at least title and url:
    # [ { 'title': 'Naruto', 'url': 'http://...' }, {...}, ... ]
    def search_titles(self, keyword):
        base = 'http://kissmanga.com/Search/SearchSuggest'
        params = {
            'type': 'Manga',
            'keyword': keyword,
        }
        url = base + '?' + urllib.urlencode(params)
        resp = urlfetch.fetch(url, None, 'POST')

        if resp.status_code != 0:
            return None

        # Kissmanga returns manga titles and links in xml format
        content = '<data>%s</data>' % resp.content
        parsed = ET.fromstring(content)

        return [{'title': item.text.strip(), 'url': item.attrib['href']}
                for item in parsed]

    # All kinds of data
    # - chapters [{title, url}, {}, ...] - latest first
    # - thumbnailUrl "url"
    # - tags [tag1, tag2, ...]
    def manga_info(self, html):
        soup = BeautifulSoup(html)
        chapters = self._chapters(soup)
        thumbnailUrl = self._thumbnail_url(soup)
        tags = self._tags(soup)
        return {'chapters': chapters,
                'thumbnailUrl': thumbnailUrl,
                'tags': tags}

    def _chapters(self, soup):
        table = soup.find('table', class_='listing')
        return [{'url': 'http://kissmanga.com' + a['href'],
                'title': a.string.strip()}
                for a in table.find_all('a')]

    def _thumbnail_url(self, soup):
        return soup.find('link', {'rel': 'image_src'})['href']

    def _tags(self, soup):
        tags = soup.find('span', text='Genres:').find_next_siblings('a')
        return [text.string.lower() for text in tags]

    # Pages urls from a chapter
    def chapter_pages_urls(self, html):
        pat = re.compile('lstImages\.push\("(.+?)"\);')
        return pat.findall(html)
