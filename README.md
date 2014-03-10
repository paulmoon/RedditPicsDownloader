Reddit Pics Downloader
======================

### About
Reddit Pics Downloader downloads popular wallpaper-worthy images from reddit's popular [wallpaper subreddits](http://www.reddit.com/r/earthporn+waterporn+skyporn+spaceporn+fireporn+destructionporn+geologyporn+winterporn+autumnporn+cityporn+villageporn+abandonedporn+infrastructureporn+machineporn+militaryporn+cemeteryporn+architectureporn+carporn+gunporn+boatporn+aerialporn+F1porn+ruralporn+animalporn+botanicalporn+humanporn+adrenalineporn+climbingporn+culinaryporn+foodporn+dessertporn+agricultureporn+designporn+albumartporn+movieposterporn+adporn+geekporn+instrumentporn+macroporn+artporn+fractalporn+exposureporn+microporn+metalporn+streetartporn+historyporn+mapporn+bookporn+newsporn+quotesporn+futureporn).

### How to run
First, you need to get an imgur API key [here](http://api.imgur.com/#register). Place the Python program in a folder where you would like your images to be downloaded, and run the program. Supported command-line arguments are:
- -top : Sort type for posts in a subreddit. Available ones are day, week, month, year, and all. Default is day.
- -sub : Subreddits to download images from. Multiple subreddits must be separated by commas without spaces e.g. wallpaper,pics,funny. Default is [wallpaper subreddits](http://www.reddit.com/r/roomporn+wallpapers+wallpaper+spaceporn+earthporn+waterporn+skyporn+spaceporn+topwalls).
- -score : Minimum threshold that the post's score must meet. Default is 500.

Example: python RedditPicsDownloader.py -top week -sub wallpapers,cars -score 1000

### Dependencies
- [PIL](http://www.pythonware.com/products/pil/)
- [PRAW](https://praw.readthedocs.org/en/latest/)

### To-Do List
- [X] Get Weekly/Monthly top posts since they are more likely to have a higher score.
- [x] Implement command line arguments support for subreddits, vote threshold, keywords etc.
- [ ] Imgur album support.
