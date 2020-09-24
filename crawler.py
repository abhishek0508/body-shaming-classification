import requests
import time
import json
import os
from urllib.request import urlopen, urlretrieve
from langdetect import detect
#searching hashtags by keyword
keyword='metoo'
url='https://www.instagram.com/web/search/topsearch/?context=blended&query={0}&__a=1'.format(keyword)
r=requests.get(url)
data=json.loads(r.text)
hashtags=[data['hashtags'][i]['hashtag']['name'] for i in range(len(data['hashtags']))]

#scraping posts by hashtag
hashtags=['bodyshaming']
all_posts=[]
for tag in hashtags:
    try:
#        print(tag)
        arr = []
        end_cursor = '' # empty for the 1st page
        page_count = 2  # desired number of pages
        for i in range(page_count):
            if end_cursor!=None:
                url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
                r = requests.get(url)
                data = json.loads(r.text)
                end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
                # value for the next page
                edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
                for item in edges:
                   arr.append(item['node'])
                time.sleep(2) # insurance to not reach a time limit
        all_posts+=arr
    except:
        continue
print(len(all_posts))
with open('bodyshaming.json', 'w') as outfile:
    json.dump(all_posts, outfile) # save to json

#used for preprocessing posts
def preprocess(text):
    if detect(text)=='en':
        text=text.split(' ')
        hashtags=[]
        processed_text=''
        for word in text:
            if '#' in word:
                hashtags.append(word[1:])
                processed_text+=word[1:]+' '
            elif word.isalpha():
                processed_text+=word+' '
        if processed_text=='':
            return None
        return processed_text,hashtags
    
with open('bodyshaming.json','r') as file:
    posts=json.load(file)
DIR='Pictures' #folder to save pictures
data={}
for post in posts:
    for edge in post['edge_media_to_caption']['edges']:
        text=edge['node']['text'] #post
    shortcode=post['shortcode']  #shortcode for post
    data[shortcode]=text
    try:
        display_url=post['display_url'] #url to image
        image_DIR=os.path.join(DIR,str(shortcode)+'.jpg')
        urlretrieve(display_url,image_DIR)
    except:
        continue
        



