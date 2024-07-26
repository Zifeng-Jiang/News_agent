from spacenews_scraper import *
from find_news_mideast import *
from satellitetoday_scraper import *

def run_news_scraper():
    result = get_spacenews()
    #print(result)

    # 特殊照顾一下中东地区，再爬取https://mideastspace.substack.com/加入原先的SpaceNews        
    roundup = get_roundup(find_url())
    result = result + roundup
    #print(roundup)

    # 加入爬取https://www.satellitetoday.com/的结果
    satellitetoday_news = get_satellitetoday_news()
    result = result + satellitetoday_news
    #print(satellitetoday_news)

    # 有些文章没有abstruct，则将标题作为abstruct
    for article in result:
        if 'abstract' not in article or article['abstract'] == '':
            article['abstract'] = article['title']
        if 'content' not in article or article['content'] == '':
            article['content'] = article['abstract']

    return result
