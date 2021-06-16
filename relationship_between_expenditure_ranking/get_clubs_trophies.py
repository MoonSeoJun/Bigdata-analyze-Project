import requests
from bs4 import BeautifulSoup

def get_clubs_trophies(select_team):
    print("club trophies Crawling start")
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    url = ['https://www.transfermarkt.com/manchester-city/erfolge/verein/281',
    'https://www.transfermarkt.com/arsenal-fc/erfolge/verein/11',
    'https://www.transfermarkt.com/chelsea-fc/erfolge/verein/631',
    'https://www.transfermarkt.com/paris-saint-germain/erfolge/verein/583',
    'https://www.transfermarkt.com/fc-barcelona/erfolge/verein/131',
    'https://www.transfermarkt.com/real-madrid/erfolge/verein/418',
    'https://www.transfermarkt.com/juventus-fc/erfolge/verein/506',
    'https://www.transfermarkt.com/liverpool-fc/erfolge/verein/31',
    'https://www.transfermarkt.com/bayern-munich/erfolge/verein/27']

    # selected url crawling
    req = requests.get(url[select_team], headers=headers)

    if req.status_code == requests.codes.ok:
            total_clubs_info = []
            for_return_club_info = []

            soup = BeautifulSoup(req.text, 'lxml')

            main_info = soup.find("div", {"class":"large-4 columns"})
            in_detail_info = main_info.find_all("td")
            
            total_info_len = len(in_detail_info)
            in_detail_info_len = int(total_info_len / 3)

            for i in range(0,in_detail_info_len):
                total_clubs_info.append([])
                for_return_club_info.append([])
        
            for i in range(0,total_info_len): # 한 개의 큼럽 당 8개의 정보가 담겨있음
                total_clubs_info[i%3].append(in_detail_info[i])
              
    for i in range(0, in_detail_info_len):
        for j in range(0, 3):
            if j != 1:
                for_return_club_info[i].append(total_clubs_info[j][i].text)
        

    return for_return_club_info