from processo import Processo
from escalonador import fila_global, adicionar_processo, obter_proximo_processo, realimentar_processo, mostrar_status_filas
from gerencia_memoria import GerenciadorDeMemoria
from gerenciador_de_recursos import tentar_alocacoes, liberar_recursos as liberar_recursos_modulo
from gerenciador_de_arquivos import ler_entrada_memoria, disc_space
import gerenciador_de_arquivos

# Instancie o gerenciador de memória uma vez
memoria = GerenciadorDeMemoria()

# Lê o arquivo de processos e cria instâncias de Processo.
def ler_processos_arquivo(caminho):
    processos = []
    with open(caminho, 'r') as f:
        for idx, linha in enumerate(f):
            if linha.strip() == "" or linha.startswith("#"):
                continue  # Ignora linhas vazias ou comentários
            campos = linha.strip().split(',')
            tempo_inicializacao = int(campos[0])
            prioridade = int(campos[1])
            tempo_cpu = int(campos[2])
            blocos_memoria = int(campos[3])
            impressora = int(campos[4])
            scanner = int(campos[5])
            modem = int(campos[6])
            disco = int(campos[7])
            pid = idx  # Ou use outro método para gerar PID único
            processo = Processo(pid, tempo_inicializacao, prioridade, tempo_cpu, blocos_memoria, impressora, scanner, modem, disco)
            processos.append(processo)
    return processos

# Adiciona todos os processos lidos na fila global para avaliação inicial.
def despachar_processos(processos):
    for processo in processos:
        fila_global.append(processo)

def avaliar_e_despachar():
    """Avalia processos na fila_global e despacha para a fila correta se possível."""
    processos_aprovados = []
    for processo in list(fila_global):  # Cria uma cópia para iterar
        if alocar_memoria(processo) and alocar_recursos(processo):
            fila_global.remove(processo)
            adicionar_processo(processo)
            # print(f"Processo {processo.pid} despachado para fila de prioridade {processo.prioridade}.")
            processos_aprovados.append(processo)
        # Se não conseguir alocar, permanece na fila_global
    return processos_aprovados

def ciclo_execucao():
    processos_em_execucao = {}  # Para controlar instrução atual de cada processo

    while True:
        avaliar_e_despachar()
        processo = obter_proximo_processo()
        if not processo:
            if not fila_global:
                break  # Fim da simulação
            continue  # Tenta despachar de novo

        # Se for a primeira vez do processo, imprime o dispatcher e o cabeçalho
        if processo.pid not in processos_em_execucao:
            processo.exibir_info()
            print()  # Linha em branco entre dispatcher e process
            print(f"process {processo.pid} =>")
            print(f"P{processo.pid} STARTED")
            processos_em_execucao[processo.pid] = 1  # Instrução atual

        instrucao_atual = processos_em_execucao[processo.pid]
        print(f"P{processo.pid} instruction {instrucao_atual}")

        processo.tempo_restante -= 1
        processos_em_execucao[processo.pid] += 1

        if processo.tempo_restante <= 0:
            print(f"P{processo.pid} return SIGINT")
            print()
            liberar_memoria(processo)
            liberar_recursos(processo)
            # print(f"Processo {processo.pid} finalizado.\n")
            processos_em_execucao.pop(processo.pid)
        else:
            # Se não terminou, volta para a fila correta
            if processo.prioridade > 0:
                realimentar_processo(processo)
            else:
                adicionar_processo(processo)  # Tempo real volta para sua fila

def alocar_memoria(processo):
    offset = memoria.allocate(processo.pid, processo.blocos_memoria, processo.prioridade == 0)
    if offset != -1:
        processo.offset_memoria = offset
        return True
    return False

def liberar_memoria(processo):
    memoria.release(processo.pid)

def alocar_recursos(processo):
    # tentar_alocacoes retorna 0 se conseguiu, 1 se bloqueou, 2 se erro
    return tentar_alocacoes(processo) == 0

def liberar_recursos(processo):
    liberar_recursos_modulo(processo.pid)

if __name__ == "__main__":
    # Lê os processos do arquivo e exibe suas informações
    processos = ler_processos_arquivo("processes.txt")
    
    processos_dict = {p.pid: p for p in processos}

    # Adiciona todos os processos lidos na fila global para avaliação inicial.
    despachar_processos(processos)

    # Avalia e despacha para as filas corretas
    avaliar_e_despachar()

    # Exibe o conteúdo da fila_global após o despacho
    # mostrar_status_filas()

    # Chama o ciclo de execução para simular o SO
    # print("\nIniciando ciclo de execução...\n")
    ciclo_execucao()

    # Aqui temos que fazer a chamada de funções para verificar a lista de processos bloquados
    # Chama sistema de arquivos para mostrar seu uso (essas funções estão em gerencia_de_recursos.py)
    # Chama de memória para mostrar seu uso
    print("Sistema de arquivos =>")
    processos_dict = {p.pid: p for p in processos}
    gerenciador_de_arquivos.processos = processos_dict  # Passa os processos no dicionario

    ler_entrada_memoria('files.txt')

    print("Mapa de ocupação do disco:")
    print(' '.join(str(b) for b in disc_space if b != 0))