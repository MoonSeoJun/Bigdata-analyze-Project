import requests
from bs4 import BeautifulSoup

# 리그 내에서 발생하는 지출액과 수익을 수집하기 위한 함수
def get_club_expenditure_few_year(start_year, end_year, team_num, league_num):
    total_clubs_info = []
    for_return_club_info = []

    for i in range(0,team_num):
        total_clubs_info.append([])
        for_return_club_info.append([])

    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # 리그에서 시작 연도와 끝 연도 동안 지출한 금액과 수익을 받아오기 위한 URL
    url = [fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={start_year}&saison_id_bis={end_year}&land_id=189&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={start_year}&saison_id_bis={end_year}&land_id=75&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={start_year}&saison_id_bis={end_year}&land_id=40&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={start_year}&saison_id_bis={end_year}&land_id=50&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0',
    fr'https://www.transfermarkt.com/transfers/einnahmenausgaben/statistik/plus/0?ids=a&sa=&saison_id={start_year}&saison_id_bis={end_year}&land_id=157&nat=&pos=&altersklasse=&w_s=&leihe=&intern=0']

    req = requests.get(url[league_num], headers=headers)

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

team_num = 10
print("Enter your want start year : ")
start_year = input()
print("Enter your want end year : ")
end_year = input()
print("Select League")
print("0 : premier_league | 1 : serie_a | 2 : bundesliga | 3 : ligue_1 | 4 : laliga")
league_num = input()

# 원하는 시작 연도와 끝 연도를 입력 받고 함수 호출
for i in range(int(start_year), int(end_year) + 1):
    total_club_info = get_club_expenditure_few_year(i, i, team_num, int(league_num))
    for i in range(0, team_num):
        print(total_club_info[i])
    print()