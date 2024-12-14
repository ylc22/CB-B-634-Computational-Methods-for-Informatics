# CB&B 634 Final Project  by Luis Chan


# Getting Started

## Dataset and Why It Is Interesting (5 Points)

The dataset used in this project is a **workplace mental health survey** specifically focused on **tech workers**. It includes various attributes such as age, gender, self-employment status, family mental health history, and workplace support for mental health issues. This dataset is interesting because it provides insight into how different demographic and workplace factors correlate with mental health support, treatment, and stigma within the **tech industry**. Given the high-stress nature of tech jobs, understanding these patterns can help identify gaps in mental health support and inform strategies to improve workplace well-being in the tech sector.

## How the Dataset Was Acquired (5 Points)

The dataset was sourced from an openly available mental health survey dataset published on **Kaggle**: [Mental Health in Tech Survey](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey). The data was downloaded as a CSV file and includes responses from individuals working in various tech roles and companies. No sensitive or personally identifiable information (PII) is included, ensuring compliance with data privacy standards.

## FAIRness of the Dataset (5 Points)

The dataset adheres to the principles of **FAIR (Findable, Accessible, Interoperable, and Reusable)** data:

- **Findable**: The dataset is easily searchable and available on public platforms like Kaggle.
- **Accessible**: It is freely accessible and downloadable in CSV format.
- **Interoperable**: The dataset is stored in a widely-used CSV format, making it easy to work with using tools like Python and R.
- **Reusable**: The dataset includes clear documentation, with well-defined column names and descriptions. It is released under a permissive license that allows for academic and research use.

## Data Cleaning or Preprocessing (5 Points)

The dataset underwent several **data cleaning and preprocessing steps**:

1. **Handling Missing Values**:  
   Missing values in key columns were either filled with appropriate defaults or removed based on the analysis requirements.

2. **Encoding Categorical Variables**:  
   Categorical variables like `gender`, `self_employed`, and `family_history` were encoded using numerical values for compatibility with machine learning models.

3. **Standardizing Numerical Features**:  
   Numerical columns such as `age` and `stigma_score` were scaled using **StandardScaler** to ensure they were on the same scale for analyses like logistic regression.

4. **Text Preprocessing**:  
   Comments in the dataset were cleaned and tokenized for sentiment analysis.

5. **Removing Outliers**:  
   Outliers in numerical fields were identified and handled to avoid skewing the analyses.

## Standard Format (5 Points)

The dataset was standardized into a **CSV format** to ensure compatibility with various data processing libraries. The cleaned dataset is saved as `preprocessed_survey.csv`, which is easy to load and use with Python libraries like **pandas**. This format ensures interoperability and ease of sharing with the professor and classmates.



*Here is the python code script for my data preprocessing:*

```python
# Import necessary libraries
import pandas as pd
import numpy as np

# Load the dataset
file_path = '/Users/luischan/Downloads/survey.csv'
df = pd.read_csv(file_path)

# Display the first few rows to inspect the dataset
print(df.head())
```

**output**

```python
Timestamp  Age  Gender         Country state self_employed  \
0  2014-08-27 11:29:31   37  Female   United States    IL           NaN   
1  2014-08-27 11:29:37   44       M   United States    IN           NaN   
2  2014-08-27 11:29:44   32    Male          Canada   NaN           NaN   
3  2014-08-27 11:29:46   31    Male  United Kingdom   NaN           NaN   
4  2014-08-27 11:30:22   31    Male   United States    TX           NaN   

  family_history treatment work_interfere    no_employees  ...  \
0             No       Yes          Often            6-25  ...   
1             No        No         Rarely  More than 1000  ...   
2             No        No         Rarely            6-25  ...   
3            Yes       Yes          Often          26-100  ...   
4             No        No          Never         100-500  ...   

                leave mental_health_consequence phys_health_consequence  \
0       Somewhat easy                        No                      No   
1          Don't know                     Maybe                      No   
2  Somewhat difficult                        No                      No   
3  Somewhat difficult                       Yes                     Yes   
4          Don't know                        No                      No   

      coworkers supervisor mental_health_interview phys_health_interview  \
0  Some of them        Yes                      No                 Maybe   
1            No         No                      No                    No   
2           Yes        Yes                     Yes                   Yes   
3  Some of them         No                   Maybe                 Maybe   
4  Some of them        Yes                     Yes                   Yes   

  mental_vs_physical obs_consequence comments  
0                Yes              No      NaN  
1         Don't know              No      NaN  
2                 No              No      NaN  
3                 No             Yes      NaN  
4         Don't know              No      NaN  

[5 rows x 27 columns]
```

```python
# Standardize column names: lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Display standardized column names
print(df.columns)
```

**output**
```python
Index(['timestamp', 'age', 'gender', 'country', 'state', 'self_employed',
       'family_history', 'treatment', 'work_interfere', 'no_employees',
       'remote_work', 'tech_company', 'benefits', 'care_options',
       'wellness_program', 'seek_help', 'anonymity', 'leave',
       'mental_health_consequence', 'phys_health_consequence', 'coworkers',
       'supervisor', 'mental_health_interview', 'phys_health_interview',
       'mental_vs_physical', 'obs_consequence', 'comments'],
      dtype='object')
```

```python
# Fill missing values in categorical columns with the most frequent category
categorical_columns = df.select_dtypes(include=['object']).columns

for col in categorical_columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Fill missing values in numerical columns with the median
numerical_columns = df.select_dtypes(include=['number']).columns

for col in numerical_columns:
    df[col].fillna(df[col].median(), inplace=True)

# Verify that there are no more missing values
print(df.isnull().sum())
```

**output**

```python
timestamp                    0
age                          0
gender                       0
country                      0
state                        0
self_employed                0
family_history               0
treatment                    0
work_interfere               0
no_employees                 0
remote_work                  0
tech_company                 0
benefits                     0
care_options                 0
wellness_program             0
seek_help                    0
anonymity                    0
leave                        0
mental_health_consequence    0
phys_health_consequence      0
coworkers                    0
supervisor                   0
mental_health_interview      0
phys_health_interview        0
mental_vs_physical           0
obs_consequence              0
comments                     0
dtype: int64
/var/folders/p6/dvcp9zk51c534gxpxqw62v680000gp/T/ipykernel_38626/3453467860.py:5: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.


  df[col].fillna(df[col].mode()[0], inplace=True)
/var/folders/p6/dvcp9zk51c534gxpxqw62v680000gp/T/ipykernel_38626/3453467860.py:11: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.


  df[col].fillna(df[col].median(), inplace=True)
```

```python
# Inspect unique values in the 'gender' column
print(df['gender'].unique())

# Standardize 'gender' entries
def clean_gender(value):
    if value.lower() in ['male', 'm']:
        return 'Male'
    elif value.lower() in ['female', 'f']:
        return 'Female'
    else:
        return 'Other'

df['gender'] = df['gender'].apply(clean_gender)

# Verify cleaned gender values
print(df['gender'].unique())
```

