from random import random

import numpy as np
from matplotlib import pyplot as plt

def generateNumber():
    return random()

def createEverything():
    # Create y values
    listClass = []
    for i in range(0,100):
        listClass.append(0)
    for j in range(0,100000):
        nb = int(generateNumber() * 100)
        listClass[nb] += 1
    # Create x values
    x = []
    for k in range(0,100):
        x.append(k)
    # Plot, gotta change yticks if we change the number of iterations on y
    plt.bar(x,listClass)
    plt.title('Aléatoire'), plt.xticks([0,100]), plt.yticks([0,900,1000, 1100])
    plt.show()



if __name__ == '__main__':
    # createEverything()
    a = np.array([[1, 2, 3], [4, 5, 6]])
    print(a.mean())

    print("Nique toi enculé :")
    input = input()
    print(type(int(input)))

