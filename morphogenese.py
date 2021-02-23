import numpy as np
import cv2
from pathlib import Path
import imageio
import time
import random

def pngToGif(lenght):
    image_path = Path(r'C:\Users\alexi\PycharmProjects\BioInspire\src\Results')
    images = []
    for i in range(lenght):
        images.append(r'C:\Users\alexi\PycharmProjects\BioInspire\src\Results\result' + str(i) + '.png')

    image_list = []
    for file_name in images:
        image_list.append(imageio.imread(file_name))


    imageio.mimwrite('Results/results.gif', image_list)


def random_initialiser(shape):
    return(
        np.random.randint(100, size=shape, dtype="uint8") + 1,
        np.random.randint(100, size=shape, dtype="uint8") + 1
    )

class Morphogene():
    def __init__(self, taux_reaction_a, taux_reaction_i,
                 vitesse_diff_a, vitesse_diff_i,
                 taux_resorption, seuil_activation,
                 width, height):
        self.taux_reaction_a = taux_reaction_a
        self.taux_reaction_i = taux_reaction_i
        self.vitesse_diff_a = vitesse_diff_a
        self.vitesse_diff_i = vitesse_diff_i
        self.taux_resorption = taux_resorption
        self.seuil_activation = seuil_activation
        self.couleur1 = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        self.couleur2 = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

        self.width = width
        self.height = height
        self.a, self.i = random_initialiser((width, height))
        self.result = np.random.randint(100, size=(width, height, 3), dtype="uint8") + 1

    def reagir(self):
        ancien_i = self.i


        for i in range(self.height):
            for j in range(self.width):
                self.i[i][j] = self.i[i][j] + (self.taux_reaction_i * self.a[i][j] *  self.a[i][j])
                if ancien_i[i][j] == 0:
                    ancien_i[i][j] = 1
                self.a[i][j] = self.a[i][j] + (self.taux_reaction_a * self.a[i][j] * self.a[i][j] / ancien_i[i][j])

    def diffuse_A(self, i, j, taux_diff, tmp_a):
        diffuse_a = self.a[i][j] * taux_diff / 8
        tmp_a[i][j] = self.a[i][j] - self.a[i][j] * taux_diff
        # Intérieur
        if(i != 0 and j != 0 and i < self.width-1 and j < self.height-1):
            tmp_a[i+1][j] += diffuse_a
            tmp_a[i-1][j] += diffuse_a
            tmp_a[i][j+1] += diffuse_a
            tmp_a[i][j-1] += diffuse_a
            tmp_a[i+1][j-1] += diffuse_a
            tmp_a[i+1][j+1] += diffuse_a
            tmp_a[i-1][j+1] += diffuse_a
            tmp_a[i-1][j-1] += diffuse_a
        # Bords
        if(i == 0 and j!=0 and j < self.height-1):
            tmp_a[i+1][j] += diffuse_a
            tmp_a[i][j+1] += diffuse_a
            tmp_a[i+1][j+1] += diffuse_a
            tmp_a[i][j-1] += diffuse_a
            tmp_a[i+1][j-1] += diffuse_a
        if(i!=0 and j==0 and i < self.width-1):
            tmp_a[i+1][j] += diffuse_a
            tmp_a[i][j+1] += diffuse_a
            tmp_a[i+1][j+1] += diffuse_a
            tmp_a[i-1][j] += diffuse_a
            tmp_a[i-1][j+1] += diffuse_a
        if(i == self.width - 1 and j != 0 and j < self.height-1):
            tmp_a[i-1][j] += diffuse_a
            tmp_a[i][j+1] += diffuse_a
            tmp_a[i][j-1] += diffuse_a
            tmp_a[i-1][j+1] += diffuse_a
            tmp_a[i-1][j-1] += diffuse_a
        if(j == self.height-1 and i != 0 and i < self.width-1):
            tmp_a[i+1][j] += diffuse_a
            tmp_a[i-1][j] += diffuse_a
            tmp_a[i][j-1] += diffuse_a
            tmp_a[i+1][j-1] += diffuse_a
            tmp_a[i-1][j-1] += diffuse_a
        # Coins
        if (i == 0 and j == 0):
            tmp_a[i + 1][j] += diffuse_a
            tmp_a[i][j + 1] += diffuse_a
            tmp_a[i + 1][j + 1] += diffuse_a
        if (i == self.width - 1 and j == 0):
            tmp_a[i - 1][j + 1] += diffuse_a
            tmp_a[i - 1][j] += diffuse_a
            tmp_a[i][j + 1] += diffuse_a
        if (i == 0 and j == self.height - 1):
            tmp_a[i + 1][j] += diffuse_a
            tmp_a[i][j - 1] += diffuse_a
            tmp_a[i + 1][j - 1] += diffuse_a
        if (i == self.width - 1 and j == self.height - 1):
            tmp_a[i - 1][j] += diffuse_a
            tmp_a[i][j - 1] += diffuse_a
            tmp_a[i - 1][j - 1] += diffuse_a

        return tmp_a

    def diffuse_I(self, i, j, taux_diff, tmp_i):
        diffuse_i = self.i[i][j] * taux_diff / 8
        tmp_i[i][j] = self.i[i][j] - self.i[i][j] * taux_diff

        if (i != 0 and j != 0 and i < self.width - 1 and j < self.height - 1):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i + 1][j - 1] += diffuse_i
            tmp_i[i + 1][j + 1] += diffuse_i
            tmp_i[i - 1][j + 1] += diffuse_i
            tmp_i[i - 1][j - 1] += diffuse_i
        # Bords
        if (i == 0 and j != 0 and j < self.height - 1):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
            tmp_i[i + 1][j + 1] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i + 1][j - 1] += diffuse_i
        if (i != 0 and j == 0 and i < self.width - 1):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
            tmp_i[i + 1][j + 1] += diffuse_i
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i - 1][j + 1] += diffuse_i
        if (i == self.width - 1 and j != 0 and j < self.height - 1):
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i - 1][j + 1] += diffuse_i
            tmp_i[i - 1][j - 1] += diffuse_i
        if (j == self.height - 1 and i != 0 and i < self.width - 1):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i + 1][j - 1] += diffuse_i
            tmp_i[i - 1][j - 1] += diffuse_i
        # Coins
        if (i == 0 and j == 0):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
            tmp_i[i + 1][j + 1] += diffuse_i
        if (i == self.width - 1 and j == 0):
            tmp_i[i - 1][j + 1] += diffuse_i
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i][j + 1] += diffuse_i
        if (i == 0 and j == self.height - 1):
            tmp_i[i + 1][j] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i + 1][j - 1] += diffuse_i
        if (i == self.width - 1 and j == self.height - 1):
            tmp_i[i - 1][j] += diffuse_i
            tmp_i[i][j - 1] += diffuse_i
            tmp_i[i - 1][j - 1] += diffuse_i
        return tmp_i


    def diffuser(self):
        taux_diff = 0.1

        for k in range(self.vitesse_diff_a):
            tmp_a = self.a
            for i in range(self.width):
                for j in range(self.height):
                    tmp_a = self.diffuse_A(i, j, taux_diff, tmp_a)
            self.a = tmp_a
        for l in range(self.vitesse_diff_i):
            tmp_i = self.i
            for i in range(self.width):
                for j in range(self.height):
                    tmp_i = self.diffuse_I(i, j, taux_diff, tmp_i)
            self.i = tmp_i
        # self.a = tmp_a
        # self.i = tmp_i

    def resorber(self):
        self.a = self.a * (1 - self.taux_resorption)
        self.i = self.i * (1 - self.taux_resorption)

    def seuiller(self):
        print(self.a.mean())
        for i in range(self.height):
            for j in range(self.width):
                if (self.a.mean() < self.a[i][j]):
                    # self.result[i][j] = [1, 73, 255]  # Rouge feu
                    self.result[i][j] = [119, 2, 108] #Zinzolin
                else:
                    self.result[i][j] = [0, 215, 255]  # Or
                # self.result[i][j] = [13, 34, 227] #Rouge
                # self.result[i][j] = self.couleur2 #Rouge


    def show(self):
        # cv2.imshow("Activateur : a", self.a)
        # cv2.imshow("Inibiteur : i", self.i)
        cv2.imshow("Resultats", self.result)
        cv2.waitKey()

    def saveimg(self, filename):
        # cv2.imwrite(filename + "_A.png", self.a)
        # cv2.imwrite(filename + "_I.png", self.i)
        cv2.imwrite(filename + ".png", self.result)

test = Morphogene(0.04, 0.0002, 1, 1, 0.00028, 150, 100, 100) #Résultats sympas -> resultats_5
# test = Morphogene(0.04, 0.0002, 1, 2, 0.06, 50, 250, 250)

startG = time.time()

for i in range(25):
    print("Ité ---> " + str(i))
    start = time.time()
    test.reagir()
    test.diffuser()
    test.resorber()
    test.seuiller()
    # test.show()
    test.saveimg("Results/result" + str(i))
    print("time : " + str(time.time() - start))

print("Global time \n ************** " + str(time.time() - startG) + " **************")
pngToGif(25)
