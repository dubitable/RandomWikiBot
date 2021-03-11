import tweepy, json, requests, io, os
from PIL import Image

class wikibot:
    def __init__(self, startpath):
        with open("keys.json","r") as file:
            keys = json.loads(file.read())

        auth = tweepy.OAuthHandler(keys["consumerkey"], keys["consumerkeysecret"])
        auth.set_access_token(keys["accesstoken"], keys["accesstokensecret"])

        self.article = startpath 
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
    
    def tweet(self, message, imageurl):
        media = self.uploadimage(imageurl)
        media = media.media_id_string
        self.api.update_status(status = message, media_ids=[media])

bot = wikibot("idk")
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Gurbanguly_Berdimuhamedow_%282017-10-02%29_02.jpg/220px-Gurbanguly_Berdimuhamedow_%282017-10-02%29_02.jpg"
bot.tweet("testing",url)