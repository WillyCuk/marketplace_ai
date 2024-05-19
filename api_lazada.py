import time
import requests
import pandas as pd


def clean_rating(value):
    value = value.split(" ")[0]
    if value.endswith('K'):
        return int(float(value[:-1]) * 1000)
    else:
        return float(value)


def clean_sell_count(value):
    value = value.split(" ")[0]
    if value.endswith('K'):
        return int(float(value[:-1]) * 1000)
    else:
        return int(value)


class lazada:
    def scrap(self, keyword):

        data = []
        dash_keyword = keyword.replace(' ', '-')
        encoded_keyword = keyword.replace(' ', '%20')
        for index in range(1, 2):
            url = f'https://www.lazada.co.id/tag/{
                dash_keyword}/?ajax=true&catalog_redirect_tag=true&page={index}&q={encoded_keyword}'

            try:
                r = requests.get(url=url, headers={
                    'Accept-Language':
                    'en-GB,en-US;q=0.9,en;q=0.8',
                    'Accept': 'application/json, text/plain, */*', 'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                })

                r_json = r.json()
                r.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

                # Attempt to parse response as JSON

                rows = r_json['mods']['listItems']

                for item in rows:
                    print(item)
                    print()
                    product_name = item['name']
                    product_price = item['price']
                    product_shop_name = item['sellerName']
                    product_location = item['location']
                    product_rating = item['ratingScore'][:
                                                         3] if item['ratingScore'] else '0'
                    product_sell = '0'
                    if 'itemSoldCntShow' in item:
                        product_sell = item['itemSoldCntShow']
                    marketplace = 'lazada'

                    data.append((product_name, product_price, product_rating, product_sell,
                                product_location, product_shop_name, marketplace))

            except requests.exceptions.RequestException as err:
                print(f"An error occurred while requesting page {
                      index}: {err}")
                continue  # Skip to the next iteration of the loop

            except (KeyError, IndexError) as err:
                print(f"An error occurred while processing page {
                      index}: {err}")
                continue  # Skip to the next iteration of the loop

        df = pd.DataFrame(data, columns=[
            'product name', 'product price', 'product rating', 'product sell count', 'product location', 'product shop name', 'marketplace'])

        df = df.drop_duplicates(subset=['product name'])
        df.reset_index(drop=True, inplace=True)

        df['product rating'] = df['product rating'].apply(
            lambda x: clean_rating(x))

        df['product sell count'] = df['product sell count'].apply(
            lambda x: clean_sell_count(x))

        return df


if __name__ == '__main__':
    lzd = lazada()
    # keyword = input("Masukkan keyword : ")
    print(lzd.scrap("boneka"))
