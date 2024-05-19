import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Rest of your code...


def clean_price(value):

    value = ''.join(value.split(" ")).split("-")[0]
    value = value.replace('Rp', '').replace(',', '.')

    if value.endswith('jt'):
        return int(float(value.split('jt')[0]) * 1000000)
    elif value.endswith('rb'):
        return int(float(value.split('rb')[0]) * 1000)
    else:
        value = value.replace('.', '')
        return int(value)


def clean_sell_count(value):

    value = ''.join(value.split(" "))
    value = value.replace('Rp', '').replace(
        ',', '.').replace('+', '').replace('terjual', '')

    if value.endswith('jt'):
        return int(float(value.split('jt')[0]) * 1000000)
    elif value.endswith('rb'):
        return int(float(value.split('rb')[0]) * 1000)
    else:
        value = value.replace('.', '')
        return int(value)


class tokopedia:
    def scrap(self, keyword):
        encoded_keyword = keyword.replace(' ', '%20')

        url = f"https://www.tokopedia.com/search?st=&q={
            encoded_keyword}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
        driver = webdriver.Chrome()
        driver.set_window_size(1300, 900)
        driver.get(url)
        data = []
        for j in range(10):
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#zeus-root")))
                time.sleep(1)
            except TimeoutException:
                # Handle the TimeoutException here
                print(
                    "Element with CSS selector '#zeus-root' not found within the specified time.")
            for i in range(2):
                driver.execute_script(
                    "window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            for item in soup.find_all('a', class_="pcv3__info-content"):
                product_name = item.find(
                    'div', class_='prd_link-product-name css-3um8ox').text
                product_price = item.find(
                    'div', class_='prd_link-product-price css-h66vau').text
                if (len(product_price.split(' ')) == 3):
                    print(product_price.split(' '))
                rating = item.find(
                    'span', class_='prd_rating-average-text css-t70v7i')
                product_rating = rating.text if rating else '0'
                sell = item.find(
                    'span', class_='prd_label-integrity css-1sgek4h')
                product_sell = sell.text if sell else '0'
                location = item.find(
                    'span', class_='prd_link-shop-loc css-1kdc32b flip')
                product_location = location.text if location else '-'
                shop_name = item.find(
                    'span', class_='prd_link-shop-name css-1kdc32b flip')
                product_shop_name = shop_name.text if shop_name else '-'
                marketplace = 'tokopedia'
                data.append((product_name, product_price,
                            product_rating,  product_sell, product_location, product_shop_name, marketplace))

            time.sleep(5)
            try:
                driver.find_element(
                    By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
            except NoSuchElementException as e:
                # If the element is not found, print the error message
                print("Element not found:", e)
                break
            time.sleep(2)

        driver.close()

        df = pd.DataFrame(data, columns=[
            'product name', 'product price', 'product rating', 'product sell count', 'product location', 'product shop name', 'marketplace'])

        # Clean and convert the 'product price' column
        df['product price'] = df['product price'].apply(
            lambda x: clean_price(x))

        df['product sell count'] = df['product sell count'].apply(
            lambda x: clean_sell_count(x))

        return df


if __name__ == "__main__":
    # tk = tokopedia()
    # df = tk.scrap('rog phone 6')
    test = clean_price('2 rb')
    print(test)
    print(9.75*1000000)
