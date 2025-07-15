class Processo:
    def __init__(self, pid, tempo_inicializacao, prioridade, tempo_cpu, blocos_memoria, impressora, scanner, modem, disco):
        self.pid = pid
        self.tempo_inicializacao = tempo_inicializacao
        self.prioridade = prioridade
        self.tempo_restante = tempo_cpu
        self.blocos_memoria = blocos_memoria
        self.impressora = int(impressora)
        self.scanner = int(scanner)
        self.modem = int(modem)
        self.disco = int(disco)
        self.offset_memoria = 0  # posição inicial na memória
        self.estado = "pronto"  # ou "executando", "finalizado"

    # TODO: colocar o formato de impressão do dispchaer conforme o pdf da especificaçao
    def exibir_info(self):
        print(f"PID: {self.pid}")
        print(f"Tempo de inicialização: {self.tempo_inicializacao}")
        print(f"Prioridade: {self.prioridade}")
        print(f"Offset da memória: {self.offset_memoria}")
        print(f"Blocos alocados: {self.blocos_memoria}")
        print(f"Impressora: {self.impressora}")
        print(f"Scanner: {self.scanner}")
        print(f"Modem: {self.modem}")
        print(f"Disco: {self.disco}")
