from modelo_comunicacao import EncoderModelo, CanalModelo, DecoderModelo

def executar_modelo(vetor_entrada, variancia):  # Nome atualizado
    encoder = EncoderModelo()
    canal = CanalModelo(variancia)
    decoder = DecoderModelo()
    print(texto_para_bits(vetor_entrada))
    saida_encoder = encoder.processar(texto_para_bits(vetor_entrada))
    saida_canal = canal.processar(saida_encoder)
    saida_decoder = decoder.processar(saida_canal)
    saida_texto = bits_para_texto(saida_decoder)
    print(saida_texto)
    taxa_erro = calcular_taxa_erro(saida_encoder, saida_decoder)

    return {
        "saida_encoder": saida_encoder,
        "saida_canal": saida_canal,
        "saida_decoder": saida_decoder,
        "taxa_erro": f'{round(taxa_erro*len(saida_encoder))}/{len(saida_encoder)}',
        "entrada_texto":vetor_entrada,
        "saida_texto":saida_texto
    }

def calcular_taxa_erro(v_entrada, saida):
    entrada = [int(bit)for bit in v_entrada]
    erros = sum(1 for e, s in zip(entrada, saida) if e != s)
    return erros / len(entrada)

def texto_para_bits(texto):
    bits = ''.join(format(ord(char), '08b') for char in texto)  # Converte cada char em 8 bits
    return [int(bit) for bit in bits]

def bits_para_texto(bits):
    bits_01 = [1 if bit > 0 else 0 for bit in bits]
    caracteres = [chr(int(''.join(map(str, bits_01[i:i+8])), 2)) for i in range(0, len(bits), 8)]
    return ''.join(caracteres)
