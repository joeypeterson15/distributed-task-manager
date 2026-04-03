import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# def stitch(epoch):
#     r_rows, r_cols, c_rows, c_cols = epoch.shape
#     return epoch.swapaxes(1, 2).reshape(r_rows * c_rows, r_cols * c_cols)

def visualize(grid):
    # reshaped_grid = []
    # for i,epoch in enumerate(grid):
    reshaped_grid = []
    for epoch in grid:
        # epoch is (2, 2, 10, 10) = (tiles_row, tiles_col, tile_h, tile_w)
        stitched = np.block([
            [epoch[0, 0], epoch[0, 1]],
            [epoch[1, 0], epoch[1, 1]]
        ])
        reshaped_grid.append(stitched)  # (20, 20)
    
    fig, ax = plt.subplots()
    im = ax.imshow(reshaped_grid[0], cmap='cool', interpolation='nearest')


    def update(frame):
        im.set_data(reshaped_grid[frame])

        return im

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, len(grid), 1),
                                interval=250)

    plt.show()
 