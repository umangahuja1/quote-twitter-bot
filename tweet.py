import tweepy
from config import *
from datetime import datetime as dt
from writer import Photo
from time import sleep


class Tweet:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth)

    def post(self):
        file = 'images/{}.png'.format(str(dt.date(dt.now())))
        status = 'Subscribe to https://www.youtube.com/c/GetSetPython\n\n#automated #getsetpython'
        self.api.update_with_media(file, status)

    def main(self):
        post_gap = 300  # time in seconds to post
        while True:
            try:
                photo = Photo()
                check = photo.main()
                if check:
                    tweet = Tweet()
                    tweet.post()
                    sleep(post_gap)
                else:
                    print('sleeping')
                    sleep(post_gap)
            except:
                pass


if __name__ == '__main__':
    main()
