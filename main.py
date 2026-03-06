import requests
import json

class AIAssistant:
    def __init__(self):
        pass

    def get_weather(self, location):
        api_key = 'YOUR_WEATHER_API_KEY'
        endpoint = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
        response = requests.get(endpoint)
        return response.json()

    def get_news(self, topic):
        api_key = 'YOUR_NEWS_API_KEY'
        endpoint = f'https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}'
        response = requests.get(endpoint)
        return response.json()

    def handle_query(self, query):
        if 'weather' in query:
            location = query.split('weather in')[-1].strip()
            return self.get_weather(location)
        elif 'news' in query:
            topic = query.split('news about')[-1].strip()
            return self.get_news(topic)
        else:
            return "I'm not sure how to help with that."