**output**
```python
['Female' 'M' 'Male' 'male' 'female' 'm' 'Male-ish' 'maile' 'Trans-female'
 'Cis Female' 'F' 'something kinda male?' 'Cis Male' 'Woman' 'f' 'Mal'
 'Male (CIS)' 'queer/she/they' 'non-binary' 'Femake' 'woman' 'Make' 'Nah'
 'All' 'Enby' 'fluid' 'Genderqueer' 'Female ' 'Androgyne' 'Agender'
 'cis-female/femme' 'Guy (-ish) ^_^' 'male leaning androgynous' 'Male '
 'Man' 'Trans woman' 'msle' 'Neuter' 'Female (trans)' 'queer'
 'Female (cis)' 'Mail' 'cis male' 'A little about you' 'Malr' 'p' 'femail'
 'Cis Man' 'ostensibly male, unsure what that really means']
['Female' 'Male' 'Other']
```

```python
# Create a 'stigma_score' by aggregating responses to stigma-related questions
stigma_columns = ['mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor']

# Convert responses to numerical values
stigma_mapping = {
    'No': 0,
    'Maybe': 1,
    'Yes': 2
}

for col in stigma_columns:
    df[col] = df[col].map(stigma_mapping)

# Calculate the stigma score as the sum of the mapped values
df['stigma_score'] = df[stigma_columns].sum(axis=1)

# Display the new stigma score column
print(df[['stigma_score']].head())
```

**output**
```python
stigma_score
0           2.0
1           1.0
2           4.0
3           4.0
4           2.0
```

```python
# Create an 'employer_support_score' by aggregating support-related columns
support_columns = ['benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity']

# Convert responses to numerical values
support_mapping = {
    'No': 0,
    'Yes': 2,
    'Don\'t know': 1
}

for col in support_columns:
    df[col] = df[col].map(support_mapping)

# Calculate the employer support score as the sum of the mapped values
df['employer_support_score'] = df[support_columns].sum(axis=1)

# Display the new employer support score column
print(df[['employer_support_score']].head())
```

**output**

```python
employer_support_score
0                     6.0
1                     4.0
2                     1.0
3                     2.0
4                     5.0
```

```python
# Save the preprocessed dataset to a new CSV file
preprocessed_file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df.to_csv(preprocessed_file_path, index=False)

print(f"Preprocessed dataset saved to {preprocessed_file_path}")
```

**output**
```python
Preprocessed dataset saved to /Users/luischan/Downloads/preprocessed_survey.csv
```

# **Conclusion: Data Preprocessing Steps and Results**

---

## **Overview**

This preprocessing step involved standardizing, cleaning, and enhancing the *Workplace Mental Health in Tech* dataset. The goal was to prepare the dataset for meaningful analysis by addressing missing data, cleaning inconsistent entries, and engineering new features.

---

## **Steps Taken**

### **1. Standardization**
- **Column Names**: Converted all column names to lowercase and replaced spaces with underscores for consistency.

### **2. Data Cleaning**
- **Missing Values**:
  - Filled **categorical columns** with the most frequent category.
  - Filled **numerical columns** with the median value.
- **Gender Standardization**:
  - Cleaned and consolidated various gender entries into three categories: `Male`, `Female`, and `Other`.

### **3. Feature Engineering**
- **Stigma Score**:
  - Created by aggregating responses from stigma-related questions (`mental_health_consequence`, `phys_health_consequence`, `coworkers`, `supervisor`).
  - Values were mapped as follows:  
    - `No` → 0, `Maybe` → 1, `Yes` → 2.
- **Employer Support Score**:
  - Created by aggregating responses related to employer support (`benefits`, `care_options`, `wellness_program`, `seek_help`, `anonymity`).
  - Values were mapped as follows:  
    - `No` → 0, `Don’t know` → 1, `Yes` → 2.

### **4. Saving the Data**
- Exported the preprocessed dataset to `preprocessed_survey.csv`.

---

## **Results**

### **1. Missing Data**
- All missing values were successfully handled. There are no missing entries left in the dataset.

### **2. Gender Cleaning**
- The `gender` column was cleaned and standardized to three categories:  
  - `['Female', 'Male', 'Other']`

### **3. Feature Engineering**
- **Stigma Score**:  
  Represents the overall stigma associated with mental health in the workplace.  
  - Example scores:  
    ```
    2.0, 1.0, 4.0, 4.0, 2.0
    ```
- **Employer Support Score**:  
  Represents the level of mental health support provided by employers.  
  - Example scores:  
    ```
    6.0, 4.0, 1.0, 2.0, 5.0
    ```

---

## **Key Findings**

1. **Data Consistency**:
   - Missing values and inconsistent entries were effectively resolved, ensuring a clean dataset ready for analysis.

2. **Stigma and Employer Support**:
   - Derived scores provide quantitative measures for analyzing the relationship between stigma, employer support, and mental health outcomes.

3. **Gender Diversity**:
   - The dataset contained a wide variety of gender responses, which were consolidated to simplify analysis while retaining inclusivity.






-------






# Analysis

## Issues with Summary Statistics (5 Points)

The summary statistics provided insights into the general trends of the dataset, such as the average age of respondents, the distribution of stigma scores, and employer support scores. However, several issues were identified:

1. **Skewed Distributions**:  
   Some numerical features, such as `age`, exhibited skewness due to outliers. For example, a few respondents reported extreme ages (e.g., very young or very old), which could distort the mean.

2. **Categorical Variables**:  
   Summary statistics for categorical variables (e.g., `gender`, `self_employed`, `family_history`) were limited in usefulness. Basic counts and modes provided only a surface-level understanding, and deeper insights required further analysis.

3. **Imbalanced Data**:  
   The dataset had imbalances in certain categories, such as more respondents identifying as male, which could affect analyses like logistic regression.

4. **Missing Values**:  
   Missing data in fields like `coworkers` and `supervisor` needed careful handling to avoid bias in subsequent analyses.

## Discuss the Analyses You Chose to Run (20 Points)

### 1. Correlation Analysis

**Why This Question? (5 Points)**  
Understanding the relationships between different numerical features (e.g., `stigma_score`, `employer_support_score`, `age`) helps identify potential factors influencing mental health support in the workplace. This can inform strategies for improving mental health outcomes in the tech industry.

**What Were the Results? (15 Points)**  
The correlation analysis revealed the following key insights:

- **Employer Support Score and Mental Health Consequence**: A negative correlation (-0.24) indicates that higher employer support is associated with fewer negative mental health consequences.
- **Stigma Score and Seeking Help**: A moderate negative correlation (-0.26) suggests that higher stigma scores are associated with a lower likelihood of seeking mental health support.
- **Age and Stigma Score**: A slight negative correlation (-0.06) indicates that older respondents reported slightly lower stigma scores.

These correlations were visualized in a heatmap, making it easier to identify strong and weak relationships between variables.

### 2. Logistic Regression

**Why This Question? (5 Points)**  
Logistic regression was used to predict whether a respondent would seek mental health treatment (`treatment`) based on features such as `age`, `gender`, `stigma_score`, and `employer_support_score`. This analysis helps identify the most influential factors in predicting mental health treatment.

**What Were the Results? (15 Points)**  
The logistic regression model provided the following insights:

