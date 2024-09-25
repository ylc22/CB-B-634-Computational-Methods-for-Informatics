# Problem Set 0 by Luis Chan

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

#### Limitations:
- **Data Size**: Plotting new case counts for many states simultaneously can result in cluttered graphs that are difficult to read and interpret. This issue becomes more significant when dealing with all 50 states at once.
- **Date Gaps**: If there are gaps in the data for certain dates (e.g., due to missing or delayed reports), this could affect the smoothness of the graph, leading to misleading spikes or drops.
- **Scaling Differences**: States with significantly different population sizes and case numbers may appear out of scale on the same graph, potentially obscuring trends in states with lower case counts.

  
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

- Mean: 39.51052792739697, Std Dev: 24.152760068601573, Min: 0.0007476719217636152, Max: 99.99154733076972
  
- **Role of the number of bins**: The number of bins in a histogram determines the granularity of the data visualization. Too few bins can oversimplify the data, hiding important details, while too many bins can create a noisy graph, making it difficult to interpret patterns. Choosing an appropriate number of bins provides a clear overview of the data distribution while maintaining enough detail to capture key patterns.
  
- **Outliers and patterns**: Upon analyzing the age distribution, no significant outliers were observed. The distribution follows a relatively normal pattern, with most individuals falling in the middle age range. This suggests that the population is well-distributed across different age groups without any extreme age values.
  
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

- Mean: 60.884134159929715, Std Dev: 18.41182426565962, Min: 3.3820836824389326, Max: 100.43579300336947
  
- **Outliers and patterns**: The histogram of the weight distribution shows a skew towards the right, indicating that most individuals fall within the range of 50 to 80 kg. There is a significant peak around 60 kg. A few outliers are observed on the lower end of the distribution, indicating some individuals have unusually low weights. However, the higher end appears more typical for this population, with fewer extreme values.

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

- **General Relationship**: From the scatterplot, the data shows that weight increases rapidly from birth to around 20 years of age, after which it stabilizes and remains relatively constant throughout adulthood. There is a noticeable leveling off between ages 20 and 60, with weights clustering around the 60-80 kg range. In older age groups, weight remains fairly stable with a slight decrease as individuals age beyond 60.

- **Outliers**: A number of outliers were identified, particularly for very young individuals with extremely low weights. For example, individuals like `Edna Williams` (0.09 years, 4.37 kg), `Ken Graser` (0.014 years, 4.03 kg), and `Matthew Almen` (0.29 years, 4.94 kg) do not follow the general trend, as their weights are much lower than the bulk of the population.

- **Process for Identifying Outliers**: Outliers were identified by inspecting the scatterplot for data points that were significantly below the general cluster of weight values for their respective age groups. Individuals with weights far below the typical range for their age were then listed as outliers in the dataset.

  
## Exercise 4: Privacy-Preserving Estimation of Drug Use

### 4a. Population Generation
```python
import random

def generate_population(n, d):
    
    population = [True] * d + [False] * (n - d)
    random.shuffle(population)
    return population

# Example usage
population = generate_population(1000, 100)
print(population)
```
### 4b. Sample and Protocol Simulation

```python
def apply_randomized_response(sample):
    
    responses = []
    
    for person in sample:
        first_flip = random.choice([True, False])  # True is heads, False is tails
        if first_flip:  # Heads
            second_flip = random.choice([True, False])  # Randomly respond True or False
            responses.append(second_flip)
        else:  # Tails
            responses.append(person)  # Report truthfully
        
    return responses

def simulate_protocol(population, sample_size):

    sample = random.sample(population, sample_size)
    return apply_randomized_response(sample)

# Example usage
responses = simulate_protocol(population, 50)
print(responses)
```

### 4c. Estimation function

```python
def estimate_drug_users(n, d, sample_size):
    
    population = generate_population(n, d)
    responses = simulate_protocol(population, sample_size)
    
    # Calculate the fraction of "True" responses
    reported_true = responses.count(True)
    
    # Apply the formula to estimate the true fraction of drug users
    estimated_fraction = (reported_true / sample_size - 0.25) / 0.5
    
    # Estimate total drug users in population
    estimated_users = max(0, estimated_fraction * n)  # Handle negative estimates gracefully
    return estimated_users

# Example usage
estimated_users = estimate_drug_users(1000, 100, 50)
```

