import os
import re
import requests


def create_dir():
    download_path = os.getcwd() + "\\RedditImages"

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path


def main():
    # Default subreddit lists
    subreddit_list = ["roomporn", "wallpapers", "spaceporn", "earthporn", "waterporn", "skyporn", "spaceporn"]
    vote_threshold = 1500
    items_limit = 100
    download_count = 0

    reddit_header = {"user-agent": "/u/zefre's popular picture downloader bot"}
    # Get a client ID from here: http://api.imgur.com/#register
    imgur_header = {"Authorization": "Client-ID <your client ID here>"}

    # Create a directory in which the downloaded pics will be stored.
    # It will be created wherever this python program is located.
    download_path = create_dir()
    # Files in the current directory. Used for not writing over existing files.
    # Set > list since O(1) > O(n) average lookup.
    current_files = set(os.listdir(download_path))

    for subreddit in subreddit_list:
        try:
            print ("\nDownloading from {} subreddit.".format(subreddit))
            subreddit_url = "http://www.reddit.com/r/{}.json?limit={}".format(subreddit, items_limit)
            req = requests.get(subreddit_url, headers=reddit_header)
            posts = [x['data'] for x in req.json()['data']['children']]

            for post in posts:
                if post["score"] > vote_threshold:
                    # See if the url is an imgur link
                    url = re.search(r"imgur.com/([\w\d]*)\.([\w]*)", post["url"])
                    if url is None or url.group is None:
                        continue
                    else:
                        # imghash = ID of the image in imgur e.g. aEaQGpz
                        imghash = url.group(1)
                        file_type = url.group(2)
                        imgur_req = requests.get("https://api.imgur.com/3/image/{}.json".format(url.group(1)),
                                                 headers=imgur_header)

                        if imgur_req is not None:
                            imgur_url = requests.get(imgur_req.json()["data"]["link"])
                            if "{}.{}".format(imghash, file_type) in current_files:
                                print ("There is a duplicate file {}.{}. Skipping.").format(imghash, file_type)
                            else:
                                output_file = open(download_path + "\{}.{}".format(imghash, file_type), "wb")
                                output_file.write(imgur_url.content)
                                print ("Downloaded {}.{} successfully!".format(imghash, file_type))
                                download_count += 1
                        else:
                            print ("Could not succesfully download the image.")
        except Exception:
            print ("Error while opening {}.\n".format(subreddit))
    print ("Downloaded {} images successfully.".format(download_count))

if __name__ == "__main__":
    main()
