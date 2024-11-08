import matplotlib
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use("Agg")


def nrz_l(data):
    signal = np.where(data == 0, -1, 1)
    return signal


def nrz_i(data):
    signal = np.zeros(len(data), dtype=int)
    current_level = -1 if data[0] == 0 else 1  # Start at bottom if first bit is 0, otherwise start with a transition

    for i in range(len(data)):
        if data[i] == 1:
            # Transition to the opposite level if the bit is 1
            current_level = -current_level
        # If data[i] is 0, remain at the current level
        signal[i] = current_level

    return signal


def bipolar_ami(data):
    signal = np.zeros(len(data), dtype=int)
    current_level = 1  # Start with a positive level for the first 1 bit

    for i in range(len(data)):
        if data[i] == 1:
            signal[i] = current_level
            current_level = -current_level  # Alternate the level for successive 1s
        # If data[i] == 0, signal[i] remains 0

    return signal


def pseudoternary(data):
    signal = np.zeros(len(data), dtype=int)
    current_level = 1  # Start with a positive level for the first 0 bit

    for i in range(len(data)):
        if data[i] == 0:
            signal[i] = current_level
            current_level = -current_level  # Alternate the level for successive 0s
        # If data[i] == 1, signal[i] remains 0 (no line signal)

    return signal


def manchester(data):
    x_values = []
    y_values = []

    for i, bit in enumerate(data):
        # Define the time intervals for each bit
        t_start = i
        t_mid = i + 0.5
        t_end = i + 1

        if bit == 0:
            # For 0: Start high, transition to low at midpoint
            x_values += [t_start, t_mid, t_mid, t_end]
            y_values += [1, 1, -1, -1]
        else:
            # For 1: Start low, transition to high at midpoint
            x_values += [t_start, t_mid, t_mid, t_end]
            y_values += [-1, -1, 1, 1]

    return x_values, y_values


def differential_manchester(data):
    x_values = []
    y_values = []

    # Initialize the current signal level; assuming we start at the bottom
    current_level = 1

    for i, bit in enumerate(data):
        # Define time intervals for each bit
        t_start = i
        t_mid = i + 0.5
        t_end = i + 1

        if bit == 0:
            # 0 bit: Transition at the start and again at the center
            current_level *= -1  # Transition at start
            x_values += [t_start, t_start, t_mid]
            y_values += [current_level, current_level, -current_level]
        else:
            # 1 bit: No transition at start, only at the center
            x_values += [t_start, t_mid]
            y_values += [current_level, -current_level]

        # Midpoint transition for both 0 and 1
        current_level *= -1
        x_values += [t_mid, t_end]
        y_values += [current_level, current_level]

    return x_values, y_values


binary_data = np.array([0, 1, 0, 0, 1, 1, 1, 0])

nrz_l_signal = nrz_l(binary_data)
nrz_i_signal = nrz_i(binary_data)
bipolar_ami_signal = bipolar_ami(binary_data)
pseudoternary_signal = pseudoternary(binary_data)
manchester_signal = manchester(binary_data)
# diff_manchester_signal = differential_manchester(binary_data)

# Visualization
plt.figure(figsize=(12, 8))


plt.subplot(3, 2, 1)
plt.step(range(len(binary_data)), nrz_l_signal, where='post')
plt.xticks(range(len(binary_data)), binary_data)  # Set binary data as x-ticks
plt.grid(True)
plt.title("NRZ-L")

plt.subplot(3, 2, 2)
# plt.figure(figsize=(6, 4))
plt.step(range(len(nrz_i_signal)), nrz_i_signal, where='post')
plt.xticks(range(len(binary_data)), binary_data)  # Display binary data as x-ticks
plt.grid(True)
plt.title("NRZ-I")
# plt.ylim(-1.5, 1.5)

plt.subplot(3, 2, 3)
plt.step(range(len(binary_data)), bipolar_ami_signal, where='post')
plt.xticks(range(len(binary_data)), binary_data)
plt.grid(True)
plt.title("Bipolar AMI")

plt.subplot(3, 2, 4)
plt.step(range(len(binary_data)), pseudoternary_signal, where='post')
plt.xticks(range(len(binary_data)), binary_data)
plt.grid(True)
plt.title("Pseudoternary")

plt.subplot(3, 2, 5)
x_values, y_values = manchester(binary_data)
plt.step(x_values, y_values, where='post')
plt.xticks(range(len(binary_data)), binary_data)  # Display binary data as x-ticks
plt.grid(True)
plt.title("Manchester")

plt.subplot(3, 2, 6)
x_values, y_values = differential_manchester(binary_data)
plt.step(x_values, y_values, where='post')
plt.xticks(range(len(binary_data)), binary_data)  # Display binary data as x-ticks
plt.title("Differential Manchester Encoding")
plt.grid(True)

plt.tight_layout()
# plt.show()
