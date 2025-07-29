from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_driver_path = ChromeDriverManager().install()
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://habr.com/ru/articles/")

time.sleep(3)

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Функция для извлечения ссылки
def extract_link(article_item):
    try:
        link_element = WebDriverWait(article_item, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".tm-article-snippet h2 a"))
        )
        return link_element.get_attribute('href')
    except Exception as e:
        print(f"Ошибка при поиске ссылки: {e}")
        return None


articles = driver.find_elements(By.CLASS_NAME, "tm-article-snippet")
parsed_articles = []

for article in articles:
    link = extract_link(article)
    if not link:
        continue
    title = article.find_element(By.CSS_SELECTOR, ".tm-article-snippet h2 a").text.strip()
    date_element = article.find_element(By.TAG_NAME, value='time').get_attribute('title')
    published_date = date_element.strip() if date_element else 'Нет даты'
    
    preview_text = title.lower()
    try:
        body = article.find_element(By.CSS_SELECTOR, ".tm-article-body")
        preview_text += " " + body.text.lower()
    except:
        pass
    
    try:
        hubs = article.find_elements(By.CSS_SELECTOR, ".tm-article-snippet__hubs-item-link")
        preview_text += " " + " ".join(hub.text.lower() for hub in hubs)
    except:
        pass
        
    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        parsed_articles.append({
            "title": title,
            "link": link,
            "published_date": published_date
            })

driver.quit()

for art in parsed_articles:
    print(f"Дата: {art['published_date']}, Заголовок: {art['title']}, Ссылка: {art['link']}")
