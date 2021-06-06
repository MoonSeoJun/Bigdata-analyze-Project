from typing import NewType
import matplotlib.pyplot as plt
import numpy as np
import club_balance
import survived_in_league

def drawing_graph(league_arr):
    labels = [league_arr[i][0] for i in range(0, len(league_arr))]
    year_15 = [league_arr[i][1] for i in range(0, len(league_arr))]
    year_16 = [league_arr[i][2] for i in range(0, len(league_arr))]
    year_17 = [league_arr[i][3] for i in range(0, len(league_arr))]
    year_18 = [league_arr[i][4] for i in range(0, len(league_arr))]
    year_19 = [league_arr[i][5] for i in range(0, len(league_arr))]

    c_bottom = np.add(year_15, year_16)
    d_bottom = np.add(c_bottom, year_17)
    f_bottom = np.add(d_bottom, year_18)

    x = range(len(labels))

    width = 0.5

    plt.bar(range(len(year_15)), year_15, width=width, label='2015')
    plt.bar(range(len(year_16)), year_16, bottom=year_15, width=width, label='2016')
    plt.bar(x, year_17, bottom=c_bottom, width=width, label='2017')
    plt.bar(x, year_18, bottom=d_bottom, width=width, label='2018')
    plt.bar(x, year_19, bottom=f_bottom, width=width, label='2019')
    plt.xticks(fontsize=7, rotation=45)
    plt.xlabel("Club name")
    plt.ylabel("Expenditure(million €)")

    ax = plt.subplot()
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

def arr_index_string_to_int(league_arr, survived_club):
    for i in range(0, len(survived_club)):
        for j in range(1, 6):
            new_string = ''.join(filter(str.isalnum, league_arr[i][j]))
            if len(new_string) == 6:
                league_arr[i][j] = int(new_string[0:3])
            elif len(new_string) == 5:
                league_arr[i][j] = int(new_string[0:2])
            else:
                league_arr[i][j] = int(new_string[0:1])
    
    return league_arr

def call_drawing_function(league_num, survived_club):
    league_arr = club_balance.print_total_club_info(league_num, survived_club)
    #print(league_arr)
    graph_arr = arr_index_string_to_int(league_arr, survived_club)
    drawing_graph(graph_arr)

if __name__ == "__main__":
    league = club_balance.serie_a
    start_year = 2015
    team_num = 21
    survived_club = survived_in_league.get_survived_clubs(league, start_year, team_num)
    call_drawing_function(league, survived_club)