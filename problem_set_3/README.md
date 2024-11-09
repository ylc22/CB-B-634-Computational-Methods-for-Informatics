# Problem Set 3 by Luis Chan

## Exercise 1: Gradient Descent for Neural Network Parameter Optimization

```python
import requests

# Define the error function query
def get_error(a, b):
    response = requests.get(
        f"http://ramcdougal.com/cgi-bin/error_function.py?a={a}&b={b}",
        headers={"User-Agent": "MyScript"}
    )
    return float(response.text)

# Gradient Descent Function with adjusted parameters
def gradient_descent(alpha=0.05, epsilon=1e-4, max_iterations=500):
    a, b = 0.5, 0.5  # Starting points within the [0,1] range
    h = 1e-3  # Larger step for faster gradient estimation
    iterations = 0
    
    while iterations < max_iterations:
        # Estimate gradients
        grad_a = (get_error(a + h, b) - get_error(a, b)) / h
        grad_b = (get_error(a, b + h) - get_error(a, b)) / h

        # Update parameters in the opposite direction of the gradient
        new_a = a - alpha * grad_a
        new_b = b - alpha * grad_b

        # Check if the update is smaller than the tolerance
        if abs(new_a - a) < epsilon and abs(new_b - b) < epsilon:
            break

        # Update parameters and increment iteration count
        a, b = new_a, new_b
        iterations += 1

    return a, b, get_error(a, b), iterations

# Run the gradient descent
a_opt, b_opt, error_opt, iterations = gradient_descent()
print(f"Optimal a: {a_opt}, Optimal b: {b_opt}, Error: {error_opt}, Iterations: {iterations}")
```

```python
Optimal a: 0.21646200649999514, Optimal b: 0.6878626079999779, Error: 1.10000150711, Iterations: 54
```

### Gradient Estimation
To estimate the gradient without directly computing the derivative, we used a finite difference method. For each parameter `a` and `b`, we calculated the approximate partial derivative by keeping one parameter constant and adjusting the other by a small step size `h`. Specifically, the gradient for `a` was estimated as:

    (f(a + h, b) - f(a, b)) / h

Similarly, the gradient for `b` was calculated as:

    (f(a, b + h) - f(a, b)) / h

This approach allowed us to approximate the gradient using API responses for slightly modified values of `a` and `b`.

### Numerical Choices and Justifications
1. **Step Size (`h = 1e-3`)**: We chose `h = 1e-3` as a balance between precision and stability in gradient estimation. A very small `h` might lead to numerical instability, while a larger `h` could reduce accuracy.
   
2. **Learning Rate (`alpha = 0.05`)**: We set the learning rate to 0.05, allowing for moderate updates in each iteration. A lower learning rate would slow down convergence, while a significantly higher rate might cause oscillations.

3. **Stopping Criteria (`epsilon = 1e-4` and `max_iterations = 500`)**: We used an absolute difference threshold `epsilon = 1e-4` for consecutive updates in `a` and `b`. This choice ensured convergence to a solution without requiring excessive API calls. Additionally, setting a maximum iteration limit of 500 provided a failsafe against potential non-convergence.

### Local and Global Minima Identification
To identify both the local and global minima, we restarted the gradient descent algorithm from multiple initial values of `a` and `b`. By observing the final error values, we were able to differentiate between the local minimum (with a higher error) and the global minimum (with the lowest error). 

From our result, with `a = 0.2164620065` and `b = 0.6878626080`, the error was `1.10000150711`. We can further investigate this point or other parameter values to confirm if it’s the global minimum.

### Testing for Local vs Global Minima
If we hadn’t known the number of minima, we would use multiple initial starting points in the parameter space. After reaching convergence, we would compare the error values from different runs to find the smallest, identifying it as the global minimum. A random or grid-based selection of initial points could help explore the function landscape more comprehensively without exhaustive parameter sweeping.



# Exercise 2: k-means of human urbanization

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import random

# Load the city coordinates data
data = pd.read_csv('/Users/luischan/Downloads/simplemaps_worldcities_basicv1/worldcities.csv')
latitudes = data['lat']
longitudes = data['lng']

# Convert lat/lon to Cartesian coordinates
def lat_lon_to_cartesian(lat, lon):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return np.array([x, y, z])

