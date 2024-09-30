from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import requests
import time
import datetime
import os

#Scraping top repositories for topics on github

#Introduction about web scrapping

#the tools we are gonna use are python, requests, BeautifulSoup, pandas, numpy

#here are the stps we are going to follow

#We will get list of topics. For each topic, we will get topic title
#topic page URL, topic description
#for each topic we will get the 25 repos in the topic from topics page
#for each repo we will grab the repo nmae, username, stars and url
#for each topic we create csv File in the following format


topic_url = "https://github.com/topics"


path = "D:/MachineLearning/WebScrapingProject/tokyoUniversity.html"


response = requests.get(topic_url)  #every request culminates ina presone which contains some content or status code
with open(path, "w", encoding="utf-8") as f:   #open the file in write mode
    f.write(response.text)

#Browse through different steps and pick on to scrape.
#we are going to scrape github explore section

response.status_code

page_contents = response.text 


page_contents[: 1000]
len(response.text)


#headers = 

#we will install beatifulsoup


doc = BeautifulSoup(page_contents, "html.parser")

topic_title_p_tags = doc.find_all("p", {'class':'f3 lh-condensed mb-0 mt-1 Link--primary'})

len(topic_title_p_tags)

(topic_title_p_tags[:5])

desc_selector = 'f5 color-fg-muted mb-0 mt-1'

topic_desc_p_tags = doc.find_all('p', {'class': desc_selector})

(topic_desc_p_tags[:5])

topic_title_p_tag0 = topic_title_p_tags[0]

topic_title_p_tag0.parent

topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})
topic_url = "https://github.com" + (topic_link_tags[0] ['href'])

(len(topic_link_tags))
topic_titles = []

for tag in topic_title_p_tags:
    topic_titles.append(tag.text)


topic_dexcriptions = []

for tag in topic_desc_p_tags:

    topic_dexcriptions.append(tag.text.strip())


topic_urls =[]
base_url = "https://github.com"

for tag in topic_link_tags:
    topic_urls .append(base_url + tag['href'])



#to create csv files
import pandas as pd

topic_dict ={
    'title': topic_titles,
    'description': topic_dexcriptions,
    'url': topic_urls
}

topics_dataframe = pd.DataFrame(topic_dict)

(topics_dataframe)

topics_dataframe.to_csv('topics.csv', index = None)

#Getting information out of a topic page

topic_page_url = topic_urls[0]

print(topic_page_url)

response = requests.get(topic_page_url)

response.status_code

len(response.text)

topic_doc = BeautifulSoup(response.text, 'html.parser')

repo_tags = topic_doc.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})


repo_tags[0]

a_tags = repo_tags[0].find_all('a')

a_tags[0].text.strip()

a_tags[1].text.strip()


base_url ='https://github.com'

repo_url = base_url + a_tags[1]['href']

print(repo_url)

star_tags = topic_doc.find_all('span',{'class': 'Counter js-social-count'})

p = (star_tags[0].text.strip())

print(p)

def parse_star_count(stars_str):

    stars_str = stars_str.strip()

    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    
print(parse_star_count(star_tags[0].text.strip()))


topics_repos_dict ={
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []  
    }





def get_repo_info(h3_tag, star_tags):

    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tags.text.strip())


    return username, repo_name, repo_url, stars


def get_topic_repos(topic_url):

    #download the page
    response = requests.get(topic_url)
    if response.status_code != 200:  #check suuccesful response
       raise Exception ("failed to load page: {}".format(topic_url))
    
    #parse using beautiful soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    
    #get h1 tags containing repo title, url, and username
    repo_tags = topic_doc.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
    
    #get star tags
    star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})
    
    #get dict info

    topics_repos_dict ={
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []  
    }

    #get repo info


    for i in range(len(repo_tags)):

        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topics_repos_dict['username'].append(repo_info[0])
        topics_repos_dict['repo_name'].append(repo_info[1])
        topics_repos_dict['repo_url'].append(repo_info[2])
        topics_repos_dict['stars'].append(repo_info[3])

    return pd.DataFrame(topics_repos_dict)

topics_repos_dataf = pd.DataFrame(topics_repos_dict)

topic4_doc = get_topic_repos(topic_urls[4])


#write a single function to:
#   1. Get the list of topics from the topics page
#   2. get the list of top repos from individual topic pages
#   3. for each topic, create a csv of the top repos for the topic
def get_topic_titles(doc):

    doc = BeautifulSoup(page_contents, "html.parser")


    topic_title_p_tags = doc.find_all("p", {'class':'f3 lh-condensed mb-0 mt-1 Link--primary'})
    
    topic_titles = []

    for tag in topic_title_p_tags:
       topic_titles.append(tag.text)

    return topic_titles

def get_topic_descriptions(doc):

    doc = BeautifulSoup(page_contents, "html.parser")

    topic_desc_p_tags = doc.find_all('p', {'class': desc_selector})
    
    topic_dexcriptions = []

    for tag in topic_desc_p_tags:

        topic_dexcriptions.append(tag.text.strip())

    return topic_dexcriptions

def get_topic_urls(doc):

    doc = BeautifulSoup(page_contents, "html.parser")

    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})
    
    topic_urls =[]

    base_url = "https://github.com"

    for tag in topic_link_tags:
        topic_urls .append(base_url + tag['href'])

    return topic_urls


def scrape_topics_in_repos():

    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to lad page  {}'.format(topic_url))
    
    topics_dict ={
        'title':  get_topic_titles(doc),
        'descriptions' : get_topic_descriptions(doc),
        'urls': get_topic_urls(doc)
    }

    return pd.DataFrame(topics_dict)

def scrape_topic(topic_url, path):

    if os.path.exists(path):
        print('The file {} is already exists. Skipping...'.format(path))

    topic_df = get_topic_repos(topic_url)
    topic_df.to_csv(path, index = None)



def scrape_topics_repos():

    print ('Scraping list o topics')
    topics_df = scrape_topics_in_repos()

    os.makedirs('data', exist_ok= True)

    for index, row in topics_df.iterrows():
        print('Scraping top repositeries for "{}"'.format(row['title']))

        scrape_topic(row['urls'], 'data/{}.csv'.format(row['title']))

print(scrape_topics_repos()) 
