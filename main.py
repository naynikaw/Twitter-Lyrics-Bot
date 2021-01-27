import lyricsgenius
import random
import tweepy
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

keys = {
    'CONSUMER_API_KEY': 'hOj4cPqpUhQXlUB5ZGrm2vcqk',
    'CONSUMER_API_SECRET_KEY': 'oTDHpFYu6wkLTts43qmEc7KWEXqEE2FHOlO6tocNQOm0uGmxtq',
    'ACCESS_TOKEN': '1348259212627898369-jQ2MepOVAxqaQ54xPqMsOuvvOd2EKP',
    'ACCESS_TOKEN_SECRET': 'cWtzgcDatYSWv5NnaPfIcHA4i03lN4DegQF9jSUwRo9U1'
}

genius = lyricsgenius.Genius("-ld3wmIcHiw63flOt-QtzRZ28fLu_S8TxUPtMOQoP17Cdx3SF-q_x5oZBSIcSo1O")
artist = genius.search_artist("The Local Train")
#print(artist.songs)

all_songs = ["Choo Lo","Dilnawaz","Aaftaab", "Dil Mere", "Aaoge Tum Kabhi", "Khudi","Mere Yaar","Vaaqif","Aakhri Salaam","Bandey","Mizaaj","Yeh Zindagi Hai","Gustaakh","Kaisey Jiyun","Manzil","Ye Zindagi Hai"]

def get_raw_lyrics():
    genius_client_access_token = "-ld3wmIcHiw63flOt-QtzRZ28fLu_S8TxUPtMOQoP17Cdx3SF-q_x5oZBSIcSo1O"
    genius = lyricsgenius.Genius(genius_client_access_token)
    random_song_title = random.choice(all_songs)
    lyrics = genius.search_song(random_song_title, "The Local Train").lyrics
    song = random_song_title.upper()
    return lyrics, song

#print(get_raw_lyrics())

def get_tweet_from(lyrics):
    lines = lyrics.split('\n')
    for index in range(len(lines)):
        if lines[index] == "" or "[" in lines[index]:
            lines[index] = "XXX"
    lines = [i for i in lines if i != "XXX"]

    random_num = random.randrange(0, len(lines)-1)
    tweet = lines[random_num] + "\n" + lines[random_num+1]
    tweet = tweet.replace("\\", "")
    tweet = transliterate(tweet, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
    return tweet

lyrics, song = get_raw_lyrics()
print(get_tweet_from(lyrics))

def handler(event, context):
    auth = tweepy.OAuthHandler(
        keys['CONSUMER_API_KEY'],
        keys['CONSUMER_API_SECRET_KEY']
    )
    auth.set_access_token(
        keys['ACCESS_TOKEN'],
        keys['ACCESS_TOKEN_SECRET']
    )
    api = tweepy.API(auth)
    lyrics, song = get_raw_lyrics()
    tweet = get_tweet_from(lyrics)
    tweet += "\nSong: " + song
    status = api.update_status(tweet)
    #bio = api.update_profile(description=song)

    return tweet