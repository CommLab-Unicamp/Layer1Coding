import numpy as np
from pyldpc import make_ldpc, decode, get_message, encode, utils
from matplotlib import pyplot as plt
import math
import pickle
import os

CACHE_FILE = 'ldpc_matrices_cache.pkl'

def string_to_numpy_bitarray(s):
    """
    Converte uma string para um array numpy de bits.
    """
    bit_array = ''.join(f'{ord(c):08b}' for c in s)
    return np.array([int(bit) for bit in bit_array])

def numpy_bitarray_to_string(bitarray):
    """
    Converte um array numpy de bits para uma string.
    """
    bit_string = ''.join(str(bit) for bit in bitarray)
    chars = [chr(int(bit_string[i:i+8], 2)) for i in range(0, len(bit_string), 8)]
    return ''.join(chars)

def encode_message(tG, v):
    """
    Codifica uma mensagem binária utilizando a matriz de codificação transposta.
    """
    return utils.binaryproduct(tG, v)

def modulate_bpsk(d):
    """
    Modula a mensagem codificada utilizando modulação BPSK.
    """
    return 1 - 2*d  # 0 -> 1, 1 -> -1

def add_noise(x, snr_db, seed=None):
    """
    Adiciona ruído gaussiano à mensagem modulada.
    """
    rng = utils.check_random_state(seed)
    sigma = 10 ** (-snr_db / 20)
    e = rng.randn(*x.shape) * sigma  # Ruído gaussiano
    return x + e

def initialize_matrices():
    """
    Inicializa as matrizes do decodificador e retorna.
    Verifica se as matrizes já estão em cache e as carrega.
    """
    n = 4 * 8 * 140
    d_v = 3
    d_c = 4
    
    # Verifica se o cache já existe
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as cache_file:
            cached_data = pickle.load(cache_file)
            cached_n, cached_d_v, cached_d_c, H, G = cached_data
            # Se os parâmetros não mudaram, retorna as matrizes em cache
            if (n == cached_n) and (d_v == cached_d_v) and (d_c == cached_d_c):
                print("Loaded matrices from cache.")
                return H, G
    
    # Se não existir cache ou parâmetros mudaram, gera as matrizes
    print("Generating new matrices...")
    seed = np.random.RandomState(42)
    H, G = make_ldpc(n, d_v, d_c, seed=seed, systematic=True, sparse=True)

    n, k = G.shape
    print("Number of message bits:", k)
    print("Number of coded bits:", n)
    print(f"Code rate {k/n = }")

    # Salva as matrizes e parâmetros no cache
    with open(CACHE_FILE, 'wb') as cache_file:
        pickle.dump((n, d_v, d_c, H, G), cache_file)
        print("Matrices saved to cache.")

    return H, G

def transmit_message(message, G, H, snr_db):
    """
    Simula o envio de uma mensagem com um único SNR (dB).
    A função converte a mensagem para bits, realiza a transmissão com modulação e decodificação,
    e retorna a string recebida após a decodificação, removendo os caracteres nulos no final.
    """
    v = string_to_numpy_bitarray(message)
    
    # Preenche com zeros até que a mensagem tenha 1122 bits
    v = np.concatenate((v, np.zeros(1122 - len(v), dtype=int)))
    
    # Codifica a mensagem
    d = encode_message(G, v)
    
    # Modula utilizando BPSK
    x = modulate_bpsk(d)
    
    # Adiciona ruído
    y = add_noise(x, snr_db)
    
    # Decodifica a mensagem
    D = decode(H, y, snr_db)
    x_decoded = get_message(G, D)
    
    # Converte os bits decodificados de volta para a string original
    decoded_message = numpy_bitarray_to_string(x_decoded)
    
    # Remove os caracteres nulos (zeros) no final da mensagem
    decoded_message = decoded_message.rstrip('\x00')
    
    # Retorna a mensagem decodificada sem os zeros no final
    return decoded_message

def variance_to_SNR_db(variance):
    snr_db = 10 * math.log(1 / variance)
    return snr_db

if __name__ == "__main__":
    # Inicializa as matrizes H e G
    H, G = initialize_matrices()

    # Defina o SNR e a mensagem de teste
    test_message = "Esta é uma mensagem de texto, que deve conter 140 caracteres. Pode não parecer, mas 140 caracteres é bastante coisa. Viu só? Enrolei mas foi"
    print(f"{len(test_message) = }")

    for snrs_db in [-3, -2, -1, 0, 1]:
        received = transmit_message(test_message, G, H, snrs_db)
        print(f"{snrs_db = }, {received = }")
