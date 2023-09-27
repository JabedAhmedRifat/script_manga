import requests
from bs4 import BeautifulSoup
import pandas as pd

manga_create_url='http://localhost:8001/manga-create/'
genre_create_url='http://localhost:8001/genre-create/'



def scrape_manga_data(url):
    page= requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    return soup
# ////////////////////////////////////////////////////////////
    
def save_data_to_excel(data, excel_filename):
    df = pd.DataFrame(data)
    df.to_excel(excel_filename, index=False)
    # print({excel_filename})
# ///////////////////////////////////////////////////////////////////////////

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
        "genre": genre_name
    }
    response = requests.post(genre_create_url, json=genre_payload)
    
    if response.status_code == 201:
        print("Response status code:", response.status_code)
    else:
        print("Response content:", response.content)


num_page = 5

for page_num in range(num_page):
    if page_num == 0:
        page_url = "https://readm.org/popular-manga"
    else:
        page_url = "https://readm.org/popular-manga/{page_num}"
        
        
    # popular page scrapping 
    
    scrap_data = scrape_manga_data(page_url)
    title_class = scrap_data.find_all('h2',{'class':'truncate'})
    
    genre_class = scrap_data.find_all('p', {'class':'poster-meta'})
    description_class = scrap_data.find_all('p', {'class':'mobile-only'})
    # details_link=scrap_data.find_all('a',{'title':''})
    
    data =[]
    
    for title, genre, description in zip(title_class, genre_class, description_class):
        title_text = title.text 
        genre_text = genre.text 
        description_text = description.text 
        details_link=str(scrap_data.find('a',{'title':title_text})['href'])
       
        
        
        
        data.append({
            'title': title_text,
            "genre":genre_text,
            "description" : description_text,
            "image link": "https//readm.org" + str(scrap_data.find('img',{"alt":title_text})['src']),
            # 'details_link':details_link,
           
        }) 
        
        #posting data for manga create
        for entry in data:
            manga_payload = {
                "title": entry['title'],
                "description": entry['description'],
                "author" : "jabed",
                "popularity":9
                }
            # print(manga_payload)
                
                    
            response = requests.post(manga_create_url, json=manga_payload)
                        
            if response.status_code == 201:
                print("Response status code:", response.status_code)
            else:
                print("Response content:", response.content)
        
                    
        
            # details start
            details_result= scrape_manga_data("https://readm.org"+ details_link)
                
                # chapter Start
                
            episod = details_result.find_all("h6", {"class":"truncate"})
            
            for e in episod:
                # print(e.text)
                # print(e.a['href'])
                chapter_link = "https://readm.org"+(e.a['href'])
                
                #scrap image from each chapter 
                
                scrap = scrape_manga_data(chapter_link)
                image_elements = scrap.find_all('img',{'class':'img-responsive'})
                for p in image_elements:
                    image_link = "https://readm.org"+ p['src']

                    if not image_link.endswith(('/1/111/mm1.png?v=12','1/111/rm2.png?v=12')):          
                        pass
                        # print(image_link)
                        