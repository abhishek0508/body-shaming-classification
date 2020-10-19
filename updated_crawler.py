import requests
import time
import json
import os
from urllib.request import urlopen, urlretrieve
from langdetect import detect
import csv  
import sys
import re

#searching hashtags by keyword
# keyword='metoo'
# url='https://www.instagram.com/web/search/topsearch/?context=blended&query={0}&__a=1'.format(keyword)
# print(url)
# r=requests.get(url)
# data=json.loads(r.text)
# hashtags=[data['hashtags'][i]['hashtag']['name'] for i in range(len(data['hashtags']))]

#scraping posts by hashtag
cnt=0
hashtags=['bodyshaming', 'stopbodyshaming']
all_posts=[]
for tag in hashtags:
    try:
#        print(tag)
        arr = []
        end_cursor = '' # empty for the 1st page
        page_count = 150  # desired number of pages
        for i in range(page_count):
            if end_cursor!=None:
                url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
                # print()
                # print(url)
                r = requests.get(url)
                data = json.loads(r.text)
                end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
                # value for the next page
                edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
                for item in edges:
                   arr.append(item['node'])
                cnt+=len(arr)
                print(cnt)
                time.sleep(2) # insurance to not reach a time limit
        print()
        all_posts+=arr
    except:
        continue

with open('bodyshaming.json', 'w') as outfile:
    json.dump(all_posts, outfile) # save to json

# sys.exit(1)

#used for preprocessing posts
def preprocess(text):
    # print(text)
    if detect(text)=='en':
        
        text=text.replace("\n", " ")
        
        text = re.sub(r"http\S+", "", text)		#Remove any links
        text = re.sub(r"www\S+", "", text)
        
        text = re.sub(r"@\S+", "", text)		#Remove any username

        text=re.sub(r"(?<=\w)([#])", r" \1", text)		#Seperate hashtags
        
        text=re.sub('[^a-zA-Z0-9#]+', ' ', text)			#Remove unwanted characters
        
        text=text.split(' ')
        
        
        hashtags=[]
        processed_text=''
        for word in text:
            if '#' in word:
                word=word[word.find('#'):]
                # print(word)
                hashtags.append(word[1:])
                # processed_text+=word[1:]+' '
            elif word.isalpha():
                processed_text+=word+' '
        if processed_text=='':
            return None
        return processed_text,hashtags
    

csvfile=open("text.csv", 'w')  
csvwriter = csv.writer(csvfile)  

txt=[]
check_txt=[]
with open('bodyshaming.json','r') as file:
    posts=json.load(file)

DIR='Pictures' #folder to save pictures
if not os.path.exists(DIR):
    os.makedirs(DIR)

data={}
pt=""
h=[]
hh=" "
ccc=0
for post in posts:
    for edge in post['edge_media_to_caption']['edges']:
        text=edge['node']['text'] #post
        # print(text)
        # print()
        try:
	        pt,h=preprocess(text)
	        hh=hh.join(h)
	        # print("newwww")
	        # print(pt)
	        # print(hh)
	        # print()
	        # print()
        except:
            continue
    if pt:
	    shortcode=post['shortcode']  #shortcode for post
	    data[shortcode]=text
	    try:
	    	if [pt,h] not in check_txt:
		        ccc=ccc+1
		        display_url=post['display_url'] #url to image
		        image_DIR=os.path.join(DIR,str(shortcode)+'.jpg')
		        check_txt.append([pt,h])
		        # print(pt)
		        # print(h)
		        pt=pt+"\n\n"+hh
		        print(ccc)
		        # print(pt)
		        txt.append([pt,image_DIR])
		        urlretrieve(display_url,image_DIR)
	    except:
	        continue
	    pt=""
	    h=""
	    hh=" "
# print(txt)
csvwriter.writerows(txt) 