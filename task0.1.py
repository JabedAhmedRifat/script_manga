import requests
from bs4 import BeautifulSoup
import pandas as pd

manga_create_url='http://localhost:8000/manga-create/'
# manga_episode_url='http://localhost:8000/manga/create_episode/'
# manga_page_url='http://localhost:8000/manga/create_page'



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
#///////////////////////////////////////////////////////////////////////////
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
    
    # image_elements =scrap_data.find_all('img')
    # image_urls = [img['src'] for img in image_elements]
    details_link=scrap_data.find_all('a',{'title':''})
    
    data =[]
    
    for title, genre, description in zip(title_class, genre_class, description_class):
        title_text = title.text 
        genre_text = genre.text 
        description_text = description.text 
        details_link=str(scrap_data.find('a',{'title':title_text})['href'])
        # print(details_link)
       
        
        
        
        data.append({
            'title': title_text,
            "genre":genre_text,
            "description" : description_text,
            "image link": "https//readm.org" + str(scrap_data.find('img',{"alt":title_text})['src']),
            'details_link':details_link,
           
        }) 
        # print(data)
        
        
        # details start
        details_result= scrape_manga_data("https://readm.org"+details_link)
       
        
        # details_summary = details_result.find_all('p',{"id":"tv-series-desc"})
        # for summary in details_summary:
        #     details_summary_text = summary.get_text()
        # print(details_summary[0].get_)
        
        # chapter Start
        
        episod = details_result.find_all("h6", {"class":"truncate"})
        
        for e in episod:
            # print(e.text)
            # print(e.a['href'])
            chapter_link = "https://readm.org"+(e.a['href'])
            scrap = scrape_manga_data(chapter_link)
            # print(scrap)
            image_elements = scrap.find_all('img',{'class':'img-responsive'})
            for p in image_elements:
                image_link = "https://readm.org"+ p['src']

                if not image_link.endswith(('/1/111/mm1.png?v=12','1/111/rm2.png?v=12')):
                    
                    print(image_link)
            # print(image_link)
            
        # more_details = details_result.find('table', {"class":"ui unstackable single line celled table"})
        # div_elements = more_details.find_all('div')
        # for div in div_elements:
        #     pass
        #     # print(div.text)
                
    excel_filename = "manga_page_" + str(page_num) + ".xlsx"
    # save_data_to_excel(data, excel_filename)
    


















# data=[]
# for x in range(0,5):
#     if x==0:
#         page_number=''
#     else:
#         page_number=x
#     print(page_number)
#     url = "https://readm.org/popular-manga/"+str(page_number)
#     print(url)
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     page.close()

#     title_class = soup.find_all('h2', {'class': 'truncate'})

#     genre_class = soup.find_all('p', {'class': 'poster-meta'})

#     description_class = soup.find_all('p', {'class': 'mobile-only'})
#     # print(description_class)


#     # image_elements = soup.find_all('img',{"alt":"Martial Peak"})
#     # print(image_elements)


#     image_elements = soup.find_all('img')
#     image_urls = [img['src'] for img in image_elements]
#     # print(image_urls)

    

#     for title, genre, description, img_urls in zip(title_class, genre_class, description_class, image_urls):
#         title_text = title.text
#         genre_text = genre.text
#         description_text = description.text
        
#         data.append({
#             "Title": title_text,
#             "Genre": genre_text,
#             "Description": description_text,
#             "Image Link": "https://readm.org"+img_urls
#         })

    
# df = pd.DataFrame(data)
# excel_filename = "manga_data_pandas.xlsx"
# df.to_excel(excel_filename, index=False,)

# print({excel_filename})
    