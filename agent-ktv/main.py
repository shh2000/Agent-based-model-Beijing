import imageio
import random

frames = []
for i in range(192):
    fname = 'pics/' + str(i) + '.jpg'
    frames.append(imageio.imread(fname))
imageio.mimsave('pics/baseline.0.1.gif', frames, 'GIF', duration=0.1)
