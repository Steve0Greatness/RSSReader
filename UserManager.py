import cryptocode
import xml.etree.ElementTree as ET
import os, os.path
import json
from CacheManager import clearCacheDir

loggedIn: str | None = None


"""

./users
-   user-images
-   user-images.toml
-   <users...>.enc

"""

def listUsers() -> list[str]:
    userDir = os.listdir("./users")
    return [ user.replace("_", " ")[:-4] for user in userDir if os.path.isfile("./users/" + user) and user.endswith(".enc") ]

def loginWData(username: str, newData: str):
    global loggedIn
    with open("DB.opml", "w+") as file:
        file.write(newData)
        loggedIn = username.replace("_", " ")

def addUser(username: str, login: str, preserveDB: bool = False, logOn: bool = False):
    """Adds an entry into the users dir for"""
    global loggedIn
    clearCacheDir()
    username = username.replace(" ", "_")
    DBData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><opml version=\"1.0\"><head><title>Feed Subscriptions</title></head><body></body></opml>"
    with open("DB.opml", "w+") as file:
        if preserveDB:
            DBData = file.read()
    if logOn:
        loginWData(username, )
    DBData = cryptocode.encrypt(DBData, login)
    with open("./users/" + username + ".enc", "x") as file:
        file.write(DBData)

def requestDeletion(username: str):
    """Removes a user from user dir. Does not prompt the user, please do that before using this."""
    clearCacheDir()
    userFile = "./users/" + username.replace(" ", "_") + ".enc"
    if username not in listUsers():
        return
    os.unlink(userFile)

def checkPassword(username: str, login: str) -> bool:
    userFile = f"./users/{username}.enc"
    try:
        with open(userFile) as file:
            ET.fromstring(cryptocode.decrypt(file.read(), login))
            return True
    except:
        return False

def changeUser(username: str, login: str):
    if not checkPassword(username, login):
        return
    loginWData()

def setRead(category: str | None, feed: str, status: bool = True):
    readPath: list[str] | str = []
    if isinstance(category, str):
        readPath.append(category)
    readPath.append(feed)
    readPath = str(loggedIn) + "/" + cryptocode.encrypt("/".join(readPath))
    with open("./ReadStatus.json", "w+") as file:
        readData = json.loads(file.read())
        readData[readPath] = status
        json.dump(readData, file)