# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:25:26 2021

@author: Shrinidhi KR
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def rendering(url):

    driver = webdriver.Chrome(ChromeDriverManager().install()) # run ChromeDriver
    driver.get(url)                                          # load the web page from the URL
    driver.refresh()                                 
    time.sleep(10)
    try:
        while(True):
            driver.find_element_by_id("showMoreBtn").click()
            time.sleep(10)
    except Exception as e:
        print(e)
    time.sleep(10)                                           # wait for the web page to load
    render = driver.page_source                              # get the page source HTML
    driver.quit()                                            # quit ChromeDriver
    
    return render                                            # return the page source HTML

search_url = 'https://wynk.in/music/my-music/my-playlists/english/caPUWEf7NebNkkcVq0_72a13f50-29cb-4482-b3b9-9c554d8d8ddf'   #wynk playlist link

wunderground_page = rendering(search_url)

wunderground_soup = BeautifulSoup(wunderground_page, 'html.parser')

soup_container = wunderground_soup.find('ul',{'class':'albumList'})

#albumListHtml = soup_container.prettify()
#text_file = open("wynk_playlist.txt", "w", encoding="utf-8")
#n = text_file.write(albumListHtml)
#text_file.close()

song_tags = soup_container.find_all('a',{'class':'dark-text-color'})
artist_tags = soup_container.find_all('a',{'class':'light-text-color w-100 float-left text-truncate'})

df = pd.DataFrame(columns=['Song','Artist/Album'])

for song,artist in zip(song_tags,artist_tags):
    sng = {'Song':song['title'],'Artist/Album':artist['title']}
    df = df.append(sng, ignore_index=True)
    
df.to_csv('wynk_english_playlist.csv',index=False)        
    