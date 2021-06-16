import matplotlib.pyplot as plt
import numpy as np
from .get_clubs_expenditure import get_club_expenditure_few_year_crawling
from .get_clubs_ranking import get_clubs_ranking_crawling
from .get_clubs_trophies import get_clubs_trophies

class Club_data:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year

        self.league_num = [0, 1, 2, 3, 4]

        self.premier_league_trophies_kind = ["English Champion", "English League Cup winner", "FA Cup Winner", "Champions League Winner", "Europa League Winner"]
        self.ligue1_league_trophies_kind = ["French Champion", "French league cup winner", "French Cup winner ", "Champions League Winner", "Europa League Winner"]
        self.laliga_league_trophies_kind = ["Spanish Champion", "Spanish Cup winner ", "Champions League Winner", "Europa League Winner"]
        self.serieA_league_trophies_kind = ["Italian Champion", "Italian Cup winner", "Champions League Winner", "Europa League Winner"]
        self.bundesliga_league_trophies_kind = ["German Champion", "German Cup winner ", "Champions League Winner", "Europa League Winner"]

        self.man_city = [0, "Manchester City", "ManCity", 0, self.premier_league_trophies_kind]
        self.arsenal = [1, "Arsenal FC", "Arsenal", 0, self.premier_league_trophies_kind]
        self.chelsea = [2, "Chelsea FC", "Chelsea", 0, self.premier_league_trophies_kind]
        self.psg = [3, "Paris Saint-Germain", "ParisSG", 1, self.ligue1_league_trophies_kind]
        self.barcelona = [4, "FC Barcelona", "Barcelona", 2, self.laliga_league_trophies_kind]
        self.real_madrid = [5, "Real Madrid", "RealMadrid", 2, self.laliga_league_trophies_kind]
        self.juventus = [6, "Juventus FC", "Juventus", 3, self.serieA_league_trophies_kind]
        self.liverpool = [7, "Liverpool FC", "Liverpool", 0, self.premier_league_trophies_kind]
        self.bayern_munich = [8, "Bayern Munich", "FCBayern", 4, self.bundesliga_league_trophies_kind]

        self.label = []
        self.club_expenditure = []
        self.club_ranking = []

        self.club_trophies_for_crawling = []
        self.league_trophies_array = []

    def set_club_trophies(self, array_for_get_trophies):
        for i in range(0, len(array_for_get_trophies)):
            array_for_get_trophies[i].append(0)

    def set_league_trophies_array(self, kind_of_league):
        for i in range(0, len(kind_of_league)):
            self.league_trophies_array.append([])

    def get_graph_needs(self, league_num, club_for_trophies, club_for_expenditure, club_for_ranking, kind_of_league_trophies):
        self.club_trophies_for_crawling = get_clubs_trophies(club_for_trophies)
        for year in range(self.start_year, self.end_year):

            self.set_league_trophies_array(kind_of_league_trophies)
            self.set_club_trophies(self.league_trophies_array)

            expenditure_result = get_club_expenditure_few_year_crawling(year,self.league_num[league_num])
            ranking_result = get_clubs_ranking_crawling(year, self.league_num[league_num])

            self.label.append(f'{str(year)[-2:]}/{str(year+1)[-2:]}')

            for i in range(0, len(ranking_result)):
                if expenditure_result[i][1] == club_for_expenditure:
                    new_string = ''.join(filter(str.isalnum, expenditure_result[i][2]))
                    if new_string[-1] == 'm':
                        self.club_expenditure.append(int(new_string[0:-1]) / 100)
                    elif new_string[-1] == 'h':
                        self.club_expenditure.append(int(new_string[0:-2]) / 1000)
                    else:
                        self.club_expenditure.append(int(new_string))
                
                if ranking_result[i][1] == club_for_ranking:
                    self.club_ranking.append(int(ranking_result[i][0]))

            if len(self.club_expenditure) < year - self.start_year + 1:
                self.club_expenditure.append(0.5)

            for i in range(0, len(self.club_trophies_for_crawling)):
                if self.club_trophies_for_crawling[i][0] == f'{str(year)[-2:]}/{str(year+1)[-2:]}':
                    for j in range(0, len(kind_of_league_trophies)):
                        if self.club_trophies_for_crawling[i][1] == kind_of_league_trophies[j]:
                            self.league_trophies_array[j][-1] += 1

    def drawing_graph(self, kind_of_league_trophies):
        fig, axs = plt.subplots(nrows=2, ncols=2)

        axs[0, 0].bar(self.label, self.club_expenditure, width=0.5, label="Expenditure")
        axs[0, 0].set_title("Club's season expenditure")
        axs[0, 0].set_xlabel("Season")
        axs[0, 0].set_ylabel("Expenditure(million €)")
        axs[0, 0].legend(loc='upper right')

        axs[0, 1].plot(self.label, self.club_ranking, label="Ranking")
        axs[0, 1].invert_yaxis()
        axs[0, 1].set_title("Club's season League Ranking")
        axs[0, 1].set_ylabel("Ranking")
        axs[0, 1].legend(loc='upper right')

        self.trophies_drawing_graph_kind(axs, self.league_trophies_array, kind_of_league_trophies)

        axs[1, 0].set_title("Club's season Trophies")
        axs[1, 0].set_ylabel("Trophies")
        axs[1, 0].legend(loc='upper right')

        axs[1, 1].remove()

        plt.show()
    
    def trophies_drawing_graph_kind(self, axs, ligue_club_trophies, ligue_trophies_kind):
        width = 0.5

        add_1 = np.add(ligue_club_trophies[0], ligue_club_trophies[1])
        add_2 = np.add(add_1, ligue_club_trophies[2])
            
        axs[1, 0].bar(self.label, ligue_club_trophies[0], width=width, label=ligue_trophies_kind[0])
        axs[1, 0].bar(self.label, ligue_club_trophies[1], width=width, bottom=ligue_club_trophies[0], label=ligue_trophies_kind[1])
        axs[1, 0].bar(self.label, ligue_club_trophies[2], width=width, bottom=add_1, label=ligue_trophies_kind[2])
        axs[1, 0].bar(self.label, ligue_club_trophies[3], width=width, bottom=add_2, label=ligue_trophies_kind[3])
        
        if(len(ligue_trophies_kind) > 4):
            add_3 = np.add(add_2, ligue_club_trophies[3])
            axs[1, 0].bar(self.label, ligue_club_trophies[4], width=width, bottom=add_3, label=ligue_trophies_kind[4])

