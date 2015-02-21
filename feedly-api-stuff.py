from libraries import feedlyclient
import requests
from bs4 import BeautifulSoup
import cfscrape
import datetime


def get_urls():
    
    # Boilerplate Feedly interaction.
    user_id = 'da75f8c1-616c-4f00-8a45-79e77cb2e99e'
    token = 'AmVJitV7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQzMTkyMzQyNzM4NywiaSI6ImRhNzVmOGMxLTYxNmMtNGYwMC04YTQ1LTc5ZTc3Y2IyZTk5ZSIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwidyI6IjIwMTUuOCIsIngiOiJzdGFuZGFyZCJ9:feedlydev'
    feedly = feedlyclient.FeedlyClient(sandbox=False) # Instantiate my client.
    user_subs = feedly.get_user_subscriptions(token) # Gets all of my subscriptions.

    urls = []
    
    for sub in user_subs:
        sub_id = sub['id'] # Gets the id of each successive subscription.
        content = feedly.get_feed_content(access_token = token, streamId = sub_id, unreadOnly = False, newerThan = False)
        articles = content['items'] # Finds the articles in the content dict.
        for article in articles:
            list_ = article['alternate'] # Pulls the article metadata like url.
            dict_ = list_[0] # Random nesting: for whatever reason the previous line returned a list of length one containing a dict.
            url = dict_['href'] # This is where the url is stored.
            urls.append(url)
            unixy_time = article['published'] # Returns when it was published in 13-digit unix-like timestamp.
            time_and_date = datetime.datetime.fromtimestamp(int(unixy_time/1000)).strftime('%a %Y-%m-%d %H:%M:%S') #convert from their weird unix-esque 13-digit time format.
            print time_and_date
    return urls        


def get_text(urls):
    all_texts = []
    
    scraper = cfscrape.create_scraper() # Bypass CloudFlare.
    for url in urls:
        html = scraper.get(url).content # Scrapes the HTML from the list of URLs.
        soup = BeautifulSoup(html)
        for script in soup(["script", "style", 'a']):  # Strips JS and other links for now.
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines()) # Breaks down multi-line headlines into one line each.
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # Drops blank lines.
        text = '\n'.join(chunk for chunk in chunks if chunk)
        all_texts.append(text)
        print text
        print '+++++++++++++++++++++++++++++++++++++'
    return all_texts    

urls = get_urls()
#texts = get_text(urls)        