import numpy as np
import cv2
from pathlib import Path
import imageio
import time
import random

def pngToGif(lenght):
    image_path = Path(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results')
    images = []
    for i in range(lenght):
        images.append(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results\result' + str(i) + '.png')

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
        self.couleur1 = [random.randint(0,256), random.randint(0,256), random.randint(0,256)]
        self.couleur2 = [random.randint(0,256), random.randint(0,256), random.randint(0,256)]

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
        mean = self.a.mean()
        # print(mean)
        for i in range(self.height):
            for j in range(self.width):
                # if (self.seuil_activation < self.a[i][j]):
                if (mean < self.a[i][j]):
                    # self.result[i][j] = [119, 2, 108] #Zinzolin
                    self.result[i][j] = self.couleur1
                    # self.result[i][j] = [255, 255, 255]
                else:
                    # self.result[i][j] = [13, 34, 227] #Rouge
                    # self.result[i][j] = [96, 203, 255] #Aurore
                    self.result[i][j] = self.couleur2
                    # self.result[i][j] = [0, 0, 0] # Noir


    def show(self):
        # cv2.imshow("Activateur : a", self.a)
        # cv2.imshow("Inibiteur : i", self.i)
        cv2.imshow("Resultats", self.result)
        cv2.waitKey()

    def saveimg(self, filename):
        print(filename + '.png')
        cv2.imwrite(filename + ".png", self.result)

def run(taux_rection_A, taux_reaction_I, vitesse_diff_A, vitesse_diff_I, taux_resorption, seuil_activation, img, nbIte, folderName):
    test = Morphogene(taux_rection_A, taux_reaction_I, vitesse_diff_A, vitesse_diff_I, taux_resorption, seuil_activation, img[0], img[1])  # Résultats sympas -> resultats_4
    # test = Morphogene(0.04, 0.0002, 1, 1, 0.06, 122, 500, 500)  # Résultats sympas -> resultats_4
    # test = Morphogene(0.04, 0.0002, 4, 25, 0.06, 250, 150, 150) #Résultats sympas -> resultats_3
    # test = Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 150, 150) #Résultats sympas -> resultats_2
    # test = Morphogene(0.04, 0.0002, 1, 6, 0.1, 50, 150, 150) #Résultats sympas -> resultats_1

    startG = time.time()

    for i in range(nbIte):
        print("Ité ---> " + str(i))
        start = time.time()
        test.reagir()
        test.diffuser()
        test.resorber()
        test.seuiller()
        # print("Results/" + folderName + "/result" + str(i))
        test.saveimg("Results/" + folderName + "/result" + str(i))
        # print("time : " + str(time.time() - start))

    print("Global time \n ************** " + str(time.time() - startG) + " **************")
    pngToGif(nbIte, folderName)

def evolve_pngToGif(choix):
    image_path = Path(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results')
    images = []
    for i in range(len(choix)):
        if(i == 0):
            images.append(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results\it1_img'
                          + str(choix[i]) + '.png')
        if (i == 1):
            images.append(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results\it2_img'
                          + str(choix[i]) + '.png')
        if (i == 2):
            images.append(r'D:\Cours\S10\Informatique bio-inspirée\TP\morphogenese\morphogenese\Results\it3_img'
                          + str(choix[i]) + '.png')

    image_list = []
    for file_name in images:
        image_list.append(imageio.imread(file_name))

    imageio.mimwrite('Results/results.gif', image_list)


def evolve():
    historiqueChoix = []
    morphs = []
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))
    morphs.append(Morphogene(0.04, 0.0002, 4, 25, 0.06, 50, 100, 100))

    # Itération 1
    for i in range(len(morphs)):
        print(i)
        morphs[i].reagir()
        morphs[i].diffuser()
        morphs[i].resorber()
        morphs[i].seuiller()
        morphs[i].saveimg("Results/it1_img" + str(i + 1))

    print(" Première itération : Tu préfères lequel ?")
    morphoChoix = input()
    choix = int(morphoChoix) - 1
    historiqueChoix.append(choix + 1)

    for i in range(len(morphs)):
        if (i != choix):
            morphs[i].a = morphs[choix].a
            morphs[i].i = morphs[choix].i
            morphs[i].couleur1 = morphs[choix].couleur1
            morphs[i].couleur2 = morphs[choix].couleur2
            morphs[i].result = morphs[choix].result

    # Itération 2
    for i in range(len(morphs)):
        print(i)
        morphs[i].reagir()
        morphs[i].diffuser()
        morphs[i].resorber()
        morphs[i].seuiller()
        morphs[i].saveimg("Results/it2_img" + str(i+1))

    print(" Deuxième itération : Tu préfères lequel ?")
    morphoChoix = input()
    choix = int(morphoChoix) - 1
    historiqueChoix.append(choix + 1)

    for i in range(len(morphs)):
        if (i != choix):
            morphs[i].a = morphs[choix].a
            morphs[i].i = morphs[choix].i
            morphs[i].couleur1 = morphs[choix].couleur1
            morphs[i].couleur2 = morphs[choix].couleur2
            morphs[i].result = morphs[choix].result


    # Itération 3
    for i in range(len(morphs)):
        print(i)
        morphs[i].reagir()
        morphs[i].diffuser()
        morphs[i].resorber()
        morphs[i].seuiller()
        morphs[i].saveimg("Results/it3_img" + str(i+1))

    print(" Deuxième itération : Tu préfères lequel ?")
    morphoChoix = input()
    choix = int(morphoChoix) - 1
    historiqueChoix.append(choix + 1)

    for i in range(len(morphs)):
        if (i != choix):
            morphs[i].a = morphs[choix].a
            morphs[i].i = morphs[choix].i
            morphs[i].couleur1 = morphs[choix].couleur1
            morphs[i].couleur2 = morphs[choix].couleur2
            morphs[i].result = morphs[choix].result

    evolve_pngToGif(historiqueChoix)


evolve()