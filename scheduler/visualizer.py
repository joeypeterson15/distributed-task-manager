import numpy as np
import matplotlib.pyplot as plt

def visualize(grid):
    block_grid = np.block(grid)
    plt.imshow(block_grid, cmap='viridis', interpolation='nearest')
    plt.show()
