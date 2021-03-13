import tweepy, json, requests, io, os, re, random
from PIL import Image
from bs4 import BeautifulSoup
from profanity import profanity

class wikibot:
    conditionlist = [":", "Main_Page", "List", "("]

    def __init__(self, articleurl=""):
        with open("keys.json","r") as file:
            keys = json.loads(file.read())

        auth = tweepy.OAuthHandler(keys["consumerkey"], keys["consumerkeysecret"])
        auth.set_access_token(keys["accesstoken"], keys["accesstokensecret"])
        self.api = tweepy.API(auth)
        self.startpath = articleurl

    def deleteimages(self):
        for elem in os.listdir("images"):
            os.remove(os.path.join("images",elem))

    def uploadimage(self, url):
        self.deleteimages()
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image.save(os.path.join("images","image")+os.path.splitext(url)[-1])
        media = self.api.media_upload(os.path.join("images",os.listdir("images")[0]))
        return media
    
    def format(self, elem):
        text = elem.text.strip().replace("(listen)","")
        text = re.sub(r"\[(.*?)\]|\((.*?)\)", "", text)
        text = text.replace("  ", " ")
        sentences = re.findall(r"(.*?\.)", text)
        text = ""
        x=0
        while x < len(sentences) and len(text)+len(sentences[x]) < 280:
            text += sentences[x]
            x+=1
        return text

    def conditions(self, text):
        if text.startswith("/wiki/") and not profanity.contains_profanity(text):
            for elem in self.conditionlist:
                if elem in text:
                    return False
            return True
        return False

    def findnewurl(self, url):
        page = requests.get(url).content
        soup = BeautifulSoup(page,"html.parser")
        links = []
        for elem in soup.find_all("a"):
            try: text = elem["href"]
            except: continue
            if self.conditions(text):
                links.append(text)
        return random.choice(links), soup

    def getarticle(self, articleurl, soup=None):
        if soup is None:
            page = requests.get(articleurl).content
            soup = BeautifulSoup(page,"html.parser")
        for elem in soup.find_all("p"):
            try: elem["class"]
            except: break
        text = self.format(elem)
        return text
    
    def getimageurl(self, url, soup=None):
        if soup is None:
            page = requests.get(url).content
            soup = BeautifulSoup(page,"html.parser")
        for image in soup.find_all("img"):
            if "//upload.wikimedia.org/wikipedia/commons/thumb/" in image["src"]:
                return "https:" + image["src"]
        return None

    def getelements(self, url, first = False):
        text = None
        while text is None or len(text) > 280 or imageurl is None:
            possibleurl = self.startpath
            if not first: possibleurl, soup = self.findnewurl(url)
            possibleurl = "https://www.wikipedia.org"+ possibleurl
            text = self.getarticle(possibleurl, soup)
            imageurl = self.getimageurl(possibleurl, soup)
        self.getimageurl = possibleurl
        with open("links.txt", "a") as file:
            file.write(possibleurl + "\n")
        return text, possibleurl, imageurl
    
    def reset(self):
        with open("links.txt","w") as file:
            file.write("")
        
    def tweet(self):
        with open("links.txt", "r") as file:
            try:
                lastline = file.readlines()[-1]
                articleurl = lastline
            except: 
                if self.startpath == "": raise ValueError("You must enter a path for the starting point in the constructor.")
                articleurl = self.startpath
        message, url, imageurl = bot.getelements(articleurl) 
        message += "\n" + articleurl
        media = self.uploadimage(imageurl)
        media = media.media_id_string
        self.api.update_status(status = message, media_ids=[media])

bot = wikibot("https://wikipedia.org/wiki/Wikipedia")
bot.tweet()