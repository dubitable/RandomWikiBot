import tweepy, json, requests, io, os, re, random
from PIL import Image
from bs4 import BeautifulSoup
from profanity import profanity

class wikibot:
    """Allows for the extraction of articles and associated images as well as the links for the next article."""
    conditionlist = [":", "Main_Page", "List", "("]

    def __init__(self, startpath=None):
        """Connects the script to the Twitter API."""
        #get the keys found in the json file
        with open("keys.json","r") as file:
            keys = json.loads(file.read())

        #initialize the api variable with the correct keys
        auth = tweepy.OAuthHandler(keys["consumerkey"], keys["consumerkeysecret"])
        auth.set_access_token(keys["accesstoken"], keys["accesstokensecret"])
        self.api = tweepy.API(auth)

        #initialize the startpath variable
        self.startpath = startpath

    def deleteimages(self):
        """Deletes all files in the images directory."""
        for elem in os.listdir("images"):
            os.remove(os.path.join("images",elem))

    def uploadimage(self, url):
        """"Returns a media object given an image url."""
        #delete all local images
        self.deleteimages()

        #get the url, save it locally, and upload it
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image.save(os.path.join("images","image")+os.path.splitext(url)[-1])

        #return a media object for twitter upload
        media = self.api.media_upload(os.path.join("images",os.listdir("images")[0]))
        return media

    def conditions(self, text):
        """Returns if a link is appropriate and to a Wikipedia article."""
        if text.startswith("/wiki/") and not profanity.contains_profanity(text):
            for elem in self.conditionlist:
                if elem in text:
                    return False
            return True
        return False

    def getsoup(self,url):
        """Returns a BeautifulSoup object for a given url."""
        page = requests.get(url).content
        return BeautifulSoup(page,"html.parser")

    def findnewurl(self, url):
        """Returns a random url found within a Wikipedia article."""
        soup = self.getsoup(url)
        links = []
        for elem in soup.find_all("a"):
            #make sure the <a> tag contains a link
            try: text = elem["href"]
            except: continue

            #make sure the link is appropriate and is a Wikipedia article
            if self.conditions(text):
                links.append(text)
        #return a random possible link
        return random.choice(links)

    def format(self, elem, url):
        """Returns formatted text by taking out elements within parentheses and restricting size."""
          #delete everything between parentheses
        text = elem.strip().replace("(listen)","")
        text = re.sub(r"\[(.*?)\]|\((.*?)\)", "", text)

        #delete double spaces
        text = text.replace("  ", " ")

        #find sentences and return as many as possible
        sentences = re.findall(r"(.*?\.)", text)
        x = len(sentences) - 1
        while len(text) > 280 - len(url):
            text = text[0: -1 * len(sentences[x])]
            x -= 1
        return text

    def getintro(self, articleurl, soup=None):
        """Returns the intro section of a Wikipedia article."""
        if soup is None: soup = self.getsoup(articleurl)
        for elem in soup.find_all("p"):
            #make sure the <p> tag is not empty
            try: elem["class"]
            except: break
        #format the text
        text = self.format(elem.text, articleurl)
        return text

    def getimageurl(self, url, soup=None):
        """Returns the source url of an image found on a Wikipedia article."""
        if soup is None: soup = self.getsoup(url)
        for image in soup.find_all("img"):
            #make sure it is the appropriate link
            if "//upload.wikimedia.org/wikipedia/commons/thumb/" in image["src"]:
                return "https:" + image["src"]
        return None

    def getelements(self, url, first=False):
        """Returns a new link found on a Wikipedia page as well as the associated text and image."""
        text = None
        while text is None or imageurl is None:
            #if it is the first post, the url will be the starting url given in the constructor
            if first:
                possibleurl = url
            #otherwise, find a new url
            else:
                possibleurl = self.findnewurl(url)
                possibleurl = "https://www.wikipedia.org"+ possibleurl
            #get the soup, intro, and imageurl
            soup = self.getsoup(possibleurl)
            text = self.getintro(possibleurl, soup)
            imageurl = self.getimageurl(possibleurl, soup)
        return text, possibleurl, imageurl

    def reset(self):
        """Deletes all lines in the links.txt file, resetting the system."""
        with open("links.txt","w") as file:
            file.write("")

    def tweet(self):
        """Tweets the elements found in getelements() and updates the links.txt file."""
        first = False
        with open("links.txt", "r") as file:
            #if the file is not empty, articleurl is the last line in the file
            try:
                lastline = file.readlines()[-1]
                articleurl = lastline.strip()
            except:
            #otherwise, set first to true
                if self.startpath is None: raise ValueError("You must enter a path for the starting point in the constructor.")
                articleurl = self.startpath
                first = True
        #get the elements
        message, url, imageurl = bot.getelements(articleurl, first)

        #add the link to the file
        with open("links.txt", "a") as file:
            file.write(url + "\n")
        message += "\n" + url
        print(message)
        print(len(message))

        #tweet the elements
        media = self.uploadimage(imageurl)
        media = media.media_id_string
        self.api.update_status(status = message, media_ids=[media])

bot = wikibot("https://wikipedia.org/wiki/Wikipedia")
bot.tweet()