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

driver.get("https://habr.com/ru/")

time.sleep(3)


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
    if link:
        title = article.find_element(By.CSS_SELECTOR, ".tm-article-snippet h2 a").text.strip()
        parsed_articles.append({"title": title, "link": link})

driver.quit()

for art in parsed_articles:
    print(f"Заголовок: {art['title']}, Ссылка: {art['link']}")
