import numpy as np
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrape_poem(poem_url):
    poem_page = urlopen(poem_url).read()
    soup = BeautifulSoup(poem_page, "lxml")
    poem = ''
    poem_string = soup.find_all("div", 
                                {"class": "KonaBody" })[0].find_all('p')[0]
    poem_string = str(poem_string)[3:-4].replace('<br/>', ' ')
    return (poem_string)

def scrape_poems_index(poems_index_url):
    poems_index = urlopen(poems_index_url).read()    
    soup = BeautifulSoup(poems_index, "lxml")
    pages = soup.find_all("div", {"class": "pagination"})
    if len(pages) == 0:
        return get_all_links(soup)
    
    pages = pages[0].find_all('a')
    result = {}
    cnt = 0
    for page in pages:
        page_link = 'https://www.poemhunter.com'+page['href']
        page_soup = BeautifulSoup(urlopen(page_link), "lxml")
        result.update(get_all_links(page_soup))
    return result

def get_all_links(page_soup):
    result = {}
    for link in page_soup.find_all('table')[0].find_all('a'):
        result[link.text] = 'https://www.poemhunter.com'+link['href']
    return result

def get_poems(poems_index, max_poems=None):
    poems = {}
    for i, (title, poem_url) in enumerate(poems_index.items()):
        print ('fetching', title, '...',)
        try:
            poems[title] = scrape_poem(poem_url)
            print ('OK\n')
        except:
            print ('impossible to fetch\n')
        if i == max_poems-1:
            return poems
    return poems

poems_index_neruda = scrape_poems_index('https://www.poemhunter.com/pablo-neruda/poems/')
poems_index_bukowski = scrape_poems_index('https://www.poemhunter.com/charles-bukowski/poems/')
poems_index_poe = scrape_poems_index('https://www.poemhunter.com/edgar-allan-poe/poems/')

poems_neruda = get_poems(poems_index_neruda, max_poems=60)
poems_bukowski = get_poems(poems_index_bukowski, max_poems=60)
poems_poe = get_poems(poems_index_poe, max_poems=60)

print (poems_neruda[0])
