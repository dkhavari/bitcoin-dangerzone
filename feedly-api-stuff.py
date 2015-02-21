from libraries import feedlyclient
import requests
from bs4 import BeautifulSoup
import cfscrape


def get_urls():
    urls = []
    
    user_id = 'da75f8c1-616c-4f00-8a45-79e77cb2e99e'
    token = 'AmVJitV7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQzMTkyMzQyNzM4NywiaSI6ImRhNzVmOGMxLTYxNmMtNGYwMC04YTQ1LTc5ZTc3Y2IyZTk5ZSIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwidyI6IjIwMTUuOCIsIngiOiJzdGFuZGFyZCJ9:feedlydev'
    
    feedly = feedlyclient.FeedlyClient(sandbox=False) #creates my client
    
    user_subs = feedly.get_user_subscriptions(token) #gets all subscriptions of mine
    
    for sub in user_subs:
        sub_id = sub['id'] #gets the id of each successive subscription
        content = feedly.get_feed_content(access_token = token, streamId = sub_id, unreadOnly = False, newerThan = False)
        articles = content['items'] #finds the articles in the content dict
        for article in articles:
            list_ = article['alternate'] #pulls the info like url and all that
            dict_ = list_[0] #for whatever reason the previous line returned a list of length one containing a dict
            url = dict_['href'] #this is where the url was hiding
            urls.append(url)
            print article['published'] #returns when it was published, not positive on the format, though
    return urls        


def get_text(urls):
    all_texts = []
    
    scraper = cfscrape.create_scraper() #this is necessary to bypass CloudFlare doing its job
    for url in urls:
        html = scraper.get(url).content #scrapes html. take that, CloudFlare
        soup = BeautifulSoup(html)
        for script in soup(["script", "style", 'a']):  #removes all js and unnecessary links, might put back links, though.
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines()) # breaks multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # drops blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        all_texts.append(text)
        print text
        print '+++++++++++++++++++++++++++++++++++++'
    return all_texts    
        


urls = get_urls()
#texts = get_text(urls)        