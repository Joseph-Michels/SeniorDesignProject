import matplotlib.pyplot as plt
import numpy as np

within = []
outside = []

with open("analysis.txt", 'r') as rf:
    for line in rf:
        # name = line[ : line.find(':') ]
        within_arr = line[ line.find('(')+1 : line.find(')')].split(',')
        outside_arr = line[ line.rfind('(')+1 : line.rfind(')')].split(',')
        # print(name, within_str, outside_str)

        w_min, w_avg, w_max = float(within_arr[0]), float(within_arr[1]), float(within_arr[2])
        o_min, o_avg, o_max = float(outside_arr[0]), float(outside_arr[1]), float(outside_arr[2])

        if w_avg != -1:
            within.append(w_avg)
        if o_avg != -1:
            outside.append(o_avg)

bins = [0.025*n for n in range(48)]
plt.hist(within, bins, alpha=0.5, label="within")
plt.hist(outside, bins, alpha=0.5, label="outside")
plt.legend(loc="upper right")
plt.title("Average Case")
plt.show()