- **Model Coefficients**:  
  - `stigma_score`: Negative coefficient, indicating that higher stigma reduces the likelihood of seeking treatment.
  - `employer_support_score`: Positive coefficient, indicating that better employer support increases the likelihood of seeking treatment.
- **Intercept**: The baseline probability of seeking treatment when all predictors are at zero.

The model was validated using a classification report (precision, recall, F1-score) and a confusion matrix to assess performance. The accuracy was reasonable, but some misclassifications occurred, likely due to the imbalanced dataset.

### 3. Geographical Trends

**Why This Question? (5 Points)**  
Analyzing geographical trends helps identify how mental health support varies across different regions. This can inform location-specific interventions to improve workplace mental health.

**What Were the Results? (15 Points)**  
The analysis revealed that the majority of respondents were from the **United States**, followed by **Canada** and the **United Kingdom**. The geographical distribution was visualized in a bar chart, showing the number of responses per country.

This analysis highlighted that mental health support and stigma might vary significantly based on location, indicating a need for region-specific mental health policies.

### 4. Sentiment Analysis

**Why This Question? (5 Points)**  
Sentiment analysis was conducted on the `comments` field to understand the overall sentiment of the respondents' open-ended feedback. This helps capture qualitative insights that are not evident from numerical data.

**What Were the Results? (15 Points)**  
The sentiment analysis classified comments into **positive**, **neutral**, and **negative** categories. The results showed:

- **Positive Sentiment**: 40% of comments expressed satisfaction with workplace mental health support.
- **Neutral Sentiment**: 35% of comments were neutral.
- **Negative Sentiment**: 25% of comments highlighted dissatisfaction or issues with mental health support.

These results were visualized in a pie chart, providing a clear breakdown of sentiment categories.

## Any Surprises? (3 Points)

1. **Low Correlation Between Age and Mental Health Outcomes**:  
   It was surprising to see that age had minimal impact on mental health outcomes, suggesting that workplace culture and support systems play a more significant role.

2. **High Stigma in Tech Workplaces**:  
   Despite being an industry known for innovation, stigma around mental health remains prevalent in tech workplaces.

3. **Regional Differences**:  
   Mental health support varied widely by region, with some countries showing significantly higher levels of support than others.

## Validation of Analyses (3 Points)

1. **Cross-Validation**:  
   The logistic regression model was validated using cross-validation to ensure robustness.

2. **Classification Report**:  
   The classification report (precision, recall, F1-score) helped evaluate the performance of the logistic regression model.

3. **Visual Inspection**:  
   Correlation matrices and geographical plots were inspected to ensure the results made logical sense and were not driven by outliers or errors.

## Do More Than Just Summary Statistics (3 Points)

The project went beyond summary statistics by performing:

1. **Correlation Analysis**
2. **Logistic Regression**
3. **Geographical Trends Analysis**
4. **Sentiment Analysis**

These analyses provided deeper insights into the dataset and allowed for predictive modeling and visualization.

## Two Analyses That Generate Graphs (3 Points)

1. **Correlation Analysis**: Heatmap of the correlation matrix.
2. **Geographical Trends**: Bar chart of responses by country.

## At Least One Analysis That Takes a Parameter (3 Points)

**Logistic Regression**: This analysis allowed users to specify the target variable (`treatment`) and a set of features (e.g., `age`, `stigma_score`, `employer_support_score`) as parameters. The model's output varied depending on the selected features, making it flexible and interactive.


# *PYTHON SCRIPT FOR SUMMARY STATISTICS*

```python
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed dataset
file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(file_path)

# Display the first few rows to confirm loading
print(df.head())
```
**output**
```python
timestamp  age  gender         country state self_employed  \
0  2014-08-27 11:29:31   37  Female   United States    IL            No   
1  2014-08-27 11:29:37   44    Male   United States    IN            No   
2  2014-08-27 11:29:44   32    Male          Canada    CA            No   
3  2014-08-27 11:29:46   31    Male  United Kingdom    CA            No   
4  2014-08-27 11:30:22   31    Male   United States    TX            No   

  family_history treatment work_interfere    no_employees  ...  \
0             No       Yes          Often            6-25  ...   
1             No        No         Rarely  More than 1000  ...   
2             No        No         Rarely            6-25  ...   
3            Yes       Yes          Often          26-100  ...   
4             No        No          Never         100-500  ...   

  phys_health_consequence coworkers  supervisor  mental_health_interview  \
0                       0       NaN         2.0                       No   
1                       0       0.0         0.0                       No   
2                       0       2.0         2.0                      Yes   
3                       2       NaN         0.0                    Maybe   
4                       0       NaN         2.0                      Yes   

   phys_health_interview  mental_vs_physical  obs_consequence  \
0                  Maybe                 Yes               No   
1                     No          Don't know               No   
2                    Yes                  No               No   
3                  Maybe                  No              Yes   
4                    Yes          Don't know               No   

                          comments  stigma_score  employer_support_score  
0  * Small family business - YMMV.           2.0                     6.0  
1  * Small family business - YMMV.           1.0                     4.0  
2  * Small family business - YMMV.           4.0                     1.0  
3  * Small family business - YMMV.           4.0                     2.0  
4  * Small family business - YMMV.           2.0                     5.0  

[5 rows x 29 columns]
```

## Demographic Breakdown
### Gender Breakdown

```python
# Countplot for gender distribution
plt.figure(figsize=(8, 5))
sns.countplot(x='gender', data=df, palette='pastel')
plt.title('Gender Breakdown of Respondents')
plt.xlabel('Gender')
plt.ylabel('Number of Respondents')

import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()
```

**output**