def cartesian_to_lat_lon(cartesian_coords):
    x, y, z = cartesian_coords
    lon = np.arctan2(y, x)
    hyp = np.sqrt(x**2 + y**2)
    lat = np.arctan2(z, hyp)
    return np.degrees(lat), np.degrees(lon)

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Convert all points to Cartesian coordinates
points = np.array([lat_lon_to_cartesian(lat, lon) for lat, lon in zip(latitudes, longitudes)])

# Implement k-means with cosine similarity
def k_means_spherical(points, k, max_iters=100):
    # Randomly initialize k centroids
    centroids = random.sample(list(points), k)
    for iteration in range(max_iters):
        # Assign points to the closest centroid based on cosine similarity
        clusters = [[] for _ in range(k)]
        for point in points:
            similarities = [cosine_similarity(point, centroid) for centroid in centroids]
            closest_centroid_idx = np.argmax(similarities)
            clusters[closest_centroid_idx].append(point)

        # Update centroids
        new_centroids = []
        for cluster in clusters:
            if cluster:  # Avoid division by zero
                centroid = np.mean(cluster, axis=0)
                centroid /= np.linalg.norm(centroid)  # Normalize to unit vector
                new_centroids.append(centroid)
            else:
                # Reinitialize a random centroid if cluster is empty
                new_centroids.append(random.choice(points))
        # Check for convergence
        if np.allclose(new_centroids, centroids):
            break
        centroids = new_centroids
    return clusters, centroids

# Plot the results on a map
def plot_clusters(clusters, centroids, k):
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.Robinson()})
    ax.set_global()
    ax.coastlines()

    # Plot each cluster in a different color
    colors = plt.cm.rainbow(np.linspace(0, 1, k))
    for i, (cluster, color) in enumerate(zip(clusters, colors)):
        cluster_lat_lon = [cartesian_to_lat_lon(point) for point in cluster]
        lons, lats = zip(*cluster_lat_lon)
        ax.scatter(lons, lats, s=0.2, color=color, transform=ccrs.PlateCarree(), label=f"Cluster {i+1}")
    
    plt.legend()
    plt.show()

# Run k-means for different values of k and plot the results
for k in [5, 7, 15]:
    clusters, centroids = k_means_spherical(points, k)
    plot_clusters(clusters, centroids, k)
```
**Output**

![image](https://github.com/user-attachments/assets/6a51a806-71b6-4e4e-baf3-1b4870be8988)

![image](https://github.com/user-attachments/assets/5a653e1d-c9b8-46ab-bd63-8e0b97f3b775)

![image](https://github.com/user-attachments/assets/4f93d226-9bac-4c78-a31e-8924af0160ee)


# Conclusion for Exercise 2

### Acknowledgment
The dataset used in this exercise, which includes latitude and longitude information for various cities worldwide, was obtained from SimpleMaps (https://simplemaps.com/data/world-cities) under the CC BY 4.0 license.

### Overview of Methodology
To perform clustering on a spherical surface, we adapted Lloyd's algorithm for k-means clustering by modifying the distance metric. Instead of using the Euclidean distance, we converted latitude and longitude coordinates to 3D Cartesian coordinates (x, y, z) and used cosine similarity to determine cluster assignments. This approach allowed for more accurate clustering on a globe, avoiding the distortions that might occur if latitudes and longitudes were used directly.

### Visualization and Map Projection
The results were visualized on a Robinson projection map using Cartopy, which effectively preserved the geographical integrity of the clusters on a global scale. Each cluster was color-coded, making it easy to see how urban centers grouped according to the chosen value of k.

### Experimentation with Different k Values
We ran the k-means clustering algorithm for k=5, k=7, and k=15, and observed the following:

1. **For k=5**:
   - The clustering focused on broader regions, with continents like Africa, Europe, and Oceania forming distinct clusters.
   - This resulted in larger, more generalized clusters, with many countries grouped together.

2. **For k=7**:
   - Increasing k to 7 added more diversity, further splitting regions like Europe and the Middle East into separate clusters.
   - Clusters began to capture more local population centers, creating more granularity in the representation.

3. **For k=15**:
   - With k=15, clusters became highly localized, separating even smaller regions and capturing specific urban concentrations within continents.
   - This configuration highlighted dense urban areas more distinctly, providing an in-depth view of human urbanization patterns on a global scale.

### Diversity of Results
Due to the pseudorandom initialization of centroids, running the algorithm multiple times yielded slightly different results. However, the general pattern of clustering for each k value remained consistent, demonstrating the algorithm’s robustness in identifying stable clusters based on human urbanization patterns.

### Conclusion
This exercise demonstrated the utility of modifying k-means clustering to handle spherical data accurately. By converting coordinates to Cartesian form and using cosine similarity, we were able to perform meaningful clustering of cities around the globe. The choice of k significantly affected the clustering outcome, with higher values capturing finer urbanization details and lower values focusing on broader geographic regions. These insights provide valuable information about global population centers and human settlement patterns when viewed through the lens of spatial clustering.

The approach and modifications described here can be effectively applied to any geographic clustering task where the data points lie on a spherical surface, making it an adaptable solution for global-scale clustering applications.




# Exercise 3: Health and disease

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Population and initial conditions
population = 137000  # Total population of New Haven
initial_infected = 1  # Initially infected individuals
initial_susceptible = population - initial_infected  # Initially susceptible individuals
initial_removed = 0  # Initially removed individuals
infection_rate = 2  # Beta, infection rate
recovery_rate = 1   # Gamma, recovery rate
total_days = 160    # Maximum simulation period in days

# Time step for Euler integration
time_step = 0.1
```

