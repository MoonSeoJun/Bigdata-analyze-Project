from matplotlib.pyplot import legend
from numpy import int8
import requests
from bs4 import BeautifulSoup

# get the survived clubs in leagues
def get_survived_clubs_crawling(current_year, want_league, team_num):
    total_clubs_info = []
    for_return_club_info = []

    # 원하는 리그 선택
    url = [fr'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id={current_year}', 
    fr'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id={current_year}',
    fr'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id={current_year}']

    for i in range(0,team_num):
        total_clubs_info.append([])
        for_return_club_info.append([])

    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    req = requests.get(url[want_league], headers=headers)

    if req.status_code == requests.codes.ok:
            soup = BeautifulSoup(req.text, 'lxml')

            club = soup.find("div", {"class":"responsive-table"})
            info_of_club = club.find_all("td")

            for i in range(1,(10 * team_num)): # 한 개의 큼럽 당 10개의 정보가 담겨있음
                total_clubs_info[i%10].append(info_of_club[i])

    for i in range(1, team_num):
        new_string = total_clubs_info[1][i].text
        for_return_club_info[i].append(new_string[0:len(new_string) - 1]) # 문자열 마지막 띄어쓰기를 지우기 위함

    return for_return_club_info


def get_survived_clubs(want_league, want_year, team_num):
    count = 0

    # 마지막 결과값을 저장하기 위한 배열
    result_arr = []

    first_club_arr = get_survived_clubs_crawling(want_year, want_league, team_num)

    # 리그에서 한 번이라도 강등을 당한 팀을 제외하기 위한 반복문
    for i in range(1, (2021 - want_year)):
        comparsion_arr = get_survived_clubs_crawling((want_year + i), want_league, team_num)
        
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


    for i in range(0, len(result_arr)):
        result_arr[i] = [result_arr[i]]

    return result_arr