import requests
from bs4 import BeautifulSoup

team_num = 19 # Bundesliga의 경우 리그에 존재하는 팀이 18개이기 때문에 19를 사용함. 나머지는 21
want_year = 2015 # 원하는 시작 연도

serie_a = 0
premier_league = 1
bundesliga = 2
laliga = 3
ligue_1 = 4

def get_club_expenditure_few_year(current_year):
    total_clubs_info = []
    for_return_club_info = []

    # 원하는 리그 선택
    url = [fr'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1/plus/?saison_id={current_year}', 
    fr'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id={current_year}']

    for i in range(0,team_num):
        total_clubs_info.append([])
        for_return_club_info.append([])

    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    req = requests.get(url[ligue_1], headers=headers)

    if req.status_code == requests.codes.ok:
            soup = BeautifulSoup(req.text, 'lxml')

            club = soup.find("div", {"class":"responsive-table"})
            info_of_club = club.find_all("td")

            for i in range(0,(10 * team_num)): # 한 개의 큼럽 당 10개의 정보가 담겨있음
                total_clubs_info[i%10].append(info_of_club[i])

    for i in range(1, team_num):
        for_return_club_info[i].append(total_clubs_info[2][i].text)

    return for_return_club_info


def tidy_result():
    count = 0

    # 마지막 결과값을 저장하기 위한 배열
    result_arr = []

    first_club_arr = get_club_expenditure_few_year(want_year)

    # 리그에서 한 번이라도 강등을 당한 팀을 제외하기 위한 반복문
    for i in range(1, (2021 - want_year)):
        comparsion_arr = get_club_expenditure_few_year((want_year + i))
        
        for j in range(1, team_num):
            for z in range(1, team_num):
                if first_club_arr[j][0] == comparsion_arr[z][0]:
                    count += 1
            
            if count == 0:
                first_club_arr[j][0] = '0'
            
            count = 0

    # 리그에서 한 번도 강등을 당하지 않은 팀만 추가
    for i in range(1, team_num):
        if first_club_arr[i][0] != '0':
            result_arr.append(first_club_arr[i][0])

    print(result_arr)

if __name__ == "__main__":
    tidy_result()