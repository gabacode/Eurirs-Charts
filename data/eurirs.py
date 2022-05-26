import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup

'''
Get Eurirs data from Euribor website
'''

all_res = []


def get_table(url):
    date = url.rpartition('/')[0].rpartition('-')[2]
    if date == 'oggi':
        date = datetime.datetime.now().date().strftime("%Y")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table), header=0)[0]
    df.columns = ['Date', '10', '15', '20', '25', '30']
    df['Date'] = (df['Date'] + '/' + date)
    df['Date'] = df['Date'].str.replace('(', '/')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    all_res.append(df)


def get_euribor_table(url):
    date = url.rpartition('/')[0].rpartition('-')[2]
    if date == 'oggi':
        date = datetime.datetime.now().date().strftime("%Y")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table), header=0)[0]
    df.columns = ['Date', '1', '3', '6', '12']
    df['Date'] = (df['Date'] + '/' + date)
    df['Date'] = df['Date'].str.replace('(', '/')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    all_res.append(df)


def get_eurirs():
    global all_res
    links = []
    url = 'https://www.euribor.it/tassi-storici-eurirs/'
    html = requests.get(url)
    body = BeautifulSoup(html.text, "html.parser")
    hrefs = body.find_all("a")
    for link in hrefs:
        if link.get("href") and "/eurirs" in link.get("href") and "euribor" not in link.get("href"):
            ref = link.get("href")
            links.append('https://www.euribor.it' + ref)
    for url in links:
        get_table(url)
    df_res = pd.concat(all_res)
    df_res.to_csv('./data/eurirs.csv', index=False)
    all_res = []
    print('Done')


def get_euribor():
    global all_res
    links = []
    url = 'https://www.euribor.it/tassi-storici-euribor/'
    html = requests.get(url)
    body = BeautifulSoup(html.text, "html.parser")
    hrefs = body.find_all("a")
    for link in hrefs:
        if link.get("href") and "/euribor" in link.get("href") and "https://www.euribor.it/" not in link.get("href"):
            ref = link.get("href")
            links.append('https://www.euribor.it' + ref)
    for url in links:
        get_euribor_table(url)
    df_res = pd.concat(all_res)
    df_res.to_csv('./data/euribor.csv', index=False)
    all_res = []
    print('Done')


get_eurirs()
get_euribor()
