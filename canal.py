import numpy as np

class Canal:
    def transmitir(self, vetor, variancia):
        ruido = np.random.normal(0, np.sqrt(variancia), len(vetor)) # Canal AWGM
        return [round(bit + ruido[i],2) for i, bit in enumerate(vetor)]
