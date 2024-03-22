import numpy as np

# Calculate option prices using the explicit finite difference method
def fd_option_pricing(option_type, S0, K, r, T, sigma, Smax, N, M):    
    dt = T / N
    ds = Smax / M
    print('dt:', dt, 'ds:', ds)
    S = np.arange(M + 1) * ds
    t = np.arange(N + 1) * dt

    alpha = 0.5 * sigma**2 * dt / ds**2
    beta = 0.5 * r * dt / ds
    gamma = r * dt
    
    # Initialize terminal condition
    C = np.zeros((M + 1, N + 1))
    if option_type == 'C':
        C[:, -1] = np.maximum(S - K, 0)
    elif option_type == 'P':
        C[:, -1] = np.maximum(K - S, 0)

    # Apply explicit finite difference method
    for j in range(N - 1, -1, -1):
        for i in range(1, M):
            C[i, j] = alpha * C[i + 1, j + 1] + (1 - 2 * alpha - beta + gamma) * C[i, j + 1] + alpha * C[i - 1, j + 1] + beta * C[i + 1, j + 1]

        # Apply boundary conditions
        if option_type == 'C':
            C[0, j] = 0
            C[-1, j] = Smax - K * np.exp(-r * (N - j) * dt)
        elif option_type == 'P':
            C[0, j] = K * np.exp(-r * (N - j) * dt)
            C[-1, j] = 0

    # Interpolate to get option price at S0
    C_fd = np.interp(S0, S, C[:, 0])
    return C_fd

# Example
T, S0, K, sigma, r, S_max, N, M  = 0.049, 30095, 25000, 0.649, 0.0014, K*2, 1000, 100

option_price = fd_option_pricing('C',S0, K, r, T, sigma, S_max)
print(option_price)
