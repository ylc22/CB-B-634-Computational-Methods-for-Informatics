# Clinical Decision Support and Data Analysis Projects

This project contains the implementation of four exercises focused on clinical decision support, analyzing COVID-19 case data, population data, and privacy-preserving estimation techniques.

## Exercise 1: Clinical Decision Support - Temperature Tester 

### 1a. Function Implementation
The `temp_tester` function creates a temperature checker for different species or contexts. It takes a normal temperature and returns a function that tests whether a given temperature is within 1 degree of that normal.

```python
def temp_tester(normal_temp):
    def tester(temp):
        return abs(temp - normal_temp) <= 1
    return tester
```


### 1b. Ambiguity in Problem Description
One ambiguity is the temperature scale. The problem does not explicitly state whether to use Celsius or Fahrenheit, which could lead to different results if interpreted differently.

### 1c. Testing

```python
# Create temperature testers
human_tester = temp_tester(37)
chicken_tester = temp_tester(41.1)

# Test cases
print(chicken_tester(42))  
print(human_tester(42))    
print(chicken_tester(43)) 
print(human_tester(35))    
print(human_tester(98.6)) 
```

Two temperature testers were defined: human_tester = temp_tester(37) and chicken_tester = temp_tester(41.1). Here are the test results:

chicken_tester(42) returns True
human_tester(42) returns False
chicken_tester(43) returns False
human_tester(35) returns False
human_tester(98.6) returns False (since it's in Fahrenheit)

## Exercise 2: Analyzing COVID-19 Case Data

### 2a. Data Acquisition and Loading

The COVID-19 data was loaded from The New York Times GitHub repository. Here's the code used to load the data:

```python
import pandas as pd

# URL for the CSV file
url = 'https://github.com/nytimes/covid-19-data/raw/master/us-states.csv'

# Load the CSV directly from the URL
data = pd.read_csv(url)

# Convert the 'date' column to datetime format for easier manipulation
data['date'] = pd.to_datetime(data['date'])

# Sort the data by state and date
data = data.sort_values(['state', 'date'])

# Calculate new daily cases by subtracting the previous day's cumulative cases within each state
data['new_cases'] = data.groupby('state')['cases'].diff().fillna(0)
```

### 2b. Visualization of New Cases

```python
import matplotlib.pyplot as plt

def plot_new_cases(states):
  
    plt.figure(figsize=(9, 6))
    
    # Plot the new cases for each state
    for state in states:
        state_data = data[data['state'] == state]
        plt.plot(state_data['date'], state_data['new_cases'], label=state)
    
    # Labeling the plot
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.title('New COVID-19 Cases by State')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Example usage:
plot_new_cases(['Arizona','Connecticut','New York','New Mexico'])
```
![image](https://github.com/user-attachments/assets/eed76ca6-39d6-4dfc-b3b2-bb20c9bcd8f4)

### 2c. Find Peak Case Dates

```python
def find_peak_case_date(state):
    
    # Filter data for the specified state
    state_data = data[data['state'] == state]
    
    # Find the date with the highest number of new cases
    peak_day = state_data.loc[state_data['new_cases'].idxmax()]
    
    return peak_day['date'], int(peak_day['new_cases'])

# Example usage:
find_peak_case_date('Illinois')
```
#### output
```python
(Timestamp('2022-01-18 00:00:00'), 93423)
```
The peak number of new COVID-19 cases in Illinois occurred on January 18, 2022, with a total of 93423 new cases reported on that day.

### 2d. Compare peak cases

```python
def compare_peak_cases(state1, state2):
    
    # Get the peak dates for both states
    peak_date1, _ = find_peak_case_date(state1)
    peak_date2, _ = find_peak_case_date(state2)
    
    # Compare the peak dates and calculate the difference in days
    if peak_date1 < peak_date2:
        first_peak_state = state1
        days_between = (peak_date2 - peak_date1).days
    else:
        first_peak_state = state2
        days_between = (peak_date1 - peak_date2).days
    
    return f"{first_peak_state} peaked first, with a difference of {days_between} days between peaks."

# Example usage:
compare_peak_cases('Missouri', 'Alabama')
```

#### output
```python
'Missouri peaked first, with a difference of 327 days between peaks.'
```
The comparison shows that Missouri peaked first, with a difference of 327 days between its peak and Alabama's peak.


### 2e. Examine individual states
```python
# Plot the new cases in Florida
plot_new_cases(['Florida'])
```
![image](https://github.com/user-attachments/assets/5ef60218-4892-4c5c-8399-51d96670f0dc)

The plot for Florida shows some large spikes in new COVID-19 cases, particularly during major waves of the pandemic. These spikes may correspond to the nationwide surges in cases caused by variants like Delta and Omicron. My reason is that as a major tourist destination, Florida may have experienced waves of infections linked to large gatherings or travel.

## Exercise 3: Analyzing Population Data

### 3a. Load and Examine Data 
```python
import pandas as pd
import sqlite3

# Load the SQLite database file into a pandas DataFrame
with sqlite3.connect("/Users/luischan/Downloads/hw0-population.db") as db:
    data = pd.read_sql_query("SELECT * FROM population", db)

# Print the columns and the number of rows
print("Columns present in the dataset:", data.columns.tolist())
print("Number of rows (individuals) in the dataset:", len(data))
```
#### output
```python
Columns present in the dataset: ['name', 'age', 'weight', 'eyecolor']
Number of rows (individuals) in the dataset: 152361
```
So there are 4 columns and 152361 rows in the dataset.

### 3b. Analyze Age Distribution

```python
# Compute statistics for the age column
age_mean = data['age'].mean()
age_std = data['age'].std()
age_min = data['age'].min()
age_max = data['age'].max()

print(f"Age - Mean: {age_mean}, Std Dev: {age_std}, Min: {age_min}, Max: {age_max}")

# Plot a histogram of the age distribution
import matplotlib.pyplot as plt

plt.figure(figsize=(7, 4))
plt.hist(data['age'], bins=30, color='yellow', edgecolor='black')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
```
#### output
```python
Age - Mean: 39.51052792739697, Std Dev: 24.152760068601573, Min: 0.0007476719217636152, Max: 99.99154733076972
```
![image](https://github.com/user-attachments/assets/1699022a-9b71-47ad-97d7-e9c14c15c964)

### 3c. Analyze Weight Distribution

```python
# Compute statistics for the weight column
weight_mean = data['weight'].mean()
weight_std = data['weight'].std()
weight_min = data['weight'].min()
weight_max = data['weight'].max()

print(f"Weight - Mean: {weight_mean}, Std Dev: {weight_std}, Min: {weight_min}, Max: {weight_max}")

# Plot a histogram of the weight distribution
plt.figure(figsize=(7, 4))
plt.hist(data['weight'], bins=30, color='green', edgecolor='black')
plt.title('Weight Distribution')
plt.xlabel('Weight (kg)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
```
#### output
```python
Weight - Mean: 60.884134159929715, Std Dev: 18.41182426565962, Min: 3.3820836824389326, Max: 100.43579300336947
```
![image](https://github.com/user-attachments/assets/01949708-8994-4b93-a3e9-679d418d770c)

### 3d. Explore Relationships

```python
# Scatter plot of weight vs age
plt.figure(figsize=(10, 6))
plt.scatter(data['age'], data['weight'], alpha=0.5, color='red')
plt.title('Scatterplot of Weight vs Age')
plt.xlabel('Age')
plt.ylabel('Weight (kg)')
plt.grid(True)
plt.show()

# Outlier detection using z-scores for weight
from scipy.stats import zscore
data['weight_zscore'] = zscore(data['weight'])

# Identify outliers (z-score greater than 3 or less than -3)
outliers = data[(data['weight_zscore'] > 3) | (data['weight_zscore'] < -3)]
print("Outliers in the dataset:")
print(outliers[['name', 'age', 'weight']])
```
#### output
```python
Outliers in the dataset:
                    name       age    weight
311        Edna Williams  0.092462  4.366853
643           Ken Graser  0.014489  4.028084
654      Kenneth Shevlin  0.014581  4.554047
685     Harold Davenport  0.155084  4.642049
930      Michael Calhoun  0.147751  4.356373
...                  ...       ...       ...
151720      Velvet Dever  0.419900  3.981101
151788         Ray Budde  0.566617  5.432551
151912    Andrew Jenkins  0.074917  5.155951
151922      Ida Williams  0.562629  5.223119
152069     Matthew Almen  0.288013  4.942842

[1035 rows x 3 columns]
```
 ![image](https://github.com/user-attachments/assets/e78a928a-1d7d-4c64-9033-1f566b5d72b9)


