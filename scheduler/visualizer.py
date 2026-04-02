import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# def stitch(epoch):
#     r_rows, r_cols, c_rows, c_cols = epoch.shape
#     return epoch.swapaxes(1, 2).reshape(r_rows * c_rows, r_cols * c_cols)

def visualize(grid):
    reshaped_grid = []
    for i,epoch in enumerate(grid):
#         epoch = epoch.transpose(0, 1, 2, 3)  # actually no-op, just clarity
#         epoch = epoch.reshape(
#             epoch.shape[0] * epoch.shape[2],
#             epoch.shape[1] * epoch.shape[3]
# )
        # if i == 0:
            # print('EPOCH 0 in visualizer: ', epoch)
        epoch = np.transpose(epoch, (0, 2, 1, 3))
        # if i == 0:
            # print('EPOCH 0 in visualizer transposed: ', epoch)
        reshaped_grid.append(np.reshape(epoch, (20,20)))
        # if i == 0:
            # print('EPOCH 0 in visualizer transposed and reshaped: ', reshaped_grid[i])
    
    fig, ax = plt.subplots()
    im = ax.imshow(reshaped_grid[0], cmap='cool', interpolation='nearest')


    def update(frame):
        im.set_data(reshaped_grid[frame])

        return im

    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, len(grid), 1),
                                interval=250)

    plt.show()
 