import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

SLEEP_TIME = 2

# Tarayıcıyı konfigüre edip başlatma
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Tarayıcı arka planda çalışır (kullanıcı arayüzü olmadan)
    options.add_argument('--no-sandbox')  # Bazı sanal ortam sorunlarını çözer
    options.add_argument('--disable-dev-shm-usage')  # Paylaşılan bellek sorunlarını çözer

    # ChromeDriver'ın bulunduğu yeri belirtmek için Service kullanıyoruz
    service = Service(executable_path='/path/to/chromedriver')

    # WebDriver'ı başlatıyoruz
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


# Ana sayfadan kategori linklerini alma
def get_category_urls(driver):
    url = "https://books.toscrape.com/"
    driver.get(url)
    time.sleep(SLEEP_TIME)
    category_elements_xpath = "//a[contains(text(), 'Travel') or contains(text(), 'Nonfiction')]"
    category_elements = driver.find_elements(By.XPATH, category_elements_xpath)
    category_urls = [element.get_attribute('href') for element in category_elements]
    return category_urls

# Kategori sayfasından kitap detay sayfalarının linklerini alma
def get_category_detail_urls(driver, category_url):
    driver.get(category_url)
    time.sleep(SLEEP_TIME)
    books_elements_xpath = "//div[@class='image_container']//a"
    books_elements = driver.find_elements(By.XPATH, books_elements_xpath)
    book_urls = [element.get_attribute('href') for element in books_elements]
    
    # Sayfalandırma kontrolü ve ek sayfalardaki kitapların linklerini alma
    MAX_PAGINATION = 3  # Örnek olarak 3 sayfa üzerinden devam ediyoruz
    for i in range(2, MAX_PAGINATION + 1):
        update_url = category_url.replace("index", f"page-{i}")
        driver.get(update_url)
        time.sleep(SLEEP_TIME)
        books_elements = driver.find_elements(By.XPATH, books_elements_xpath)
        if not books_elements:
            break
        temp_urls = [element.get_attribute('href') for element in books_elements]
        book_urls.extend(temp_urls)
    
    return book_urls

# Kitap detaylarını alma
def get_product_detail(driver, book_url):
    driver.get(book_url)
    time.sleep(SLEEP_TIME)
    content_div = driver.find_element(By.XPATH, "//div[@class='content']")
    inner_html = content_div.get_attribute('innerHTML')
    
    soup = BeautifulSoup(inner_html, "html.parser")
    
    name_elem = soup.find("h1")
    book_name = name_elem.get_text()
    
    price_elem = soup.find("p", attrs={"class": "price_color"})
    book_price = price_elem.get_text()
    
    regex = re.compile("^star-rating")
    star_elem = soup.find("p", attrs={"class": regex})
    book_star_count = star_elem["class"][-1] if star_elem else "Not rated"
    
    desc_elem = soup.find("div", attrs={"id": "product_description"})
    book_desc = desc_elem.find_next_sibling().text if desc_elem else "No description"
    
    product_info = {}
    table_rows = soup.find("table").find_all("tr")
    for row in table_rows:
        key = row.find("th").text
        value = row.find("td").text
        product_info[key] = value
    
    return {
        "Name": book_name,
        "Price": book_price,
        "Star Rating": book_star_count,
        "Description": book_desc,
        **product_info
    }

# Tüm süreci çalıştırma ve DataFrame döndürme
def scrape_books_to_df():
    driver = start_driver()
    try:
        category_urls = get_category_urls(driver)
        all_books_details = []
        
        for category_url in category_urls:
            book_urls = get_category_detail_urls(driver, category_url)
            for book_url in book_urls:
                book_detail = get_product_detail(driver, book_url)
                all_books_details.append(book_detail)
        
        # DataFrame'e dönüştürme
        df = pd.DataFrame(all_books_details)
        return df
    finally:
        driver.quit()

# Streamlit uygulaması
def main():
    st.title("Books Scraping App")
    st.write("This app scrapes book details from the Travel and Nonfiction categories on books.toscrape.com.")

    if st.button("Start Scraping"):
        with st.spinner("Scraping data..."):
            books_df = scrape_books_to_df()
            st.success("Scraping completed!")
            st.write(books_df)
            csv = books_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="books_details.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
