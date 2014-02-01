import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from handlers.auth import Otaku, pyhash
import datetime


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        # User is guaranteed to have logged in via Google thanks to app.yaml
        # rules
        user = users.get_current_user()

        # Try to get existing user. If not found, this is a brand new user
        query = Otaku.query(Otaku.userid == user.user_id())
        otaku = query.get()
        if otaku is None:
            otaku = Otaku()
            otaku.userid = user.user_id()

        # This token will be used for subsequent REST API requests - some sort
        # of sessionID, I guess...
        apiToken = pyhash(otaku.userid, str(datetime.datetime.now()))

        template_values = {
            'apiToken': apiToken,
            'username': user.nickname(),
            'userid': user.user_id(),
        }
        path = os.path.join(os.path.dirname(__file__) +
                            '/../templates/', 'index.html')
        self.response.out.write(template.render(path, template_values))

        # Update current token to check in REST API backend
        otaku.api_token = apiToken
        otaku.put()
