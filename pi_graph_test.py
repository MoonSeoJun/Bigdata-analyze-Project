import matplotlib.pyplot as plt


fig, axs = plt.subplots(nrows=2, ncols=2)

data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
names = list(data.keys())
values = list(data.values())
rank_arr = [i ** 2 for i in range(1, 5)]
rand_arr = []


# plot time signal:
axs[0, 0].plot(names, values)

axs[0, 1].plot(names, rank_arr)

axs[1,1].remove()

fig.tight_layout()
plt.show()
