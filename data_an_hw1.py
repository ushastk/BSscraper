# -*- coding: utf-8 -*-
"""data_an_hw1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KyJ7mB4FwQNpvG--MXVgiFXhxwyfIajr
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

columns = [
    'Title',
    'Genre',
    'Developer',
    'Publisher',
    'Released',
    'Platform',
    'Reviewer_rating',
    'User_rating',
    'Description',
    'Author_review'
]

df = pd.DataFrame(columns=columns)

n = int(input("Input count of page. "))

for i in range(1, n+1):
    link = "https://www.old-games.ru/catalog/?page=" + str(i)
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    print(i)
    for item in soup.find('table',class_="listtable").find_all('a',href=re.compile('/game/[0-9]{4,5}.html')):
        url = 'https://www.old-games.ru' + item.get('href')
        game = requests.get(url)
        bs = BeautifulSoup(game.text, 'lxml')
        title = bs.h1.string # name of game
        genre = bs.find('table',class_='gameinfo').find_all('a',class_='orangelink')[0].text
        developer = bs.find('table',class_='gameinfo').find_all('a',class_='orangelink')[1].text
        publisher = bs.find('table',class_='gameinfo').find_all('a',class_='orangelink')[2].text
        released = bs.find('table',class_='gameinfo').find_all('a',class_='orangelink')[3].text
        platform = bs.find('table',class_='gameinfo').find_all('a',class_='orangelink')[4].text
        reviewer_rating = bs.find('div',class_='rating-box').find('img')['title']
        user_rating = bs.find_all('div', class_='rating-box')[1].find('img')['title']
        description = bs.find('div',id='reviewtext').get_text() # text about game
        author_review = bs.find('div',class_='game_review_author').a.text # author review
        data = {
        'Title': title,
        'Genre': genre,
        'Developer': developer,
        'Publisher': publisher,
        'Released': released,
        'Platform': platform,
        'Reviewer_rating':reviewer_rating,
        'User_rating': user_rating,
        'Description': description,
        'Author_review': author_review
        }
        df_game = pd.DataFrame(data,index=[0])
        df = pd.concat([df, df_game], ignore_index=True)
        print(item)


df.to_csv("data_analysis_hw1_old-games.scv")