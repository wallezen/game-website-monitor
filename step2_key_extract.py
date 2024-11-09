import openai  # 确保已安装 openai 库
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import time
import logging
import os
from openai import OpenAI

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置OpenAI API密钥
openai.api_key = 'xxxx'  # 替换为实际的API密钥


def extract_keywords_from_game_names(game_names):
    """使用GPT API从游戏名称中提取关键词"""
    keywords = ""
    try:
        sys_prompt = "You are a Google SEO expert. I will give you some game information, and you need to help me summarize the information into a single Google SEO keyword. Please output only the keyword."
        # prompt = "从以下游戏名称中提取相关的AI关键词:\n\n" + "\n".join(game_names)
        model_name = "gpt-4o-mini"  # "gpt-4o", #gpt-4o gpt-3.5-turbo  gpt-4o-ca, gpt-3.5-turbo-16k
        client = OpenAI(
            api_key=openai.api_key,
            base_url="https://api.chatanywhere.tech/v1"
        )
        messages = [{'role': 'system', 'content': sys_prompt},
                    {'role': 'user', 'content': game_names}, ]
        completion = client.chat.completions.create(model=model_name, messages=messages)
        ans_str = completion.choices[0].message.content
        return ans_str
        logging.info("关键词提取成功")
    except Exception as e:
        logging.error(f"关键词提取时出错: {e}")
    return keywords

def main():
    """主函数"""
    filename = f'game_monitor_results_{datetime.now().strftime("%Y%m%d")}.csv'
    data = pd.read_csv(filename)
    game_names = data['game_name'].dropna().tolist()
    titles = data['title'].dropna().tolist()
    count = 0
    keyword_list = []
    for i in range(len(game_names)):
        name= game_names[i]
        title = titles[i]
        if name != titles:
            name = name + " " + title
        print("name", name)
        count += 1
        # if count > 2:
        #     break
        keyword = extract_keywords_from_game_names(name)
        print("keyword", keyword)
        keyword_list.append(keyword)

    # 将关键词列表添加到数据框中
    data['keywords'] = keyword_list  # 新增关键词列
    save_name = filename.replace(".csv", "_update.csv")
    data.to_csv(save_name, index=False)  # 保存为新的CSV文件

if __name__ == "__main__":
    main()
