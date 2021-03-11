import tweepy, json, requests, io, os, re, random
from PIL import Image
from bs4 import BeautifulSoup
from profanity import profanity

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
        text = re.match(r"(.*?\.)", text).groups()[0]
        return text

    def getarticle(self, articleurl):
        page = requests.get(articleurl).content
        soup = BeautifulSoup(page,"html.parser")
        for elem in soup.find_all("p")[0:4]:
            try: elem["class"]
            except: break
        text = self.format(elem)
        return text
    
    def findnewurl(self, url):
        page = requests.get(url).content
        soup = BeautifulSoup(page,"html.parser")
        links = []
        for elem in soup.find_all("a"):
            try: text = elem["href"]
            except: continue
            if text.startswith("/wiki/") and ":" not in text and "Main_Page" not in text and "(" not in text and not profanity.contains_profanity(text):
                links.append(text)
        return random.choice(links)
    
    def getimageurl(self, url):
        page = requests.get(url).content
        soup = BeautifulSoup(page,"html.parser")
        for image in soup.find_all("img"):
            if "//upload.wikimedia.org/wikipedia/commons/thumb/" in image["src"]:
                return "https:" + image["src"]
        return None

    def getelements(self, url):
        text = None
        while text is None or len(text) > 280 or imageurl is None:
            possibleurl = "https://www.wikipedia.org"+self.findnewurl(url)
            text = self.getarticle(possibleurl)
            imageurl = self.getimageurl(possibleurl)
        self.article = possibleurl
        return possibleurl, text, imageurl

    def tweet(self, message, url, imageurl):
        media = self.uploadimage(imageurl)
        media = media.media_id_string
        self.api.update_status(status = message, media_ids=[media])

url = "https://en.wikipedia.org/wiki/Wikipedia"
bot = wikibot(url)
bot.getelements(url)