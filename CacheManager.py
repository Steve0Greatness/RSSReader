"""Manage the cache."""

from DBManager import feeds, feedInDB, Feed, findFeed
import feedparser
import os, shutil
import xml.etree.ElementTree as ET
from datetime import datetime
import toml, requests

def cachePaths() -> list[str]:
    """This functions takes no input, instead using the user's saved feeds."""
    parsedFeeds = list()
    for category in feeds.values():
        parsedFeeds += list(getCachePath(feed.title, category) for feed in category)
    return parsedFeeds

def getCachePath(feedTitle: str, category: str | None = None, includeCache: bool = True):
    """Gives a full cache path"""
    finalPath = [ "cache" ]
    if not includeCache:
        finalPath.remove("cache")
    if category is not None:
        finalPath.append(category)
    finalPath.append(feedTitle)
    return "/".join(finalPath) + ".xml"

def checkReCache() -> bool:
    """Checks if it is currently time to re-query and re-cache all feeds without user input(the user is able to set the length between in a setting)."""
    currentTime:     int = round(datetime.now().timestamp())
    lastQueried:     int = toml.load("FeedInfo.toml")["lastQueried"]
    timeBetween:     int = toml.load("Settings.toml")["timeBetweenReloads"]
    nextQueryPeriod: int = lastQueried + timeBetween
    return currentTime >= nextQueryPeriod

def updateLastQueried() -> None:
    """Updates the time that all feeds were last updated"""
    currentTime: int = round(datetime.now().timestamp())
    feedInfo:    int = toml.load("FeedInfo.toml")
    feedInfo["lastQueried"] = currentTime
    toml.dump(feedInfo, open("FeedInfo.toml", "w"))
    return

def buildFeedCacheMap() -> dict[str, str]:
    """Returns a dict where the keys are the cache path of the feed, and the value is the xmlUrl"""
    parsedFeeds = {}
    for categoryTitle, category in feeds.items():
        for feed in category:
            cachePath = getCachePath(feed.title, categoryTitle)
            parsedFeeds[cachePath] = feed.xmlUrl
    return parsedFeeds

def clearCacheDir() -> None:
    """Removes the cache"""
    for item in os.listdir("cache"):
        currentPath = f"cache/{item}"
        if os.path.isfile(currentPath) or os.path.islink(currentPath):
            os.unlink(currentPath)
        elif os.path.isdir(currentPath):
            shutil.rmtree(currentPath)

def buildCacheDir() -> None:
    """Makes all directories needed for the cache dir to work"""
    clearCacheDir()
    for category in feeds:
        os.mkdir(f"cache/{category}")

def queryFeeds(Force: bool = False):
    """Query all feeds and cache them to the cache directory"""
    if not Force and not checkReCache():
        return
    buildCacheDir()
    cacheMap = buildFeedCacheMap()
    for cachePath, xmlUrl in cacheMap.items():
        with open(cachePath, "w") as xmlCache:
            xmlCache.write(requests.get(xmlUrl))

def querySingle(feed: Feed, feedCategory: str | None = None):
    """This always gets initiated by the User, wether by adding a new feed or the user requesting a single feed get rechecked"""
    buildCacheDir()
    with open(getCachePath(feed.title, feedCategory), "w") as xmlCache:
        xmlCache.write(requests.get(feed.xmlUrl))

def getFeedContent(feedTitle: str, category: str | None) -> any:
    cachePath:        str  = getCachePath(feedTitle, category)
    inDataBase:       bool = feedInDB(feedTitle, category)
    cacheNonexistent: bool = not os.path.exists(cachePath)
    if cacheNonexistent and not inDataBase:
        return { "_error": "Cannot find this in the DB" }
    elif cacheNonexistent and inDataBase:
        querySingle(findFeed(feedTitle, category), category)
    return feedparser.parse(cachePath)

def getAllFeedContents(showRead: bool = True):
    pass
