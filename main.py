import configparser
import praw
import requests
from saucenao_api import SauceNao

with open("id.ini") as idbot:  # Read the .ini for the API keys and password
    config = configparser.ConfigParser()
    config.read_file(idbot)

bot = praw.Reddit(client_id=config["REDDIT"]["client_id"],
                  client_secret=config["REDDIT"]["client_secret"],
                  password=config["REDDIT"]["password"],
                  username="n3r0T",
                  user_agent="Nothing for today? Then, I'll go sleep right now...")

sleepobeepo = bot.subreddit('sleepobeepo')

footer = "\n\n\n\n ^this ^message ^was ^sent ^[automatically](https://github.com/n3r0t/sleepobeepo)"


def isDeleted(postURL):
    page = requests.get(postURL, data=None, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' })
    return page.status_code == 404


def imgSearch(imgURL, postID):
    """use SauceNao to get the source of the picture and
    post a reply to the Reddit thread wit the source"""
    imgSource = SauceNao(api_key=config["SNAO"]["apikey"]).from_url(imgURL)
    comment = bot.submission(postID)
    if imgSource[0].similarity >= 87.00:
        comment.reply(f"Source: {imgSource[0].url}" + footer)
        print(f"{imgSource[0].url} -- {imgSource[0].similarity}%")
    else:
        comment.reply(f"No good source found." + footer)


def checkNewSubmission():
    """Check new submissions then check if I already posted,
    if I haven't, it search for the source of the picture posted"""

    # Check for new submissions
    lastSubmissionsURL = requests.get(
        "https://api.pushshift.io/reddit/search/submission/?subreddit=sleepobeepo&sort=desc&size=25")
    lastSubmissionsData = lastSubmissionsURL.json()

    # check for the comments
    linkID = f"t3_{lastSubmissionsData['data'][0]['id']}"
    linkIDURL = requests.get(f"https://api.pushshift.io/reddit/search/comment/?subreddit=sleepobeepo&link_id={linkID}")
    linkIDData = linkIDURL.json()

    print(f"{lastSubmissionsData['data'][0]['title']} -- {lastSubmissionsData['data'][0]['permalink']}")
    if not isDeleted(lastSubmissionsData['data'][0]['url_overridden_by_dest']):
        if linkIDData['data']:
            numberOfN3r0tComment = 0
            for comment in linkIDData['data']:
                if comment['author'] == 'n3r0T':
                    numberOfN3r0tComment += 1  # It check if I already posted in the thread
            if numberOfN3r0tComment == 0:
                print("No post by n3r0T, posting the source.")
                imgSearch(lastSubmissionsData['data'][0]["url_overridden_by_dest"],
                          lastSubmissionsData['data'][0]['id'])
            else:
                print("n3r0T already posted.")
        else:
            print("No comment, posting the source.")
            imgSearch(lastSubmissionsData['data'][0]["url_overridden_by_dest"], lastSubmissionsData['data'][0]['id'])
    else:
        print("Post deleted. Not posting.")

    print("Done.")


checkNewSubmission()
