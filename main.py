import streamlit as st
from pitcher_agent import PitcherAgent
from scripter_agent import ScripterAgent
from langgraph.graph import StateGraph
from typing import List, TypedDict
import json
from io import StringIO
from scraper_tools import run_news_scraper

class NewsState(TypedDict):
    region: str
    news_list: List[dict]
    selected_news: dict

# 构建完整的LangGraph
main_graph = StateGraph(NewsState)

pitcher_agent = PitcherAgent()
main_graph.add_node("pitcher", pitcher_agent.run)
scripter_agent = ScripterAgent()
main_graph.add_node("scripter", scripter_agent.run)
main_graph.add_edge("pitcher", "scripter")

# 设置图的入口点和出口点
main_graph.set_entry_point("pitcher")
main_graph.set_finish_point("scripter")

# streamlit app page
st.set_page_config(page_icon="📰", page_title="SpaceNews Agents")
st.title('📰SpaceNews Agents🤖')

"""Hello 👋🏻 You can get space/satellite news from all over the world through SpaceNews Agents."""
st.write("China | Middle East | Africa | Central Asia | Southeast Asia | Latin America | AI | Launch")
btn = st.button("Start Collecting and Summarizing")
message_placeholder = st.empty()
if btn:
    message_placeholder.empty()  # Clear previous success or error messages
    with st.spinner('Collecting and summarizing news...'):
        #regions = ["china"]
        regions = ["china", "middle_east", "africa", "central_asia", "southeast_asia", "latin_america"]
        best_news = []
        news_list = run_news_scraper()
        for news in news_list:
            # 初始化所有可能的字段，避免 KeyError
            news.setdefault('title', '')
            news.setdefault('link', '')
            news.setdefault('published_date', '')
            news.setdefault('tag', '')
            news.setdefault('summary', '')
            news.setdefault('abstract', '')
            news.setdefault('content', '')
        for region in regions:
            # 初始化状态
            initial_state = {
                "region": region,
                "news_list": news_list,
                "selected_news": {}
            }

            # 运行LangGraph
            app = main_graph.compile()
            final_state = app.invoke(initial_state)
            selected_news = final_state["selected_news"]
            if 'title' in selected_news:
                selected_news["region"] = region
                #print(json.dumps(selected_news, indent=4, ensure_ascii=False))
                best_news.append(selected_news)
        # 将 best_news 列表转换为带格式的 txt 文件
        news_txt = StringIO()
        for article in best_news: 
            news_txt.write(f"region: {article.get('region', 'N/A')}\n")
            news_txt.write(f"title: {article.get('title', 'N/A')}\n")
            news_txt.write(f"link: {article.get('link', 'N/A')}\n")
            news_txt.write(f"date: {article.get('date', 'N/A')}\n")
            news_txt.write(f"tag: {article.get('tag', 'N/A')}\n")
            news_txt.write(f"summary: {article.get('summary', 'N/A')}\n")
            news_txt.write(f"abstract: {article.get('abstract', 'N/A')}\n")
            news_txt.write(f"content: {article.get('content', 'N/A')}\n")
            news_txt.write("\n")  # 每两个新闻条目之间间隔一行

        news_txt.seek(0)
        news_txt_content = news_txt.getvalue()
        message_placeholder.success("News summarization completed successfully!")
        st.download_button(
            label="Download News Summary as TXT",
            data=news_txt_content,
            file_name="news_summary.txt",
            mime="text/plain",
        )
