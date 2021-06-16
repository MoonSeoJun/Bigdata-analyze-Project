import requests
from bs4 import BeautifulSoup

def get_club_expenditure_few_year_crawling(want_year, league_select):
    print(f"{want_year} year Expenditure Crawling start")
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # 리그에서 시작 연도와 끝 연도 동안 지출한 금액과 수익을 받아오기 위한 URL
    url = [f'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=189&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    f'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=50&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    f'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=157&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    f'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=75&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    f'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=40&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0']

    # selected url crawling
    req = requests.get(url[league_select], headers=headers)

    if req.status_code == requests.codes.ok:
            total_clubs_info = []
            for_return_club_info = []

            soup = BeautifulSoup(req.text, 'lxml')

            club = soup.find("div", {"class":"responsive-table"})
            info_of_club = club.find_all("td")

            info_len = len(info_of_club)
            team_num = int(info_len / 8)

            for i in range(0,team_num):
                total_clubs_info.append([])
                for_return_club_info.append([])
        
            for i in range(0,info_len): # 한 개의 큼럽 당 8개의 정보가 담겨있음
                total_clubs_info[i%8].append(info_of_club[i])
                
    for i in range(0, team_num):
        for j in range(0, 8):
            if j != 1:
                for_return_club_info[i].append(total_clubs_info[j][i].text)

    print(f"{want_year} year Expenditure Crawling end")

    return for_return_club_info

