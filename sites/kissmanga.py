import urlparse
import urllib
from google.appengine.api import urlfetch
from sites import get_html
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class Kissmanga(object):

    def get_chapter_name(self, url):
        parsed = urlparse.urlparse(url)
        return parsed.path.split('/')[-1]

    def get_pages(self, url):
        html = get_html(url)

        # Create regex to match page link
        pat = re.compile('lstImages\.push\("(.+?)"\);')
        page_links = pat.findall(html)

        # Regex to match page image file name
        ipat = re.compile('/([0-9]{3}\.(png|jpg))\?')
        self.pages = ((ipat.findall(x)[0][0], x) for x in page_links)

    # Return a list of dictionaries that store at least title and url:
    # [ { 'title': 'Naruto', 'url': 'http://...' }, {...}, ... ]
    def search_title(self, keyword):
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
    # - chapters {title, url}
    # - thumbnailUrl
    # - tags
    def get_manga_info(self, html):
        soup = BeautifulSoup(html)
        chapters = self.get_chapters(soup)
        thumbnailUrl = self.get_thumbnail_url(soup)
        return {'chapters': chapters, 'thumbnailUrl': thumbnailUrl}

    # Chapters - latest first
    def get_chapters(self, soup):
        table = soup.find('table', class_='listing')
        return [{'url': 'http://kissmanga.com' + a['href'],
                'title': a.string.strip()}
                for a in table.find_all('a')]

    # Thumbnail url
    def get_thumbnail_url(self, soup):
        return soup.find('link', {'rel': 'image_src'})['href']
