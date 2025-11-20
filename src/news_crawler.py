import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_naver_news(category_id):
    URL=f'https://news.naver.com/section/{category_id}'

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item', limit=10)

        news_list = []
        for item in items:
            news_list.append({
                'title': item.find('title').text,
                'link': item.find('link').text,
                'description': BeautifulSoup(item.find('description').text, 'html.parser').get_text(),
                'pub_date': item.find('pubDate').text
            })
        
        return news_list
    
    except Exception as e:
        print(f'[failed: {e}]')
        return []
    
def get_all_news():
    categories = {
        '정치': '100',
        '경제': '101',
        '사회': '102',
        'IT/과학': '105'
    }
    
    all_news = {}
    
    for name, code in categories.items():
        print(f'[{name} news crawling]')
        all_news[name] = fetch_naver_news(code)
    
    return all_news

if __name__ == '__main__':
    news = get_all_news()
    for category, items in news.items():
        print(f'\n{category}: {len(items)}개')