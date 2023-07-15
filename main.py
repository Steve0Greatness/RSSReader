import DBManager, CacheManager, UserManager
import feedparser
import toml

# RSS_MIMES = ( "application/rss+xml", "application/rdf+xml", "application/atom+xml", "application/xml" )

FeedInfo = {}
def reloadDetails():
    global FeedInfo
    FeedInfo = toml.load("FeedInfo.toml")

def queryFeed(uri: str):
    feed = feedparser.parse(uri)
    htmlUrl = tuple( link["href"] for link in feed["feed"]["links"] if link["type"] == "text/html" )[0]
    title = feed["feed"]["title"]
    return DBManager.Feed(title, uri, htmlUrl)

if __name__ == "__main__":
    # queryFeed("https://reddit.com/r/doom/.rss")
    # print(CacheManager.cachePaths())
    print(UserManager.listUsers())
    pass