import tweepy, json

with open("keys.json","r") as file:
    keys = json.loads(file.read())

auth = tweepy.OAuthHandler(keys["consumerkey"], keys["consumerkeysecret"])
auth.set_access_token(keys["accesstoken"], keys["accesstokensecret"])

api = tweepy.API(auth)