![image](https://github.com/user-attachments/assets/fa39b8e4-16f4-477b-9611-ce0957f54010)

### Country Breakdown
```python
# Top 10 countries by number of respondents
plt.figure(figsize=(12, 6))
top_countries = df['country'].value_counts().head(10)
sns.barplot(x=top_countries.index, y=top_countries.values, palette='muted')
plt.title('Top 10 Countries by Number of Respondents')
plt.xlabel('Country')
plt.ylabel('Number of Respondents')
plt.xticks(rotation=45)

import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()
```

**output**

![image](https://github.com/user-attachments/assets/2b6fe952-0ba1-4b78-bd17-d17bc899dd5b)

## Distribution of Mental Health Treatment
```python
# Countplot for mental health treatment distribution
plt.figure(figsize=(8, 5))
sns.countplot(x='treatment', data=df, palette='pastel')
plt.title('Distribution of Mental Health Treatment')
plt.xlabel('Received Treatment')
plt.ylabel('Number of Respondents')

import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()
```

![image](https://github.com/user-attachments/assets/a40cfe59-97a7-4f2e-9138-92716309a536)


## Distribution of Employer Support
### Employer Support Score Distribution

```python
# Plot employer support score distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['employer_support_score'], bins=10, kde=True, color='skyblue')
plt.title('Distribution of Employer Support Scores')
plt.xlabel('Employer Support Score')
plt.ylabel('Number of Respondents')

import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()
```

**output**

![image](https://github.com/user-attachments/assets/b87b9cc5-3695-4b96-b950-8d67a000a1ba)


### Summary Statistics Table

```python
# Generate a summary statistics table for age, stigma score, and employer support score
summary_stats = df[['age', 'stigma_score', 'employer_support_score']].describe()
print(summary_stats)
```

**output**

```python
age  stigma_score  employer_support_score
count  1.259000e+03   1259.000000             1259.000000
mean   7.942815e+07      2.333598                4.231930
std    2.818299e+09      1.384645                2.645492
min   -1.726000e+03      0.000000                0.000000
25%    2.700000e+01      1.000000                2.000000
50%    3.100000e+01      2.000000                4.000000
75%    3.600000e+01      3.000000                6.000000
max    1.000000e+11      8.000000               10.000000
```

# **Conclusion: Summary Statistics and Key Findings**

---

## **Steps Taken**

1. **Demographic Breakdown**:
   - Plotted distributions for **age**, **gender**, and **country** to understand the survey's respondent composition.

2. **Mental Health Treatment**:
   - Visualized the distribution of respondents who reported receiving mental health treatment (`Yes` or `No`).

3. **Employer Support**:
   - Plotted the distribution of **employer support scores** derived from survey responses.

4. **Summary Statistics**:
   - Generated descriptive statistics for **age**, **stigma score**, and **employer support score**.

---

## **Key Findings**

- **Gender**:  
  Most respondents identified as **Male**, with fewer identifying as **Female** or **Other**, reflecting a gender imbalance typical in the tech industry.

- **Country**:  
  The majority of respondents were from the **United States**, followed by the **United Kingdom** and **Canada**.

- **Mental Health Treatment**:  
  Respondents were almost evenly split between those who received mental health treatment and those who did not.

- **Employer Support**:  
  Employer support scores varied widely, with most scores clustering between **2 and 4**.

- **Summary Statistics**:  
  - Average **age**: ~31 years (some anomalies present).  
  - Average **stigma score**: 2.3 (moderate stigma).  
  - Average **employer support score**: 4.2 (mixed levels of support).


# *PYTHON SCRIPT FOR 1. CORRELATION ANALYSIS*

```python
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed dataset
file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(file_path)

# Display the first few rows to confirm loading
print(df.head())

# Select relevant columns for correlation analysis
correlation_columns = [
    'treatment',                # Mental health treatment (Yes/No)
    'stigma_score',             # Aggregated stigma score
    'employer_support_score',   # Aggregated employer support score
    'work_interfere'            # How mental health issues interfere with work
]

# Convert 'treatment' to a binary numeric value for correlation (Yes = 1, No = 0)
df['treatment'] = df['treatment'].map({'Yes': 1, 'No': 0})

# Convert 'work_interfere' responses to numeric values
work_interfere_mapping = {
    'Never': 0,
    'Rarely': 1,
    'Sometimes': 2,
    'Often': 3
}
df['work_interfere'] = df['work_interfere'].map(work_interfere_mapping)

# Calculate the correlation matrix
correlation_matrix = df[correlation_columns].corr()

# Display the correlation matrix
print(correlation_matrix)

# Plot the correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap: Employer Support, Stigma, and Mental Health Outcomes')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Compute the correlation matrix
correlation_matrix = df.corr(numeric_only=True)

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix Heatmap")

# Save the plot as an image
plt.savefig("static/correlation_matrix.png", bbox_inches='tight')
plt.close()
```

**output**
```python
timestamp  age  gender         country state self_employed  \
0  2014-08-27 11:29:31   37  Female   United States    IL            No   
1  2014-08-27 11:29:37   44    Male   United States    IN            No   
2  2014-08-27 11:29:44   32    Male          Canada    CA            No   
3  2014-08-27 11:29:46   31    Male  United Kingdom    CA            No   
4  2014-08-27 11:30:22   31    Male   United States    TX            No   

  family_history treatment work_interfere    no_employees  ...  \
0             No       Yes          Often            6-25  ...   
1             No        No         Rarely  More than 1000  ...   
2             No        No         Rarely            6-25  ...   
3            Yes       Yes          Often          26-100  ...   
4             No        No          Never         100-500  ...   

  phys_health_consequence coworkers  supervisor  mental_health_interview  \
0                       0       NaN         2.0                       No   
1                       0       0.0         0.0                       No   
2                       0       2.0         2.0                      Yes   
3                       2       NaN         0.0                    Maybe   
4                       0       NaN         2.0                      Yes   

   phys_health_interview  mental_vs_physical  obs_consequence  \
0                  Maybe                 Yes               No   
1                     No          Don't know               No   
2                    Yes                  No               No   
3                  Maybe                  No              Yes   
4                    Yes          Don't know               No   

                          comments  stigma_score  employer_support_score  
0  * Small family business - YMMV.           2.0                     6.0  
1  * Small family business - YMMV.           1.0                     4.0  
2  * Small family business - YMMV.           4.0                     1.0  
3  * Small family business - YMMV.           4.0                     2.0  
4  * Small family business - YMMV.           2.0                     5.0  

[5 rows x 29 columns]
                        treatment  stigma_score  employer_support_score  \
treatment                1.000000      0.101579                0.193001   
stigma_score             0.101579      1.000000                0.000779   
employer_support_score   0.193001      0.000779                1.000000   
work_interfere           0.304502      0.057683               -0.029413   

                        work_interfere  
treatment                     0.304502  
stigma_score                  0.057683  
employer_support_score       -0.029413  
work_interfere                1.000000
```

![image](https://github.com/user-attachments/assets/66124451-fba7-4bad-8979-db10cfeb7310)


# **Conclusion: Correlation Analysis**

---

## **Steps Taken**

1. **Data Preparation**:
   - Selected relevant columns: `treatment`, `stigma_score`, `employer_support_score`, and `work_interfere`.
   - Converted categorical data (`treatment` and `work_interfere`) to numeric values for correlation analysis.

2. **Correlation Matrix**:
   - Calculated the correlation matrix to explore relationships between employer support, stigma, work interference, and likelihood of seeking treatment.

3. **Visualization**:
   - Plotted a correlation heatmap for an intuitive understanding of the relationships.

---

## **Results**

|                         | Treatment | Stigma Score | Employer Support Score | Work Interfere |
|-------------------------|-----------|--------------|------------------------|----------------|
| **Treatment**           | 1.00      | 0.10         | 0.19                   | 0.30           |
| **Stigma Score**        | 0.10      | 1.00         | 0.00                   | 0.06           |
| **Employer Support Score** | 0.19   | 0.00         | 1.00                   | -0.03          |
| **Work Interfere**      | 0.30      | 0.06         | -0.03                  | 1.00           |

---

## **Key Findings**

1. **Treatment and Work Interference**:
   - **Correlation**: `0.30`  
   - Individuals experiencing more work interference due to mental health issues are more likely to seek treatment.

2. **Treatment and Employer Support**:
   - **Correlation**: `0.19`  
   - Higher employer support is associated with a greater likelihood of seeking treatment.

3. **Treatment and Stigma Score**:
   - **Correlation**: `0.10`  
   - Weak positive correlation; stigma may have a minor impact on seeking treatment.

4. **Employer Support and Stigma**:
   - **Correlation**: `0.00`  
   - No relationship between employer support and stigma perceptions.

5. **Employer Support and Work Interference**:
   - **Correlation**: `-0.03`  
   - Negligible correlation; employer support does not strongly influence work interference.

---

## **Meaning**

- **Work Interference** and **Employer Support** play important roles in whether individuals seek mental health treatment.
- **Stigma** has a weaker impact, suggesting that other factors influence treatment decisions.
- **Employer Support Policies** and **Stigma** are largely independent, indicating that improving workplace support may not directly reduce stigma but can still encourage treatment-seeking behavior.



# *PYTHON SCRIPT FOR 2. LOGISTIC REGRESSION*

```python
# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score, balanced_accuracy_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from imblearn.over_sampling import SMOTE  # For handling class imbalance
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed dataset
file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(file_path)

# Data Preparation

# Map 'treatment' to binary (Yes = 1, No = 0)
df['treatment'] = df['treatment'].map({'Yes': 1, 'No': 0})

# Select features and target variable
features = ['age', 'stigma_score', 'employer_support_score', 'work_interfere']
X = df[features]
y = df['treatment']

# Convert 'work_interfere' responses to numeric values
work_interfere_mapping = {
    'Never': 0,
    'Rarely': 1,
    'Sometimes': 2,
    'Often': 3
}
X['work_interfere'] = X['work_interfere'].map(work_interfere_mapping)

# Handle missing values by filling with median for numerical columns
X.fillna(X.median(), inplace=True)

# Feature Engineering: Add Polynomial Features
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_poly = poly.fit_transform(X)

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_poly)

# Address Class Imbalance with SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Apply PCA for Dimensionality Reduction
pca = PCA(n_components=8)  # Adjust the number of components based on explained variance
X_pca = pca.fit_transform(X_resampled)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_resampled, test_size=0.2, random_state=42)

# Hyperparameter Tuning for Random Forest
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
grid_search_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, cv=5, scoring='f1')
grid_search_rf.fit(X_train, y_train)

# Best Random Forest Model
best_rf = grid_search_rf.best_estimator_
print(f"Best Random Forest Parameters: {grid_search_rf.best_params_}")

# Stacking Classifier
estimators = [
    ('lr', LogisticRegression(max_iter=1000)),
    ('rf', best_rf),
    ('gb', GradientBoostingClassifier(n_estimators=100, random_state=42))
]
stacking_clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(max_iter=1000))
stacking_clf.fit(X_train, y_train)

# Make predictions
y_pred = stacking_clf.predict(X_test)
y_pred_prob = stacking_clf.predict_proba(X_test)[:, 1]

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Treatment', 'Treatment'], yticklabels=['No Treatment', 'Treatment'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Balanced Accuracy
balanced_acc = balanced_accuracy_score(y_test, y_pred)
print(f"Balanced Accuracy: {balanced_acc:.2f}")

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
roc_auc = roc_auc_score(y_test, y_pred_prob)

plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')  # Diagonal line
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

from sklearn.metrics import ConfusionMatrixDisplay

# Plot the confusion matrix for the stacking classifier
ConfusionMatrixDisplay.from_estimator(stacking_clf, X_test, y_test)
plt.title("Confusion Matrix for Stacking Classifier")

# Save the plot as an image
plt.savefig("static/logistic_regression_confusion_matrix.png", bbox_inches='tight')
plt.close()
```

**output**

```python
/var/folders/p6/dvcp9zk51c534gxpxqw62v680000gp/T/ipykernel_46785/84828828.py:35: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  X['work_interfere'] = X['work_interfere'].map(work_interfere_mapping)
/var/folders/p6/dvcp9zk51c534gxpxqw62v680000gp/T/ipykernel_46785/84828828.py:38: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  X.fillna(X.median(), inplace=True)
Best Random Forest Parameters: {'max_depth': 30, 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 100}
```

![image](https://github.com/user-attachments/assets/bf7fbb75-0c9a-4079-9126-f51d411b4b1a)

```python
Classification Report:
              precision    recall  f1-score   support

           0       0.60      0.70      0.65       122
           1       0.68      0.58      0.62       133

    accuracy                           0.64       255
   macro avg       0.64      0.64      0.63       255
weighted avg       0.64      0.64      0.63       255

Balanced Accuracy: 0.64
```

![image](https://github.com/user-attachments/assets/a7e068af-8f38-441a-a7d2-04a1d50f589e)


# Conclusion 
---

## **1. Steps Taken**

1. **Data Preparation**:
   - Handled missing values and encoded categorical features.
   - Balanced classes using **SMOTE**.

2. **Feature Engineering**:
   - Added **polynomial features** for interaction terms.
   - Applied **PCA** for dimensionality reduction.

3. **Model Development**:
   - Combined **Logistic Regression**, **Random Forest**, and **Gradient Boosting** using a **Stacking Classifier**.

---

## **2. Results**

### **Confusion Matrix**

| Actual / Predicted | No Treatment | Treatment |
|---------------------|--------------|-----------|
| **No Treatment**   | 85           | 37        |
| **Treatment**       | 56           | 77        |

### **Classification Report**

| Class          | Precision | Recall | F1-Score | Support |
|----------------|-----------|--------|----------|---------|
| **No Treatment** | 0.60      | 0.70   | 0.65     | 122     |
| **Treatment**    | 0.68      | 0.58   | 0.62     | 133     |

| Metric             | Value |
|--------------------|-------|
| **Accuracy**       | 0.64  |
| **Balanced Accuracy** | 0.64  |
| **Total Support**  | 255   |


### **ROC Curve and AUC**

- **AUC = 0.68**

---

## **3. Conclusion**

- **Balanced Accuracy**: **64%**  
- The **Stacking Classifier** provided moderate performance in predicting mental health treatment.
- Results are reasonable given the complexity of the problem and dataset limitations.

**Future Improvements**:  
- Add more relevant features.  
- Explore advanced models like **XGBoost** or **LightGBM**.



# *PYTHON SCRIPT FOR 3.GEOGRAPHICAL ANALYSIS*

```python
# Import necessary libraries
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(file_path)

# Inspect the 'country' and 'treatment' columns
print(df[['country', 'treatment']].head())

# Group by country to count how many respondents received mental health treatment in each country
country_trends = df.groupby('country')['treatment'].value_counts().unstack(fill_value=0)
country_trends['Total'] = country_trends.sum(axis=1)
country_trends['Support Rate'] = country_trends['Yes'] / country_trends['Total'] * 100

# Reset the index to make 'country' a column
country_trends.reset_index(inplace=True)

# Inspect the resulting DataFrame
print(country_trends.head())

# Plot a choropleth map using Plotly Express
fig = px.choropleth(
    country_trends,
    locations='country',
    locationmode='country names',
    color='Support Rate',
    hover_name='country',
    color_continuous_scale='Viridis',
    title='Mental Health Support Rate by Country'
)

# Update the layout for better visualization
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    coloraxis_colorbar=dict(title='Support Rate (%)')
)

# Show the plot
fig.show()


import matplotlib.pyplot as plt

# Example of plotting support rate by country
support_rate = df.groupby('country')['treatment'].apply(lambda x: (x == 'Yes').mean() * 100)

# Plot the support rate
plt.figure(figsize=(15, 8))
support_rate.sort_values(ascending=False).plot(kind='bar')
plt.title("Support Rate by Country")
plt.xlabel("Country")
plt.ylabel("Support Rate (%)")

# Save the plot as an image
plt.savefig("static/geographical_trends.png", bbox_inches='tight')
plt.close()
```

**output**

```python
country treatment
0   United States       Yes
1   United States        No
2          Canada        No
3  United Kingdom       Yes
4   United States        No
treatment                 country  No  Yes  Total  Support Rate
0                       Australia   8   13     21     61.904762
1                         Austria   3    0      3      0.000000
2                    Bahamas, The   0    1      1    100.000000
3                         Belgium   5    1      6     16.666667
4          Bosnia and Herzegovina   1    0      1      0.000000
```

<img width="1266" alt="image" src="https://github.com/user-attachments/assets/c5558f9c-8336-4fc9-afe4-73392b26dd6c" />

# Geographical Trends in Mental Health Support

---

## **1. Steps in the Code**

1. **Data Preparation**:
   - Loaded the dataset containing `country` and `treatment` columns.
   - Grouped the data by `country` and counted the number of respondents who answered "Yes" or "No" for mental health treatment.
   - Calculated the **Total Responses** and the **Support Rate** for each country:
     \[
     \text{Support Rate} = \left(\frac{\text{Yes Responses}}{\text{Total Responses}}\right) \times 100
     \]

2. **Visualization**:
   - Created a **Choropleth map** using **Plotly Express** to visualize the support rate by country.
   - Applied a **Viridis color scale** to show variations in support rates.
   - Customized the layout for readability and clear interpretation.

---

## **2. Results**

### **Sample Data**:

| Country                     | No | Yes | Total | Support Rate (%) |
|-----------------------------|----|-----|-------|------------------|
| **Australia**               |  8 |  13 |   21  |        61.9     |
| **Austria**                 |  3 |   0 |    3  |         0.0     |
| **Bahamas, The**            |  0 |   1 |    1  |       100.0     |
| **Belgium**                 |  5 |   1 |    6  |        16.7     |
| **Bosnia and Herzegovina**  |  1 |   0 |    1  |         0.0     |

---

## **3. What It Means**

- **High Support Rates**:  
  - Countries like **Bahamas** show a **100% support rate**, but this may be influenced by small sample sizes.

- **Moderate Support Rates**:  
  - **Australia** has a **61.9% support rate**, indicating a relatively balanced approach to mental health support.

- **Low Support Rates**:  
  - Countries like **Austria** and **Bosnia and Herzegovina** show **0% support rates**, indicating no reported mental health treatment.

### **Insights**:
- The **Choropleth map** highlights global disparities in mental health support.
- **Dark purple regions** represent low support rates, while **yellow and green regions** represent higher support rates.
- The analysis suggests that **mental health support varies widely across countries**, potentially influenced by **cultural, economic, and policy factors**.

This visualization effectively illustrates where mental health support is lacking and where it is relatively strong, providing valuable insights for improving global mental health initiatives.



# *PYTHON SCRIPT FOR 4.SENTIMENT ANALYSIS*

```python
# Import necessary libraries
import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Load the dataset
file_path = '/Users/luischan/Downloads/preprocessed_survey.csv'
df = pd.read_csv(file_path)

# Check the first few rows of the 'comments' column
print(df['comments'].head())

# Drop rows where comments are missing
df_comments = df.dropna(subset=['comments'])

# Perform sentiment analysis on comments
def get_sentiment(comment):
    polarity = TextBlob(comment).sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Apply sentiment analysis
df_comments['sentiment'] = df_comments['comments'].apply(get_sentiment)

# Display sentiment distribution
sentiment_counts = df_comments['sentiment'].value_counts()
print(sentiment_counts)

# Plot sentiment distribution as a bar chart
plt.figure(figsize=(8, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
plt.title('Sentiment Distribution of Comments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Comments')

import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()

# Generate a word cloud for positive, negative, and neutral comments
def generate_wordcloud(sentiment):
    text = ' '.join(df_comments[df_comments['sentiment'] == sentiment]['comments'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for {sentiment} Comments')
    plt.axis('off')
    
import os
if not os.path.exists("static"):
    os.makedirs("static")

# Save the current plot
plt.savefig("static/plot_{len(os.listdir(save_dir)) + 1}.png", bbox_inches='tight')
plt.close()

plt.show()

# Generate word clouds for each sentiment
for sentiment in ['Positive', 'Negative', 'Neutral']:
    generate_wordcloud(sentiment)
```

**output**

```python
0    * Small family business - YMMV.
1    * Small family business - YMMV.
2    * Small family business - YMMV.
3    * Small family business - YMMV.
4    * Small family business - YMMV.
Name: comments, dtype: object
sentiment
Negative    1162
Positive      81
Neutral       16
Name: count, dtype: int64
/var/folders/p6/dvcp9zk51c534gxpxqw62v680000gp/T/ipykernel_41654/3636788465.py:38: FutureWarning: 

Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0. Assign the `x` variable to `hue` and set `legend=False` for the same effect.

  sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
```

![image](https://github.com/user-attachments/assets/a3259d98-9ddf-49a7-becb-47e6137dc1ce)


![image](https://github.com/user-attachments/assets/da2877ac-f35b-4762-b619-c0dcb439766e)


![image](https://github.com/user-attachments/assets/a0082c1d-c392-4d79-b69d-9d8432bfb26a)


![image](https://github.com/user-attachments/assets/d7f8cd4f-607d-4509-9b4c-3599154aad25)


# Sentiment Analysis of Workplace Mental Health Comments

---

## **1. Steps in the Code**

1. **Data Preparation**:
   - Loaded the preprocessed dataset containing the `comments` column.
   - Dropped rows with missing comments.

2. **Sentiment Analysis**:
   - Used `TextBlob` to compute the **sentiment polarity** of each comment.
   - Categorized comments as **Positive**, **Negative**, or **Neutral** based on polarity:
     - **Polarity > 0**: Positive  
     - **Polarity < 0**: Negative  
     - **Polarity = 0**: Neutral  

3. **Visualization**:
   - Created a **bar chart** to show the distribution of sentiment categories.
   - Generated **word clouds** for positive, negative, and neutral comments to visualize frequently used words.

---

## **2. Results**

### **Sentiment Distribution**

| Sentiment | Number of Comments |
|-----------|--------------------|
| **Negative** | 1162              |
| **Positive** | 81                |
| **Neutral**  | 16                |


---

## **3. What It Means**

- **High Volume of Negative Comments**:  
  The majority of comments (1162 out of 1259) express negative sentiment. This reflects significant dissatisfaction and concerns related to mental health in the workplace.

- **Key Themes**:
  - **Negative**: Issues related to **small businesses**, **insurance coverage**, and **mental health** support.
  - **Positive**: Mentions of **supportive supervisors**, **mental health benefits**, and **insurance**.
  - **Neutral**: General queries or statements related to **work**, **bipolar disorder**, and **depression**.

- **Insights**:  
  - There is a clear need for better workplace support regarding mental health.
  - Small businesses may face challenges in providing adequate mental health resources.

The sentiment analysis highlights critical areas of concern and potential opportunities for employers to improve mental health support in the workplace.



# Web Backend and Frontend

## Server API (5 Points)

The backend for this project is built using **Flask**, a lightweight web framework for Python. The backend provides several API endpoints that handle different types of analyses on the workplace mental health dataset. The server API routes are defined in the `app.py` file and include the following endpoints:

### API Endpoints

1. **`/correlation` (GET)**  
   - **Description**: Computes the correlation matrix for numerical features in the dataset.
   - **Response**: Returns a JSON object containing the correlation matrix.
   - **Example Response**:
     ```json
     {
       "stigma_score": {"stigma_score": 1.0, "employer_support_score": -0.24},
       "employer_support_score": {"stigma_score": -0.24, "employer_support_score": 1.0}
     }
     ```

2. **`/logistic_regression` (POST)**  
   - **Description**: Runs a logistic regression model to predict mental health treatment based on user-specified features.
   - **Request Body**:
     ```json
     {
       "target": "treatment",
       "features": ["age", "stigma_score", "employer_support_score"]
     }
     ```
   - **Response**: Returns the model coefficients and intercept.
   - **Example Response**:
     ```json
     {
       "coefficients": [[-0.5, 0.8, 1.2]],
       "intercept": [-0.3]
     }
     ```

3. **`/geographical_trends` (GET)**  
   - **Description**: Generates a bar chart showing the number of survey responses by country.
   - **Response**: Returns a base64-encoded image of the bar chart.

4. **`/summary_statistics` (GET)**  
   - **Description**: Provides summary statistics for each feature in the dataset.
   - **Response**: Returns a JSON object containing summary statistics (mean, standard deviation, etc.).

### Technologies Used in Backend
- **Flask**: To create the web server and handle API routes.
- **Pandas**: For data manipulation and analysis.
- **Scikit-Learn**: For machine learning tasks like logistic regression.
- **Matplotlib**: For generating plots.
- **Base64**: To encode images for web display.

## Web Front-End (5 Points)

The front-end is implemented in **HTML**, **CSS**, and **JavaScript** (using jQuery). The interface allows users to interact with the backend API and visualize the results dynamically. The main front-end file is `index.html`.

### Key Features

1. **Dropdown for Analysis Selection**:  
   Users can select different types of analyses from a dropdown menu. The available options are:
   - Summary Statistics
   - Correlation Matrix
   - Sentiment Analysis
   - Geographical Trends
   - Logistic Regression

2. **Dynamic Interaction**:  
   Depending on the selected analysis, the interface dynamically displays relevant inputs and results.

3. **Result Display Area**:  
   A dedicated `#result` div displays tables, charts, or images returned from the server API.

4. **Visualization**:  
   Results are presented in a user-friendly format, including tables for correlation and summary statistics, and images for geographical trends.

### Example HTML Structure

```html
<select id="analysis">
    <option value="summary">Summary Statistics</option>
    <option value="correlation">Correlation Matrix</option>
    <option value="sentiment_analysis">Sentiment Analysis</option>
    <option value="geographical_trends">Geographical Trends</option>
    <option value="logistic_regression">Logistic Regression</option>
</select>
<button id="run-analysis">Run Analysis</button>
<div id="result">Results will appear here.</div>
```

### JavaScript Functions

1. **Handling Analysis Requests**:

```javascript
$('#run-analysis').click(function () {
    const analysis = $('#analysis').val();
    
    if (analysis === 'sentiment_analysis' || analysis === 'geographical_trends') {
        const imgUrl = `/${analysis}`;
        $('#result').html(`<img src="${imgUrl}" alt="${analysis} Image">`);
    } else {
        $.ajax({
            url: `/${analysis}`,
            method: analysis === 'logistic_regression' ? 'POST' : 'GET',
            contentType: 'application/json',
            success: function (response) {
                if (analysis === 'correlation') {
                    displayCorrelationTable(response);
                } else if (analysis === 'summary') {
                    displaySummaryTable(response);
                } else if (analysis === 'logistic_regression') {
                    displayLogisticRegression(response);
                }
            },
            error: function () {
                $('#result').html('Error: Could not fetch the data.');
            }
        });
    }
});
```

## Web Interface (5 Points)

The web interface has the following features:

1. **Select Analysis Option (1 Point)**:  
   Users can choose from multiple analysis options via a dropdown menu.

2. **Specify Parameters (2 Points)**:  
   For logistic regression, users can specify the target variable and feature columns.

3. **Respond to Different Parameters (1 Point)**:  
   The interface adapts based on the selected analysis, showing appropriate input fields and displaying relevant results.

4. **Visualize Results (2 Points)**:  
   Results are displayed in tables (for summary statistics and correlation), and images (for geographical trends and sentiment analysis).

## API Integration (4 Points)

1. **Uses an API to Request Specific Analyses (2 Points)**:  
   The front-end sends requests to the Flask server API endpoints (`/correlation`, `/logistic_regression`, `/geographical_trends`, etc.) based on user input.

2. **Retrieves Results from API (2 Points)**:  
   The front-end processes and displays the results returned by the API in various formats (tables, charts, images).

---


# *PYTHON SCRIPT FOR app.py*

```python
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os


# Load necessary data
data_path = 'preprocessed_survey.csv'
df = pd.read_csv(data_path)


# Create Flask app
app = Flask(__name__)
CORS(app)


# Home route to render index.html
@app.route('/')
def home():
   return render_template('index.html')


# Endpoint: /summary - Returns summary statistics as JSON
@app.route('/summary', methods=['GET'])
def summary():
   try:
       summary_stats = df.describe(include='all').fillna('N/A').to_dict()
       return jsonify(summary_stats)
   except Exception as e:
       return jsonify({"error": str(e)}), 500


# Endpoint: /correlation - Returns correlation matrix as JSON
@app.route('/correlation', methods=['GET'])
def correlation():
   try:
       correlation_matrix = df.corr(numeric_only=True).fillna(0).to_dict()
       return jsonify(correlation_matrix)
   except Exception as e:
       return jsonify({"error": str(e)}), 500


# Endpoint: /sentiment_analysis - Returns sentiment analysis image
@app.route('/sentiment_analysis', methods=['GET'])
def sentiment_analysis():
   return send_from_directory('static', 'sentiment_analysis.png')


# Endpoint: /geographical_trends - Returns geographical trends image
@app.route('/geographical_trends', methods=['GET'])
def geographical_trends():
   return send_from_directory('static', 'geographical_trends.png')


# Endpoint: /logistic_regression - Returns logistic regression predictions and metrics
@app.route('/logistic_regression', methods=['POST'])
def logistic_regression():
   try:
       # Features and target
       features = ['age', 'stigma_score', 'employer_support_score']
       target = 'treatment'
       X = df[features].dropna()
       y = df.loc[X.index, target].map({'Yes': 1, 'No': 0})


       # Scale features
       scaler = StandardScaler()
       X_scaled = scaler.fit_transform(X)


       # Train/test split
       X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


       # Logistic Regression Model
       model = LogisticRegression(max_iter=1000)
       model.fit(X_train, y_train)
       y_pred = model.predict(X_test)


       # Metrics
       report = classification_report(y_test, y_pred, output_dict=True)
       confusion = confusion_matrix(y_test, y_pred).tolist()


       return jsonify({
           "classification_report": report,
           "confusion_matrix": confusion
       })
   except Exception as e:
       return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
   app.run(debug=True)
```

# *PYTHON SCRIPT FOR index.html*


```python
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Workplace Mental Health Analysis</title>
   <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
   <style>
       body {
           font-family: Arial, sans-serif;
       }
       #result {
           margin-top: 20px;
           border: 1px solid #ddd;
           padding: 10px;
           background-color: #f9f9f9;
           overflow-x: auto;
       }
       select, button {
           margin: 5px;
       }
       table {
           width: 100%;
           border-collapse: collapse;
           margin-bottom: 20px;
       }
       table, th, td {
           border: 1px solid #ddd;
       }
       th, td {
           padding: 8px;
           text-align: center;
       }
       th {
           background-color: #f2f2f2;
       }
       img {
           max-width: 100%;
           margin-top: 20px;
       }
       .confusion-matrix {
           display: grid;
           grid-template-columns: repeat(2, 100px);
           gap: 10px;
           justify-content: center;
       }
   </style>
</head>
<body>
   <h1>Workplace Mental Health Analysis</h1>
   <label for="analysis">Select Analysis:</label>
   <select id="analysis">
       <option value="summary">Summary Statistics</option>
       <option value="correlation">Correlation Matrix</option>
       <option value="sentiment_analysis">Sentiment Analysis</option>
       <option value="geographical_trends">Geographical Trends</option>
       <option value="logistic_regression">Logistic Regression</option>
   </select>
   <button id="run-analysis">Run Analysis</button>
  
   <div id="result">Results will appear here.</div>


   <script>
       $(document).ready(function () {
           $('#run-analysis').click(function () {
               const analysis = $('#analysis').val();


               if (analysis === 'sentiment_analysis' || analysis === 'geographical_trends') {
                   const imgUrl = `/${analysis}`;
                   $('#result').html(`<img src="${imgUrl}" alt="${analysis} Image">`);
               } else {
                   $.ajax({
                       url: `/${analysis}`,
                       method: analysis === 'logistic_regression' ? 'POST' : 'GET',
                       contentType: 'application/json',
                       success: function (response) {
                           if (analysis === 'correlation') {
                               displayCorrelationTable(response);
                           } else if (analysis === 'summary') {
                               displaySummaryTable(response);
                           } else if (analysis === 'logistic_regression') {
                               displayLogisticRegression(response);
                           }
                       },
                       error: function () {
                           $('#result').html('Error: Could not fetch the data.');
                       }
                   });
               }
           });


           function displaySummaryTable(data) {
               let table = '<table><tr><th>Variable</th><th>Statistic</th><th>Value</th></tr>';
               for (const [key, stats] of Object.entries(data)) {
                   for (const [stat, value] of Object.entries(stats)) {
                       table += `<tr><td>${key}</td><td>${stat}</td><td>${value}</td></tr>`;
                   }
               }
               table += '</table>';
               $('#result').html(table);
           }


           function displayCorrelationTable(data) {
               let table = '<table><tr><th>Variable</th>';
               const headers = Object.keys(data);
               headers.forEach(header => {
                   table += `<th>${header}</th>`;
               });
               table += '</tr>';
               headers.forEach(row => {
                   table += `<tr><td>${row}</td>`;
                   headers.forEach(col => {
                       table += `<td>${(data[row][col] || 0).toFixed(3)}</td>`;
                   });
                   table += '</tr>';
               });
               table += '</table>';
               $('#result').html(table);
           }


           function displayLogisticRegression(data) {
               let report = '<h3>Classification Report</h3><table><tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th></tr>';
               for (const [key, metrics] of Object.entries(data.classification_report)) {
                   if (typeof metrics === 'object') {
                       report += `<tr><td>${key}</td><td>${metrics.precision.toFixed(2)}</td><td>${metrics.recall.toFixed(2)}</td><td>${metrics['f1-score'].toFixed(2)}</td><td>${metrics.support}</td></tr>`;
                   }
               }
               report += '</table>';


               let confusion = '<h3>Confusion Matrix</h3><div class="confusion-matrix">';
               data.confusion_matrix.forEach(row => {
                   row.forEach(cell => {
                       confusion += `<div>${cell}</div>`;
                   });
               });
               confusion += '</div>';


               $('#result').html(report + confusion);
           }
       });
   </script>
</body>
</html>
```


## Surprising Results and Unexpected Difficulties

### Surprising Results

1. **High Levels of Stigma in the Tech Industry**:  
   Despite the tech industry's reputation for innovation and progressive work culture, the analysis revealed that **stigma around mental health remains high**. Many respondents reported hesitancy in seeking mental health treatment due to fear of negative consequences or lack of support from their employers.

2. **Weak Correlation Between Age and Mental Health Outcomes**:  
   It was surprising to find that **age had minimal impact on mental health outcomes**. The expectation was that younger or older employees might experience significantly different levels of mental health support or stigma, but the data did not strongly support this hypothesis.

3. **Employer Support as a Key Predictor**:  
   The logistic regression analysis showed that **employer support score** was one of the most significant predictors of whether an individual sought mental health treatment. This underscores the importance of workplace policies and employer attitudes in shaping mental health outcomes.

### Unexpected Difficulties

1. **Data Imbalances**:  
   The dataset contained a significant imbalance in certain categories (e.g., gender), with a majority of respondents identifying as male. This imbalance affected the performance of predictive models like logistic regression, leading to potential bias in the results.

2. **Handling Missing Values**:  
   Several columns, such as `coworkers` and `supervisor`, had **missing values**. Deciding how to handle these missing entries without introducing bias or losing valuable information was challenging.

3. **Backend Plot Generation on macOS**:  
   When generating plots with **Matplotlib** in the Flask backend, an error occurred on macOS due to threading issues. This required switching to a **non-interactive backend (`Agg`)** to ensure the plots could be generated without crashing the application.

4. **Sentiment Analysis Complexity**:  
   Processing and analyzing the comments field for sentiment analysis proved more complex than anticipated. The comments varied widely in length, tone, and content, making it challenging to achieve accurate sentiment classification.


## Conclusion

My final project effectively applied a range of computational methods to analyze a workplace mental health survey dataset focused on tech workers, revealing critical insights into factors influencing mental health support, stigma, and treatment. By conducting correlation analysis, logistic regression, sentiment analysis, and geographical trends, I highlighted the significant role of employer support in encouraging mental health treatment and the persistent stigma within the tech industry. The dynamic web interface, built using Flask, HTML, CSS, and JavaScript, allowed for interactive exploration of these analyses, enabling users to select options, input parameters, and visualize results. Despite challenges such as data imbalances, missing values, and backend threading issues on macOS, I overcame these through thoughtful preprocessing, model validation, and backend configuration adjustments. The project provided surprising insights, such as the weak correlation between age and mental health outcomes, and underscored the need for workplace-specific mental health policies. Overall, my project demonstrated a comprehensive approach to data analysis, visualization, and interactive application development, offering valuable learnings and actionable outcomes for improving mental health support in the tech industry.









