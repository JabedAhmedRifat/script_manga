import requests
from bs4 import BeautifulSoup
import pandas as pd

manga_create_url='http://localhost:8000/manga-create/'
genre_create_url='http://127.0.0.1:8000/genre-create/'



# def scrape_manga_data(url):
#     page= requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     page.close()
#     return soup
# # ////////////////////////////////////////////////////////////
    
# def save_data_to_excel(data, excel_filename):
#     df = pd.DataFrame(data)
#     df.to_excel(excel_filename, index=False)
#     # print({excel_filename})
# # ///////////////////////////////////////////////////////////////////////////

genres_to_add = [
    "Action",
    "Adventure",
    "Fantasy",
    "Romance",
    "Comedy",
    "Martial Arts",
    "Historical",
    "Shounen",
    "Isekai",
    "Drama",
    "Supernatural",
    
]

for genre_name in genres_to_add:
    genre_payload = {
        "name": genre_name
    }
    response = requests.post(genre_create_url, json=genre_payload)
    
    if response.status_code == 201:
        print("Response status code:", response.status_code)
    else:
        print("Response content:", response.content)

