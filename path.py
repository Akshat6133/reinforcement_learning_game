from os import getcwd
c = getcwd()
print(c)

import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
# Plot the data
plt.plot(x, y)
# Set the title and labels
plt.title("Sine Wave")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
# Save the plot as a PNG, JPEG and PDF files
plt.savefig(f"{c}/output/sine_wave.png")
plt.savefig(f"{c}/output/sine_wave.jpg")
plt.savefig(f"{c}/output/sine_wave.pdf")