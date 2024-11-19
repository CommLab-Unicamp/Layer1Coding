from encoder import Encoder
from canal import Canal
from decoder import Decoder

class EncoderModelo:
    def __init__(self):
        self.encoder = Encoder()

    def processar(self, vetor):
        # Implementacao especifica do Encoder
        return self.encoder.codificar(vetor)

class CanalModelo:
    def __init__(self,variancia):
        self.canal = Canal()
        self.variancia = variancia

    def processar(self, vetor):
        # Implementacao especifica do Canal AWGN
        return self.canal.transmitir(vetor, self.variancia)

class DecoderModelo:
    def __init__(self):
        self.decoder = Decoder()

    def processar(self, vetor):
        # Implementacao especifica do Decoder
        return self.decoder.decodificar(vetor)
