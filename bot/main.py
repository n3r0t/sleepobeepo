import argparse

from prawcore import NotFound

import api
import logs
import errors
from imgsearch import imgSearch


def getSubreddit():
    """grab args given when running the bot"""
    subParser = argparse.ArgumentParser()
    subParser.add_argument('Subreddit',
                           metavar='sub',
                           type=str,
                           help='link to subreddit')

    arg = subParser.parse_args().Subreddit
    try:
        bot.subreddits.search_by_name(arg, exact=True)
    except NotFound:
        logger.warning("Wrong subreddit specified, exiting script now.")
        exit()

    return arg


def postSource(submission):
    footer = "\n\n\n\n ^this ^message ^was ^sent ^[automatically](https://github.com/n3r0t/sleepobeepo)"
    try:
        bot.submission(submission.id).reply(f'Source: {imgSearch(submission.url)} {footer}')
    except errors.NoSourceFound:
        bot.submission(submission.id).reply(f'No source found.{footer}')

def streamSubmissions(subreddit: str) -> None:
    """
    Stream of subreddit's submissions then check if source was already posted.
    If no source was posted, will search for it.
    :param subreddit: String of the wanted subreddit (given automatically with getSubreddit()
    :return: Nothing. Will continuously stream submissions till script is stoped by an external source.
    """
    sleepobeepo = bot.subreddit(subreddit)
    source_list = ["twitter", "pixiv"]

    logger.info(f'Streaming r/{subreddit}.')
    for submission in sleepobeepo.stream.submissions(skip_existing=True):
        logger.info(f"Checking {submission.title} -- {submission.permalink}\n")
        if submission.is_robot_indexable:
            if not submission.comments.list():
                logger.info("No comment. Searching for source.\n")
                postSource(submission)
            for comment in submission.comments:
                if any(x in comment.body.lower() for x in source_list):
                    logger.info("Source already posted. Ignoring post.\n")
                    break
                else:
                    logger.info("No source posted. Searching for source.\n")
                    postSource(submission)
        else:
            logger.info("Post deleted. Not searching.\n")


if __name__ == "__main__":
    logger = logs.setup(__name__)
    bot = api.reddit()
    streamSubmissions(getSubreddit())