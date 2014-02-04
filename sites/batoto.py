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
            })
        return titles

    def manga_info(self, html):
        soup = BeautifulSoup(html)
        chapters = self._chapters(soup)
        thumbnailUrl, tags = self._thumbnail_url_and_tags(soup)
        return {'chapters': chapters,
                'thumbnailUrl': thumbnailUrl,
                'tags': tags}

    def _chapters(self, soup):
        table = soup.find('table', class_='chapters_list')
        en_rows = table.findAll(u'tr', class_=u'lang_English')

        chapters = []
        for row in en_rows:
            a = row.find('a')
            url = a['href']
            title = a.contents[1].strip()
            chapters.append({
                'title': title,
                'url': url
            })
        return chapters

    def _thumbnail_url_and_tags(self, soup):
        box = soup.find('div', class_='ipsBox')
        thumb = box.find('img')['src']

        # This cell stores <a> that store tags
        tags_cell = box.find('td', text='Genres:').find_next_sibling('td')
        tags = [a.find('span').contents[1].lower() for a in tags_cell]

        return (thumb, tags)

    def chapter_pages(self, html):
        soup = BeautifulSoup(html)

        # a <select> tag has options that each points to a page
        opts = soup.find('select', id='page_select').find_all('option')
        urls = [opt['value'] for opt in opts]

        # Page 1 has already been fetched (stored in this html param, duh!)
        # so let's save ourselves an http request
        pages_htmls = [html]
        urls = urls[1:]

        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
        }

        for url in urls:
            resp_code = 404
            tries = 0
            while resp_code != 200 and tries < 77:
                resp = urlfetch.fetch(url, headers=headers)
                resp_code = resp.status_code
                tries += 1
            pages_htmls.append(resp.content)

        returns = []
        for page_html in pages_htmls:
            soup = BeautifulSoup(page_html)
            img_url = soup.find('img', id='comic_page')['src']
            filename = img_url.split('/')[-1]
            returns.append({
                'filename': filename,
                'url': img_url
            })
        return returns
