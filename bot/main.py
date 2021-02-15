import api
from errors import *
from imgsearch import imgSearch

bot = api.reddit()

footer = "\n\n\n\n ^this ^message ^was ^sent ^[automatically](https://github.com/n3r0t/sleepobeepo)"

source_list = ["twitter", "pixiv"]


def streamSubmissions(subreddit: str) -> None:
    """
    Stream of subreddit's submissions then check if source was already posted.
    If no source was posted, it will search for it.
    :param subreddit: String of the wanted subreddit
    :return: Nothing. Will continuously stream submissions till script is stoped by an external source.
    """
    sleepobeepo = bot.subreddit(subreddit)
    print(f'Streaming r/{subreddit}.')
    for submission in sleepobeepo.stream.submissions(skip_existing=True):
        print(f"Checking {submission.title} -- {submission.permalink}\n")
        if submission.is_robot_indexable:
            print(submission)
            if not submission.comments.list():
                print("No comment. Searching for source.\n")
                try:
                    bot.submission(submission.id).reply(f'Source: {imgSearch(submission.url)} {footer}')
                except NoSourceFound:
                    bot.submission(submission.id).reply(f'No source found.{footer}')
            for comment in submission.comments:
                if any(x in comment.body.lower() for x in source_list):
                    print("Source already posted. Ignoring post.\n")
                    break
                else:
                    print("No source posted. Searching for source.\n")
                    imgSearch(submission.url)
        else:
            print("Post deleted. Not searching.\n")


if __name__ == "__main__":
    streamSubmissions('sleepobeepo')
