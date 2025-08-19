

import yake
from newsapi import NewsApiClient
import config
import requests
from bs4 import BeautifulSoup

def news_search(key):
    # Init
    newsapi = NewsApiClient(api_key=config.news_api_key)

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q=key,
                                              category='business',
                                              language='en',
                                              country='us')

    # /v2/everything
    all_articles = newsapi.get_everything(q=key,
                                          sources='',
                                          domains='',
                                          language='en',
                                          sort_by='relevancy',
                                          page=2)

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()

    #print(top_headlines)
    #print("OOOOOOOOOOOOOOOO")
    #print(all_articles)
    #print("OOOOOOOOOOOOOOOO")
    #print(sources)
    return all_articles['articles']


def yake_extract(article_link):
    print(article_link)
    res = requests.get(article_link)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    result = soup.find_all(text=True)
    text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        'div',
        'button',
        'li',
        'form'
    ]

    for t in result:
        if t.parent.name not in blacklist:
            #print(t.parent.name)
            text += '{} '.format(t)
    print("start")
    print(text)
    # Simple usage with default parameters
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)

    for kw, score in keywords:
        print(f"{kw} ({score})")

    '''
    # With custom parameters
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en",  # language
        n=3,  # ngram size
        dedupLim=0.9,  # deduplication threshold
        dedupFunc='seqm',  # deduplication function
        windowsSize=1,  # context window
        top=10,  # number of keywords to extract
        features=None  # custom features
    )

    keywords = custom_kw_extractor.extract_keywords(text)
    '''

def test():


    articles = news_search('soccer')

    i = 0
    for article in articles:
        if i < 5:
            yake_extract(article['url'])
        else:
            break
        i += 1
if __name__ == '__main__':
    test()