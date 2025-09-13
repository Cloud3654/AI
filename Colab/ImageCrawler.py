import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scroll_down(driver, pause_time=1.0, scrolls=10):
    for _ in range(scrolls):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(pause_time)

def get_google_image_urls(query, max_links=100):
    print(f"[INFO] Google 이미지 크롤링 시작: {query}")
    driver = create_driver(headless=False)  # 헤드리스 끄고 디버깅용
    search_url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    driver.get(search_url)
    image_urls = set()
    scroll_down(driver, pause_time=1.5, scrolls=15)

    thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
    print(f"[INFO] 썸네일 개수: {len(thumbnails)}")
    for img in thumbnails:
        try:
            img.click()
            time.sleep(1)
            actual_images = driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_img in actual_images:
                src = actual_img.get_attribute('src')
                if src and src.startswith('http') and not src.startswith('https://encrypted-tbn0.gstatic.com'):
                    image_urls.add(src)
                    print(f"[DEBUG] 수집된 URL: {src}")
                    if len(image_urls) >= max_links:
                        driver.quit()
                        return list(image_urls)
        except Exception as e:
            print(f"[ERROR] 이미지 클릭 오류: {e}")
    driver.quit()
    return list(image_urls)

def get_bing_image_urls(query, max_links=100):
    print(f"[INFO] Bing 이미지 크롤링 시작: {query}")
    driver = create_driver(headless=False)
    search_url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    image_urls = set()
    scroll_down(driver, pause_time=1.5, scrolls=10)

    thumbnails = driver.find_elements(By.CSS_SELECTOR, "a.iusc")
    print(f"[INFO] 썸네일 개수: {len(thumbnails)}")
    for thumb in thumbnails:
        try:
            m = thumb.get_attribute("m")
            # 'm' 속성은 JSON 형태임
            import json
            meta = json.loads(m)
            murl = meta.get("murl")
            if murl:
                image_urls.add(murl)
                print(f"[DEBUG] 수집된 URL: {murl}")
                if len(image_urls) >= max_links:
                    driver.quit()
                    return list(image_urls)
        except Exception as e:
            print(f"[ERROR] Bing 이미지 수집 오류: {e}")
    driver.quit()
    return list(image_urls)

def get_yandex_image_urls(query, max_links=100):
    print(f"[INFO] Yandex 이미지 크롤링 시작: {query}")
    driver = create_driver(headless=False)
    search_url = f"https://yandex.com/images/search?text={query.replace(' ', '+')}"
    driver.get(search_url)
    image_urls = set()
    scroll_down(driver, pause_time=1.5, scrolls=10)

    thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.serp-item__thumb img")
    print(f"[INFO] 썸네일 개수: {len(thumbnails)}")
    for img in thumbnails:
        try:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                image_urls.add(src)
                print(f"[DEBUG] 수집된 URL: {src}")
                if len(image_urls) >= max_links:
                    driver.quit()
                    return list(image_urls)
        except Exception as e:
            print(f"[ERROR] Yandex 이미지 수집 오류: {e}")
    driver.quit()
    return list(image_urls)

def main():
    query = "Dieback Blueberry"
    max_images = 100  # 사이트별 최대 수집 개수

    google_urls = get_google_image_urls(query, max_images)
    print(f"Google 이미지 총 수집: {len(google_urls)}개")

    bing_urls = get_bing_image_urls(query, max_images)
    print(f"Bing 이미지 총 수집: {len(bing_urls)}개")

    yandex_urls = get_yandex_image_urls(query, max_images)
    print(f"Yandex 이미지 총 수집: {len(yandex_urls)}개")

    # 필요 시 파일로 저장 가능
    all_urls = {
        'google': google_urls,
        'bing': bing_urls,
        'yandex': yandex_urls
    }
    for engine, urls in all_urls.items():
        with open(f"{engine}_images.txt", "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")

if __name__ == "__main__":
    main()
