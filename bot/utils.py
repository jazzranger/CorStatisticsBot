import requests
import json
from bot.models import Statistic, News
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def get_statistics(place):
    stat = Statistic()
    url = "https://covid-193.p.rapidapi.com/statistics"
    querystring = {"country": place}
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "7f5fba1042msh2fe8a4fbc17cdb7p19fa4bjsnb52f175808e9"
    }

    request = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(request.text)["response"][0]

    stat.country = response['country'] if response["country"] != "All" else "World"
    stat.country = "Россия" if response['country'] == 'Russia' else "Мир" if response["country"] == "All" else "World"
    stat.cases_new = response['cases']['new'] if response['cases']['new'] else 0
    stat.cases_recovered = response['cases']['recovered']
    stat.cases_critical = response['cases']['critical']
    stat.cases_total = response['cases']['total']
    stat.deaths_new = response['deaths']['new'] if response['deaths']['new'] else 0
    stat.deaths_total = response['deaths']['total']
    stat.date = datetime.strptime(response['day'], '%Y-%m-%d').date()
    return stat


def get_news():
    url = "http://newsapi.org/v2/top-headlines"
    querystring = {"q": 'коронавирус',
                   "apiKey": '6138e478031e4ddf904377d5a51c64e0',
                   "country": 'ru'}

    request = requests.request("GET", url, params=querystring)
    response = json.loads(request.text)["articles"]

    news_arr = []
    for item in response:
        news = News()
        news.title = item['title']
        news.description = item['description']
        news.url = item['url']
        news_arr.append(news)
    return news_arr[random.randint(0, len(news_arr)-1)]


def get_statistics_history(place):

    date = datetime.now().date() - timedelta(days=1)  # История идёт до вчера, т.к. за сегодня данных может ещё не быть
    dates = [date - timedelta(days=1) * num for num in range(7)][::-1]

    url = "https://covid-193.p.rapidapi.com/history"
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "7f5fba1042msh2fe8a4fbc17cdb7p19fa4bjsnb52f175808e9"
    }

    querystrings = [{"day": str(day), "country": place} for day in dates]
    responses = [requests.request("GET", url, headers=headers, params=query).text for query in querystrings]
    cases_total = [json.loads(response)["response"][0]["cases"]["total"] for response in responses]
    deaths_total = [json.loads(response)["response"][0]["deaths"]["total"] for response in responses]
    cases_recovered = [json.loads(response)["response"][0]["cases"]["recovered"] for response in responses]

    dates = [date.strftime("%d.%m.%Y") for date in dates]
    plt.figure(figsize=(9, 3))
    plt.plot(dates, cases_total, label="Заражено", marker='X')
    plt.plot(dates, cases_recovered, label="Выздоровело", marker='X')
    plt.plot(dates, deaths_total, label="Умерло", marker='X')
    plt.legend()
    plt.title(place.title())
    plt.tight_layout()
    plt.savefig("images/graph.png")
    img = open("images/graph.png", "rb")

    return img
