import xml.etree.ElementTree as ET
import shutil, os.path

class Feed():
    """Basic information about a feed, not including any actual content of a feed."""
    def __init__(self, title: str, xmlUrl: str, htmlUrl: str):
        self.title:   str = title
        self.xmlUrl:  str = xmlUrl
        self.htmlUrl: str = htmlUrl
    def __str__(self):
        return f"<outline text=\"{self.title}\" title=\"{self.title}\" type=\"rss\" xmlUrl=\"{self.xmlUrl}\" htmlUrl=\"{self.htmlUrl}\"/>"

feeds: dict[str | None, list[Feed]] = {
    None: []
}
"""All feeds arranged by category.

The category `None` is the default category, it cannot be removed or deleted.

A `Feed` contains information about a single feed. Attrs: title, xmlUrl, htmlUrl."""

def parseFeed(feedTree: ET.Element) -> dict[str | None,  list[Feed]]:
    """Parse feeds from an XML element tree(or element)"""
    feeds: dict[str | None, list[Feed]] = {
        None: []
    }
    for child in feedTree:
        attrs = child.attrib
        title = attrs["title"]
        isFeed = "xmlUrl" in attrs
        if isFeed:
            feeds[None].append(
                Feed(title, attrs["xmlUrl"], attrs["htmlUrl"])
            )
            continue
        feeds[title] = []
        for child_ in child:
            feeds[title].append(
                Feed(child_.attrib["title"], child_.attrib["xmlUrl"], child_.attrib["htmlUrl"])
            )
    return feeds

def reloadFeeds():
    """Re-Read DB.opml to update the feeds variable."""
    global feeds
    BODY: ET.Element = ET.parse('DB.opml').getroot()[1]
    feeds            = parseFeed(BODY)
    return feeds
reloadFeeds()

def addFeed(feed: Feed, category: str | None = None):
    """Adds a new feed to DB.opml"""
    XMLDoc:  ET.ElementTree = ET.parse('DB.opml')
    newFeed: ET.Element     = ET.fromstring(str(feed))
    if category is not None:
        XMLDoc.getroot()[1].append(newFeed)
    else:
        BODY = XMLDoc.getroot()[1]
        subElements = len(BODY)
        for outline in BODY:
            index = len(BODY) - subElements
            if "xmlUrl" in outline.attrib or (outline.attrib["title"] != category and subElements != 1):
                continue
            elif outline.attrib["title"] != category:
                newCategory = ET.fromstring(f"<outline title=\"{category}\" text=\"{category}\"></outline>")
                newCategory.append(newFeed)
                XMLDoc.getroot()[1].append(newCategory)
            else:
                XMLDoc.getroot()[1][index].append(newFeed)
            subElements = subElements - 1
    with open("DB.opml", "w") as file:
        file.write(ET.tostring(XMLDoc))
    reloadFeeds()

def feedInDB(feedTitle: str, category: str | None = None) -> bool:
    """Checks if the feed exists in the DataBase"""
    reloadFeeds()
    categoryExists = category in feeds
    feedInCategory = categoryExists and feedTitle in tuple(feed.title for feed in feeds[category])
    return feedInCategory

def copyDB(copyToDir: str = "~/Downloads"):
    """Places a copy of DB.opml into the designated directory(user's downloads dir by default)"""
    copyPath = os.path.expandUser(copyToDir)
    shutil.copyfile("BD.opml", copyPath)

def findFeed(feedTitle: str, category: str | None = None) -> Feed:
    for feed in feeds[category]:
        if feed.title != feedTitle:
            continue
        return feed