import matplotlib.pyplot as plt
import numpy as np
from .get_clubs_expenditure import get_club_expenditure_few_year_crawling
from .get_clubs_ranking import get_clubs_ranking_crawling
from .get_clubs_trophies import get_clubs_trophies

class Club_data:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year

        self.league_num = [0]

        self.premier_league_trophies_kind = ["English Champion", "English League Cup winner", "FA Cup Winner", "Champions League Winner", "Europa League Winner"]
        self.man_city = [0, "Manchester City", "ManCity"]
        self.arsenal = [1, "Arsenal FC", "Arsenal"]
        self.chelsea = [2, "Chelsea FC", "Chelsea"]

        self.label = []
        self.club_expenditure = []
        self.club_ranking = []

        self.club_trophies = []
        self.premier_league_club_trophies = [[],[],[],[],[]]

    def set_premier_league_club_trophies(self):
        for i in range(0, len(self.premier_league_trophies_kind)):
            self.premier_league_club_trophies[i].append(0)

    def get_graph_needs(self, club_for_trophies,club_for_expenditure, club_for_ranking):
        self.club_trophies = get_clubs_trophies(club_for_trophies)
        for year in range(self.start_year, self.end_year):
            self.set_premier_league_club_trophies()
            expenditure_result = get_club_expenditure_few_year_crawling(year,self.league_num[0])
            ranking_result = get_clubs_ranking_crawling(year, self.league_num[0])
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

            for i in range(0, len(self.club_trophies)):
                if self.club_trophies[i][0] == f'{str(year)[-2:]}/{str(year+1)[-2:]}':
                    for j in range(0, len(self.premier_league_trophies_kind)):
                        if self.club_trophies[i][1] == self.premier_league_trophies_kind[j]:
                            self.premier_league_club_trophies[j][-1] += 1

    def drawing_graph(self):
        width = 0.5

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

        add_1 = np.add(self.premier_league_club_trophies[0], self.premier_league_club_trophies[1])
        add_2 = np.add(add_1, self.premier_league_club_trophies[2])
        add_3 = np.add(add_2, self.premier_league_club_trophies[3])
        
        axs[1, 0].bar(self.label, self.premier_league_club_trophies[0], width=width, label="English Champion")
        axs[1, 0].bar(self.label, self.premier_league_club_trophies[1], width=width, bottom=self.premier_league_club_trophies[0], label="English League Cup")
        axs[1, 0].bar(self.label, self.premier_league_club_trophies[2], width=width, bottom=add_1, label="FA Cup")
        axs[1, 0].bar(self.label, self.premier_league_club_trophies[3], width=width, bottom=add_2, label="Champions League")
        axs[1, 0].bar(self.label, self.premier_league_club_trophies[4], width=width, bottom=add_3, label="Europa League")

        axs[1, 0].set_title("Club's season Trophies")
        axs[1, 0].set_ylabel("Trophies")
        axs[1, 0].legend(loc='upper right')
        

        axs[1, 1].remove()

        plt.show()

if __name__ == "__main__":
    graphs_datas = Club_data(2015, 2021)
    graphs_datas.get_graph_needs(graphs_datas.man_city[0], graphs_datas.man_city[1], graphs_datas.man_city[2])
    graphs_datas.drawing_graph()