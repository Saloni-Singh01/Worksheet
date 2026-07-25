# Python Scientific Libraries Demo
# Math | NumPy | Matplotlib | Seaborn | SciPy

import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ----------------------------------------
# Student Details
# ----------------------------------------
print("UID               : 25MCA20087")
print("Section/Group     : 25MCA-2A")
print("Date of Performance : 21-07-2026")
print("Subject Code      : 25CAP-702")
print()

# ----------------------------------------
# 1. Math Library
# ----------------------------------------
print("1. MATH LIBRARY")

number = 25

print("Square Root :", math.sqrt(number))
print("Factorial   :", math.factorial(5))
print("Power       :", math.pow(3, 4))
print("Value of Pi :", math.pi)
print("Sin(90°)    :", math.sin(math.radians(90)))

# ----------------------------------------
# 2. NumPy Library
# ----------------------------------------
print("\n2. NUMPY LIBRARY")

arr = np.array([10, 20, 30, 40, 50])

print("Array    :", arr)
print("Mean     :", np.mean(arr))
print("Sum      :", np.sum(arr))
print("Max      :", np.max(arr))
print("Min      :", np.min(arr))
print("Std Dev  :", np.std(arr))

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print("\nMatrix:")
print(matrix)

print("\nTranspose:")
print(matrix.T)

# ----------------------------------------
# 3. SciPy Library
# ----------------------------------------
print("\n3. SCIPY LIBRARY")

data = [12, 15, 14, 10, 18, 20, 15, 17, 19]

print("Mean   :", np.mean(data))
print("Median :", np.median(data))
print("Mode   :", stats.mode(data, keepdims=True))

# ----------------------------------------
# 4. Matplotlib Line Graph
# ----------------------------------------
x = np.arange(1, 11)
y = x * 2

plt.figure(figsize=(7, 4))
plt.plot(x, y, marker='o')
plt.title("Matplotlib Line Graph")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.grid(True)
plt.show()

# ----------------------------------------
# 5. Seaborn Bar Chart
# ----------------------------------------
plt.figure(figsize=(7, 4))

sns.barplot(
    x=["A", "B", "C", "D", "E"],
    y=[12, 25, 18, 30, 20]
)

plt.title("Seaborn Bar Chart")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()

# ----------------------------------------
# 6. Histogram
# ----------------------------------------
marks = [
    55, 67, 72, 80, 91,
    65, 70, 88, 76, 95,
    62, 78, 81, 69, 73,
    84, 90, 66, 79, 85
]

plt.figure(figsize=(7, 4))

sns.histplot(marks, bins=6, kde=True)

plt.title("Student Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()

print("\nProgram Executed Successfully!")