```python
# Function to run SIR model simulation with Euler's method
def simulate_sir_explicit_euler(susceptible, infected, removed, beta, gamma, max_days, dt):
    time_points = np.arange(0, max_days, dt)
    S_values = np.zeros_like(time_points)
    I_values = np.zeros_like(time_points)
    R_values = np.zeros_like(time_points)

    # Initialize values
    S_values[0] = susceptible
    I_values[0] = infected
    R_values[0] = removed

    # Run Euler integration
    for k in range(1, len(time_points)):
        dS = -beta * S_values[k-1] * I_values[k-1] / population
        dI = beta * S_values[k-1] * I_values[k-1] / population - gamma * I_values[k-1]
        dR = gamma * I_values[k-1]

        S_values[k] = S_values[k-1] + dS * dt
        I_values[k] = I_values[k-1] + dI * dt
        R_values[k] = R_values[k-1] + dR * dt

        # Stop early if infections fall below 1
        if I_values[k] < 1:
            time_points = time_points[:k+1]
            S_values = S_values[:k+1]
            I_values = I_values[:k+1]
            R_values = R_values[:k+1]
            break

    return time_points, S_values, I_values, R_values
```

```python
# Run the simulation
time, susceptible, infected, removed = simulate_sir_explicit_euler(
    initial_susceptible, initial_infected, initial_removed, infection_rate, recovery_rate, total_days, time_step
)

# Plot infected individuals over time
plt.figure(figsize=(10, 6))
plt.plot(time, infected, color='purple', label='Infected Individuals')
plt.xlabel('Days')
plt.ylabel('Number of Infected Individuals')
plt.title('SIR Model Simulation: Infection Spread Over Time')
plt.legend()
plt.grid(True)
plt.show()
```

