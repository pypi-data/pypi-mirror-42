from sgwc import search_articles

articles = search_articles('lol')
print(articles)
print(articles[0].save())