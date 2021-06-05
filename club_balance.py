import requests
from bs4 import BeautifulSoup

team_num = 10
start_year = 2012
end_year = 2020

# Select League
premier_league = 0
serie_a = 1
bundesliga = 2
ligue_1 = 3
laliga = 4


# 리그 내에서 발생하는 지출액과 수익을 수집하기 위한 함수
def get_club_expenditure_few_year(start_year, end_year, team_num):
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

    # selected url crawling
    req = requests.get(url[premier_league], headers=headers)

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
def print_total_club_info():
    for i in range(int(start_year), int(end_year) + 1):
        total_club_info = get_club_expenditure_few_year(i, i, team_num)
        for i in range(0, team_num):
            print(total_club_info[i])
        print()


if __name__ == "__main__":
    print_total_club_info()