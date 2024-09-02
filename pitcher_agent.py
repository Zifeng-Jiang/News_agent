from openai import OpenAI
import json
import re
from region_filter import *

class PitcherAgent:
    def pitch(self, news_list: list):
        if len(news_list) > 1:
            # 定义 prompt 模板
            sample_json = """
            {
                "title": "Title of the best article"
            }
            """
            prompt = [{
                "role": "system",
                "content": "You are an expert in satellite&AI technologies field tasked with selecting the best commercial satellite news article from the list below and providing its title in JSON format."
            }, {
                "role": "user",
                "content": f"Here are the news articles' title and part of the content:\n\n" + 
                        "\n\n".join([f"Title: {article['title']}\n Content: {article['content'][:1000]}\n" for article in news_list]) +
                        f"\n\nYour task is to select the most relevant and noteworthy and positive article from the news above and return its title in the following JSON format:\n"
                        f"{sample_json}\n"
            }]

            client = OpenAI(
                api_key="sk-TzvAm1AGbpwILDIN37Be6fDe1bAb4d2b9731EdE47b944e23", 
                base_url="https://free.gpt.ge/v1/"
            )
        
            completion = client.chat.completions.create(
                model = "gpt-3.5-turbo-16k",
                messages = prompt,
                temperature = 0.6,
            )
            response = completion.choices[0].message.content

            # 解析大模型的输出
            pattern = r'\{[^{}]*\}'
            match = re.search(pattern, response)
            if match:
                selected_news = json.loads(match.group(0))  
            else:
                selected_news = {"error": "Failed to parse the response from the model"}
        elif len(news_list) == 1: 
            selected_news = news_list[0]
        else:
            selected_news = {"error": "No news for this region"}
        return selected_news

    def run(self, state: dict):
        news_list = state['news_list']
        region = state['region']
        if region in ['AI', 'launch', 'commercial']:
            # print("The news to be pitched in", region)
            # print(news_list)
            selected_news = self.pitch(news_list)
        else:
            news_list = filter_news_by_region(news_list, region)
            # print("The news to be pitched in", region)

            # for news in news_list:
            #     print(news)

            selected_news = self.pitch(news_list)
            #print(selected_news)
        # find the selected_news
        if 'error' not in selected_news:
            matching_news = None
            for news in news_list:
                if selected_news['title'].lower() in news['title'].lower():
                    matching_news = news
                    break

            if matching_news:
                print("Found matching news")
                state['selected_news'] = matching_news
                #print(matching_news)
            
            else:
                print("No matching news found.")
                state['selected_news'] = {"region": state['region'], "news": "No matching news for " + state['region']}
        else:
            state['selected_news'] = {"region": state['region'], "news": "No news for " + state['region']}

        return state
        