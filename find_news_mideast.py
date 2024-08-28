from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from lxml import html
from selenium.webdriver.chrome.options import Options

def find_url():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(service=ChromeService(), options=options)
    driver.set_window_size(1400,1000)

    # 目标网页的URL
    url = 'https://mideastspace.substack.com/'

    # 打开网页
    driver.get(url)
    
    # 仅等待主页上可能包含文章的部分加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home-body"]/div[1]/div'))
    )

    # 获取所有包含文章标题的链接元素
    links = driver.find_elements(By.XPATH, '//a[contains(text(), "Middle East Space Roundup")]')

    # 保存结果的列表
    result_list = []

    # 遍历链接元素，提取标题和链接
    for link in links:
        href = link.get_attribute('href')
        
        entry = {
            'link': href
        }
        result_list.append(entry)
        break  # 找到第一个匹配的链接后停止搜索

    # 打印并保存结果
    if result_list:
        latest_roundup = result_list[0]
        print('最新的Middle East Space Roundup:')
        print('链接:', latest_roundup['link'])
        # 关闭浏览器
        driver.quit()
        return latest_roundup['link']
    else:
        print('未找到Middle East Space Roundup的内容')
        driver.quit()
        return None

def filter_mideast_result(result_list):
    filtered_articles = []
    for article in result_list:
        content = article['content'].lower()
        if not any(keyword in content for keyword in ["israel", "military", "politics", "geopolitics"]):
            filtered_articles.append(article)
    return filtered_articles

def get_roundup(url):
    if not url:
        return []

    # 发送GET请求获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'

    # 解析网页内容
    tree = html.fromstring(response.content)

    # 定义标题和段落的通用XPath
    title_xpath = '//h1[contains(@class, "header-anchor-post")]/strong'
    paragraph_xpath = '//p'

    # 提取所有标题和段落
    titles = tree.xpath(title_xpath)
    paragraphs = tree.xpath(paragraph_xpath)

    # 保存结果的列表
    result_list = []

    # 提取标题和对应的内容
    for i, title in enumerate(titles):
        title_text = title.text_content().strip()
        content = []

        # 找到当前标题的父级元素，再找所有的下一个兄弟元素（段落）
        current_element = title.getparent().getnext()
        while current_element is not None and (current_element.tag != 'h1'):
            if current_element.tag == 'p':
                content.append(current_element.text_content().strip())
            current_element = current_element.getnext()

        content_text = " ".join(content)
        
        # 创建包含标题和内容的字典
        entry = {
            'title': title_text,
            'link': url,
            'content': content_text
        }
        
        # 将字典添加到列表中
        result_list.append(entry)
    return filter_mideast_result(result_list)

    
