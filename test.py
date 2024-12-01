import numpy as np

arr = np.array([1, 2, 3, 4, 5])
test_values = [2, 4, 6]

result = np.isin(arr, test_values)
print(result) 