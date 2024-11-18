from test_pyldpc import *

H, G = initialize_matrices()

default_message = "Esta é uma mensagem de texto, que deve conter 140 caracteres. Pode não parecer, mas 140 caracteres é bastante coisa. Viu só? Enrolei mas foi"

msg = input("Digite a mensagem de teste a ser enviada (max 140 caracteres), ou deixe em branco para uma mensagem padrão.\n\nMensagem > ")

# Verifica se a mensagem tem mais de 140 caracteres
if len(msg) == 0:
    msg = default_message
elif len(msg) > 140:
    print("Erro: A mensagem excede o limite de 140 caracteres.")
    exit()

print("\nTamanho da mensagem a ser enviada (caracteres):", len(msg))
print(f"\nMensagem: \"{msg}\"")

# Solicita a variância do ruído gaussiano
variance = float(input("Digite agora a variância do ruído gaussiano no canal discreto: "))

print("Enviando mensagem...\n\n")

# Calcula o SNR a partir da variância
snr_db = variance_to_SNR_db(variance)

# Envia a mensagem e recebe a mensagem decodificada
received_msg = transmit_message(msg, G, H, snr_db)

# Converte a mensagem original e a mensagem recebida em arrays de bits
original_bits = string_to_numpy_bitarray(msg)
received_bits = string_to_numpy_bitarray(received_msg)

# Calcula o número de erros de bits
num_errors = np.sum(original_bits != received_bits)

# Calcula a taxa de erro de bits (BER)
ber = num_errors / len(original_bits) * 100

# Exibe a mensagem recebida e a taxa de erro
print(f"\nMensagem recebida: \"{received_msg}\"")
print(f"Quantidade de erros de caractere: {num_errors}")
print(f"Taxa de erro de bits (BER): {ber:.2f}%")
