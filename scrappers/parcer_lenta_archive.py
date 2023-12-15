import requests
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import random
import numpy as np
import re
import pandas as pd

base_url = 'https://lenta.ru/'
year = 2006
month = 1
day = 1
page_number = 1
counter = 0
news_urls = set()  # all urls to links
news_lenta = []  # data for all news
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


def analyze_page(url0):
    """
    in goes url of a news page,
    out goes same url, time_and_date, rubric_text, full news text
    """

    try:
        page0 = requests.get(url0, headers=headers)
    except:
        print('ERROR OCCURED')
        return None, None, None, None, None

    soup0 = BeautifulSoup(page0.text, 'html')

    date = str(soup0.find_all('a', {'class': 'topic-header__item topic-header__time'}))
    soup1 = BeautifulSoup(date, "html.parser")
    time_tag = soup1.find("a", class_="topic-header__item topic-header__time")
    try:
        time_and_date = str(time_tag.text)
    except:
        time_and_date = None

    tag = str(soup0.find_all('a', {'class': 'topic-header__item topic-header__rubric'}))
    soup1 = BeautifulSoup(tag, "html.parser")
    rubric_tag = soup1.find("a", class_="topic-header__rubric")
    try:
        rubric_text = rubric_tag.text
    except:
        rubric_text = None

    title = str(soup0.find_all('span', {'class': 'topic-body__title'}))
    soup1 = BeautifulSoup(title, "html.parser")
    title = soup1.find("span", class_="topic-body__title")
    try:
        title_text = title.text
    except:
        title_text = None

    text = soup0.find_all('p', {'class': 'topic-body__content-text'})
    soup1 = BeautifulSoup(str(text), "html.parser")
    clean_text = soup1.get_text()

    return url0, time_and_date, rubric_text, title_text, clean_text


for year in range(2006, 2023):
    for month in range(1, 12):
        for day in range(1, 31):
            while True:

                url = base_url + str(year)
                if month <= 9:
                    url = url + '/0' + str(month)
                else:
                    url = url + '/' + str(month)
                if day <= 9:
                    url = url + '/0' + str(day) + '/page/' + str(page_number)
                else:
                    url = url + '/' + str(day) + '/page/' + str(page_number)

                prev_len = len(news_urls)

                print(url)
                try:
                    page = requests.get(url)
                except:
                    # print("ERROR OCCURED")
                    continue
                soup = BeautifulSoup(page.text, 'html.parser')

                for link in soup.find_all('a'):
                    if '/news/20' in link.get('href'):
                        full_url = 'https://lenta.ru' + link.get('href')
                        news_urls.add(full_url)
                        # print(full_url)

                if prev_len == len(news_urls):
                    break
                # print(page_number)
                page_number = page_number + 1

            # sleep(random.random())
            page_number = 1


# len(news_urls)

df1 = pd.DataFrame(news_urls)
df1.to_excel('urls_lenta_archive.xlsx')

for link in tqdm(news_urls):
    res = analyze_page(link)
    # print(res)
    news_lenta.append(res)
    # sleep(random.random())
    counter += 1
    if counter % 1000 == 0:
        df = pd.DataFrame(news_lenta)
        df.columns = ['url', 'date and time', 'tag', 'title', 'text']
        df.to_excel('parsed_news_lenta_archive.xlsx')


df = pd.DataFrame(news_lenta)
df.columns = ['url', 'date and time', 'tag', 'title', 'text']
df.to_excel('parsed_news_lenta_archive.xlsx')
