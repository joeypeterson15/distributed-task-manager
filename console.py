import numpy as np

# m = np.array([[i for i in range(3)] for _ in range(3)])
# n = np.array([[i for i in range(3)] for _ in range(3)])
# col = n[:, 0:1]
# m = np.hstack((m, col))
# print(m)
# col = n[1, 0:1]
# print(col)
# col = n[2, 1:2]
# print(col)


n =np.array([[0 for _ in range(3)] for _ in range(3)])
print('n', n)
m = (n[1:2,:])
print('m', m)
n = np.vstack((m, n))
# n = np.transpose(n)
print(n)

# def collect_regions(rows, cols):
#     res = []
#     seen = [False for _ in range(rows)]
#     def permute(curr):
#         if len(curr) == 2:
#             res.append(curr.copy())
#             return
        
#         for i in range(rows):
#             # if not seen[i]:
#             #     seen[i] = True
#             #     curr.append(i)
#             #     permute(curr)
#             #     curr.pop()
#             #     seen[i] = False
#             curr.append(i)
#             permute(curr)
#             curr.pop()``
#     permute([])
#     return res

# print(collect_regions(3, 3))

# def collect_regions(n_cols, n_rows):
#     return [[m,n] for n in range(n_cols) for m in range(n_rows)]

# print(collect_regions(3, 3))

print(10 // 1)