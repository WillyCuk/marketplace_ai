# import scrapping_blibli as sb
# import scrap_api_bukalapak as bk
# import scrapping_lazada as lz
# import api_tokopedia as tk
# import filter_data as fd
# import pandas as pd

# keyword = input("Masukkan keyword produk yang ingin dicari : ")

# # init all scrapping class
# blibli_scrap = sb.blibli()
# bukalapak_scrap = bk.bukalapak()
# lazada_scrap = lz.lazada()
# tokopedia_scrap = tk.tokopedia()
# filter = fd.filteringData()


# def scrap_data():
#     df_lazada = lazada_scrap.scrap(keyword)
#     print("lazada done")
#     df_blibli = blibli_scrap.scrap(keyword)
#     print("blibli done")
#     df_bukalapak = bukalapak_scrap.scrap(keyword)
#     print("bukalapak done")
#     df_tokopedia = tokopedia_scrap.scrap(keyword)
#     print(df_blibli.shape)
#     print(df_bukalapak.shape)
#     print(df_lazada.shape)
#     print(df_tokopedia.shape)
#     df = pd.concat([df_blibli, df_bukalapak, df_lazada,
#                    df_tokopedia], ignore_index=True)
#     return df


# df = scrap_data()

# df = filter.filter_data(df, keyword)

# sorted_rating = df.sort_values(by='product rating', ascending=False)
# sorted_price_descending = df.sort_values(
#     by='product price', ascending=False)
# sorted_price_ascending = df.sort_values(
#     by='product price')
# sorted_sell_count_descending = df.sort_values(
#     by='product sell count', ascending=False)
# sorted_sell_count_ascending = df.sort_values(
#     by='product sell count')
# filter_kota = pd.DataFrame()

# menu = 1

# while menu:
#     print(f"Scrapping data produk {keyword} selesai")
#     print("="*60)
#     print("Pilihan Filter")
#     print("="*60)
#     print(f"""
# 1. Harga
# 2. Rating (Descending)
# 3. Jumlah Terjual
# 4. Lokasi Toko
# 5. Exit""")
#     print("="*60)

#     opt = None
#     while True:
#         try:
#             opt = int(input("Pilihan filter : "))
#             break  # Break the loop if input is successfully converted to int
#         except ValueError:
#             print("Mohon masukkan angka yang valid.")

#     if opt == 1:
#         print("Filter Harga")
#         print("="*60)
#         print('''
# 1. Descending
# 2. Ascending''')
#         print("="*60)
#         while True:
#             try:
#                 option = int(
#                     input("Pilihan filter : "))
#                 if option == 1:
#                     print("Filter Harga Descending Selesai")
#                     print("="*60)
#                     print(sorted_price_descending.head())
#                     print(
#                         "Untuk melihat data lebih jelas, silahkan cek melalui file excel yang sudah digenerate.")

#                 elif option == 2:
#                     print("Filter Harga Ascending Selesai")
#                     print("="*60)
#                     print(sorted_price_ascending.head())
#                     print(
#                         "Untuk melihat data lebih jelas, silahkan cek melalui file excel yang sudah digenerate.")
#                 elif option >= 3:
#                     raise ValueError
#                 break  # Break the loop if input is successfully converted to int
#             except ValueError:
#                 print("Mohon masukkan angka yang valid.")

#     elif opt == 2:
#         print("Filter Rating")
#         print("="*60)
#         print("Filter Rating Descending Selesai")
#         print("="*60)
#         print(sorted_rating.head())

#     elif opt == 3:
#         print("Filter Jumlah Terjual")
#         print("="*60)
#         print('''
# 1. Descending
# 2. Ascending''')
#         print("="*60)
#         while True:
#             try:
#                 option = int(
#                     input("Pilihan filter : "))
#                 if option == 1:
#                     print("Filter Jumlah Terjual Descending Selesai")
#                     print("="*60)
#                     print(sorted_price_descending.head())
#                     print(
#                         "Untuk melihat data lebih jelas, silahkan cek melalui file excel yang sudah digenerate.")

#                 elif option == 2:
#                     print("Filter Jumlah Terjual Ascending Selesai")
#                     print("="*60)
#                     print(sorted_price_ascending.head())
#                     print(
#                         "Untuk melihat data lebih jelas, silahkan cek melalui file excel yang sudah digenerate.")
#                 elif option >= 3:
#                     raise ValueError
#                 break  # Break the loop if input is successfully converted to int
#             except ValueError:
#                 print("Mohon masukkan angka yang valid.")

#     elif opt == 4:
#         print("Filter Lokasi Toko")
#         print("="*60)
#         kota = input("Lokasi Kota : ")
#         filter_kota = filter.filter_kota(df, kota)
#         print("Filter Lokasi Toko Medan Selesai")
#         print("="*60)
#         print(filter_kota)

#     elif opt == 5:
#         print('='*60)
#         print("Terima kasih")
#         menu = 0

#     else:
#         print("Masukkan angka yang valid")


# with pd.ExcelWriter(f'{keyword}-final.xlsx') as writer:
#     df.to_excel(writer, sheet_name='original data', index=False)
#     sorted_rating.to_excel(writer, sheet_name='sorted rating', index=False)
#     sorted_price_ascending.to_excel(
#         writer, sheet_name='sorted price ascending', index=False)
#     sorted_price_descending.to_excel(
#         writer, sheet_name='sorted price descending', index=False)
#     sorted_sell_count_ascending.to_excel(
#         writer, sheet_name='sorted sell count ascending', index=False)
#     sorted_sell_count_descending.to_excel(
#         writer, sheet_name='sorted sell count descending', index=False)
#     if not filter_kota.empty:
#         filter_kota.to_excel(writer, sheet_name='filter kota', index=False)

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import api_blibli as sb
import api_bukalapak as bk
import api_lazada as lz
import api_tokopedia as tk
import filter_data as fd

app = FastAPI()

# Initialize all scraping classes
blibli_scrap = sb.blibli()
bukalapak_scrap = bk.bukalapak()
lazada_scrap = lz.lazada()
tokopedia_scrap = tk.tokopedia()
filter = fd.filteringData()

# Define the scraping function


def scrap_data(keyword):
    df_blibli = blibli_scrap.scrap(keyword)
    df_bukalapak = bukalapak_scrap.scrap(keyword)
    df_lazada = lazada_scrap.scrap(keyword)
    df_tokopedia = tokopedia_scrap.scrap(keyword)
    df = pd.concat([df_blibli, df_bukalapak, df_lazada,
                    df_tokopedia], ignore_index=True)
    return df

# Define the API route for scraping


@app.get('/api/scrape')
async def scrape(keyword: str = ""):
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword not provided")
    df = scrap_data(keyword)
    json_compatible_item_data = df.to_dict(orient='records')
    return JSONResponse(content=json_compatible_item_data)
