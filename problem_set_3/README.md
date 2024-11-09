# Problem Set 3

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
