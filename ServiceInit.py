"""Initializes all directories and files the service needs to run."""

from os import mkdir
from os.path import exists, isdir, isfile
from types import FunctionType

def dirExists(dir: str) -> bool:
    """"""
    return exists(dir) and isdir(dir)

def fileExists(dir: str) -> bool:
    """"""
    return exists(dir) and isfile(dir)

def mkFile(dir: str, content: str = "") -> bool:
    """"""
    with open(dir, "x") as file:
        file.write(content)

def iniDir(dir: str):
    """"""
    if not dirExists(dir):
        mkdir(dir)

def iniFile(dir: str, content: str = ""):
    """"""
    if not fileExists(dir):
        mkFile(dir, content)

FUNCTIONS: tuple[FunctionType] = (
    iniDir,
    iniFile
)

ACTIONS: tuple[tuple[str | tuple[str]]] = (
    (
        "./cache",
        "./users",
        "./users/images"
    ),
    (
        "./users/images.toml",
        "./ReadStatus.json",
        ("./DB.opml", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><opml version=\"1.0\"><head><title>Feed Subscriptions</title></head><body></body></opml>")
    )
)

def main():
    for index, array in enumerate(ACTIONS):
        func = FUNCTIONS[index]
        for item in array:
            if isinstance(item, tuple):
                func(*item)
                continue
            func(item)