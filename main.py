import DBManager, CacheManager, UserManager
from os import mkdir
from os.path import exists, isdir, isfile

def dirExists(dir: str) -> bool:
    return exists(dir) and isdir(dir)

def fileExists(dir: str) -> bool:
    return exists(dir) and isfile(dir)

def mkFile(dir: str) -> bool:
    with open(dir, "x") as file:
        file.write("")

def iniDir(dir):
    if not dirExists(dir):
        mkdir(dir)

def iniFile(dir):
    if not fileExists(dir):
        mkFile(dir)

def init():
    iniDir("./cache")
    iniDir("./users")
    iniDir("./users/images")
    iniFile("./users/images.toml")
    iniFile("./ReadStatus.json")

if __name__ == "__main__":
    init()
