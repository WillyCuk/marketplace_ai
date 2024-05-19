import requests
import pandas as pd


def clean_price(value):
    value = value.replace("Rp", '').replace('.', '')
    return value


def clean_sell_count(value):
    if type(value) == int:
        return value
    value = ''.join(value.split(" ")).replace(
        ',', '.').replace(' ', '').replace('terjual', '').replace('+', '')
    if value.endswith('rb'):
        return int(float(value.split('rb')[0]) * 1000)
    else:
        return int(value)


class tokopedia:

    def scrap(self, keyword):
        data = []
        url = 'https://gql.tokopedia.com/graphql/SearchProductQueryV4'
        header = {
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': '_UUID_NONLOGIN_=720c345dd5797b86e6424b822e1a3852; _UUID_NONLOGIN_.sig=jT6y_kZ1LK6AMxMAgC2DSY8psiU; DID=537681d47c4aa436142d94d175bf3697e43ac04386456e3cb27c924e93fe9e425d658980388179108f3e0dac66d83202; DID_JS=NTM3NjgxZDQ3YzRhYTQzNjE0MmQ5NGQxNzViZjM2OTdlNDNhYzA0Mzg2NDU2ZTNjYjI3YzkyNGU5M2ZlOWU0MjVkNjU4OTgwMzg4MTc5MTA4ZjNlMGRhYzY2ZDgzMjAy47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; __auc=6c08416517e6123d90fd9257a3e; _UUID_CAS_=93092143-68b9-4b22-8411-99755519dd74; _CASE_=7a23654865233b333336352d23604865233b312d236d636d233b234b606a60737560215174726075232d23624865233b3036372d236d6e6f66233b23232d236d6075233b23232d2371426e233b23232d23764865233b30333330313236342d23724865233b30303432313436322d237255787164233b233369232d23766972233b235a7a5d2376607364696e7472645e68655d233b30333330313236342d5d23726473776862645e757871645d233b5d2333695d232d5d235e5e757871646f606c645d233b5d2356607364696e747264725d237c2d7a5d2376607364696e7472645e68655d233b312d5d23726473776862645e757871645d233b5d2330346c5d232d5d235e5e757871646f606c645d233b5d2356607364696e747264725d237c5c237c; _tt_enable_cookie=1; _ttp=0c83bcd1-48b7-4da6-8cc8-db139258cd81; _gcl_au=1.1.845220842.1664936997; _jxx=6fb384d0-f436-11ec-8093-dd2b22bf5d48; _jx=6fb384d0-f436-11ec-8093-dd2b22bf5d48; _fbp=fb.1.1664937124394.782192026; _gid=GA1.2.2032349107.1670290391; _abck=24C8EA6A9C23EC796649AAEDD4A9C6C0~0~YAAQX3Fidq3IlnmEAQAAwtsz6gkAT3zZImnXud8xhgQi0MoAKrpmG5+jGAiTWse8C5edpCKHKhgGRBkX2uaBKRUBtOdzTjjPsDwEWP1UYyVKACJojklvDERHBJ0Bo4CKl6ReZZ0VaZzC665K86yzrdXFep0Z1Miig1AKO7xjjuDTLd9KnSiGK23YvRXQNoAkuG1xmx/ZY0+yGKzzM1oWj1s3Rj32D4Y60t/9nYkl1K3ovqw9VRMjUqrirLtrTUIZKr3qEhB4de6Z6McNo3ZmCWf+bLD2x9ys9lJFG+Hqvj4OjnUDfusFyg07EwrW1CHQZkzx8vifMCtxp6Y80eD+wifghfQW6mG+Tmi5Gj7ZPPr5MsWp5HkRgd5CKgxWh0XjbdH/N71bCesqUdY3qJaMEOr8oIUHnUMyiCRt~-1~-1~-1; bm_sz=D9001AE372A38E73CA5095803515BF16~YAAQX3FidrDIlnmEAQAAwtsz6hLMcjN7yRffsfAQiWh1PcUGm8opEEsMX12aXpxgFqgOKlwxOL8nwFWSmBiK9Rc5Oc+Ig8zAo8d4GTHReMzamE4f6YtYnnezvivZpBmFWa92pf9LCBOEK67GF4PIgB+errhLsKHh5CndQ0pdhrCKm4pyvAJGCNytf7ebQhR2D1ceIZs3ZGWRAn5ERzOt0ftq77hhqM4rll2GuLMNdAZIRhdsGi99aR6M9k5fVE1lXaZSlWa/lBOjYTBLi3q0LHKV+/Fi3QWth48GSAKWVuf/6u7eNfo=~4342083~4474424; bm_mi=8CC8AAA3CA7494670FD0730CDACB0A14~YAAQX3Fidl/KlnmEAQAAdSQ06hKNkbwvdqkHf78U1l5yG5GgFzMVejYbk3Epo78t7SlOVQ/ENtO0AnktfNY3RAdtgvsRojLtv5nzAWz3FaOmdt/H6QBW0ynDsrAzc2cfGS7wCrryB5Z6nzJ2SdpQP5DnXWCXIWgC274nZHPIYoAGZJCRDWIXsQW/d/Wh22Gdo0LRz7AFaXXPlUWbfmj7epxVvdImDW5/3+JLtQ/bLYsbaK8LVWnCcBAbg0T16YZKxJ64fP06UODnpEvMRtZuw/B6c1RSPI5dTdHie9gAnuw1YcYkpcncY1QKWjTKkcKdcPmehHMdrMcvdtrJiXZnIRRHhis0dE4=~1; _SID_Tokopedia_=CiBJb208EovvAezTP1A8vOMiH7kxUI6KCrJs-J8TgnENt1zdQhBeeeRtxCqp_6CNfK9I8B0A_zc5i0R32eNq-JaPoKRclSgBwrmebqGY7GWsY--fF_ub1mVAOd8qEoQG; _gcl_aw=GCL.1670376596.Cj0KCQiA7bucBhCeARIsAIOwr--1FgKqo5Q_D0Vm7sYKwu3JbQsxPcDfK4nPa9XH6LWNX18Oza5Q0aAp69EALw_wcB; _gac_UA-126956641-6=1.1670376597.Cj0KCQiA7bucBhCeARIsAIOwr--1FgKqo5Q_D0Vm7sYKwu3JbQsxPcDfK4nPa9XH6LWNX18Oza5Q0aAp69EALw_wcB; ak_bmsc=DD5839BB05909ACAE7ED6BAA6A629008~000000000000000000000000000000~YAAQX3FidmnKlnmEAQAAkjc06hJVrC2YwsnffeaKzsOhCtp1Rq0VJpKyi3ZwplBeW1ST0SrcrsXpvOX7jk/+W6FSRtYbSNrH1em66J7hFDOR3dlRml79vdmJn70+sCQjEtMVb3vVE8dc7E4AZbyAegYQ5edecCr9y7RkG+6P8NVJbg8STzXOdafe2GlPzaGmEstGXzD3DmhrLnjv3YA7XXabOGNJqDLxRLiWM5zRZOuqHJ3nyq6ACDABfMA5SR/vl0C++mReMGxSKd7YA0lxS+y6eBO3R3+18WWb444sNdMMOFcKEkUjCJaXJ0ef3YoKdfG0x353MJ3Bu5CI3qGuenmHKf1j5iiGDkfAcYz+6uFoFxtr7kLPlEyiKthE4QWBnt7gZxWoSsCFOlnUrag4qkUSFmBc23YAqjaSy985Z14i7Bg1vhaZV9Jj9Nb6sE+1uKk6mDb/sk0SR+RpGYO2jKCYQMv67TilpJCC4MBxkG0CYMPKPIGst/VnowiUX/pHjVHWxQ0lu3l9BwS82+wfuQBtQn5vey7BCqR9; __asc=c9577090184ea3436d39aa6ec81; _gac_UA-9801603-1=1.1670376604.Cj0KCQiA7bucBhCeARIsAIOwr--1FgKqo5Q_D0Vm7sYKwu3JbQsxPcDfK4nPa9XH6LWNX18Oza5Q0aAp69EALw_wcB; _dc_gtm_UA-126956641-6=1; _ga_70947XW48P=GS1.1.1670376597.9.1.1670376665.60.0.0; _ga=GA1.2.676038250.1642307241; _dc_gtm_UA-9801603-1=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }

        index = 0
        for page in range(1, 11):
            query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&page={page}&q={keyword}&related=true&rows=200&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start={index}&topads_bucket=true&unique_id=720c345dd5797b86e6424b822e1a3852&user_addressId=&user_cityId=176&user_districtId=2274&user_id=&user_lat=&user_long=&user_postCode=&user_warehouseId=12210375&variants="}},"query":"query SearchProductQueryV4($params: String\u0021) {{\\n  ace_search_product_v4(params: $params) {{\\n    header {{\\n      totalData\\n      totalDataText\\n      processTime\\n      responseCode\\n      errorMessage\\n      additionalParams\\n      keywordProcess\\n      componentId\\n      __typename\\n    }}\\n    data {{\\n      banner {{\\n        position\\n        text\\n        imageUrl\\n        url\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      backendFilters\\n      isQuerySafe\\n      ticker {{\\n        text\\n        query\\n        typeId\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      redirection {{\\n        redirectUrl\\n        departmentId\\n        __typename\\n      }}\\n      related {{\\n        position\\n        trackingOption\\n        relatedKeyword\\n        otherRelated {{\\n          keyword\\n          url\\n          product {{\\n            id\\n            name\\n            price\\n            imageUrl\\n            rating\\n            countReview\\n            url\\n            priceStr\\n            wishlist\\n            shop {{\\n              city\\n              isOfficial\\n              isPowerBadge\\n              __typename\\n            }}\\n            ads {{\\n              adsId: id\\n              productClickUrl\\n              productWishlistUrl\\n              shopClickUrl\\n              productViewUrl\\n              __typename\\n            }}\\n            badges {{\\n              title\\n              imageUrl\\n              show\\n              __typename\\n            }}\\n            ratingAverage\\n            labelGroups {{\\n              position\\n              type\\n              title\\n              url\\n              __typename\\n            }}\\n            componentId\\n            __typename\\n          }}\\n          componentId\\n          __typename\\n        }}\\n        __typename\\n      }}\\n      suggestion {{\\n        currentKeyword\\n        suggestion\\n        suggestionCount\\n        instead\\n        insteadCount\\n        query\\n        text\\n        componentId\\n        trackingOption\\n        __typename\\n      }}\\n      products {{\\n        id\\n        name\\n        ads {{\\n          adsId: id\\n          productClickUrl\\n          productWishlistUrl\\n          productViewUrl\\n          __typename\\n        }}\\n        badges {{\\n          title\\n          imageUrl\\n          show\\n          __typename\\n        }}\\n        category: departmentId\\n        categoryBreadcrumb\\n        categoryId\\n        categoryName\\n        countReview\\n        customVideoURL\\n        discountPercentage\\n        gaKey\\n        imageUrl\\n        labelGroups {{\\n          position\\n          title\\n          type\\n          url\\n          __typename\\n        }}\\n        originalPrice\\n        price\\n        priceRange\\n        rating\\n        ratingAverage\\n        shop {{\\n          shopId: id\\n          name\\n          url\\n          city\\n          isOfficial\\n          isPowerBadge\\n          __typename\\n        }}\\n        url\\n        wishlist\\n        sourceEngine: source_engine\\n        __typename\\n      }}\\n      violation {{\\n        headerText\\n        descriptionText\\n        imageURL\\n        ctaURL\\n        ctaApplink\\n        buttonText\\n        buttonType\\n        __typename\\n      }}\\n      __typename\\n    }}\\n    __typename\\n  }}\\n}}\\n"}}]'

            r = requests.post(
                url=url, headers=header, data=query)

            data_product = r.json()[
                0]['data']['ace_search_product_v4']['data']['products']
            for item in data_product:
                print(item)
                index += 1
                product_name = item['name']
                product_price = item['price']
                product_shop_name = item['shop']['name']
                product_location = item['shop']['city']
                product_rating = item['rating']
                product_sell = 0
                if len(item['labelGroups']) != 0:
                    index_with_integrity = next((index for index, item in enumerate(
                        item['labelGroups']) if item.get('position') == 'integrity'), None)
                    if index_with_integrity is not None:
                        product_sell = item['labelGroups'][index_with_integrity]['title']
                marketplace = 'tokopedia'
                # product_image = item['imageUrl']
                # product_url = item['url']
                data.append((product_name, product_price,
                            product_rating,  product_sell, product_location, product_shop_name, marketplace))

        df = pd.DataFrame(data, columns=[
            'product name', 'product price', 'product rating', 'product sell count', 'product location', 'product shop name', 'marketplace'])

        df = df.drop_duplicates(subset=['product name'])
        df.reset_index(drop=True, inplace=True)

        # Clean and convert the 'product price' column
        df['product price'] = df['product price'].apply(
            lambda x: clean_price(x))

        df['product sell count'] = df['product sell count'].apply(
            lambda x: clean_sell_count(x))

        return df


if __name__ == "__main__":
    keyword = 'rog phone 6'
    toko_scrap = tokopedia()
    df = toko_scrap.scrap(keyword)
    print(df)
