# Random WikiBot
Every day, this bot publishes a semi-random Wikipedia article to the [@random_wikibot](https://twitter.com/random_wikibot) account on Twitter. It's also immortal.
## How Does It Work?
This program is actually loosely based upon a game I used to play with my friends called "Wikipedia Speedrun". Due to the sheer amount of Wikipedia articles as well as the links present on each, it is possible to go from any article to another just by clicking links. The fastest to do so, usually concerning completely unrelated concepts, such as "Turkmenistan" to "Chicharrones", would win. The bot acts in a very similar way: for the first post, it requires a starting path, which I chose to be the "Wikipedia" article of Wikipedia. The program will then find the intro text, an image, and a link found on the page for the next article so that the cycle continues. The links that have already been used are stored in "links.txt", so that if you tweet once and stop the program, it will pick up where it left off. The articles are passed through a profanity check so that inappropriate material is not published. To publish it periodically, I used the "Tasks" system on PythonAnywhere so that I did not have to run the program locally. Thus, wikibot will continue publishing content until something I have not foreseen happens or the universe ends.
## How To Make Your Own WikiBot
#### Apply for a Twitter Developer Account
Although bots are usually not encouraged on most social medias, Twitter actually provides an API that allows an impressive range of actions, most notably tweeting for this use case. The first thing you need to do is create a Twitter account, and then apply for an associated developer account at https://developer.twitter.com/en/apply-for-access. Once you have access to this account, you can create a standalone app or a project (I chose a standalone app as I only needed the tweet feature). This will generate different keys (you can always generate new ones if you forget to copy and paste). You will need the "Consumer Key", "Consumer Key Secret", "AccessToken", and "Access Token Secret".
#### Configuration
You may have noticed that there is a half-empty json file in the repository called "template.json". This is where you will fill in each key received in the last step (between the quotation marks). Do not forget to rename it to "keys.json" in order for the program to open the correct file (or modify the path in the constructor of the wikibot class in wikibot.py). You will also need to install the following modules: "tweepy", "Pillow", "bs4", and "profanity" (use this [link](https://docs.python.org/3/installing/index.html) if you do not know how to). The program should be fully functional now.
#### Running in the cloud
This program is actually the second version of my WikiBot: I made the original when I was less experienced and when I used a janky Instagram bot library. Even if it was far from perfect, it worked. However, I soon came accross a sizeable problem: I had to run it locally and continuously, using "time.sleep()" to create periodic posting. This was inconvenient on an immense amount of levels, so I came up with a solution for this version: hosting the bot in the cloud using PythonAnywhere. They have a system called "Tasks" which can run a program daily for free users. After you have created an account, upload the project directory (containing "links.txt", "images" folder, "wikibot.py", and "keys.json") to the site. Open a console and create a [virtualenv](https://help.pythonanywhere.com/pages/Virtualenvs/) where you can install all the modules. Finally, you can add a task using this virtual environment by using this template:
```
/home/myusername/.virtualenvs/myvenv/bin/python /home/myusername/myproject/mytask.py
```
The bot will now tweet daily without you needing to intervene.
## Functionality
```
wikibot(startpath=None)
```

The WikiBot Class allows for the extraction and tweeting of articles and associated images as well as the links for the next article. The script does not need to run continuously, as past articles are stored locally in "links.txt". The constructor will connect the bot to the Twitter API and initialize the `wikibot.api` and `wikibot.startpath` instance variables.  

Parameters:
- `startpath`: a url (`string`) to the Wikipedia article you would like to begin with - the program will only tweet the corresponding article if "links.txt" is empty, so it is not necessary to specify this argument if is not (optional argument set at `None` by default).  
```
wikibot.tweet()
```

Tweets the elements found in getelements() and updates the "links.txt" file. If "links.txt" is empty, it will use startpath as a url, otherwise it will find a new one based off the last url in "links.txt".   

```
wikibot.getelements(url, first = False)
```

If first is `True`, return the intro and associated image of the `url` Wikipedia article. If first is `False`, find a new url found within the `url` Wikipedia article, and return the new url, intro and associated image of the new article.  

Parameters:
- `url`: a url (`string`) to a Wikipedia article.
- `first`: a value (`bool`) determining if this is the first tweet or not.
```
wikibot.findnewurl(url)
```

Returns a random url found within a `url` Wikipedia article.  

Parameters:
- `url`: a url (`string`) to a Wikipedia article.
```
wikibot.getintro(url, soup=None)
```

Returns the intro section of an `url` Wikipedia article.

Parameters:
- `url`: a url (`string`) to a Wikipedia article.  
- `soup`: a `BeautifulSoup` object of the source code of a Wikipedia article.
```
wikibot.getimageurl(url, soup=None)
```

Returns the source url of an image found on a Wikipedia article.  

Parameters:
- `url`: a url (`string`) to a Wikipedia article.  
- `soup`: a `BeautifulSoup` object of the source code of a Wikipedia article.

```
wikibot.uploadimage(url)
```

Returns a tweepy media object given an image source.

Parameters:
- `url`: the source url (`string`) to an image.

```
wikibot.getsoup(url)
```

Returns a BeautifulSoup object for a given url.  

Parameters:
- `url`: a url (`string`) to a website.

```
wikibot.conditions(url)
```

Returns True if a link is appropriate and to a Wikipedia article.    

Parameters:
- `url`: a url (`string`) to a website.

```
wikibot.format(text)
```

Returns formatted text by taking out elements within parentheses and restricting size.  

Parameters:
- `text`: a text (`string`).

```
wikibot.reset()
```

Deletes all lines in the links.txt file, resetting the system.  

```
wikibot.deleteimages()
```

Returns a BeautifulSoup object for a given url.  
