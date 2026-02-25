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
#             curr.pop()
#     permute([])
#     return res

# print(collect_regions(3, 3))

def collect_regions(n_cols, n_rows):
    return [[m,n] for n in range(n_cols) for m in range(n_rows)]

print(collect_regions(3, 3))
