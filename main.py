#Reddit Crawler by Dewey McPherson
#Version 1.3

import os
import praw
from pathlib import Path
import urllib.request
import re
import sys
import prawcore
import time


def createFileName(subfolder, url, title):
    url_split = url.split('.')
    ext = '.' + url_split[-1]
    file = os.path.join(subfolder, title)
    return file + ext


# Thanks slowkow on github https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_illegal(string):
    emoji_pattern = re.compile('['
                           u'\U0001F600-\U0001F64F'  # emoticons
                           u'\U0001F300-\U0001F5FF'  # symbols & pictographs
                           u'\U0001F680-\U0001F6FF'  # transport & map symbols
                           u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                           u'\U00002702-\U000027B0'
                           u'\U000024C2-\U0001F251'
                           ']+', flags=re.UNICODE)
    regex = re.compile('[^a-zA-Z]')
    string = emoji_pattern.sub(r'', string)
    return regex.sub('', string)


# Thanks /u/gavin19 from reddit
def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except prawcore.NotFound:
        exists = False
    return exists


#Passing 1 puts on standard 60 sec nap.
#Passing 2 puts on nap with the message about pissing off reddit
#Passing 3 is a time out.
#Passing 4 is the long nap, 30 minutes.
def naptime(choice):
    if choice == 1:
        print('[NAP] Reached maximum requests per minute.. taking a nap.')
        time.sleep(60)
        print('[WAKE] Resuming...')
        return 0
    elif choice == 2:
        print('[NAP] Looks like we pissed off reddit. Starting one minute break early!')
        time.sleep(60)
        print('[WAKE] Resuming...')
        return 0
    elif choice == 3:
        print('[NAP] This request failed... Placing on 15 second cooldown.')
        time.sleep(15)
        print('[WAKE] And we\'re back!')
        return 0
    elif choice == 4:
        print('[SLEEP] Going to sleep...')
        time.sleep(1800)
        print('[WAKE] Waking up...')
        return 0


MAIN_DIR = str(Path.home()) + '\\Pictures\\Reddit Crawler'

print('Reddit Crawler 1.3 by /u/Gordramus')
print('==================================')

# Creates main directory if does not exist
if not os.path.isdir(MAIN_DIR):
    os.mkdir(MAIN_DIR)

# Creating reddit session
user_agent = 'Reddit Crawler 1.3 by /u/Gordramus'
reddit = praw.Reddit('bot1', user_agent=user_agent)

sub_file = open(r'Subreddits.txt', 'r')
subreddits = sub_file.read().split(' ')
sub_file.close()

req_count = 0
while True:
    for subname in subreddits:
        if req_count == 30:
            req_count = naptime(1)
        if sub_exists(subname):
            sub_folder = os.path.join(MAIN_DIR, subname)
            img_count = 0  # How many posts you want to pull
            try:
                for post in reddit.subreddit(subname).hot(limit=50):
                    req_count += 1
                    if req_count == 30:
                        req_count = naptime(1)
                    if img_count >= 15:
                        break
                    if not os.path.isdir(sub_folder):
                        os.mkdir(sub_folder)
                    print('[POST] ' + post.title)
                    url = str(post.url)
                    if url.endswith('jpg') or url.endswith('jpeg') or url.endswith('png'):
                        title = remove_illegal(post.title[:12])
                        filename = createFileName(sub_folder, url, title)
                        if not os.path.exists(filename):
                            print('[URL] ' + url)
                            print('[FILE] ' + filename)
                            try:
                                urllib.request.urlretrieve(url, filename)
                            except:
                                naptime(3)
                            else:
                                img_count += 1
                        else:
                            print('[SKIP] ' + filename + ' already exists! Skipping OwO')
            except:
                req_count = naptime(2)

    req_count = naptime(4)

