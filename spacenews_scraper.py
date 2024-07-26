import requests
from lxml import html
from datetime import datetime, timedelta

def get_spacenews():
    # 获取当前日期
    today = datetime.now()
    one_week_ago = today - timedelta(days=8)

    # 初始化一个空列表用于存储新闻数据
    news_list = []

    # 定义函数爬取单个页面的新闻
    def scrape_page(url):
        response = requests.get(url)
        tree = html.fromstring(response.content)
        articles = tree.xpath('//article')
        #print(f'Found {len(articles)} articles on page {url}')

        for article in articles:
            title = article.xpath('.//header/h2/a/text()')
            title = title[0].strip() if title else 'No Title'
            #print(f'Title: {title}')
            
            abstract = article.xpath('.//div[1]/p/text()')
            abstract = abstract[0].strip() if abstract else 'No Abstract'
            #print(f'Abstract: {abstract}')
            
            tag = article.xpath('.//span/a/text()')
            tag = tag[0].strip() if tag else 'No Tag'
            #print(f'Tag: {tag}')
            
            date_str = article.xpath('.//div[2]/span[3]/a/time[1]/@datetime')
            date_str = date_str[0] if date_str else None
            #print(f'Date: {date_str}')

            # 确保每条新闻都有title, tag, abstract, date
            if title == 'No Title' or tag == 'No Tag' or abstract == 'No Abstract' or date_str is None:
                #print('Missing necessary information. Skipping...')
                continue

            date = datetime.strptime(date_str[:10], '%Y-%m-%d') if date_str else None

            # 判断新闻是否在一周内
            if date and date < one_week_ago:
                #print('Date is older than one week. Stopping...')
                return False

            link = article.xpath('.//header/h2/a/@href')
            link = link[0] if link else 'No Link'
            #print(f'Link: {link}')
            
            # 爬取新闻内容
            news_content = scrape_content(link) if link != 'No Link' else 'No Content'
            #print(f'Content: {news_content[:100]}...')  # 仅显示前100个字符以节省空间
            
            # 将新闻信息存储在字典中
            news = {
                'title': title,
                'tag': tag,
                'date': date_str,
                'link': link,
                'abstract': abstract,               
                'content': news_content
            }
            news_list.append(news)

        return True

    # 定义函数爬取新闻内容
    def scrape_content(url):
        response = requests.get(url)
        tree = html.fromstring(response.content)
        paragraphs = tree.xpath('//div[@class="entry-content"]/p')
        content = '\n'.join([p.text_content().strip() for p in paragraphs if p.text_content().strip()])
        return ' '.join(content.replace('\n', ' ').replace('\t', ' ').replace('\xa0', ' ').replace('\r', ' ').split())

    # 开始爬取第一页
    base_url = 'https://spacenews.com/?s&orderby=post_date&order=desc'
    page_num = 1

    while True:
        page_url = f'{base_url}&paged={page_num}'
        print(f'Scraping page {page_num}...')
        if not scrape_page(page_url):
            break
        page_num += 1
    filtered_list = []
    for news in news_list:
        if news['tag'].lower() not in ['policy & politics', 'military', 'opinion']:
            filtered_list.append(news)

    return filtered_list
