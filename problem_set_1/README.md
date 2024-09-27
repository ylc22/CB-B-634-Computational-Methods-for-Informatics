# Exercise 1: Efficiently Search Patient Data

## Objective:
Analyze patient data from an XML file to gain insights into patient demographics. Organize the data to allow efficient O(log n) searches for patients of a given age.

---

### 1a. Plot Age Distribution (3 points)

- **Age Distribution**:
  A histogram was plotted to show the distribution of ages among the patients. The plot helps visualize the spread of ages and whether any patients share the same age.

- **Evidence of Shared Ages**:
  No patients were found to share the same exact age. All ages are unique.

- **Extra Credit (2 points)**:
  Having multiple patients with the same age would complicate the binary search because you would need to account for all occurrences of that age. The solution would need to handle ranges of patients with the same age efficiently.

---

### 1b. Plot Gender Distribution (3 points)

- **Gender Distribution**:
  The dataset includes both male and female patients. A bar chart was plotted to show the distribution of genders. The categories used are "male" and "female."

---

### 1c. Sort Patients by Age (3 points)

- **Sorting Patients**:
  The patients were sorted by age using Python’s built-in `sorted()` function. The result is a list where each patient is ordered by their age.

- **Oldest Patient**:
  The oldest patient in the dataset is identified after sorting.

---

### 1d. Finding the Second Oldest Patient (4 points)

- **Method for Finding the Second Oldest in O(n) Time**:
  Iterate through the list once, keeping track of the largest and second-largest ages. This method ensures a linear-time solution, O(n), for finding the second oldest patient.

- **Advantages of Sorting vs. O(n) Solution**:
  Sorting (O(n log n)) is useful when you need to perform multiple queries on the dataset, such as finding the top k oldest patients. The O(n) solution is faster for a single query but doesn’t provide sorted data for future queries.

---

### 1e. Binary Search for Specific Age (2 points)

- **Binary Search Implementation**:
  A binary search was implemented to find the patient who is exactly 41.5 years old. The search returns the patient if found or `None` if no patient with that age exists.

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

