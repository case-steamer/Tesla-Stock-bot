import requests
from datetime import datetime
import os

TEST_FILE = "test_data.json"
TEST_NEWS = "test_news.json"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
up = "🔺"
down = "🔻"


def get_news():
    call = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    return call


def send_message(note):
    message = note
    elon_token = os.environ["ELON_TOKEN"]
    elon_id = os.environ["ELON_ID"]
    telegram_URL = ('https://api.telegram.org/bot' +
                    elon_token +
                    '/sendMessage?chat_id=' +
                    elon_id + '&parse_mode=Markdown&text=' +
                    message)
    telegram_response = requests.get(url=telegram_URL)
    return telegram_response


def generate_messages(content: list, percent_value: float, character: str):
    message_list = []
    message_one = f"TSLA:  {character} {percent_value}%"
    message_list.append(message_one)
    for item in content:
        key = list(item.keys())
        value = item[key[0]]
        message = f"""
Headline: {key[0]}
Read here: {value}
"""
        message_list.append(message.strip().split('\n'))
    return message_list



# today = str(datetime.now().year).zfill(2) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2)
# print(today)
###DEVELOPMENT TEST CODE
year = str(datetime.now().year) #"2025"
month = str(datetime.now().month).zfill(2)  #"02"
day = str(datetime.now().day).zfill(2)  #"05"
today = year + "-" + month + "-" + day
yesterday = year + "-" + month + "-" + str(int(day) - 1).zfill(2)
yesterday_minus_one = year + "-" + month + "-" + str(int(day) - 2).zfill(2)
# with open(file=TEST_FILE, mode="r") as test:
#     data = json.load(test)
print(yesterday)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ["STOCK_API"]
}

news_parameters = {
    "q": COMPANY_NAME,
    "apikey": os.environ["NEWS_API"],
    "sortBy": "publishedAt",
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data = response.json()
print(data)
if yesterday == data["Meta Data"]["3. Last Refreshed"]:
    print(True)
    yesterday_data = data["Time Series (Daily)"][yesterday]
    minus_one_data = data["Time Series (Daily)"][yesterday_minus_one]
    yesterday_close = float(yesterday_data['4. close'])
    minus_one_close = float(minus_one_data['4. close'])
    close_difference = round(abs(float(yesterday_close) - float(minus_one_close)), 2)
    if yesterday_close > minus_one_close:
        icon = up
    elif yesterday_close < minus_one_close:
        icon = down
    print(icon)

    percentage = round((close_difference/minus_one_close * 100), 2)
    if percentage > 5:
        print(percentage)

        #RUN CODE
        news_data = get_news()
        news = news_data.json()

        #TEST CODE
        # with open(file=TEST_NEWS, mode="r", encoding="Latin-1") as file:
        #     news = json.load(file)

        article_one = news["articles"][0]
        article_two = news["articles"][1]
        article_three = news["articles"][2]
        articles = [article_one, article_two, article_three]
        article_data = []

        for a in articles:
            article = {a["title"]: a["url"]}
            article_data.append(article)

        messages = generate_messages(content=article_data, percent_value=percentage, character=icon)
        for m in messages:
            if m == messages[0]:
                print(send_message(m))
            else:
                message_to_send = m[0] + "\n" + m[1]
                print(send_message(message_to_send))


