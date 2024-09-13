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
