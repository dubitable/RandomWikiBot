import tweepy, json, requests, io, os, re
from PIL import Image
from bs4 import BeautifulSoup

class wikibot:
    def __init__(self, startpath):
        with open("keys.json","r") as file:
            keys = json.loads(file.read())

        auth = tweepy.OAuthHandler(keys["consumerkey"], keys["consumerkeysecret"])
        auth.set_access_token(keys["accesstoken"], keys["accesstokensecret"])

        self.articleurl = startpath 
        self.api = tweepy.API(auth)

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
        return re.match(r"(.*?\.)", text).groups()[0]

    def getarticle(self, articleurl = None):
        if articleurl is None: articleurl = self.articleurl
        page = requests.get(articleurl).content
        soup = BeautifulSoup(page,"html.parser")
        for elem in soup.find_all("p")[0:4]:
            try: elem["class"]
            except: break
        text = self.format(elem)
        return text

    def tweet(self, message, imageurl):
        media = self.uploadimage(imageurl)
        media = media.media_id_string
        self.api.update_status(status = message, media_ids=[media])

bot = wikibot("https://en.wikipedia.org/wiki/Wikipedia")
print(bot.getarticle())