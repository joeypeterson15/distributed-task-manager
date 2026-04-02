import numpy as np
import json
import time


rng = np.random.default_rng()
# matrix = rng.random(size=(20,4,4))
# np.save('matrix.npy', matrix)
# np.savetxt('matrix.csv', matrix, delimiter=',')

mock_data = np.load('epochs.npy')
actual_data = np.load('real_epochs.npy')

actual_data = np.squeeze(actual_data)

assert actual_data.shape == mock_data.shape

print(actual_data[0][0][0])
print(mock_data[0][0][0])

epochs = 20
for epoch in range(epochs):
    print(epoch, ': ', mock_data[epoch] == actual_data[epoch])