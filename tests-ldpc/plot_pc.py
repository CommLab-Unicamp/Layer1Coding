import matplotlib.pyplot as plt
import numpy as np
import math

def variance_to_SNR_db(variance):
    snr_db = 10 * math.log10(1 / variance)
    return snr_db

# Função para ler os dados do arquivo
def read_data(filename):
    snr = []
    pc = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            snr_value = float(parts[0].split('=')[1].strip())
            pc_value = float(parts[1].split('=')[1].strip())
            snr.append(snr_value)
            pc.append(pc_value)
    return snr, pc

# Lê os dados do arquivo
filename = 'dados_pc.txt'
snr_db, pc = read_data(filename)

# Variâncias para as linhas verticais
variances = [1, 2]
vertical_lines = [variance_to_SNR_db(var) for var in variances]

# Configuração do gráfico
plt.figure(figsize=(10, 6))

# Plota os dados fornecidos
plt.semilogy(snr_db, pc, marker='o', label='Probabilidade de erro Pc')

# Adiciona linhas verticais para as variâncias
for var, line_pos in zip(variances, vertical_lines):
    plt.axvline(x=line_pos, color='r', linestyle='--', label=f'Variância = {var}')

# Configurações dos eixos e título
plt.title('Código LDPC de taxa R = 1/4 e energia de símbolo Es = 1', fontsize=14)
plt.xlabel('SNR (dB) = $E_s / \\sigma^2$ (dB)', fontsize=12)
plt.ylabel('Probabilidade de erro de caractere Pc', fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Adiciona a legenda
plt.legend(fontsize=10)

# Mostra o gráfico
plt.tight_layout()
plt.show()
