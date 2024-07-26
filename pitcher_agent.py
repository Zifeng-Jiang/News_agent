from langchain_community.llms import Tongyi
import json
import os
import re
from region_filter import *

os.environ['DASHSCOPE_API_KEY'] = 'sk-4a6d7c3447314975bcebf0b2f1e1e29e'
llm = Tongyi()

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
                "content": "You are an expert in satellite&AI technologies field tasked with selecting the best news article from the list below and providing its details in JSON format. Do not select sensitive titles."
            }, {
                "role": "user",
                "content": f"Here are the news articles:\n\n" + 
                        "\n\n".join([f"Title: {article['title']}\nContent: {article['abstract']}\nContent: {article['content']}" for article in news_list]) +
                        f"\n\nYour task is to select the most relevant and noteworthy article from the news above and provide its title in the following JSON format:\n"
                        f"{sample_json}\n"
            }]

            response = llm.invoke(prompt)
            #print("The LLM response is : ",response," !!!!!!End of response") 
            #print(type(response))
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
        news_list = filter_news_by_region(news_list, state['region'])
        #print("The news to be pithced", news_list)
        selected_news = self.pitch(news_list)
        #print(selected_news)
        # find the selected_news
        if 'error' not in selected_news:
            matching_news = None
            for news in news_list:
                if news['title'] == selected_news['title']:
                    matching_news = news
                    break

            if matching_news:
                print("Found matching news")

                state['selected_news'] = matching_news
            
            else:
                print("No matching news found.")
                state['selected_news'] = selected_news
        else:
            state['selected_news'] = {"region": state['region'], "news": "No news for" + state['region']}

        return state
        