#!/usr/bin/env python

import argparse
import os
from PIL import Image
import praw
import re
import requests
import sys

class RedditPicsDownloader:
    def __init__(self, sort_type = "day",
                subreddits_list = ["roomporn", "wallpapers", "wallpaper", "spaceporn",
                          "earthporn", "waterporn", "skyporn", "spaceporn", "topwalls"],
                score_threshold = 500):

        self.sort_type = sort_type
        self.subreddit_list = subreddits_list
        self.score_threshold = score_threshold
        # Get a reddit API account from here: 
        self.user = praw.Reddit("/u/zefre's popular picture downloader bot")
        # Get a client ID from here: http://api.imgur.com/#register
        self.imgur_header = {"Authorization": "Client-ID 6dd439316e641d3"}
        self.items_limit = 1000
        self.download_count = 0
        self.min_width = 1440
        self.min_height = 900
        # Create a directory in which the downloaded pics will be stored (same dir as this program).
        self.download_path = self.create_dir()
        # Files in the current directory. Used for not writing over existing files.
        # Set > list since O(1) > O(n) average lookup.
        self.current_files = set(os.listdir(self.download_path))

    def get_submissions(self, subreddit):
        # Why am I not using self.sort_type for these?
        return {
            "week": self.user.get_subreddit(subreddit).get_top_from_week(limit=self.items_limit),
            "month": self.user.get_subreddit(subreddit).get_top_from_month(limit=self.items_limit),
            "year": self.user.get_subreddit(subreddit).get_top_from_year(limit=self.items_limit),
            "all": self.user.get_subreddit(subreddit).get_top_from_all(limit=self.items_limit)
        }.get(self.sort_type, self.user.get_subreddit(subreddit).get_top_from_day(limit=self.items_limit))

    def download_images(self):
        for subreddit in self.subreddit_list:
            for submission in self.get_submissions(subreddit):
                if submission.score >= self.score_threshold:
                    # Make sure the image came from imgur.com
                    url = re.search(r"imgur.com/([\w\d]*)\.([\w]*)", submission.url)
                    if url is None or url.group is None:
                        continue
                    print ("Getting {}...".format(url.group(0)))

                    # imghash = ID of the image in imgur e.g. aEaQGpz
                    imghash = url.group(1)
                    file_type = url.group(2)
                    self.write_to_file(imghash, file_type, subreddit)
        print ("Downloaded {} images successfully.".format(self.download_count))

    def write_to_file(self, imghash, file_type, subreddit):
        try:
            imgur_req = requests.get("https://api.imgur.com/3/image/{}.json".format(imghash),
                                     headers=self.imgur_header)
            if imgur_req is not None:
                imgur_url = requests.get(imgur_req.json()["data"]["link"])
                if "{}.{}".format(imghash, file_type) in self.current_files:
                    print ("File already exists in current directory ({}.{}). Skipping.".format(imghash, file_type))
                else:
                    image_path = self.download_path + "{}.{}".format(imghash, file_type)
                    with open(image_path, "wb") as output_file:
                        output_file.write(imgur_url.content)
                        image = Image.open(image_path)
                        if image.size[0] < self.min_height or image.size[1] < self.min_width:
                            print ("{}.{} is too short or narrow (image: {} x {}, required: {} x {})."
                                    .format(imghash, file_type, image.size[1], image.size[0], self.min_width, self.min_height))
                            os.remove(image_path)
                        else:
                            print ("Downloaded {}.{} successfully.".format(imghash, file_type))
                            self.download_count += 1
            else:
                print ("Could not succesfully download the image.")
        except Exception:
            print ("Error while opening {} subreddit.\n".format(subreddit))

    def create_dir(self):
        if os.name == "posix":
            download_path = os.getcwd() + "/RedditImages/"
        else:
            download_path = os.getcwd() + "\\RedditImages\\"
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        return download_path

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\t\t\t--- RedditPicsDownloader ---
        This program allows you to download popular images from subreddits (reddit.com).""")
    parser.add_argument("-top", help="Sort type of posts: day/week/month/year/all", type=str,
                        default="day", choices=["day", "week", "month", "year", "all"])
    parser.add_argument("-sub", help="Subreddits to query separated by a comma without spaces e.g. wallpaper,spaceporn,earthporn", type=str,
                        default="roomporn, wallpapers, wallpaper, spaceporn, earthporn, waterporn, skyporn, spaceporn, topwalls")
    parser.add_argument("-score", help="Minimum post score threshold e.g. 500", type=int, default=500)

    args = vars(parser.parse_args(sys.argv[1:]))
    sort_type = args["top"]
    subreddits_list = args["sub"].strip().replace(" ", "").split(",")
    score_threshold = args["score"]

    rpd = RedditPicsDownloader(sort_type, subreddits_list, score_threshold) 
    rpd.download_images()

if __name__ == "__main__":
    main()