- **Handling Negative Estimates**: When estimating the number of drug users based on randomized response protocol, random variability may sometimes produce negative estimates. To address this, the function sets negative estimates to zero, as a negative number of drug users is not logically possible. This method ensures that the final estimate remains realistic and avoids erroneous outcomes caused by random fluctuations in the data.


### 4d. Run a simulation
```python
# Run a simulation for the given parameters
population_size = 1000
drug_users = 100
sample_size = 50

estimated_users = estimate_drug_users(population_size, drug_users, sample_size)
print(f"Estimated number of drug users: {estimated_users}")
```
#### output
```python
Estimated number of drug users: 300.00000000000006
```

### 4e. Explore variability of estimate 
```python
import numpy as np
import matplotlib.pyplot as plt

def run_multiple_simulations(n, d, sample_size, repetitions=1000):
  
    estimates = []
    for _ in range(repetitions):
        estimates.append(estimate_drug_users(n, d, sample_size))
    
    return estimates

# Run simulations and plot a histogram
estimates = run_multiple_simulations(1000, 100, 50, 1000)

plt.hist(estimates, bins=30, color='blue', edgecolor='black')
plt.title('Histogram of Estimated Drug Users')
plt.xlabel('Estimated Number of Drug Users')
plt.ylabel('Frequency')
plt.show()
```
![image](https://github.com/user-attachments/assets/4c999d36-41d7-4d4d-a3d9-539ecc2d2277)

 **Number of Repetitions**: The experiment was repeated 1,000 times to provide a sufficiently large sample to observe the variability in the estimates. A larger number of repetitions helps in getting a more accurate distribution of the estimated number of drug users.

- **Histogram of Estimates**: The histogram shows a wide range of estimates, with a large number of estimates near zero and a gradual decline as the estimated number of drug users increases. This variability is expected due to the randomness introduced by the randomized response protocol.

- **Errors and Variability**: The high frequency of low estimates, including zero, indicates that the randomness in the protocol often underestimates the true number of drug users. The tail of the histogram shows some larger estimates, but these are less frequent. This pattern highlights the potential for both under- and over-estimation, with a bias towards lower estimates due to random variability and privacy-preserving randomness.

### 4f. Explore relationship between sample size and standard deviation of possible predictions

```python
ef explore_sample_size_variability(n, d_values, sample_size_range):
    
    mean_estimates = {d: [] for d in d_values}
    std_devs = {d: [] for d in d_values}
    
    for sample_size in sample_size_range:
        for d in d_values:
            estimates = run_multiple_simulations(n, d, sample_size, 100)
            mean_estimates[d].append(np.mean(estimates))
            std_devs[d].append(np.std(estimates))
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    
    for d in d_values:
        plt.plot(sample_size_range, mean_estimates[d], label=f'Mean Estimate (d={d})')
        plt.fill_between(sample_size_range, 
                         np.array(mean_estimates[d]) - np.array(std_devs[d]), 
                         np.array(mean_estimates[d]) + np.array(std_devs[d]), 
                         alpha=0.2)
    
    plt.xlabel('Sample Size')
    plt.ylabel('Estimated Number of Drug Users')
    plt.title('Effect of Sample Size on Estimates')
    plt.legend()
    plt.show()

# Example usage
sample_size_range = list(range(10, 1001, 10))
explore_sample_size_variability(1000, [100, 500], sample_size_range)
```

![image](https://github.com/user-attachments/assets/30ebc08a-635a-4fd7-b4a4-eeca466fc818)

- **Findings**: As the sample size increases, the variability (represented by the shaded region of ±1 standard deviation) decreases for both scenarios (populations with 100 and 500 drug users). In smaller sample sizes, there is significant variability, with estimates fluctuating widely. However, as the sample size grows larger, the estimates become more stable, converging toward the true number of drug users. This shows that larger sample sizes result in more accurate estimates with reduced uncertainty. The trend is similar in both scenarios, but the population with 500 users shows less initial variability compared to the population with 100 users due to the larger underlying proportion of drug users in the sample.

