import configparser
import json
import os
import random
from urllib.request import urlopen

import praw
from saucenao_api import SauceNao

with open("id.ini") as idbot:
    config = configparser.ConfigParser()
    config.read_file(idbot)

bot = praw.Reddit(client_id=config["REDDIT"]["client_id"],
                  client_secret=config["REDDIT"]["client_secret"],
                  password=config["REDDIT"]["password"],
                  username="n3r0T",
                  user_agent="Nothing for today? Then, I'll go sleep right now...")

bot.validate_on_submit = True
sleepobeepo = bot.subreddit('sleepobeepo')

footer = ""


def isPicture(file):
    from PIL import Image
    try:
        Image.open(file)
        return True
    except IOError:
        return False


pathG11 = "C:/Users/NRTALPHA/Pictures/g11SpiritAnimal"
files = os.listdir(pathG11)
rdm = random.randrange(len(files))
fullpath = f'{pathG11}/{files[rdm]}'
while not isPicture(fullpath):
    print("check extension")
    rdm = random.randrange(len(files))
    fullpath = f'{pathG11}/{files[rdm]}'


def incrementDay():
    f = open(".day", "r")
    content = int(f.read())
    content += 1
    numberDay = str(content)
    f.close()
    f = open(".day", "w")
    f.write(numberDay)
    f.close()
    return numberDay


# subreddit.submit_image(f'Daily G11 #{numberDay}',fullpath)
# os.rename(fullpath,f'{pathG11}/posted/{files[rdm]}')
def imgSearch(imgURL, postID):
    imgSource = SauceNao(api_key=config["SNAO"]["apikey"]).from_url(imgURL)
    comment = bot.submission(postID)  # Reply to post with the source
    if imgSource[0].similarity >= 87.00:
        comment.reply(f"Source: {imgSource[0].url}")
        print(f"{imgSource[0].url} -- {imgSource[0].similarity}%")
    else:
        comment.reply(f"No good source found.")


def idkMan():
    lastSubmissionsURL = urlopen(
        "https://api.pushshift.io/reddit/search/submission/?subreddit=sleepobeepo&sort=desc&size=25")
    lastSubmissionsData = json.loads(lastSubmissionsURL.read())
    # print(lastSubmissionsData)
    linkID = f"t3_{lastSubmissionsData['data'][0]['id']}"
    linkIDURL = urlopen(f"https://api.pushshift.io/reddit/search/comment/?subreddit=sleepobeepo&link_id={linkID}")
    linkIDData = json.loads(linkIDURL.read())
    print(lastSubmissionsData['data'][0]['title'])
    if linkIDData['data']:
        temp = 0
        for comment in linkIDData['data']:
            if comment['author'] != 'n3r0T':
                temp += 1
        if temp > 0:
            print("No post by n3r0T, posting the source")
            imgSearch(lastSubmissionsData["data"][0]["url_overridden_by_dest"], lastSubmissionsData['data'][0]['id'])
    else:
        print("No comment, posting the source")
        imgSearch(lastSubmissionsData["data"][0]["url_overridden_by_dest"], lastSubmissionsData['data'][0]['id'])


idkMan()
