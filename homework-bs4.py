import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'


def parse_habr_articles(url, keywords):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        results = []

        for article in articles:
            title_elem = article.find('h2')
            if not title_elem:
                continue
            title = title_elem.text.strip()
            link = title_elem.find('a')['href'] if title_elem.find('a') else None
            if not link:
                continue

            time_elem = article.find('time')
            date = datetime.fromisoformat(time_elem['datetime']).strftime('%Y-%m-%d') if time_elem else 'N/A'

            # Собираем весь текст превью (включая хабы и основной текст)
            preview_text = ''

            # Основной текст превью
            body = article.find('div', class_='tm-article-body')
            if body:
                preview_text += body.text.lower()

            # Хабы (теги)
            hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
            hub_text = ' '.join(hub.text.lower() for hub in hubs)
            preview_text += ' ' + hub_text

            if any(keyword.lower() in preview_text for keyword in keywords):
                full_link = link if link.startswith('http') else f'https://habr.com{link}'
                results.append({
                    'date': date,
                    'title': title,
                    'link': full_link
                })

        return results

    except Exception as e:
        print(f'Ошибка: {e}')
        return []


if __name__ == '__main__':
    articles = parse_habr_articles(URL, KEYWORDS)
    if not articles:
        print("Нет статей с указанными ключевыми словами.")
    for article in articles:
        print(f"{article['date']} – {article['title']} – {article['link']}")