import matplotlib.pyplot as plt
import numpy as np
from src.tutils import BaseStateSystem
import time
import random
import cv2

def laplacian2D(a, dx):
    return (
        - 4 * a
        + np.roll(a,1,axis=0)
        + np.roll(a,-1,axis=0)
        + np.roll(a,+1,axis=1)
        + np.roll(a,-1,axis=1)
    ) / (dx ** 2)


def random_initialiser(shape):
    return(
        np.random.normal(loc=0, scale=0.05, size=shape),
        np.random.normal(loc=0, scale=0.05, size=shape)
    )


class TwoDimensionalRDEquations(BaseStateSystem):
    def __init__(self, Da, Db, Ra, Rb,
                 initialiser=random_initialiser,
                 width=1000, height=1000,
                 dx=1, dt=0.1, steps=1):
        self.Da = Da #Vitesse diffusion
        self.Db = Db
        self.Ra = Ra #Taux de reaction
        self.Rb = Rb

        self.initialiser = initialiser
        self.width = width
        self.height = height
        self.shape = (width, height)
        self.dx = dx # Activateur
        self.dt = dt # Inhibiteur
        self.steps = steps

    def initialise(self):
        self.t = 0
        self.a, self.b = self.initialiser(self.shape)

    def update(self):
        for _ in range(self.steps):
            self.t += self.dt
            self._update()

    def _update(self):
        # unpack so we don't have to keep writing "self"
        a, b, Da, Db, Ra, Rb, dt, dx = (
            self.a, self.b, #Ptetre resorption diffusion
            self.Da, self.Db,
            self.Ra, self.Rb,
            self.dt, self.dx
        )

        La = laplacian2D(a, dx)
        Lb = laplacian2D(b, dx)

        delta_a = dt * (Da * La + Ra(a, b))
        delta_b = dt * (Db * Lb + Rb(a, b))

        self.a += delta_a
        self.b += delta_b

    def draw(self, ax):
        ax[0].clear()
        ax[1].clear()

        ax[0].imshow(self.a, cmap='jet')
        ax[1].imshow(self.b, cmap='jet')

        ax[0].grid(b=False)
        ax[1].grid(b=False)

        ax[0].set_title("A, t = {:.2f}".format(self.t))
        ax[1].set_title("B, t = {:.2f}".format(self.t))

    def initialise_figure(self):
        fig, ax = plt.subplots(nrows=1, ncols=2)
        return fig, ax


Da, Db, alpha, beta = 1, 100, -0.005, 10


def Ra(a, b): return a - a ** 3 - b + alpha


def Rb(a, b): return (a - b) * beta


width = 500
dx = 1
dt = 0.001

start = time.time()
TwoDimensionalRDEquations(
    Da, Db, Ra, Rb,
    width=width, height=width,
    dx=dx, dt=dt, steps=20
).plot_time_evolution("2dRD.png", n_steps=150)

print(time.time() -start)