if __name__ == "__main__":
    premier_league_num = 0
    ligue_1_num = 1
    laliga_num = 2
    serie_A_num = 3
    bundesliga_num = 4

    print("----Relationship between expenditure and ranking----")
    print("Select the club")
    print("| ---Premier League--- | ---Ligue 1--- | ---La liga---  | ---Serie A--- | ---Bundesliga--- |")
    print("|  0. Manchest City    |   3. PSG      | 4. Barcelona   |  6. Juventus  | 8. Bayern Munich |")
    print("|  1. Arsenal FC       |               | 5. Real Madrid |               |                  |")
    print("|  2. Chelsea FC       |               |                |               |                  |")
    print("|  7. Liverpool FC     |               |                |               |                  |")

    select_club_num = input("--> ")

    print("Select start year")
    
    start_year = int(input("--> "))

    print("Select end year")

    end_year = int(input("--> "))

    graphs_datas = Club_data(start_year, end_year + 1)

    club_dict = {"0":graphs_datas.man_city, 
    "1":graphs_datas.arsenal, 
    "2":graphs_datas.chelsea, 
    "3":graphs_datas.psg, 
    "4":graphs_datas.barcelona, 
    "5":graphs_datas.real_madrid, 
    "6":graphs_datas.juventus,
    "7":graphs_datas.liverpool,
    "8":graphs_datas.bayern_munich}

    selected_club = club_dict[select_club_num]

    print(selected_club)

    graphs_datas.get_graph_needs(selected_club[3], selected_club[0], selected_club[1], selected_club[2], selected_club[4])
    graphs_datas.drawing_graph(selected_club[4])