import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import time
import logging
import os
import random

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_game_names(filename):
    """从CSV文件中加载game_name列"""
    try:
        data = pd.read_csv(filename)
        game_names = data['keywords'].dropna().tolist()
        url = data['url'].dropna().tolist()
        logging.info("成功加载游戏名称")
        return [game_names, url]
    except Exception as e:
        logging.error(f"加载游戏名称时出错: {e}")
        return []

def get_ai_trends(filename, timeframe='today 1-m'):
    pytrends = TrendReq(retries=3, backoff_factor=0.5, hl='en-US', tz=360, timeout=(5, 10))

    ai_keywords_orgin, urls = load_game_names(filename)
    ai_keywords = []
    for i in range(len(ai_keywords_orgin)):
        url = urls[i]
        if "post" not in url:
            ai_keywords.append(ai_keywords_orgin[i])


    all_trends = pd.DataFrame()

    for i in range(0, len(ai_keywords), 2):
        keywords_batch = ai_keywords[i:i+2]
        try:
            pytrends.build_payload(keywords_batch, timeframe=timeframe)
            interest_over_time = pytrends.interest_over_time()
            if not interest_over_time.empty:
                all_trends = pd.concat([all_trends, interest_over_time], axis=1)
            time.sleep(random.uniform(3, 8))  # 增加延迟以避免被封禁
        except Exception as e:
            logging.error(f"Error fetching trends for {keywords_batch}: {e}")

    return all_trends


def calculate_trend_increase(df, urls):
    print("df.columns", df.columns)
    trends_data = []
    for column in df.columns:
        if column != 'isPartial':
            start_value = df[column].iloc[0]  # 确保获取单个值
            end_value = df[column].iloc[-1]    # 确保获取单个值
            max_value = df[column].max()
            avg_value = df[column].mean()
            if isinstance(start_value, (int, float)) and start_value > 0:  # 检查是否为数值
                print("end_value", start_value, end_value)
                increase = (end_value - start_value) / start_value * 100
                trends_data.append({
                    'topic': column,
                    'url': urls[df.columns.get_loc(column)],
                    'start_value': start_value,
                    'end_value': end_value,
                    'max_value': max_value,
                    'avg_value': avg_value,
                    'increase': increase
                })

    trends_df = pd.DataFrame(trends_data)
    if not trends_df.empty:
        trends_df = trends_df.sort_values('increase', ascending=False).reset_index(drop=True)
    return trends_df

def save_data(df, filename):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"数据保存成功: {filename}")
    except Exception as e:
        logging.error(f"保存数据时出错 {filename}: {e}")

def collect_google_trends_data():
    logging.info("开始收集最近30天的Google Trends数据")
    filename = f'game_monitor_results_{datetime.now().strftime("%Y%m%d")}_update.csv'
    trends_df = get_ai_trends(filename)

    if not trends_df.empty:
        ai_keywords_orgin, urls = load_game_names(filename)
        increases_df = calculate_trend_increase(trends_df, urls)
        logging.info("increases_df: ", increases_df)
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_data(trends_df, f'data/genai_trends_raw_30days_{timestamp}.csv')
        save_data(increases_df, f'data/genai_trends_increases_30days_{timestamp}.csv')
    else:
        logging.warning("没有收集到Google Trends数据")

if __name__ == "__main__":
    logging.info("Google Trends GenAI 30天数据收集脚本启动")
    collect_google_trends_data()
    logging.info("数据收集完成")
