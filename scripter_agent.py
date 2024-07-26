from langchain_community.llms import Tongyi
from datetime import datetime
import os

os.environ['DASHSCOPE_API_KEY'] = 'sk-4a6d7c3447314975bcebf0b2f1e1e29e'
llm = Tongyi()

class ScripterAgent:
    def script(self, article: dict):
        content = article['content']
        word_count = len(content.split())
        # 如果content的词数小于250，则直接返回content作为summary
        if word_count < 250:
            return content
        
        prompt = [{
            "role": "system",
            "content": "You are an expert news editor."
        }, {
            "role": "user",
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n\n"
                       f"Here are the details of the best news article:\n\n"
                       f"Title: {article['title']}\n"
                       f"Tag: {article['tag']}\n"
                       f"Abstract: {article['abstract']}\n"
                       f"Content: {article['content']}\n\n"
                       f"Your task is to summarize the article into 150-200 words, highlighting the main points and ensuring it's well-written and coherent. "
                       f"Please return the summarized article in plain text, do not return other content"
        }]

        response = llm.invoke(prompt)

        # 解析大模型的输出
        summarized_content = response.strip().replace('\n', ' ') if response else "Failed to summarize the content."

        return summarized_content

    def run(self, state: dict):
        selected_news = state['selected_news']
        if 'news' not in selected_news:
            summarized_content = self.script(selected_news)
            selected_news['summary'] = summarized_content
            state['selected_news'] = selected_news  # 更新 state
        return state

