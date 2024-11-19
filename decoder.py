class Decoder:
    def decodificar(self, vetor):
        return [1 if bit > 0 else 0 for bit in vetor]
