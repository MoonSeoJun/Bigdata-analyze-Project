from bs4.builder import TreeBuilder
import requests
from bs4 import BeautifulSoup

team_num = 25
start_year = 2015
end_year = 2020

# Select League
premier_league = 0
serie_a = 1 
bundesliga = 2
ligue_1 = 3
laliga = 4

# 리그 내에서 발생하는 지출액과 수익을 수집하기 위한 함수
def get_club_expenditure_few_year(want_year, team_num, league_select):
    total_clubs_info = []
    for_return_club_info = []

    for i in range(0,team_num):
        total_clubs_info.append([])
        for_return_club_info.append([])

    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # 리그에서 시작 연도와 끝 연도 동안 지출한 금액과 수익을 받아오기 위한 URL
    url = [fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=189&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=75&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=40&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=50&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={want_year}&saison_id_bis={want_year}&land_id=157&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0']

    # selected url crawling
    req = requests.get(url[league_select], headers=headers)

    if req.status_code == requests.codes.ok:
            soup = BeautifulSoup(req.text, 'lxml')

            club = soup.find("div", {"class":"responsive-table"})
            info_of_club = club.find_all("td")
        
            for i in range(0,(8 * team_num)): # 한 개의 큼럽 당 8개의 정보가 담겨있음
                total_clubs_info[i%8].append(info_of_club[i])
                
    for i in range(0, team_num):
        for j in range(0, 8):
            if j != 1:
                for_return_club_info[i].append(total_clubs_info[j][i].text)

    return for_return_club_info
    
# 원하는 시작 연도와 끝 연도를 입력 받고 함수 호출
def print_total_club_info(league_num, survived_clubs):
    total_club_info = []
    for i in range(start_year, end_year + 1):
        total_club_info.append(get_club_expenditure_few_year(i, team_num, league_num))

    return append_data_to_survived_club_arr(survived_clubs, total_club_info)

def append_data_to_survived_club_arr(survived_club, total_club):
    for year in range(0, 5):
        for i in range(0, len(survived_club)):
            for j in range(0 ,team_num):
                if survived_club[i][0] == total_club[year][j][1]: # 클럽 이름 비교
                    survived_club[i].append(total_club[year][j][2])

            if len(survived_club[i]) < year + 2:
                survived_club[i].append('5')

    return survived_club