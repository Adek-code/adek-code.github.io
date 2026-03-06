import requests
import json
from datetime import datetime

class AIAssistant:
    """AI Assistant that can handle weather queries, news requests, and general questions"""
    
    def __init__(self):
        self.weather_api_key = 'YOUR_WEATHER_API_KEY'
        self.news_api_key = 'YOUR_NEWS_API_KEY'
    
    def get_weather(self, location):
        """Fetch weather data for a specific location"""
        try:
            api_key = self.weather_api_key
            endpoint = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                return {
                    'location': data['location']['name'],
                    'temperature': data['current']['temp_c'],
                    'condition': data['current']['condition']['text'],
                    'humidity': data['current']['humidity'],
                    'wind_speed': data['current']['wind_kph']
                }
            else:
                return {'error': 'Could not fetch weather data'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_news(self, topic, language='en'):
        """Fetch news articles about a specific topic"""
        try:
            api_key = self.news_api_key
            endpoint = f'https://newsapi.org/v2/everything?q={topic}&language={language}&sortBy=publishedAt&apiKey={api_key}'
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data['articles'][:5]:  # Get top 5 articles
                    articles.append({
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'published_at': article['publishedAt']
                    })
                return {'articles': articles, 'total_results': data['totalResults']}
            else:
                return {'error': 'Could not fetch news data'}
        except Exception as e:
            return {'error': str(e)}
    
    def handle_query(self, user_query):
        """Main function to process user queries and route to appropriate handler"""
        query_lower = user_query.lower()
        
        if 'weather' in query_lower:
            # Extract location from query
            if 'weather in' in query_lower:
                location = user_query.split('weather in')[-1].strip()
            elif 'weather for' in query_lower:
                location = user_query.split('weather for')[-1].strip()
            else:
                return {'response': 'Please specify a location for weather. Example: "weather in London"'}
            
            return {'type': 'weather', 'data': self.get_weather(location)}
        
        elif 'news' in query_lower or 'latest' in query_lower:
            # Extract topic from query
            if 'news about' in query_lower:
                topic = user_query.split('news about')[-1].strip()
            elif 'news on' in query_lower:
                topic = user_query.split('news on')[-1].strip()
            elif 'latest news' in query_lower:
                topic = user_query.split('latest news')[-1].strip()
            else:
                return {'response': 'Please specify a topic for news. Example: "news about technology"'}
            
            return {'type': 'news', 'data': self.get_news(topic)}
        
        else:
            return {
                'type': 'general',
                'response': 'I can help you with:\n1. Weather queries (e.g., "weather in Paris")\n2. Latest news (e.g., "news about AI")\n3. Or ask me anything else!'
            }

    def main():
        """Main function to run the AI Assistant"""
        assistant = AIAssistant()
        
        print("=" * 60)
        print("Welcome to AI Assistant!")
        print("=" * 60)
        print("\nI can help you with:")
        print("- Weather information (e.g., 'weather in London')")
        print("- Latest news (e.g., 'news about technology')")
        print("- General questions\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Assistant: Goodbye! Have a great day!")
                break
            
            if not user_input:
                continue
            
            result = assistant.handle_query(user_input)
            print("\nAssistant:")
            
            if result['type'] == 'weather':
                if 'error' in result['data']:
                    print(f"Error: {result['data']['error']}")
                else:
                    weather = result['data']
                    print(f"Location: {weather['location']}")
                    print(f"Temperature: {weather['temperature']}°C")
                    print(f"Condition: {weather['condition']}")
                    print(f"Humidity: {weather['humidity']}%")
                    print(f"Wind Speed: {weather['wind_speed']} km/h")
            
            elif result['type'] == 'news':
                if 'error' in result['data']:
                    print(f"Error: {result['data']['error']}")
                else:
                    news = result['data']
                    print(f"Found {news['total_results']} articles. Here are the top 5:\n")
                    for i, article in enumerate(news['articles'], 1):
                        print(f"{i}. {article['title']}")
                        print(f"   Published: {article['published_at']}")
                        print(f"   {article['description']}\n")
            
            else:
                print(result['response'])
            
            print()

if __name__ == '__main__':
    main()