import numpy as np
from matplotlib import pyplot as plt


elements = [0, 1, 2, 3, 4, 5, 6, 7] #P1 to P8
probabilities = [0.5 / 8, 2.5 / 8, 0.75 / 8, 2 / 8, 0.5 / 8, 1 / 8, 0.25 / 8, 0.5 / 8] # Probabilities

def chooseValue():
    return np.random.choice(elements, 1, p=list(probabilities))

def createEverything():
    # Create y values
    listClass = []
    for i in range(0,8):
        listClass.append(0)
    for j in range(0,100000):
        nb = int(chooseValue())
        print(nb)
        listClass[nb] += 1
    # Create x values
    x = []
    for k in range(0,8):
        x.append(k)
    # Plot, gotta change yticks if we change the number of iterations on y
    plt.bar(x,listClass)
    plt.title('Discret à poids')
    plt.show()



if __name__ == '__main__':
    createEverything()