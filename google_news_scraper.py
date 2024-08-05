import feedparser
from datetime import datetime, timedelta

def get_google_news():
    # Google News RSS feed URL (近似的查询)
    rss_url = 'https://news.google.com/rss/search?q=satellite+space+news+when:7d+-Isreal+-Russia+-Ukraine+-military+-war+-combat+-geopolitics+-political&hl=en-US&gl=US&ceid=US:en'
    
    # 解析 RSS feed
    feed = feedparser.parse(rss_url)
    
    news_list = []
    
    for entry in feed.entries:
        # 解析发布时间并加8小时
        published_gmt = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
        published_gmt_plus_8 = published_gmt + timedelta(hours=8)
        
        news = {
            'title': entry.title,
            'link': entry.link,
            'date': published_gmt_plus_8.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'content': entry.title
        }
        news_list.append(news)
    
    return news_list
