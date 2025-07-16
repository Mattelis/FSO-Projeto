class GerenciadorDeMemoria:

    def __init__(self, total_de_blocos=1024, reservado_para_rt=64):
        self.total_de_blocos = total_de_blocos  # Total de blocos na memória
        self.reservado_para_rt = reservado_para_rt  # Blocos reservados para processos de tempo real

        self.inicio_user_blocks = reservado_para_rt  # Índice de início da região de usuário
        self.memoria = [None] * self.total_de_blocos  # Lista de memória: None = livre, ID = ocupado

        # Tabela de controle: associa id ao offset e num_blocos
        self.tabela_alocacoes = {}

    def allocate(self, id: int, num_blocos: int, tempo_real: bool) -> int:
        """
        Tenta alocar um segmento contíguo de memória para o processo.
        """
        if num_blocos > (self.total_de_blocos - self.reservado_para_rt) and not tempo_real:
            return -2 # Mata o processo de usuáro por n possuir memória

        if num_blocos > self.total_de_blocos and tempo_real:
            return -2# Mata o processo de tempo real por n possuir memória
            
        # Delimita região de busca dependendo do tipo de processo
        inicio = 0 if tempo_real else self.inicio_user_blocks
        final = self.total_de_blocos

        for i in range(inicio, final - num_blocos + 1):
            segmento_livre = all(self.memoria[j] is None for j in range(i, i + num_blocos)) # Busca segmento livre
            if segmento_livre:
                for j in range(i, i + num_blocos):
                    self.memoria[j] = id  # Marca os blocos como ocupados (aloca)
                self.tabela_alocacoes[id] = (i, num_blocos)  # Salva inicio e tamanho para gerenciamento depois
                return i  # Retorna o offset da alocação

        return -1  # Não foi possível alocar os blocos na memória

    def release(self, id: int) -> None:
        """
        Libera todos os blocos de memória ocupados pelo processo com determinado id.
        """
        if id in self.tabela_alocacoes:
            offset, num_blocos = self.tabela_alocacoes[id] #infos de um id
            for i in range(offset, offset + num_blocos):
                self.memoria[i] = None  # Libera os blocos
            del self.tabela_alocacoes[id]  # Remove o registro do processo
