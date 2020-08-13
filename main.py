import configparser
import time

import praw
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

saucenao = SauceNao(api_key=config["SNAO"]["apikey"])

footer = "\n\n\n\n ^this ^message ^was ^sent ^[automatically](https://github.com/n3r0t/sleepobeepo)"


def imgSearch(imgURL, postID):
    """use SauceNao to get the source of the picture and
    post a reply to the Reddit thread wit the source"""
    imgSource = saucenao.from_url(imgURL)
    comment = bot.submission(postID)
    if imgSource[0].similarity >= 87.00:
        comment.reply(f"Source: {imgSource[0].url} {footer}")
        print(f"{imgSource[0].url} -- {imgSource[0].similarity}%")
    else:
        comment.reply(f"No good source found." + footer)


def checkNewSubmission():
    """Check new submissions then check if I already posted,
    if I haven't, it search for the source of the picture posted"""
    startTime = time.time()
    for submission in sleepobeepo.new(limit=3):
        sub = bot.submission(id=submission.id)
        print(f"{submission.title} -- {submission.permalink}")
        if submission.is_robot_indexable:
            if sub.comments.list():
                numberOfN3r0tComment = 0
                for comment in sub.comments:
                    if comment.author == 'n3r0T':
                        numberOfN3r0tComment += 1  # It check if I already posted in the thread
                if numberOfN3r0tComment == 0:
                    print("No post by n3r0T, posting the source.")
                    imgSearch(sub.url,submission.id)
                else:
                    print("n3r0T already posted.\n")
            else:
                print("No comment, posting the source.")
                imgSearch(sub.url,submission.id)
        else:
            print("Post deleted. Not posting.\n")

    print(f"Done at {time.strftime('%H:%M:%S', time.localtime())} in {round(time.time() - startTime,2)} sec.\n\n")


checkNewSubmission()
