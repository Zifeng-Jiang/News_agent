from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
from datetime import datetime, timedelta
import time
import requests

def get_satellitetoday_news():
    # 获取当前日期
    today = datetime.now()
    one_week_ago = today - timedelta(days=8)
    
    # 构建 URL
    date_range = f"{one_week_ago.strftime('%Y-%m-%d')}--{today.strftime('%Y-%m-%d')}"
    base_url = f"https://www.satellitetoday.com/?s=&order=desc&orderby=post_date&date_range={date_range}"
    
    # 配置 Selenium WebDriver
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(service=ChromeService(), options=options)
    driver.set_window_size(1400,1000)
    #driver = webdriver.Chrome(service=Service("/home/jzf/chromedriver_linux"), options=chrome_options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 打开目标网站
    driver.get(base_url)
    time.sleep(1.5)  # 等待页面加载
    
    # 模拟下拉操作直到没有更多内容加载
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)  # 等待内容加载
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # 获取页面内容
    page_content = driver.page_source
    tree = html.fromstring(page_content)
    articles = tree.xpath('//article')
    #print(f'Found {len(articles)} articles on page {base_url}')
    
    news_list = []

    for article in articles:
        title = article.xpath('.//div[2]/div[1]/h1/a/text()')
        title = title[0].strip() if title else 'No Title'
        #print(f'Title: {title}')

        abstract = article.xpath('.//div[2]/div[2]/text()')
        abstract = abstract[0].strip() if abstract else 'No Abstract'
        #print(f'Abstract: {abstract}')

        tag = article.xpath('.//div[2]/div[1]/div[2]/h4/a/text()')
        tag = tag[0].strip() if tag else 'No Tag'
        #print(f'Tag: {tag}')

        date_str = article.xpath('.//div[2]/div[1]/div[1]/text()')
        date_str = date_str[0].strip() if date_str else None
        #print(f'Date: {date_str}')
        
        link = article.xpath('.//div[2]/div[1]/h1/a/@href')
        link = link[0] if link else 'No Link'
        #print(f'Link: {link}')

        # 定义函数爬取新闻内容
        def scrape_content(url):
            response = requests.get(url)
            tree = html.fromstring(response.content)

            # 使用更准确的XPath来抓取内容
            content_divs = tree.xpath('//div[contains(@class, "inner_content")]')
            content = ""
            for div in content_divs:
                paragraphs = div.xpath('.//p/span')
                content += '\n'.join([p.text_content().strip() for p in paragraphs if p.text_content().strip()])
                content += '\n'
            
            content = content.strip()  # 移除多余的换行符
            return ' '.join(content.replace('\n', ' ').replace('\t', ' ').replace('\xa0', ' ').replace('\r', ' ').split())
        
        # 爬取新闻内容
        #news_content = scrape_content(link)
        news_content = ''  # 反爬机制爬不到content，但是有abstract和link

        # 将新闻信息存储在字典中
        news = {
            'title': title,
            'abstract': abstract,
            'tag': tag,
            'date': date_str,
            'link': link,
            'content': news_content
        }
        news_list.append(news)

    driver.quit()

    filtered_list = []
    for news in news_list:
        if news['tag'].lower() not in ['government/military', 'government', 'uncategorized']:
            filtered_list.append(news)
            
    return filtered_list
