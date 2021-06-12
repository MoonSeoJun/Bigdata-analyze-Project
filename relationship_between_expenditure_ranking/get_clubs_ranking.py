import requests
from bs4 import BeautifulSoup

def get_clubs_ranking_crawling(want_year, league_select):
    print(f"{want_year} year Ranking Crawling start")
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    url = [f'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={want_year}']

    # selected url crawling
    req = requests.get(url[league_select], headers=headers)

    if req.status_code == requests.codes.ok:
            total_clubs_info = []
            for_return_club_info = []

            soup = BeautifulSoup(req.text, 'lxml')

            club = soup.find("div", {"class":"box tab-print"})
            info_of_club = club.find_all("td")

            info_len = len(info_of_club)
            team_num = int(info_len / 6)

            for i in range(0,team_num):
                total_clubs_info.append([])
                for_return_club_info.append([])
        
            for i in range(0,info_len): # 한 개의 큼럽 당 8개의 정보가 담겨있음
                total_clubs_info[i%6].append(info_of_club[i])
                
    for i in range(0, team_num):
        for j in range(0, 6):
            if j != 1:
                new_string = ''.join(filter(str.isalnum, total_clubs_info[j][i].text))
                for_return_club_info[i].append(new_string)

    print(f"{want_year} year Ranking Crawling end")

    return for_return_club_info