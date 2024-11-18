"""
================================================
Coding - Decoding simulation of a random message
================================================

This example shows a simulation of the transmission of a binary message
through a gaussian white noise channel with an LDPC coding and decoding system.
"""

import numpy as np
from pyldpc import make_ldpc, decode, get_message, encode
from matplotlib import pyplot as plt

# n = 4 * 10 bytes (sinal codificada)
# k é a mensagem original, sem codificação
# R = 1 / 4, então k = 10 bytes em teoria, na pratica fica 82 bits, mas é só concatenar dois zeros.
n = 4*8*10
d_v = 3
d_c = 4
seed = np.random.RandomState(42)
##################################################################
# First we create an LDPC code i.e a pair of decoding and coding matrices
# H and G. H is a regular parity-check matrix with d_v ones per row
# and d_c ones per column

H, G = make_ldpc(n, d_v, d_c, seed=seed, systematic=True, sparse=True)

n, k = G.shape
print("Number of coded bits:", k)

##################################################################
# Now we simulate transmission for different levels of noise and
# compute the percentage of errors using the bit-error-rate score
# The coding and decoding can be done in parallel by column stacking.

errors = []
snrs = np.linspace(-3, 1, 10)
v = np.arange(k) % 2  # fixed k bits message
n_trials = 100  # number of transmissions with different noise
V = np.tile(v, (1, 1)).T  # stack v in columns

for snr in snrs:
    error = 0.

    for i in range(n_trials):
        y = encode(G, V, snr, seed=seed)
        D = decode(H, y, snr)

        x = get_message(G, D)
        error += abs(v - x).sum()

    error /= k * n_trials
    errors.append(error)

print(snrs)
print(errors)

plt.figure()
plt.plot(snrs, errors, color="indianred")
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.ylabel("Bit error rate (log scale)")
plt.xlabel("SNR")
plt.title("Bit Error Rate vs SNR")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()
