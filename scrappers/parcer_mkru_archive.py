import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import random
import pandas as pd
from time import sleep

url_to_parce = 'https://www.mk.ru/news/'
counter = 0
news_urls = set() # all urls to links
news_mkru = [] # data for all news
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def analyze_page(url0):
    """
    Returns a tuple with 
    url0, time_and_date, tags, title_text, full_text
    Parameters:
    url0 is a link to the news (string)
    """

    try:
        page0 = requests.get(url0, headers=headers)
    except:
        return None, None, None, None, None
    
        
    soup0 = BeautifulSoup(page0.text, 'html')

    time_tag  = soup0.find('time', class_ = 'meta__text')             
    try:    
        time_and_date = time_tag.get_text(strip=True)
    except:
        time_and_date = None
    
    tag_elements = soup0.find_all('a', class_='article__tag-item')
    try:
        tags = [tag.get_text() for tag in tag_elements]
    except:
        tags = None
        
    title = (soup0.find('h1', class_ =  'article__title'))
    try:
        title_text = title.text
    except:
        title_text = None

    text_contents = (soup0.find('div', class_ =  'article__body'))
    try:
        full_text = text_contents.text
    except:
        full_text = None
        
    return url0, time_and_date, tags, title_text, full_text


def get_pages():
    """
    in goes nothing,
    out goes news url - urls of all news pages
    """
    for year in tqdm(range(1998, 2023)):
    	for month in range(1, 12):
        	for day in range(1, 31):

            	url = url_to_parce + str(year)+ '/' + str(month) + '/' + str(day) + '/'
                
            	try:
                	page = requests.get(url)
            	except:
                	continue
            	if page.status_code == 429: #Received a 429 Too Many Requests status.
                	#print('429')
                	sleep(100) # Waiting before retrying...
                	continue
                    
            	soup = BeautifulSoup(page.text, 'html.parser')
            	for link in soup.find_all('a', class_='news-listing__item-link'):
                	news_urls.add(link.get('href'))

            	sleep(2)
	return news_urls


def get_news(news_urls):
    """
    in goes news_urls,
    out goes news_mkru - df of all news pages
    """
    for link in tqdm(news_urls):
    	if link in existing_links:
        	continue
    	res = analyze_page(link)
    	# print(res)
    	news_mkru.append(res)
    	#sleep(1)
    	counter += 1
    	if counter % 10000 == 0:
        	df = pd.DataFrame(news_mkru)
        	df.columns = ['url','date and time', 'tag', 'title', 'text']
        	df.to_excel('parsed_news_mkru_archive.xlsx')

    return news_mkru


news_urls = get_pages()

df1 = pd.DataFrame(news_urls)
df1.to_excel('urls_mkru_archive.xlsx')
df = pd.read_excel('urls_mkru_archive.xlsx')
news_urls = set(df)

news_mkru = get_news(news_urls)

df = pd.DataFrame(news_mkru)
df.columns = ['url','date and time', 'tag', 'title', 'text']
df.to_excel('parsed_news_mkru_archive.xlsx')
