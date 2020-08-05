import praw,configparser,os,random

with open("id.ini") as idbot:
    config = configparser.ConfigParser()
    config.read_file(idbot)

bot = praw.Reddit(client_id=config["SECRET"]["client_id"],
                  client_secret=config["SECRET"]["client_secret"],
                  password=config["SECRET"]["password"],
                  username="n3r0T",
                  user_agent="Nothing for today? Then, I'll go sleep right now...")

bot.validate_on_submit = True

pathG11 = "C:/Users/NRTALPHA/Pictures/g11SpiritAnimal"
files = os.listdir(pathG11)
fullpath = f'{pathG11}/{files[random.randrange(len(files))]}'

f = open(".day", "r")
content = int(f.read())
content += 1
numberDay = str(content)
f.close()

f = open(".day", "w")
f.write(numberDay)
f.close()

subreddit = bot.subreddit('sleepobeepo')
subreddit.submit_image(f'Daily G11 #{numberDay}',fullpath)

os.rename(fullpath,f'/posted/{numberDay}')
