from test_pyldpc import *

# Inicializa as matrizes H e G
H, G = initialize_matrices()

# Define a mensagem padrão
default_message = "Esta é uma mensagem de texto, que deve conter 140 caracteres. Pode não parecer, mas 140 caracteres é bastante coisa. Viu só? Enrolei mas foi"

# Solicita a entrada do usuário
msg = input("Digite a mensagem de teste a ser enviada (max 140 caracteres), ou deixe em branco para uma mensagem padrão.\n\nMensagem > ")

# Verifica se a mensagem tem mais de 140 caracteres
if len(msg) == 0:
    msg = default_message
elif len(msg) > 140:
    print("Erro: A mensagem excede o limite de 140 caracteres.")
    exit()

# Exibe informações da mensagem
print("\nTamanho da mensagem a ser enviada (caracteres):", len(msg))
print(f"\nMensagem: \"{msg}\"\n")

# Solicita a variância do ruído gaussiano
variance = float(input("Digite agora a variância do ruído gaussiano no canal discreto: "))

print("\nEnviando mensagem...\n")

# Calcula o SNR a partir da variância
snr_db = variance_to_SNR_db(variance)

# Envia a mensagem e recebe a mensagem decodificada
received_msg = transmit_message(msg, G, H, snr_db)

# Calcula o número de erros de caractere
num_char_errors = sum(1 for a, b in zip(msg, received_msg) if a != b)

# Calcula a taxa de erro de caracteres
char_error_rate = num_char_errors / len(msg) * 100

# Exibe a mensagem recebida e a taxa de erro de caracteres
print(f"\nMensagem recebida: \"{received_msg}\"")
print(f"\nQuantidade de erros de caracteres: {num_char_errors}")
print(f"Taxa de erro de caracteres: {char_error_rate:.2f}%")
