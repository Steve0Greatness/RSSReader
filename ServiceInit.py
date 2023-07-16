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

def mkFile(dir: str) -> bool:
    """"""
    with open(dir, "x") as file:
        file.write("")

def iniDir(dir: str):
    """"""
    if not dirExists(dir):
        mkdir(dir)

def iniFile(dir: str):
    """"""
    if not fileExists(dir):
        mkFile(dir)

FUNCTIONS: tuple[FunctionType] = (
    iniDir,
    iniFile
)

ACTIONS: tuple[tuple[str]] = (
    (
        "./cache",
        "./users",
        "./users/images"
    ),
    (
        "./users/images.toml",
        "./ReadStatus.json"
    )
)

def main():
    for index, array in enumerate(ACTIONS):
        func = FUNCTIONS[index]
        for item in array:
            func(item)