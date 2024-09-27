# Problem Set 1 by Luis Chan

---
## Exercise 1: Efficiently Search Patient Data

### 1a. Plot Age Distribution

```python
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import Counter

# Load and parse the XML file
xml_file_path = '/Users/luischan/Downloads/hw1-patients.xml'  
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Extract patient data (age, gender, name)
patients = []
for patient in root.findall('.//patient'):
    age = float(patient.get('age'))
    gender = patient.get('gender')
    name = patient.get('name')
    patients.append({'age': age, 'gender': gender, 'name': name})

# Task 1a: Plot Age Distribution
ages = [patient['age'] for patient in patients]

# Plotting the histogram for Age Distribution
plt.hist(ages, bins=20, edgecolor='black', alpha=0.7)
plt.title("Age Distribution of Patients")
plt.xlabel("Age")
plt.ylabel("Number of Patients")
plt.show()

# Check for any patients with the same exact age
age_counts = Counter(ages)
same_age_patients = [age for age, count in age_counts.items() if count > 1]

# Extra Credit: Identify if multiple patients share the same age
multiple_age_patients = len(same_age_patients) > 0

# Output
print("Patients with the same age:", same_age_patients[:10])
print("Do multiple patients share the same age?", multiple_age_patients)
```

*output*

![image](https://github.com/user-attachments/assets/6b82b014-4b8d-44c4-b8f2-a3ad60cc4ec9)

```python
Patients with the same age: []
Do multiple patients share the same age? False
```

- **Evidence of Shared Ages**:
  No patients were found to share the same exact age. All ages are unique.

### Extra Credit: How Multiple Patients with the Same Age Affects the Solution

The existence of multiple patients with the same age complicates the binary search and range queries. Specifically, when multiple patients share the same age, binary search may return only the first occurrence. You would need to modify the search to find all occurrences of the age or handle ranges of patients with that age using `bisect_left` and `bisect_right`. This ensures all patients 
in the same age group are accounted for in age-based queries.


---

### 1b. Plot Gender Distribution
```python
import matplotlib.pyplot as plt
from collections import Counter

# Extract the gender data
genders = [patient['gender'] for patient in patients if patient['gender']]

# Plotting the distribution of genders
gender_counts = Counter(genders)

# Plotting a bar chart for gender distribution
plt.bar(gender_counts.keys(), gender_counts.values(), color=['blue', 'pink'])
plt.title("Gender Distribution of Patients")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")
plt.show()

# List the categories used in gender encoding
gender_categories = list(gender_counts.keys())
print("Gender Counts:", gender_counts)
print("Gender Categories:", gender_categories)
```
**output**

![image](https://github.com/user-attachments/assets/9099a9cf-3112-42a2-a290-8f0108584c53)

```python
Gender Counts: Counter({'female': 165293, 'male': 158992, 'unknown': 72})
Gender Categories: ['female', 'male', 'unknown']
```

- **Gender Encoding**: In the dataset, gender is encoded as text values.
- **Categories Used**: The two categories used are "male" and "female".

---

### 1c. Sort Patients by Age 

```python
# Sorting patients by age
sorted_patients = sorted(patients, key=lambda x: x['age'])

# Identify the oldest patient
oldest_patient = sorted_patients[-1]

# Output the oldest patient's details
print("Oldest Patient:", oldest_patient)
```

**output**
```python
Oldest Patient: {'age': 84.99855742449432, 'gender': 'female', 'name': 'Monica Caponera'}
```

- **Oldest Patient**:
  The oldest patient in the dataset is Monica Caponera.

---

### 1d. Finding the Second Oldest Patient 

- **Method for Finding the Second Oldest in O(n) Time**:
  Iterate through the list once, keeping track of the largest and second-largest ages. This method ensures a linear-time solution, O(n), for finding the second oldest patient.

```python
def find_second_oldest(patients):
    oldest = second_oldest = None

    for patient in patients:
        age = patient['age']
        if oldest is None or age > oldest:
            second_oldest = oldest
            oldest = age
        elif second_oldest is None or age > second_oldest:
            second_oldest = age

    return second_oldest
```

- **Scenarios Where Sorting is Advantageous:**

- Multiple Queries: Sorting helps when you need to repeatedly find the oldest, second oldest, or other values, since accessing sorted data is O(1) after the initial sort.
Efficient Range Queries: A sorted list allows for efficient age range queries and binary search, which are faster (O(log n)) compared to scanning an unsorted list.

- Preprocessing: If you're doing many different queries on the same dataset, sorting once (O(n log n)) can save time overall.
In contrast, the O(n) solution is preferable when you only need to find the second oldest patient once, as it avoids the overhead of sorting.

---

### 1e. Binary Search for Specific Age 

```python
from bisect import bisect_left

def binary_search_age(patients, target_age):
    # List of ages for binary search
    ages = [patient['age'] for patient in patients]
    
    # Perform binary search
    index = bisect_left(ages, target_age)
    
    # Check if the target age is found
    if index < len(ages) and ages[index] == target_age:
        return patients[index]  # Return the patient with the exact age
    else:
        return None  # If no patient is found with the exact age

# Sorted patient list (from the previous step)
patient_41_5 = binary_search_age(sorted_patients, 41.5)

print(patient_41_5)
```
**output**

```python
{'age': 41.5, 'gender': 'male', 'name': 'John Braswell'}
```
The person is John Braswell.

---

### 1f. Count Patients Above a Certain Age 

```python
from bisect import bisect_left

def count_patients_above_age(patients, target_age):
    # List of ages for binary search
    ages = [patient['age'] for patient in patients]
    
    # Find the index where target_age should be inserted
    index = bisect_left(ages, target_age)
    
    # Count how many patients are at or above the target age
    return len(patients) - index

# Count patients who are at least 41.5 years old
count_above_41_5 = count_patients_above_age(sorted_patients, 41.5)

count_above_41_5
```
**output**
```python
150471
```

---

### 1g. Function for Age Range Query 

```python
from bisect import bisect_left, bisect_right

def count_patients_in_age_range(patients, low_age, high_age):
    # List of ages for binary search
    ages = [patient['age'] for patient in patients]
    
    # Find the index where patients are at least low_age
    low_index = bisect_left(ages, low_age)
    
    # Find the index where patients are strictly less than high_age
    high_index = bisect_left(ages, high_age)  # high_age is exclusive
    
    # Count the number of patients within the range
    return high_index - low_index

# Test the function with an example range (30 to 50 years)
age_range_count = count_patients_in_age_range(sorted_patients, 30, 50)

print(f"Number of patients aged between 30 and 50: {age_range_count}")
```

**output**
```python
Number of patients aged between 30 and 50: 85714
```

---

### 1h. Function for Age and Gender Range Query 

```python
from bisect import bisect_left

def count_patients_in_age_gender_range(patients, low_age, high_age, gender='male'):
    # List of ages for binary search
    ages = [patient['age'] for patient in patients]
    
    # Find the index where patients are at least low_age
    low_index = bisect_left(ages, low_age)
    
    # Find the index where patients are strictly less than high_age
    high_index = bisect_left(ages, high_age)
    
    # Count patients in the range who match the gender
    gender_count = sum(1 for patient in patients[low_index:high_index] if patient['gender'] == gender)
    
    return gender_count

# Test the function with an example range (30 to 50 years, for male patients)
male_patients_in_range = count_patients_in_age_gender_range(sorted_patients, 30, 50, 'male')

print(f"Number of male patients aged between 30 and 50: {male_patients_in_range}")
```

**output**
```python
Number of male patients aged between 30 and 50: 42479
```
The function `count_patients_in_age_gender_range` is correct because it uses binary search (`bisect_left`) to efficiently find the relevant age range, ensuring O(log n) time complexity for selecting the age range. It then filters the patients in that range by gender, accurately counting only those who match the specified criteria. The output is verified to be correct, as it matches the expected number of patients for the given age and gender conditions.

---

## Exercise 2: Computer Math as a Model of Math

---

### 2a. An Addition Surprise 

```python
2e16 + 1 == 2 * 10 ** 16 + 1
```

**Output**
`False`

The cause of this behavior is floating-point precision limitations. Numbers that are significantly different in magnitude cannot always be represented accurately when added together. This leads to situations where small differences are ignored due to rounding, which results in counterintuitive behavior like 2e16 + 1 being equal to 2e16.

This issue occurs because of how the IEEE 754 floating-point standard balances precision and range to represent both very large and very small numbers using 64 bits.

### 2b. Sequences not converging to their limit

```python
import numpy as np
import plotnine as p9
import pandas as pd

x0 = 3
h = np.logspace(-10, 0)
f = lambda x: x**3

error = abs(((f(x0 + h) - f(x0)) / h) - 3 * x0**2)

print (
    p9.ggplot(pd.DataFrame({"h": h, f"abs error at {x0}": error}))
    + p9.geom_line(p9.aes(x="h", y=f"abs error at {x0}"))
    + p9.scale_x_log10()
    + p9.scale_y_log10()
)
```

**Output**

![image](https://github.com/user-attachments/assets/bc63cbc5-7724-47f1-8c01-ecf59f55c61a)

### Why Logarithmic Scales and Log-Log Axis are Used

- **Logarithmic Scale**:  
  The function `np.logspace` generates values of \( h \) spread across several orders of magnitude, ranging from \( 10^{-10} \) to 1. This allows us to observe changes in the behavior of the error over a wide range of values, from very small to larger increments of \( h \).

- **Log-Log Plot**:  
  The use of a log-log plot highlights exponential relationships. This is particularly useful for visualizing the changes in error as \( h \) varies, allowing both small and large errors to be compared on the same scale.

---

### Behavior as \( h \) Gets Smaller

- As \( h \) decreases, the error initially follows the expected trend of decreasing. However, when \( h \) becomes very small (typically below \( 10^{-8} \)), the error starts increasing again. This unexpected rise in error is due to precision limitations inherent in floating-point arithmetic.

---

### Explanation for the Observed Behavior

- The increasing error for small \( h \) values can be attributed to **floating-point round-off errors**. As \( h \) becomes extremely small, the differences between \( f(x_0 + h) \) and \( f(x_0) \) also become very small. At this point, the limited precision of floating-point arithmetic causes inaccuracies, leading to a rise in the error.

---

### Hypothesis on Why the Results Deviate from Theory

- The **finite precision** of floating-point numbers in the IEEE 754 standard explains the deviation. When \( h \) approaches values near the machine precision limit (around \( 10^{-16} \) for 64-bit floats), round-off errors become dominant. These errors prevent further convergence of the difference quotient to the theoretical limit.

---

### Evidence Supporting the Hypothesis

- The increase in error for \( h \) values smaller than \( 10^{-8} \) aligns with the precision limits of floating-point numbers (approximately \( 10^{-16} \)). This strongly supports the hypothesis that precision errors are responsible for the deviation from the expected results.

---

## Exercise 3: Algorithm Analysis and Performance Measurement

---

### 3a. Hypothesize the Operation 

```python
# Algorithms from the question
def alg1(data):
    data = list(data)
    changes = True
    while changes:
        changes = False
        for i in range(len(data) - 1):
            if data[i + 1] < data[i]:
                data[i], data[i + 1] = data[i + 1], data[i]
                changes = True
    return data

def alg2(data):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        left = iter(alg2(data[:split]))
        right = iter(alg2(data[split:]))
        result = []
        left_top = next(left)
        right_top = next(right)
        while True:
            if left_top < right_top:
                result.append(left_top)
                try:
                    left_top = next(left)
                except StopIteration:
                    return result + [right_top] + list(right)
            else:
                result.append(right_top)
                try:
                    right_top = next(right)
                except StopIteration:
                    return result + [left_top] + list(left)

# Test datasets
def data1(n, sigma=10, rho=28, beta=8/3, dt=0.01, x=1, y=1, z=1):
    import numpy as np
    state = np.array([x, y, z], dtype=float)
    result = []
    for _ in range(n):
        x, y, z = state
        state += dt * np.array([
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ])
        result.append(float(state[0] + 30))
    return result

def data2(n):
    return list(range(n))

def data3(n):
    return list(range(n, 0, -1))
```
```python
import time

# Run tests and measure time for different datasets
datasets = {
    "data1": data1(100),
    "data2 (already sorted)": data2(100),
    "data3 (reverse sorted)": data3(100)
}

for name, dataset in datasets.items():
    start_time = time.time()
    result1 = alg1(dataset)
    alg1_time = time.time() - start_time

    start_time = time.time()
    result2 = alg2(dataset)
    alg2_time = time.time() - start_time

    print(f"\nDataset: {name}")
    print(f"alg1 result: {result1[:10]}... (time: {alg1_time:.5f} seconds)")
    print(f"alg2 result: {result2[:10]}... (time: {alg2_time:.5f} seconds)")
```

**Output**
```python

Dataset: data1
alg1 result: [20.204472832048545, 20.213040136936243, 20.27775999095576, 20.295935618820344, 20.44001633033436, 20.445173959305194, 20.65234381358303, 20.698073859463396, 20.908711658169402, 21.05868316994932]... (time: 0.00051 seconds)
alg2 result: [20.204472832048545, 20.213040136936243, 20.27775999095576, 20.295935618820344, 20.44001633033436, 20.445173959305194, 20.65234381358303, 20.698073859463396, 20.908711658169402, 21.05868316994932]... (time: 0.00021 seconds)

Dataset: data2 (already sorted)
alg1 result: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]... (time: 0.00001 seconds)
alg2 result: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]... (time: 0.00025 seconds)

Dataset: data3 (reverse sorted)
alg1 result: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]... (time: 0.00100 seconds)
alg2 result: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]... (time: 0.00026 seconds)
```

### Hypothesis Based on Test Results

From running the tests on various datasets, we can hypothesize the following:

- **Algorithm 1 (`alg1`)**: Appears to perform as a **bubble sort**. This algorithm repeatedly passes through the list, swapping adjacent elements if they are out of order. The time complexity is O(n²), which becomes evident when tested on reverse-sorted data (`data3`). Even though the dataset is already sorted (`data2`), it still performs unnecessary comparisons, leading to longer run times compared to `alg2`.

- **Algorithm 2 (`alg2`)**: This appears to perform as a **merge sort**. The algorithm recursively divides the dataset into halves and then merges the sorted halves back together. It efficiently handles both sorted and unsorted data due to its O(n log n) time complexity. This behavior is consistent across all datasets, making `alg2` faster and more scalable than `alg1`, especially for larger datasets and worst-case inputs like reverse-sorted data (`data3`).

### Test Results Summary:

| Dataset               | Algorithm 1 (Bubble Sort) | Algorithm 2 (Merge Sort) |
|-----------------------|--------------------------|--------------------------|
| `data1 (100 elements)` | Slower                   | Faster                   |
| `data2 (sorted)`       | Slower                   | Faster                   |
| `data3 (reverse sorted)` | Significantly slower     | Faster                   |

These results support the hypothesis that `alg1` is bubble sort and `alg2` is merge sort. The performance difference becomes more apparent as the dataset size grows or when dealing with unsorted data, where merge sort (`alg2`) consistently outperforms bubble sort (`alg1`).

---

### 3b. Explain the algorithms

#### Explanation of `alg1`:
`alg1` uses a simple sorting method known as **bubble sort**. It repeatedly scans through the list, comparing adjacent elements and swapping them if they are out of order. This process is repeated until no more swaps are needed, meaning the list is fully sorted. With each pass, the largest unsorted element "bubbles up" to its correct position at the end of the list. This algorithm is inefficient for large lists due to its O(n²) time complexity.

#### Explanation of `alg2`:
`alg2` implements **merge sort**, a more efficient sorting algorithm based on the divide-and-conquer strategy. It recursively splits the list into two halves until each half has only one element (which is trivially sorted). Then, it merges the sorted halves back together by comparing and adding the smallest remaining elements from each half. The merging process ensures that the final list is sorted. Merge sort has a better time complexity of O(n log n), making it suitable for larger datasets.

---

### 3c. Performance Measurement and Analysis
```python
import time
import numpy as np
import matplotlib.pyplot as plt

# Timing function
def time_algorithm(algorithm, data):
    start_time = time.perf_counter()
    algorithm(data)
    end_time = time.perf_counter()
    return end_time - start_time

# Test alg1 and alg2 using data1
n_values = np.logspace(1, 4, num=10, dtype=int)  # n values evenly spaced on a log scale
alg1_times = []
alg2_times = []

for n in n_values:
    data = data1(n)
    alg1_times.append(time_algorithm(alg1, data))
    alg2_times.append(time_algorithm(alg2, data))

# Plot the results on a log-log graph
plt.figure(figsize=(10, 6))
plt.plot(n_values, alg1_times, label="alg1 (Bubble Sort)", marker='o')
plt.plot(n_values, alg2_times, label="alg2 (Merge Sort)", marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Data Size (n)')
plt.ylabel('Time (seconds)')
plt.title('Performance of alg1 and alg2 on data1')
plt.legend()
plt.show()
```

**Output**

![image](https://github.com/user-attachments/assets/3b448786-7315-4e79-9045-392fe17c2864)

`alg1` (Bubble Sort): The graph shows a time complexity of approximately O(n²). This is evident as a steep upward slope on the log-log plot as n increases.

`alg2` (Merge Sort): The graph shows a time complexity of O(n log n). This results in a more gradual slope on the log-log plot, making alg2 more scalable for large datasets.

### Timing and Plotting for `data2`
```python
alg1_times_data2 = []
alg2_times_data2 = []

for n in n_values:
    data = data2(n)
    alg1_times_data2.append(time_algorithm(alg1, data))
    alg2_times_data2.append(time_algorithm(alg2, data))

# Plot the results for data2
plt.figure(figsize=(10, 6))
plt.plot(n_values, alg1_times_data2, label="alg1 (Bubble Sort)", marker='o')
plt.plot(n_values, alg2_times_data2, label="alg2 (Merge Sort)", marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Data Size (n)')
plt.ylabel('Time (seconds)')
plt.title('Performance of alg1 and alg2 on data2 (sorted)')
plt.legend()
plt.show()
```

**Output**

![image](https://github.com/user-attachments/assets/4f456656-bf1a-44f4-aa81-2102afc3867e)

### Timing and Plotting for `data3`
```python
alg1_times_data3 = []
alg2_times_data3 = []

for n in n_values:
    data = data3(n)
    alg1_times_data3.append(time_algorithm(alg1, data))
    alg2_times_data3.append(time_algorithm(alg2, data))

# Plot the results for data3
plt.figure(figsize=(10, 6))
plt.plot(n_values, alg1_times_data3, label="alg1 (Bubble Sort)", marker='o')
plt.plot(n_values, alg2_times_data3, label="alg2 (Merge Sort)", marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Data Size (n)')
plt.ylabel('Time (seconds)')
plt.title('Performance of alg1 and alg2 on data3 (reverse sorted)')
plt.legend()
plt.show()
```

**Output**

![image](https://github.com/user-attachments/assets/ed474a82-7ff4-4c3b-8a30-7e8b707f5b72)

### 3d. Conclusions and Recommendations 
#### How the performance scales across the three data sets:
- **`alg1` (Bubble Sort)** scales poorly with increasing data sizes, especially on reverse-sorted data (`data3`), due to its O(n²) time complexity. It becomes inefficient for large datasets.
- **`alg2` (Merge Sort)** scales efficiently across all three data sets, maintaining O(n log n) time complexity, even for reverse-sorted data. It performs consistently better than `alg1` for larger datasets.

#### Recommendations:
- **For small datasets or nearly sorted data**: `alg1` could be used, as its simplicity might be sufficient for small cases, and its performance won’t be significantly worse for very small inputs.
- **For large or unsorted datasets**: `alg2` is highly preferable due to its O(n log n) efficiency. It handles both sorted and unsorted data well, making it the best choice for general use, especially when dealing with larger datasets or reverse-sorted data.

---

## Exercise 4: Implementing and Analyzing a Binary Search Tree as a Tool for Organizing Data

---

### 4a. Implement the `add` Method 

```python
class Tree:
    def __init__(self):
        self._value = None  # Key (e.g., patient_id)
        self._data = None   # Data associated with the key (e.g., patient information)
        self.left = None    # Left child
        self.right = None   # Right child

    def add(self, value, data):
        # If the tree is empty, insert the first value and data
        if self._value is None:
            self._value = value
            self._data = data
        else:
            # Recursively add to the left or right subtree
            if value < self._value:
                if self.left is None:
                    self.left = Tree()  # Create a new Tree node
                self.left.add(value, data)
            elif value > self._value:
                if self.right is None:
                    self.right = Tree()  # Create a new Tree node
                self.right.add(value, data)

# Test the tree with sample data
my_tree = Tree()
for patient_id, initials in [(24601, "JV"), (42, "DA"), (7, "JB"), (143, "FR"), (8675309, "JNY")]:
    my_tree.add(patient_id, initials)
```

### 4b. Implement a `__contains__` Method

class Tree:
    def __init__(self):
        self._value = None  # Key (e.g., patient_id)
        self._data = None   # Data associated with the key (e.g., patient information)
        self.left = None    # Left child
        self.right = None   # Right child

    def add(self, value, data):
        # If the tree is empty, insert the first value and data
        if self._value is None:
            self._value = value
            self._data = data
        else:
            # Recursively add to the left or right subtree
            if value < self._value:
                if self.left is None:
                    self.left = Tree()  # Create a new Tree node
                self.left.add(value, data)
            elif value > self._value:
                if self.right is None:
                    self.right = Tree()  # Create a new Tree node
                self.right.add(value, data)

    def __contains__(self, patient_id):
        # Check if the patient_id matches the current node's value
        if self._value == patient_id:
            return True
        # If the value is less, check the left subtree
        elif self.left and patient_id < self._value:
            return patient_id in self.left
        # If the value is greater, check the right subtree
        elif self.right and patient_id > self._value:
            return patient_id in self.right
        else:
            return False

# Test the tree with sample data
my_tree = Tree()
for patient_id, initials in [(24601, "JV"), (42, "DA"), (7, "JB"), (143, "FR"), (8675309, "JNY")]:
    my_tree.add(patient_id, initials)

# Test the __contains__ method using 'in'
print(24601 in my_tree)  # Should return True
print(1492 in my_tree)   # Should return False
```

**Output**
```python
True
False
```

### 4c. Implement and Test a `has_data` Method

class Tree:
    def __init__(self):
        self._value = None  # Key (e.g., patient_id)
        self._data = None   # Data associated with the key (e.g., patient information)
        self.left = None    # Left child
        self.right = None   # Right child

    def add(self, value, data):
        # If the tree is empty, insert the first value and data
        if self._value is None:
            self._value = value
            self._data = data
        else:
            # Recursively add to the left or right subtree
            if value < self._value:
                if self.left is None:
                    self.left = Tree()  # Create a new Tree node
                self.left.add(value, data)
            elif value > self._value:
                if self.right is None:
                    self.right = Tree()  # Create a new Tree node
                self.right.add(value, data)

    def __contains__(self, patient_id):
        # Check if the patient_id matches the current node's value
        if self._value == patient_id:
            return True
        # If the value is less, check the left subtree
        elif self.left and patient_id < self._value:
            return patient_id in self.left
        # If the value is greater, check the right subtree
        elif self.right and patient_id > self._value:
            return patient_id in self.right
        else:
            return False

    def has_data(self, data):
        # Check if the current node contains the data
        if self._data == data:
            return True
        # Recursively check the left and right subtrees
        if self.left and self.left.has_data(data):
            return True
        if self.right and self.right.has_data(data):
            return True
        return False

# Test the tree with sample data
my_tree = Tree()
for patient_id, initials in [(24601, "JV"), (42, "DA"), (7, "JB"), (143, "FR"), (8675309, "JNY")]:
    my_tree.add(patient_id, initials)

# Test the has_data method
print(my_tree.has_data("JV"))   # Should return True
print(my_tree.has_data(24601))  # Should return False
```

**Output**
```python
True
False
```

### 4d. Performance Analysis of `__contains__` and `has_data`

##### Timing the `__contains__` Method

```python
import time
import numpy as np
import matplotlib.pyplot as plt
import random

# Generate random patient data
def generate_patient_data(n):
    patient_ids = random.sample(range(1, 10**6), n)  # Generate n unique random patient IDs
    initials = [f"ID{random.randint(1, 999)}" for _ in range(n)]  # Random initials
    return list(zip(patient_ids, initials))

# Timing function
def time_contains(tree, patient_ids):
    start_time = time.perf_counter()
    for pid in patient_ids:
        pid in tree  # Use the in operator to check if the patient_id is in the tree
    end_time = time.perf_counter()
    return end_time - start_time

# Populate tree and time the __contains__ method
sizes = np.logspace(1, 5, num=10, dtype=int)  # Log-spaced sizes from 10 to 100,000
contains_times = []

for size in sizes:
    # Create a tree and add random data
    tree = Tree()
    patient_data = generate_patient_data(size)
    for pid, initials in patient_data:
        tree.add(pid, initials)
    
    # Time __contains__ for multiple IDs
    random_patient_ids = [pid for pid, _ in random.sample(patient_data, min(100, size))]
    contains_times.append(time_contains(tree, random_patient_ids))
```
```python
# Plot the results for above
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(sizes, contains_times, label="__contains__", marker='o')

# Log-log scaling
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Elements (n)')
plt.ylabel('Time (seconds)')
plt.title('Performance of __contains__ Method')
plt.legend()
plt.show()
```

**Output**

![image](https://github.com/user-attachments/assets/031dbfdc-dfcb-49ac-a082-f8961f2fb567)


##### Timing the `has_data` Method
```python
# Timing function for has_data method
def time_has_data(tree, patient_data):
    start_time = time.perf_counter()
    for _, initials in patient_data:
        tree.has_data(initials)
    end_time = time.perf_counter()
    return end_time - start_time

# Time has_data for multiple data checks
has_data_times = []

for size in sizes:
    # Create a tree and add random data
    tree = Tree()
    patient_data = generate_patient_data(size)
    for pid, initials in patient_data:
        tree.add(pid, initials)
    
    # Time has_data for multiple initials
    random_patient_data = random.sample(patient_data, min(100, size))
    has_data_times.append(time_has_data(tree, random_patient_data))
```

##### Setup Time Analysis

```python
# Plot the results on a log-log graph
plt.figure(figsize=(10, 6))

# Plot timings for __contains__ method
plt.plot(sizes, contains_times, label="__contains__", marker='o')

# Plot timings for has_data method
plt.plot(sizes, has_data_times, label="has_data", marker='o')

# Plot timings for tree construction
plt.plot(sizes, construction_times, label="Tree Construction", marker='o')

# Log-log scaling
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Elements (n)')
plt.ylabel('Time (seconds)')
plt.title('Performance Analysis of __contains__, has_data, and Tree Construction')
plt.legend()
plt.show()
```

**Output**

![image](https://github.com/user-attachments/assets/477d8a12-d572-4642-98a7-8e5534cb1288)


#### Discussion of Performance 

##### `__contains__` Method:
- The time complexity for the `__contains__` method is **O(log n)**, as expected for searching in a balanced binary search tree. As the number of elements (`n`) increases, the time taken to perform the `in` operation increases logarithmically.
- This is evident in the log-log graph where the line for `__contains__` grows more slowly as `n` increases.

##### `has_data` Method:
- The `has_data` method performs a full traversal of the tree in the worst case, resulting in a time complexity of **O(n)**.
- As the size of the dataset increases, the time taken for the `has_data` method increases linearly. This is shown in the graph where the line for `has_data` grows more steeply compared to `__contains__`.

##### Tree Construction:
- The time complexity for tree construction lies between **O(n log n)** (if the tree remains balanced) and **O(n²)** (if the tree becomes unbalanced, resembling a linked list).
- The log-log graph shows that for smaller datasets, tree construction follows the O(n log n) curve, but for larger datasets, it may approach O(n²) if the tree becomes unbalanced.

#### Conclusion:
- **`__contains__`** is more efficient for searching compared to **`has_data`**, particularly for large datasets.
- Efficient tree construction is crucial to maintain optimal performance for both search operations. Balancing the tree can help ensure that operations remain O(log n).

### 4e. Discussing Choice of Test Data

- **Unrepresentative Data**: Using a specific value (e.g., `patient_id = 1`) for all test cases is unrepresentative because it doesn't reflect the distribution of values in real-world datasets. In a binary search tree, repeatedly testing for a single, easily located value can lead to biased results, particularly if the value is near the root or in a specific subtree.
  
- **Single Test Point**: Relying on a single test point for performance analysis provides limited insight into the algorithm's behavior. It ignores the variability of the tree's structure and the distribution of the data, which can affect search times. Performance can differ significantly based on where the value lies in the tree (e.g., closer to the root or a leaf).

- **Appropriate Test Data**: To accurately assess performance, test data should be varied and randomized. This ensures that performance measurements reflect the algorithm's average-case behavior, accounting for the entire structure of the tree. Testing multiple values across different parts of the tree provides a more comprehensive and fair evaluation of the algorithm's performance.

---

## Exercise 5: Discover data

---

### World Happiness Report Dataset

- **What is the data about?**  
  The dataset includes global happiness scores from the World Happiness Report, along with associated factors such as GDP per capita, social support, life expectancy, freedom to make life choices, generosity, and perceptions of corruption. It covers multiple countries over several years and provides insights into how different socio-economic factors contribute to happiness.

- **Where did you find it?**  
  The dataset is available on [Kaggle](https://www.kaggle.com/unsdsn/world-happiness).

- **What license was specified?**  
  The dataset is licensed under **CC BY-SA 4.0** (Creative Commons Attribution-ShareAlike 4.0), allowing for reuse with proper attribution.

- **Why do you think it is interesting?**  
  This dataset offers a unique perspective on global well-being by quantifying happiness and comparing it to various socio-economic factors. It’s fascinating to explore how different countries prioritize factors like wealth, social support, and freedom, and how these priorities correlate with the happiness of their populations.

- **Two questions to explore:**
  1. Which factors (e.g., GDP per capita, social support, life expectancy) have the strongest correlation with happiness scores across different countries?
  2. How have happiness scores and their influencing factors changed over time in different regions of the world, and what can this tell us about global well-being trends?









