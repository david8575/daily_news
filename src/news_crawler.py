import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_naver_news(category_id):
    URL=f'https://news.naver.com/section/{category_id}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        news_list = []
        headlines = soup.select('a.sa_text_title')

        for item in headlines[:15]:
            title = item.get_text(strip=True)
            link = item.get('href', '')
            
            if link.startswith('/'):
                link = 'https://news.naver.com' + link
            
            description = ''
            try:
                article_response = requests.get(link, headers=headers, timeout=10)
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                article_body = article_soup.select_one('article#dic_area')

                if article_body:
                    description = article_body.get_text(strip=True)[:200] + '...'
            except:
                pass

            news_list.append({
                'title': title,
                'link': link,
                'description': description,
                'pub_date': datetime.now().strftime('%Y-%m-%d %H:%M')
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
        for item in items:
            print(f"- {item['title']} ({item['link']})")
            print(f"  {item['description']}\n")