import numpy as np
import matplotlib.pyplot as plt

in_array = [1, 1.2, 1.488, 1.6, 1.8, 2]
out_array = np.log(in_array)

print("out_array : ", out_array)

plt.plot(in_array, in_array,
         color='blue', marker="*")

# red for numpy.log()
plt.plot(out_array, in_array,
         color='red', marker="o")

plt.title("numpy.log()")
plt.xlabel("out_array")
plt.ylabel("in_array")
plt.savefig("./sandbox/tmp/graph.png")