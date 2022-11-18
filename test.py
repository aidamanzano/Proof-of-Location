import numpy as np

class Car:
    #position_history = []
    def __init__(self, position: list, velocity: list):
        self.position_history = []
        self.position = np.array(position)
        self.velocity= np.array(velocity)
        self.position_history.append(np.array(self.position))

    def move(self, dt):
        self.position += self.velocity * dt
        self.position_history.append(self.position)

Mercedes = Car([1,1], [2,3])
print(Mercedes.position)
print(Mercedes.position_history)

Mercedes.move(5)
print(Mercedes.position)
print(Mercedes.position_history)

Hyundai = Car([3,5], [1,1])
print('Position Hyundai before moving', Hyundai.position)
print('Position history hyundai before moving',Hyundai.position_history)

Hyundai.move(2)
print(Hyundai.position)
print(Hyundai.position_history)

print(np.array([-5,8])*(-1))



a = np.array([4. , 5.5])
print((np.ceil(a)).astype(int))

import matplotlib.pyplot as plt

array = np.array([[[0.953, 0.938, 0.938],
[0.959, 0.951, 0.944],
[0.977, 0.976, 0.973]]])

fig, ax = plt.subplots()
ax.matshow(array, cmap='Greens')
ax.axis('off')
for (i, j), z in np.ndenumerate(array[0]):
    ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

fig = plt.gcf()
plt.show()