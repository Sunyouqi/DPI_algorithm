from k_means import K_means_algo
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt



data = load_breast_cancer()


# run k_means with k = 2 to 7
a = K_means_algo(data.data)
distortion_list = []
x_axis = [2 , 3 , 4 , 5 , 6 , 7 ]
for i in range(2,8):
    solution = a.k_means(i)
    cur = solution.calc_distortion()
    distortion_list.append(cur)
    
    
    
# draw graph of all distortions
plt.plot(x_axis, distortion_list,'bo')
plt.axis([0,8,0,150000])
plt.suptitle('Distortion Vs K value')
plt.xlabel('K value')
plt.ylabel('Distortion')
plt.show()


