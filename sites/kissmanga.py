import urlparse
from sites import get_html
import re


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
