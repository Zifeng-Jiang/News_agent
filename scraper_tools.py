from spacenews_scraper import *
from find_news_mideast import *
from satellitetoday_scraper import *
from AI_launch_commercial import *
from google_news_scraper import *
from space_africa_scraper import *

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

    AI_news = add_news('AI')
    #print(len(AI_news))
    launch_news = add_news('launch')
    #print(len(launch_news))
    commercial_news = add_news('commercial')
    #print(len(commercial_news))
    result = result + AI_news + launch_news + commercial_news
    #result = AI_news + launch_news + commercial_news
    # 加入爬取google news的结果
    google_news = get_google_news()
    result = result + google_news
    # 加入爬取Space in Africa的结果
    africa_news = get_spaceinafrica()
    result = result + africa_news


    # 有些文章没有abstruct，则将标题作为abstruct
    for article in result:
        if 'abstract' not in article or article['abstract'] == '':
            article['abstract'] = article['title']
        if 'content' not in article or article['content'] == '':
            article['content'] = article['abstract']

    return result
