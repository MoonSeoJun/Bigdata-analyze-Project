import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
from .total_league_expenditure import get_league_expenditure_crawling
from .get_clubs_expenditure import get_club_expenditure_crawling


class Pie_chart:
    def __init__(self, want_year):
        self.__want_year = want_year
        self.__total_transfer_expenditure = 0
        self.__expenditure_for_pie_chart = []
        self.__crawling_club_expenditure = []
        self.__club_name = []

        # 생성되면서 그래프에 필요한 배열 완성
        self.__crawling_total_transfer_expenditure = get_league_expenditure_crawling(self.__want_year)
        self.__crawling_clubs_transfer_expenditure()

        self.__get_data_for_graph()

    # 그래프를 위해 데이터를 정리하는 함수
    def __get_data_for_graph(self):
        self.__get_club_name(self.__crawling_club_expenditure)
        self.__get_total_transfer_expenditure()
        self.__get_clubs_transfer_expenditure()
        self.__divide_league_expenditure(self.__crawling_club_expenditure)
        self.__remove_low_percentages()

    # 전 세계 리그에서 지출한 금액을 합해주는 함수
    def __get_total_transfer_expenditure(self):
        for i in range(0, len(self.__crawling_total_transfer_expenditure)):
            self.__crawling_total_transfer_expenditure[i][2] = self.__change_amount_unit(self.__crawling_total_transfer_expenditure[i][2])
            self.__total_transfer_expenditure += self.__crawling_total_transfer_expenditure[i][2]

    # 5대 리그에 속한 클럽이 지출한 금액을 million 단위로 변환하는 함수
    def __get_clubs_transfer_expenditure(self):
        for i in range(0, len(self.__crawling_club_expenditure)):
            for j in range(0, len(self.__crawling_club_expenditure[i])):
                self.__crawling_club_expenditure[i][j][3] = self.__change_amount_unit(self.__crawling_club_expenditure[i][j][3])

    # 리그에 속한 클럽의 이름을 배열에 저장하는 함수
    def __get_club_name(self, crawling_arr):
        self.__club_name = [crawling_arr[i][j][1] for i in range(0, len(crawling_arr)) for j in range(0, len(crawling_arr[i])) if crawling_arr[i][j][2] == " Premier League " or crawling_arr[i][j][2] == " Ligue 1 " or crawling_arr[i][j][2] == " LaLiga " or crawling_arr[i][j][2] == " Serie A " or crawling_arr[i][j][2] == " Bundesliga "]

    # 이적 시장에서 가장 많은 이적료를 지출하는 5대 리그에 소속한 클럽의 지출액을 받아오는 그래프
    def __crawling_clubs_transfer_expenditure(self):
        for i in range(0, 5):
            self.__crawling_club_expenditure.append(get_club_expenditure_crawling(self.__want_year, i))
    
    # 금액 단위를 제거하는 반복문
    def __change_amount_unit(self, amount):
        if amount == '-':
            amount = 0
            return amount

        new_string = ''.join(filter(str.isalnum, amount))
        if new_string[-1] == 'm':
            amount = (int(new_string[0:-1]) / 100)
        elif new_string[-1] == 'h':
            amount = (int(new_string[0:-2]) / 1000)
        elif new_string[-1] == 'n':
            amount = (int(new_string[0:-2]) * 10)

        return amount

    # 리그에서 지출한 금액을 이적시장 전체로 나눠 배열에 추가
    def __divide_league_expenditure(self, crawling_arr):
        self.__expenditure_for_pie_chart = [round(((crawling_arr[i][j][3] / self.__total_transfer_expenditure) * 100 ), 1) for i in range(0, len(crawling_arr)) for j in range(0, len(crawling_arr[i])) if crawling_arr[i][j][2] == " Premier League " or crawling_arr[i][j][2] == " Ligue 1 " or crawling_arr[i][j][2] == " LaLiga " or crawling_arr[i][j][2] == " Serie A " or crawling_arr[i][j][2] == " Bundesliga "]

    # 낮은 비율의 지출 금액 삭제하고 Other이라는 변수에 저장하는 함수
    def __remove_low_percentages(self):
        other_num = 0

        for i in range(0, len(self.__expenditure_for_pie_chart)):
            if self.__expenditure_for_pie_chart[i] < 1:
                other_num += self.__expenditure_for_pie_chart[i]
                self.__expenditure_for_pie_chart[i] = 0
                self.__club_name[i] = "0"

        self.__club_name.append("Other")
        self.__expenditure_for_pie_chart.append(other_num)

    # 그래프를 그려주는 함수
    def drawing_graph(self):
        fig, ax = plt.subplots()

        ratio = [i for i in self.__expenditure_for_pie_chart if i != 0]
        alabels = [i for i in self.__club_name if i != "0"]
        explode = [0.05 for i in range(0, len(ratio))]

        wedges, labels, autopct = ax.pie(ratio, labels=alabels, explode=explode,autopct='%.1f%%', startangle=90, counterclock=False)
        plt.title(f"{self.__want_year}/{self.__want_year + 1} season  Total Transfer Expenditure €{round(self.__total_transfer_expenditure, 2)}m")
        plt.setp(labels, fontsize=5.4, rotation=15)

        dataframe = {
            "Club Name" : alabels,
            "Expenditure Percentages" : ratio,
        }

        print(alabels)
        print(ratio)

        df = pd.DataFrame(dataframe, index=[i for i in range(1, len(alabels) + 1)])

        print(df)

        plt.show()

if __name__ == "__main__":
    pie = Pie_chart(2018) # 여기에 원하는 연도를 입력하세요
    pie.drawing_graph()