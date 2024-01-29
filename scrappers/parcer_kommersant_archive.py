import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import pandas as pd

url_to_parce = 'https://www.kommersant.ru/archive/news/day/'
base_url = 'https://www.kommersant.ru'
counter = 0
news_urls = set() # all urls to links
news_kommersant = [] # data for all news
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def analyze_page(url0):
    """
    Returns a tuple with 
    url0, time_and_date, rubric_text, title_text, full_text
    Parameters:
    url0 is a link to the news (string)
    """

    try:
        page0 = requests.get(url0, headers=headers)
    except:
        return None, None, None, None, None
    
        
    soup0 = BeautifulSoup(page0.text, 'html')

    time_tag  = soup0.find('time', class_ = 'doc_header__publish_time')             
    try:    
        time_and_date = time_tag.get_text(strip=True)
    except:
        time_and_date = None
    
    tag = (soup0.find('a', class_ = 'decor'))
    try:
        rubric_text = tag.text
    except:
        rubric_text = None
        
    title = (soup0.find('h1', class_ =  'doc_header__name js-search-mark'))
    try:
        title_text = title.text
    except:
        title_text = None

    text_contents = [p.get_text() for p in soup0.find_all('p', class_='doc__text')]
    full_text = '\n'.join(text_contents)
    
    return url0, time_and_date, rubric_text, title_text, full_text



def get_pages():
    """
    in goes nothing,
    out goes news url - urls of all news pages
    """
    for year in tqdm(range(2002, 2023)):
    	for month in range(1, 12):
        	for day in range(1, 31):

            	url = url_to_parce + str(year)
            	if month <= 9:
                	url = url + '-0' + str(month)
            	else:
                	url = url + '-' + str(month)
            	if day <= 9:
               		url = url + '-0' + str(day) 
            	else:
                	url = url + '-' + str(day) 
                
            	#print(url)
            	try:
                	page = requests.get(url)
            	except:
                	# print("ERROR OCCURED")
                	continue
            	soup = BeautifulSoup(page.text, 'html.parser')

            	for link in soup.find_all('a', class_='uho__link uho__link--overlay'):
                	news_urls.add(base_url + link.get('href'))


            	sleep(2)
    return news_urls



def get_news(news_urls):
    """
    in goes news_urls,
    out goes news_kommersant - df of all news pages
    """
    for link in tqdm(news_urls):
    	if link in existing_links:
        	continue
    	res = analyze_page(link)
    	#print(res)
    	news_kommersant.append(res)
    	sleep(1)
    	counter += 1
    	if counter % 100 == 0:
    	    df = pd.DataFrame(news_kommersant)
        	df.columns = ['url','date and time', 'tag', 'title', 'text']
        	df.to_excel('parsed_news_kommersant_archive.xlsx')
    return news_kommersant



news_urls = get_pages()

df1 = pd.DataFrame(news_urls)
df1.to_excel('urls_kommersant_archive.xlsx')
df = pd.read_excel('urls_kommersant_archive.xlsx')
news_urls = set(df[0])

news_kommersant = get_news(news_urls)

df = pd.DataFrame(news_kommersant)
df.columns = ['url','date and time', 'tag', 'title', 'text']
df.to_excel('parsed_news_kommersant_archive.xlsx')
