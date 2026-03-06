import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def visualize(grid):
    reshaped_grid = []
    for epoch in grid:
        epoch = np.transpose(epoch, (0, 2, 1, 3))
        reshaped_grid.append(np.reshape(epoch, (50,50)))
    # print('reshaped grid', reshaped_grid)
    
    fig, ax = plt.subplots()
    im = ax.imshow(reshaped_grid[0], cmap='cool', interpolation='nearest')

    def update(frame):
        im.set_data(reshaped_grid[frame])

        return im

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, len(grid), 1),
                                interval=750)

    plt.show()
 