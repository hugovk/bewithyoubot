#!/usr/bin/env python
# encoding: utf-8
"""
TODO haha funny joke
"""
from __future__ import print_function
import argparse
import datetime
import inflect
import sys
import twitter  # pip install twitter
import webbrowser
import yaml  # pip install pyyaml

# from pprint import pprint


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def timestamp():
    """ Print a timestamp and the filename with path """
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + " " +
          __file__)


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def tweet_it(string, credentials, image=None):
    """ Tweet string and image using credentials """
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file
    auth = twitter.OAuth(
        credentials['access_token'],
        credentials['access_token_secret'],
        credentials['consumer_key'],
        credentials['consumer_secret'])
    t = twitter.Twitter(auth=auth)

    print_it("TWEETING THIS:\n" + string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:

        if image:
            print("Upload image")

            # Send images along with your tweets.
            # First just read images from the web or from files the regular way
            with open(image, "rb") as imagefile:
                imagedata = imagefile.read()
            t_up = twitter.Twitter(domain='upload.twitter.com', auth=auth)
            id_img = t_up.media.upload(media=imagedata)["media_id_string"]

            result = t.statuses.update(status=string, media_ids=id_img)
        else:
            result = t.statuses.update(status=string)

        url = "http://twitter.com/" + \
            result['user']['screen_name'] + "/status/" + result['id_str']
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def timecheck():
    """Only run at certain hour"""
    if args.test:
        return

    utcnow = datetime.datetime.utcnow()

    # Only run at noon-ish UTC
    if utcnow.hour == 12:
        return
    else:
        exit()


def thingy():
    month = datetime.datetime.utcnow().strftime("%B")  # May
    day_number = '{dt.day}'.format(dt=datetime.datetime.utcnow())  # 4

    p = inflect.engine()
    dayth = p.ordinal(p.number_to_words(day_number))  # fourth

    tweet = "{0} the {1} be with you".format(month, dayth)
    return tweet


if __name__ == "__main__":

    timestamp()

    parser = argparse.ArgumentParser(
        description="On the Xth day of Christmas @MyTruLuvSent2Me",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/bewithyoubot.yaml',
        # default='E:/Users/hugovk/Dropbox/bin/data/bewithyoubot.yaml',
        help="YAML file location containing Twitter and Wordnik keys/secrets")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: go through the motions but don't tweet anything")
    args = parser.parse_args()

    timecheck()

    credentials = load_yaml(args.yaml)

    tweet = thingy()
    print(tweet)

    tweet_it(tweet, credentials)

# End of file
