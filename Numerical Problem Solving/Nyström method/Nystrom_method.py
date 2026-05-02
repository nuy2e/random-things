import numpy as np
import matplotlib.pyplot as plt

def forcing_function(x: np.ndarray) -> np.ndarray:
    """
    Evaluates the forcing function f(x) = 1 - x.

    Args:
        x (np.ndarray): Array of spatial coordinates.

    Returns:
        np.ndarray: Evaluated values of the forcing function.
    """
    return 1 - x

def exact_solution(x: np.ndarray) -> np.ndarray:
    """
    Evaluates the exact analytical solution of the Fredholm integral equation.

    Args:
        x (np.ndarray): Array of spatial coordinates.

    Returns:
        np.ndarray: Evaluated values of the exact solution.
    """
    term1 = 1 - x
    coef = 2 * (4 - np.pi) / (np.pi**2 - 4)
    term2 = np.pi * np.cos(x) + 2 * np.sin(x)
    
    return term1 + coef * term2

def solve_fredholm_nystrom(N: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Solves the Fredholm integral equation using the Nystrom method 
    with rectangular approximation.

    Args:
        N (int): Number of integration intervals/nodes.

    Returns:
        tuple: A tuple containing:
            - x_nodes (np.ndarray): The midpoints of the integration intervals.
            - y_num (np.ndarray): The calculated numerical solution at the nodes.
    """
    # 1. Define the grid nodes (midpoints of the intervals)
    x_edges = np.linspace(0, np.pi/2, N+1)
    x_nodes = (x_edges[:-1] + x_edges[1:]) / 2

    # 2. Construct the Kernel matrix K
    diff_matrix = x_nodes[:, np.newaxis] - x_nodes[np.newaxis, :]
    K = np.cos(diff_matrix)

    # 3. Construct the identity matrix and the main operator matrix M
    I = np.eye(N)
    M = I - K / N

    # 4. Evaluate the forcing function vector
    f_vec = forcing_function(x_nodes)

    # 5. Solve the linear system M * y = f
    y_num = np.linalg.inv(M) @ f_vec

    return x_nodes, y_num

def plot_results(x_nodes: np.ndarray, y_num: np.ndarray) -> None:
    """
    Plots the numerical solution against the exact analytical solution.

    Args:
        x_nodes (np.ndarray): The grid points where the numerical solution was evaluated.
        y_num (np.ndarray): The numerical solution values.
    """
    N = len(x_nodes)
    plt.figure(figsize=(8, 6))

    # Generate a dense grid for a smooth analytical curve
    x_smooth = np.linspace(0, np.pi/2, 200)
    y_smooth = exact_solution(x_smooth)

    # Plot lines
    plt.plot(x_smooth, y_smooth, color='red', linestyle='-', linewidth=2, 
             label='Exact Solution')
    plt.plot(x_nodes, y_num, color='blue', marker='o', linestyle='--', 
             markersize=8, label=f'Numerical (N={N})')

    # Formatting
    plt.title('Numerical vs. Exact Solution of the Fredholm Integral Equation', 
              fontsize=14, pad=15)
    plt.xlabel('x (radians)', fontsize=12)
    plt.ylabel('y(x)', fontsize=12)
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xlim([0, np.pi/2])
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    # Define the number of chunks/nodes
    NUMBER_OF_NODES = 5
    
    # Calculate solutions
    nodes, numerical_solution = solve_fredholm_nystrom(NUMBER_OF_NODES)
    
    # Visualize the results
    plot_results(nodes, numerical_solution)