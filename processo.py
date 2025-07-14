class Processo:
    def __init__(self, pid, prioridade, offset_memoria, blocos_memoria, impressora, scanner, modem, disco, tempo_cpu):
        self.pid = pid
        self.prioridade = prioridade
        self.offset_memoria = offset_memoria  # posição inicial na memória
        self.blocos_memoria = blocos_memoria
        self.impressora = bool(impressora)
        self.scanner = bool(scanner)
        self.modem = bool(modem)
        self.disco = bool(disco)
        self.tempo_restante = tempo_cpu
        self.estado = "pronto"  # ou "executando", "finalizado"

    def exibir_info(self):
        print(f"PID: {self.pid}")
        print(f"Prioridade: {self.prioridade}")
        print(f"Offset da memória: {self.offset_memoria}")
        print(f"Blocos alocados: {self.blocos_memoria}")
        print(f"Impressora: {self.impressora}")
        print(f"Scanner: {self.scanner}")
        print(f"Modem: {self.modem}")
        print(f"Disco: {self.disco}")
