import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urlparse, urljoin
from io import StringIO

SLEEP_TIME = 2

# Tarayıcıyı konfigüre edip başlatma
def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver

# Robots.txt dosyasını kontrol etme
def get_robots_txt(url):
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")
    response = requests.get(robots_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Robots.txt dosyasından izin verilen sayfaları bulma
def parse_robots_txt(robots_txt):
    allow_paths = []
    disallow_paths = []
    f = StringIO(robots_txt)
    for line in f:
        line = line.strip()
        if line.startswith("Allow:"):
            path = line.split("Allow:")[1].strip()
            allow_paths.append(path)
        elif line.startswith("Disallow:"):
            path = line.split("Disallow:")[1].strip()
            disallow_paths.append(path)
    return allow_paths, disallow_paths

# Kullanıcının girdiği URL'yi ve robots.txt'yi kullanarak izin verilen sayfaları listeleme
def get_allowed_urls(base_url, allow_paths):
    allowed_urls = [urljoin(base_url, path) for path in allow_paths if path != "/"]
    return allowed_urls

# İzin verilen sayfalardan veri çekme
def get_page_data(driver, url):
    driver.get(url)
    time.sleep(SLEEP_TIME)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Örnek veri çekme işlemi: başlık ve metin
    page_title = soup.title.get_text() if soup.title else "No title"
    page_text = soup.get_text()

    return {
        "URL": url,
        "Title": page_title,
        "Content": page_text[:200]  # İlk 200 karakteri gösteriyoruz
    }

# Tüm süreci çalıştırma ve DataFrame döndürme
def scrape_allowed_pages(base_url, allow_paths):
    driver = start_driver()
    try:
        allowed_urls = get_allowed_urls(base_url, allow_paths)
        all_page_data = []
        
        for url in allowed_urls:
            page_data = get_page_data(driver, url)
            all_page_data.append(page_data)
        
        df = pd.DataFrame(all_page_data)
        return df
    finally:
        driver.quit()

# Streamlit uygulaması
def main():
    st.title("Generalized Web Scraping App")
    st.write("This app scrapes data from allowed pages of a website based on its robots.txt file.")

    # Kullanıcıdan URL alma
    url = st.text_input("Enter the URL of the website:")
    
    if url:
        st.write(f"Checking robots.txt for {url}...")
        robots_txt = get_robots_txt(url)
        
        if robots_txt:
            allow_paths, disallow_paths = parse_robots_txt(robots_txt)
            
            if allow_paths:
                st.write("Allowed paths found:")
                st.write(allow_paths)

                if st.button("Start Scraping"):
                    with st.spinner("Scraping allowed pages..."):
                        scraped_df = scrape_allowed_pages(url, allow_paths)
                        st.success("Scraping completed!")
                        st.write(scraped_df)
                        csv = scraped_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="scraped_data.csv",
                            mime="text/csv",
                        )
            else:
                st.warning("No allowed paths found in robots.txt.")
        else:
            st.error("Failed to retrieve robots.txt.")

if __name__ == "__main__":
    main()
