from typing import NewType
import matplotlib.pyplot as plt
import numpy as np
from . import club_balance
from . import survived_in_league

def drawing_graph(league_arr, start_year, end_year):
    labels = [league_arr[i][0] for i in range(0, len(league_arr))]
    x = range(len(labels))
    width = 0.5
    count = 0

    for year in range(1, end_year - start_year + 1):
        year_count = end_year - (end_year - start_year - year + 1)

        current_bar = [league_arr[i][year] for i in range(0, len(league_arr))]

        year_1 = [league_arr[i][year - 2] for i in range(0, len(league_arr))]
        year_2 = [league_arr[i][year - 1] for i in range(0, len(league_arr))]
        
        if count == 0:
            plt.bar(x, current_bar, width=width, label=f'{year_count}/{(year_count + 1)}')
            count += 1
        elif count == 1:
            bottom_bar = [league_arr[i][year - 1] for i in range(0, len(league_arr))]
            plt.bar(x, current_bar, bottom=bottom_bar, width=width, label=f'{year_count}/{(year_count + 1)}')
            count += 1
        elif count == 2:
            add_arr = np.add(year_1, year_2)
            plt.bar(x, current_bar, bottom=add_arr, width=width, label=f'{year_count}/{(year_count + 1)}')
            count += 1
        else:
            add_arr = np.add(add_arr, year_2)
            plt.bar(x, current_bar, bottom=add_arr, width=width, label=f'{year_count}/{(year_count + 1)}')

    plt.xticks(fontsize=7, rotation=45)
    plt.xlabel("Club name")
    plt.ylabel("Expenditure(million €)")

    ax = plt.subplot()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

def arr_index_string_to_int(league_arr, survived_club, end_year):
    for i in range(0, len(survived_club)):
        for j in range(1, (end_year - start_year + 1)):
            new_string = ''.join(filter(str.isalnum, league_arr[i][j]))
            if new_string[-1] == 'm':
                league_arr[i][j] = int(new_string[0:-1]) / 100
                '''
                elif len(new_string) == 5:
                    league_arr[i][j] = int(new_string[0:-1])
                else:
                    league_arr[i][j] = int(new_string[0:-1])
                '''
            elif new_string[-1] == 'h':
                league_arr[i][j] = int(new_string[0:-2]) / 1000
            else:
                league_arr[i][j] = int(new_string)
    
    return league_arr

def call_drawing_function(league_num, survived_club, start_year, end_year):
    league_arr = club_balance.get_club_expenditure(league_num, survived_club, start_year, end_year)
    graph_arr = arr_index_string_to_int(league_arr, survived_club, end_year)
    drawing_graph(graph_arr, start_year, end_year)

if __name__ == "__main__":
    while True:
        print("Select the league")
        print("0 : Premier League | 1 : Serie A | 2 : Bundesliga | 3 : Ligue1 | 4 : La Liga")
        league = int(input())

        print("Input the start year")
        start_year = int(input())

        print("Input the end year")
        end_year = int(input()) # if your select 2020, last season is 2019/2020

        if start_year > end_year:
            print("-----------------------------------------")
            print("!Start year can not bigger than End year!")
            print("Try Input again\n")
        elif league < 0 or league > 4:
            print("-----------------------------------------")
            print("!This league number is not exist!")
            print("Try Input again\n")
        elif end_year > 2021:
            print("-----------------------------------------")
            print("!21/22 season was not updated!")
            print("Try Input again\n")
        else:
            break

    survived_club = survived_in_league.get_survived_clubs(league, start_year, end_year)
    call_drawing_function(league, survived_club, start_year, end_year)