from processo import Processo
from escalonador import fila_global, adicionar_processo, obter_proximo_processo, realimentar_processo
# from gerencia_memoria import alocar_memoria, liberar_memoria
# from gerenciador_de_recursos import alocar_recursos, liberar_recursos

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
        # print para debugar
        print(f"Processo {processo.pid} adicionado à fila global.")

def avaliar_e_despachar():
    """Avalia processos na fila_global e despacha para a fila correta se possível."""
    processos_aprovados = []
    for processo in list(fila_global):  # Cria uma cópia para iterar
        if alocar_memoria(processo) and alocar_recursos(processo):
            fila_global.remove(processo)
            adicionar_processo(processo)
            print(f"Processo {processo.pid} despachado para fila de prioridade {processo.prioridade}.")
            processos_aprovados.append(processo)
        # Se não conseguir alocar, permanece na fila_global
    return processos_aprovados

def ciclo_execucao():
    while True:
        avaliar_e_despachar()
        processo = obter_proximo_processo()
        if not processo:
            if not fila_global:
                break  # Fim da simulação
            continue  # Tenta despachar de novo
        # Executa 1 quantum
        processo.tempo_restante -= 1
        print(f"Executando processo {processo.pid} (restante: {processo.tempo_restante})")
        if processo.tempo_restante <= 0:
            liberar_memoria(processo)
            liberar_recursos(processo)
            print(f"Processo {processo.pid} finalizado.")
        else:
            if processo.prioridade > 0:
                realimentar_processo(processo)
            else:
                adicionar_processo(processo)  # Tempo real volta para sua fila

if __name__ == "__main__":
    processos = ler_processos_arquivo("processes.txt")
    print("Processos lidos do arquivo:")
    for p in processos:
        print(f"PID: {p.pid}, Tempo Inicialização: {p.tempo_inicializacao}, Prioridade: {p.prioridade}")

    despachar_processos(processos)
    print("\nConteúdo da fila_global após despacho:")
    for p in fila_global:
        print(f"PID: {p.pid}, Prioridade: {p.prioridade}")

    # Avalia e despacha para as filas corretas
    avaliar_e_despachar()
    print("\nConteúdo das filas após avaliação:")

    from escalonador import fila_tempo_real, fila_usuario_1, fila_usuario_2, fila_usuario_3

    print("Tempo real:", [p.pid for p in fila_tempo_real])
    print("Usuário 1:", [p.pid for p in fila_usuario_1])
    print("Usuário 2:", [p.pid for p in fila_usuario_2])
    print("Usuário 3:", [p.pid for p in fila_usuario_3])

    # Chama o ciclo de execução para simular o SO
    print("\nIniciando ciclo de execução...\n")
    ciclo_execucao()