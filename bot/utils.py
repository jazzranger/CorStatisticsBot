import requests
import json
from bot.models import Statistic, News
from datetime import datetime
import random


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