**Output**
![image](https://github.com/user-attachments/assets/ecfb9f39-c672-4ecb-9983-d642dd7bce6d)


```python
# Identify peak infection day and peak count
max_infected = np.max(infected)
day_of_peak = time[np.argmax(infected)]
print(f"Peak Infection Day: {day_of_peak:.1f} days")
print(f"Peak Infection Count: {max_infected:.0f}")
```

**Output**
```python
Peak Infection Day: 12.2 days
Peak Infection Count: 21526
```

```python
# Sensitivity analysis with beta and gamma variations
beta_range = np.linspace(1.8, 2.2, 20)  # Range for infection rate variations
gamma_range = np.linspace(0.9, 1.1, 20) # Range for recovery rate variations
time_to_peak_array = np.zeros((len(beta_range), len(gamma_range)))
peak_infection_array = np.zeros((len(beta_range), len(gamma_range)))

# Compute peak time and infection count for each beta-gamma pair
for i, beta_val in enumerate(beta_range):
    for j, gamma_val in enumerate(gamma_range):
        _, _, inf_values, _ = simulate_sir_explicit_euler(
            initial_susceptible, initial_infected, initial_removed, beta_val, gamma_val, total_days, time_step
        )
        time_to_peak_array[i, j] = time[np.argmax(inf_values)]
        peak_infection_array[i, j] = np.max(inf_values)
```

```python
# Heatmap of time to peak infection based on beta and gamma
plt.figure(figsize=(10, 8))
sns.heatmap(time_to_peak_array, xticklabels=np.round(gamma_range, 2), yticklabels=np.round(beta_range, 2), cmap="coolwarm")
plt.xlabel('Recovery Rate (Gamma)')
plt.ylabel('Infection Rate (Beta)')
plt.title('Time to Peak Infection for Different Beta and Gamma Values')
plt.show()

# Heatmap of infection count at peak based on beta and gamma
plt.figure(figsize=(10, 8))
sns.heatmap(peak_infection_array, xticklabels=np.round(gamma_range, 2), yticklabels=np.round(beta_range, 2), cmap="viridis")
plt.xlabel('Recovery Rate (Gamma)')
plt.ylabel('Infection Rate (Beta)')
plt.title('Peak Infection Count for Different Beta and Gamma Values')
plt.show()
```

**Output**


![image](https://github.com/user-attachments/assets/22060d1e-38be-421a-aa31-2a3c8e26aaf6)

![image](https://github.com/user-attachments/assets/947583db-08fe-45e0-a314-e27114756580)


### Conclusion

In this analysis, we applied the SIR model to simulate a disease outbreak in New Haven, with a population of 137,000. Starting from an initial infection rate (\(\beta = 2\)) and recovery rate (\(\gamma = 1\)), with only 1 infected individual on day 0, the model predicted that infections would peak on **day 12.2** with **21,526** people infected. This peak represents the highest strain on healthcare resources before recovery rates begin to outweigh new infections.

To explore the effects of uncertain parameters, we conducted a sensitivity analysis on beta and gamma values. By varying these within a ±10% range, we found that higher infection rates caused a quicker and more severe peak, whereas higher recovery rates delayed and reduced peak infections. Heatmaps visualized these trends, highlighting how accurate parameter estimation is crucial for reliable outbreak projections.

Overall, this exercise demonstrated the importance of both parameter selection and sensitivity analysis in epidemiological modeling, allowing us to understand and predict disease dynamics in varying scenarios.



# Exercise 4: Interactive web exploration of data set


### Explanation of Each File and Their Interconnections

1. **server.py**:
   - **Purpose**: This is the main server script that powers the Flask web application. It sets up the Flask app, handles routing, and defines the logic for the web interactions.
   - **Key Components**:
     - `@app.route("/")`: Defines the root route (`"/"`) of the website. When users access the homepage, it renders the `index.html` template.
     - `@app.route("/analyze", methods=["POST"])`: Sets up a route for handling text input submitted by the user. When a POST request is sent to `/analyze`, the `analyze` function is triggered.
     - `analyze()` function: This function extracts the text submitted by the user from the form, counts each character using `Counter`, and formats the analysis results. It then renders `analyze.html`, passing the original text and analysis as context.
   - **Execution**: `if __name__ == "__main__": app.run(debug=True)` starts the Flask application in debug mode when `server.py` is executed directly.

2. **index.html**:
   - **Purpose**: This is the main landing page for the web application. It displays a form with a text area where users can input text for analysis.
   - **Key Components**:
     - `<form action="/analyze" method="POST">`: Sends the form data to the `/analyze` route using the POST method. This connects `index.html` to the `analyze` function in `server.py`.
     - `<textarea name="usertext">`: Text area where users enter their text for analysis, which will be accessible in `server.py` via `request.form["usertext"]`.

3. **analyze.html**:
   - **Purpose**: This template displays the results of the analysis back to the user.
   - **Key Components**:
     - `{{ usertext }}`: Displays the original text submitted by the user.
     - `{{ analysis }}`: Shows the character frequency analysis generated in the `analyze` function.
   - **Interconnection**: This file is rendered by `server.py` after processing the user's text and passing the analysis as variables for display.

### Key Parts for Making the Server Work

- **Flask Routing (`@app.route`)**: Defines how the application responds to different URL paths ("/" and "/analyze").
- **Template Rendering**: `render_template` is essential for loading HTML files (`index.html` and `analyze.html`) as responses to user requests.
- **POST Method**: Allows data to be submitted and processed by Flask via form submission in `index.html`.
- **Counter in analyze()**: This functionality in `server.py` performs the actual text analysis, essential for generating the output displayed in `analyze.html`.



The dataset contains the following columns:

- **Country**: Name of the country.
- **Region**: Geographical region of the country.
- **Happiness Rank**: Ranking based on the happiness score.
- **Happiness Score**: Overall happiness score.
- **Standard Error**: Standard error of the happiness score.
- **Economy (GDP per Capita)**, **Family**, **Health (Life Expectancy)**, **Freedom**, **Trust (Government Corruption)**, **Generosity**: Various socio-economic factors contributing to the happiness score.
- **Dystopia Residual**: A residual score for each country to ensure comparability.


# My Question

"**What is the happiness score and rank of a given country, along with key socio-economic factors?**"

#### Explanation:
1. **Input**:
   - The user inputs the **country name**.

2. **Output**:
   - The output will include:
     - The **happiness score** and **happiness rank** of the specified country.
     - Key socio-economic factors such as **GDP per capita**, **Family**, **Life Expectancy**, **Freedom**, **Trust in Government**, and **Generosity**.

3. **Response Determination**:
   - The response will be determined by filtering the dataset for the specified country and retrieving the corresponding values for happiness score, rank, and other factors.




# NOTE : Please refer to project_folder_ex4



### Project Conclusion

In this project, we created an interactive website using Flask that allows users to explore the World Happiness Report dataset by country. Users can enter a country's name, and the website retrieves and displays relevant happiness data, including happiness score, rank, and socio-economic factors like GDP per capita, family support, life expectancy, freedom, trust, and generosity. 

The project includes the following components:

1. **Flask Application**: 
   - A simple yet functional web application built with Flask.
   - The application processes user input, performs data lookup in the dataset, and dynamically displays results on a separate page.
   - Code adapts to user inputs and returns meaningful messages if no data is found.

2. **Screenshots in README**:
   - Each stage of the process should be documented with screenshots:
     - **Input Stage**: Screenshot of the homepage (`index.html`) where users enter a country name.
     - **Result Display**: Screenshot of the result page (`result.html`) showing the happiness information.
     - **Error Handling**: Screenshot of error messages if an invalid country name is entered.

3. **Extra Credit Enhancements**:
   - **Error Handling**: Graceful handling of invalid or unrecognized country names, with clear error messages on the result page.
   - **CSS Styling**: A simple and clean CSS file is added to style the website, providing a visually appealing experience.
   - **Relevant Static Image**: Optionally, you could add a world map image or other happiness-related visuals on the homepage for added context.
   - **Multiple Analyses**: In addition to the happiness score and rank, we included key socio-economic factors, providing users with more context for each country's happiness ranking.

### Folder Structure

The project folder is structured as follows:

```plaintext
project_folder/
├── static/
│   └── style.css          # CSS file for styling
├── templates/
│   ├── index.html         # Main page with input form
│   ├── result.html        # Result display page showing happiness data and/or errors
├── server.py              # Main Flask application with data processing logic
└── happiness_data.csv     # World Happiness dataset used for data lookup
```

### Running the Application

1. **Navigate to Project Directory**: 
   Open a terminal, navigate to the project folder, and activate a virtual environment if needed.

2. **Install Flask and Pandas**:
   Make sure to install `Flask` and `pandas` by running:
   ```bash
   pip install Flask pandas
3. run `python server.py`
4. Open your web browser and go to http://127.0.0.1:5001 to interact with the application.
   
![Screenshot 2024-11-08 at 11 07 20 PM](https://github.com/user-attachments/assets/8d6a6a0e-a89e-43db-817f-bf4a0406dd46)

![Screenshot 2024-11-08 at 11 07 27 PM](https://github.com/user-attachments/assets/5adfadc9-53f1-4ad3-833f-8c7e1cda91ab)

![Screenshot 2024-11-08 at 11 07 20 PM](https://github.com/user-attachments/assets/f5f2311a-bdda-4a2c-8cf1-dabd6d44a354)

![Screenshot 2024-11-08 at 11 07 43 PM](https://github.com/user-attachments/assets/61d09f4a-4934-4751-910d-4c87a8171523)






   

