# Clinical Decision Support and Data Analysis Projects

This project contains the implementation of four exercises focused on clinical decision support, analyzing COVID-19 case data, population data, and privacy-preserving estimation techniques.

## Exercise 1: Clinical Decision Support - Temperature Tester (20 points)

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
print(chicken_tester(42))  # True, within 1 degree of 41.1
print(human_tester(42))    # False, 42 is way too high for 37
print(chicken_tester(43))  # False, more than 1 degree away from 41.1
print(human_tester(35))    # False, too low for a human's normal temp of 37
print(human_tester(98.6))  # False, normal temp in Fahrenheit, not Celsius
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
data = pd.read_csv('https://github.com/nytimes/covid-19-data/raw/master/us-states.csv')


### 2b. Visualization of New Cases


