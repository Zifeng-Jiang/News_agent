import requests
from lxml import html
from datetime import datetime, timedelta

def add_news(topic):
    url = ''
    if topic == 'AI':
        url = "https://spacenews.com/section/AI/"
    elif topic == 'launch':
        url = "https://spacenews.com/section/launch-archive/"
    elif topic == 'commercial': 
        url = "https://spacenews.com/section/commercial-archive/"

    # 获取当前日期
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)

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
            title = title[0].strip() if title else ''
            #print(f'Title: {title}')
            
            abstract = article.xpath('.//div[1]/p/text()')
            abstract = abstract[0].strip() if abstract else ''
            #print(f'Abstract: {abstract}')
            
            date_str = article.xpath('.//div/span[3]/a/time[1]/@datetime')
            date_str = date_str[0] if date_str else None
            #print(f'Date: {date_str}')

            #确保每条新闻都有title, abstract, date
            if title == '' or date_str is None:
                #print('Missing necessary information. Skipping...')
                continue

            date = datetime.strptime(date_str[:10], '%Y-%m-%d') if date_str else None

            # 判断新闻是否在一周内
            if date and date < one_week_ago:
                #print('Date is older than one week. Stopping...')
                return False

            link = article.xpath('./div/header/h2/a/@href')
            link = link[0] if link else 'No Link'
            #print(f'Link: {link}')
            
            # 爬取新闻内容和图片
            #news_content, news_images = scrape_content_and_images(link) if link != 'No Link' else ('No Content', [])
            news_content = scrape_content_and_images(link) if link != 'No Link' else 'No Content'
            #print(f'Content: {news_content[:100]}...')  # 仅显示前100个字符以节省空间
            
            # 将新闻信息存储在字典中
            news = {
                'title': title,
                'date': date_str,
                'link': link,
                'abstract': abstract,               
                'content': news_content
                #'images': news_images
            }
            news_list.append(news)

        return True

    # 定义函数爬取新闻内容和图片
    def scrape_content_and_images(url):
        response = requests.get(url)
        tree = html.fromstring(response.content)
        paragraphs = tree.xpath('//div[@class="entry-content"]/p')
        content = '\n'.join([p.text_content().strip() for p in paragraphs if p.text_content().strip()])
        content = ' '.join(content.replace('\n', ' ').replace('\t', ' ').replace('\xa0', ' ').replace('\r', ' ').split())

        # images = tree.xpath('//figure[contains(@class, "post-thumbnail")]//img/@src')
        # image_data = []
        # for img_url in images:
        #     try:
        #         img_response = requests.get(img_url)
        #         if img_response.status_code == 200:
        #             image_data.append(BytesIO(img_response.content))
        #             #print(f"Successfully fetched image from {img_url}")
        #         #else:
        #             #print(f"Failed to retrieve image {img_url}, status code {img_response.status_code}")
        #     except Exception as e:
        #         print(f"Exception occurred while fetching image {img_url}: {e}")
        
        return content #, image_data

    # 开始爬取第一页
    base_url = url
    page_num = 1

    while True:
        page_url = f'{base_url}?paged={page_num}'
        print(f'Scraping page {page_num}...')
        if not scrape_page(page_url):
            break
        page_num += 1

    filtered_list = []
    for news in news_list:
        if 'military' not in news['title'] and 'military' not in news['abstract'] and \
        'politics' not in news['title'] and 'politics' not in news['abstract']:
            news['tag'] = topic
            filtered_list.append(news)
    return filtered_list