import cryptocode
import xml.etree.ElementTree as ET
import os

loggedIn = None

def listUsers() -> list[str]:
    userDir = os.listdir("./users")
    return [ user.replace("_", " ")[:-4] for user in userDir ]

def addUser(username: str, login: str, preserveDB: bool = False, logOn: bool = False):
    """Adds an entry into the users dir for"""
    global loggedIn
    username = username.replace(" ", "_")
    DBData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><opml version=\"1.0\"><head><title>Feed Subscriptions</title></head><body></body></opml>"
    with open("DB.opml", "w+") as file:
        if preserveDB:
            DBData = file.read()
        if logOn:
            file.write(DBData)
            loggedIn = username.replace("_", " ")
    DBData = cryptocode.encrypt(DBData, login)
    with open("./users/" + username + ".enc", "x") as file:
        file.write(DBData)

def requestDeletion(username: str):
    """Removes a user from user dir. Does not prompt the user, please do that before using this."""
    userFile = "./users/" + username.replace(" ", "_") + ".enc"
    if username not in listUsers():
        return
    os.unlink(userFile)
