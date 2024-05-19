import requests
import pandas as pd


class bukalapak:
    def scrap(self, keyword):
        data = []
        # Meminta token oauth
        req_token = requests.post(
            'https://accounts.bukalapak.com/auth_proxies/request_token').json()
        access_token = req_token['access_token']
        for index in range(1, 13):
            encoded_keyword = keyword.replace(' ', '+')

            url = f'https://api.bukalapak.com/multistrategy-products?keywords={encoded_keyword}&limit=50&offset=0&facet=true&page={
                index}&shouldUseSeoMultistrategy=false&isLoggedIn=true&show_search_contexts=true&access_token={access_token}'
            r = requests.get(url).json()
            if len(r) == 0:
                break
            rows = r['data']

            for item in rows:
                print(item)
                print()
                product_name = item['name']
                product_price = item['price']
                product_location = item['store']['address']['city']
                product_shop_name = item['store']['name']
                product_rating = item['rating']['average_rate']
                product_sell = item['stats']['sold_count']
                # product_url = item['url']
                # product_image = item['images']['large_urls'][0]
                marketplace = 'bukalapak'
                data.append((product_name, product_price, product_rating, product_sell,
                            product_location, product_shop_name,  marketplace))

        df = pd.DataFrame(data, columns=[
            'product name', 'product price', 'product rating', 'product sell count', 'product location', 'product shop name',  'marketplace'])

        df = df.drop_duplicates(subset=['product name'])
        df.reset_index(drop=True, inplace=True)

        return df


# Example usage:
if __name__ == "__main__":
    bl = bukalapak()
    keyword = input("Enter keyword: ")
    df = bl.scrap(keyword)
    df.to_excel(f"{keyword}-bukalapak.xlsx")
    print(df)
