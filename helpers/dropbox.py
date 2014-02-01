import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

consumer_key = config.get("Dropbox", "ConsumerKey")
consumer_secret = config.get("Dropbox", "ConsumerSecret")
token_url = config.get("Dropbox", "TokenURL")
authorize_url = config.get("Dropbox", "AuthorizeURL")
