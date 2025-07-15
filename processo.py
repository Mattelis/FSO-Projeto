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

    def exibir_info(self):
        print("dispatcher =>")
        print(f" PID: {self.pid}")
        print(f" offset: {self.offset_memoria}")
        print(f" blocks: {self.blocos_memoria}")
        print(f" priority: {self.prioridade}")
        print(f" time: {self.tempo_restante}")
        print(f" printers: {int(self.impressora)}")
        print(f" scanners: {int(self.scanner)}")
        print(f" modems: {int(self.modem)}")
        print(f" drives: {int(self.disco)}")
