from os import getenv

from sqlalchemy import URL


class Config:
    DATABASE = getenv("DATABASE", "sqlite")
    DATABASE_NAME = getenv("DATABASE_NAME", "data.db")
    DATABASE_USER = getenv("DATABASE_USER")
    DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")
    DATABASE_HOST = getenv("DATABASE_HOST")
    DATABASE_PORT = getenv("DATABASE_PORT")
    SQLALCHEMY_DATABASE_URI = (
        URL.create(
            drivername=DATABASE,
            username=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            database=DATABASE_NAME,
        )
        if DATABASE != "sqlite"
        else f"sqlite:///{DATABASE_NAME}"
    )
    DEBUG = getenv("DEBUG", True)
    SYMBOLS = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
        ".",
        "~",
    ]
