# CB&B 634 Final Project by Luis Chan


# Getting Started

## Dataset and Why It Is Interesting (5 Points)

The dataset used in this project is a **workplace mental health survey** that includes various attributes such as age, gender, self-employment status, family mental health history, and workplace support for mental health issues. This dataset is interesting because it provides insight into how different demographic and workplace factors correlate with mental health support, treatment, and stigma in the workplace. Understanding these patterns can help identify gaps in mental health support and inform strategies to improve workplace well-being.

## How the Dataset Was Acquired (5 Points)

The dataset was sourced from an openly available mental health survey dataset published on platforms like **Kaggle** or similar public repositories. The data was downloaded as a CSV file and includes responses from individuals working in various industries. No sensitive or personally identifiable information (PII) is included, ensuring compliance with data privacy standards.

## FAIRness of the Dataset (5 Points)

The dataset adheres to the principles of **FAIR (Findable, Accessible, Interoperable, and Reusable)** data:

- **Findable**: The dataset is easily searchable and available on public platforms.
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
