"""
Setup all api access in one file for easier use across the project.
"""

import configparser

from praw import Reddit
from saucenao_api import SauceNao

with open(".\id.ini") as id_file:  # Read the .ini for the API keys and password
    config = configparser.ConfigParser()
    config.read_file(id_file)


def reddit():
    return Reddit(client_id=config["REDDIT"]["client_id"],
                  client_secret=config["REDDIT"]["client_secret"],
                  password=config["REDDIT"]["password"],
                  username=config["REDDIT"]["username"])


def saucenao():
    return SauceNao(api_key=config["SNAO"]["apikey"])
