# Módulo responsável pelas filas e escalonamento dos processos

from collections import deque

# Fila de tempo real (prioridade 0) - FIFO, sem preempção
fila_tempo_real = deque(maxlen=1000)

# Filas de usuário (prioridades 1, 2, 3) - com realimentação e aging
fila_usuario_1 = deque(maxlen=1000)  # prioridade 1 (mais alta entre usuários)
fila_usuario_2 = deque(maxlen=1000)  # prioridade 2
fila_usuario_3 = deque(maxlen=1000)  # prioridade 3 (mais baixa)

# Fila global para avaliação inicial (opcional)
fila_global = deque(maxlen=1000)

QUANTUM = 1  # Quantum de 1ms para processos de usuário

# Adiciona processo a fila conforme prioridade
def adicionar_processo(processo):
    if processo.prioridade == 0:
        fila_tempo_real.append(processo)
    elif processo.prioridade == 1:
        fila_usuario_1.append(processo)
    elif processo.prioridade == 2:
        fila_usuario_2.append(processo)
    elif processo.prioridade == 3:
        fila_usuario_3.append(processo)
    else:
        raise ValueError("Prioridade inválida para processo.")

# Retorna o próximo processo a ser executado, seguindo as prioridades
def obter_proximo_processo():
    if fila_tempo_real:
        return fila_tempo_real.popleft()
    elif fila_usuario_1:
        return fila_usuario_1.popleft()
    elif fila_usuario_2:
        return fila_usuario_2.popleft()
    elif fila_usuario_3:
        return fila_usuario_3.popleft()
    else:
        return None

# Rebaixa o processo para a próxima fila de menor prioridade
def realimentar_processo(processo):
    if processo.prioridade == 1:
        processo.prioridade = 2
        fila_usuario_2.append(processo)
    elif processo.prioridade == 2:
        processo.prioridade = 3
        fila_usuario_3.append(processo)
    elif processo.prioridade == 3:
        fila_usuario_3.append(processo) #permanece na última fila
    else:
        pass  # tempo real não é realimentado
