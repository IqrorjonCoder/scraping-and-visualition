import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import matplotlib.pyplot as plt


def requester_and_get_html(url):
    res = requests.get(url)
    return bs4(res.text, "html.parser")


def get_news_linkes():
    html = requester_and_get_html("https://kun.uz/uz/news/list")
    big_div = html.find('div', class_="daily-news max-w")

    a_linkes = big_div.find_all('a', class_="daily-block l-item ")

    linkes_list = [i['href'] for i in a_linkes]

    return linkes_list


def get_text_from_linkes():
    linkes_list = get_news_linkes()

    texts = []

    for x in linkes_list:

        html = requester_and_get_html(f"https://kun.uz{x}")
        main_div = html.find('div', class_="single-layout__center slc")

        h4 = main_div.find_all('h4')
        p = main_div.find_all('p')
        title = main_div.find('div', class_='single-header__title')

        texts.append(title.text)
        for i in h4:  texts.append(i.text)
        for i in p:   texts.append(i.text)

        texts.append(
            "\n -----------------------------------------------------------separate------------------------------------------------------------------------ \n")

    return '\n'.join(texts)


def main():
    for text in get_text_from_linkes().split(
            "\n -----------------------------------------------------------separate------------------------------------------------------------------------ \n"):

        name = ' '.join(text.split()[:3])

        must_replace_words = [" bilan ", " va ", " dan ", " bu ", " Bu ", " Men ", " men ", " u ", " U ", " Ular ",
                              " ular ", " Biz ", " biz ", ". ", ", ", " ", "-", "–", '"', "'", "”", "“", ' ta ',
                              ' uning ', '«', '»', '“', '”']
        for i in range(10000):  must_replace_words.append(str(i))

        for x in range(5):
            for i in range(len(must_replace_words)):
                text = text.replace(must_replace_words[i], " ")

        text = text.split()

        # -------------------------------- Visualition ---------------------------------------- #

        r = {}
        for i in text:
            r[i] = text.count(i)

        data = pd.Series(r).reset_index()
        data.columns = ['words', 'counts']
        data = data.sort_values(by=['counts'], ascending=False)[:10]

        x = data['words']
        y = data['counts']

        plt.figure(figsize=(16, 6))

        plt.title(name, fontsize=40)

        plt.bar(x, y)


main()