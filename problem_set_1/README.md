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

### 1f. Count Patients Above a Certain Age (2 points)

- **Counting Patients Above 41.5**:
  Using arithmetic and the result of the binary search, the number of patients who are at least 41.5 years old was determined. This can be computed directly from the position returned by the binary search.

---

### 1g. Function for Age Range Query (4 points)

- **Efficient Age Range Query**:
  A function was written to return the number of patients who are at least `low_age` years old but strictly less than `high_age` years old in O(log n) time after initial sorting.

---

### 1h. Function for Age and Gender Range Query (4 points)

- **Age and Gender Query**:
  The previous function was modified to return the number of male patients in the specified age range, all in O(log n) time after initial data setup. This allows for efficient filtering by both age and gender.

