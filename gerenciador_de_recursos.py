from processo import Processo

scanner = [-1]   # Todo recurso é tratado como array para padronizr, mesmo se 2 só tem 1 unidade
modem = [-1]
impressora = [-1,-1] 
sata = [-1,-1]

recursos = [scanner,modem,impressora,sata]


scanwait = [[]]
modemwait = [[]]
imprwait = [[],[]]
satawait = [[],[]]

waitlist = [scanwait,modemwait,imprwait,satawait]   # Lista  global que inclui todas as filas de espera por conveniência
processwait = {}    # Dicioinário com chave = id do processo e valor igual a um Blocking do. Um blocking é removido quando um processo se encerra por completo

class Blocking: # Classe usada para guardar informações dos recursos que o processo usa
    def __init__(self,blocklist):
        self.waiting = 0  # número de recursos que o bloqueiam, o máximo será len(blocklist)
        self.bloqueios = blocklist # Lista dos recursos que bloqueiam tuplas (tipo de recurso, código do recurso), utilizado para saber de que filas tirar e em que filas colocar

def processo_espera(pid):
    if pid in processwait.keys():
        return 1
    else:
        return 0
    
def processo_pronto(pid):   # Confere se o processo está pronto para entrar na fila
    if processwait[pid].waiting == 0:
        return 0
    else:
        return 1
    
def tentar_alocacoes(processo):
    # Usado após a criação do processo para tentar fazer suas alocações
    blocklist = []
    if processo.scanner > 0:
        blocklist.append((0,processo.scanner - 1))
    if processo.modem > 0:
        blocklist.append((1,processo.modem - 1))
    if processo.impressora > 0:
        blocklist.append((2,processo.impressora - 1))
    if processo.disco > 0:
        blocklist.append((3,processo.disco - 1))
    blocking = Blocking(blocklist)  # Criando um objeto blocking
    waitnum = 0 
    for bloqueio in blocklist:
        reclivre = checar_recurso(bloqueio[0],bloqueio[1])  # Checa se esse recurso está livre
        waitlist[bloqueio[0]][bloqueio[1]].append(processo.pid)  # Coloca o processo na lista de espera
        if reclivre == 1:
            waitnum += 1
        elif reclivre > 1:
            return 2    # Indica que o recurso não existe e o processo deve ser destruído
    if waitnum ==  0:
        for bloqueio in blocking.bloqueios:
            waitlist[bloqueio[0]][bloqueio[1]].remove(processo.pid)
        processwait[processo.pid] = blocking # colocando o blocking no dicionário de processos bloqueados
        aloca_avisa_recursos(processo.pid)
        return 0    # indica que o processo está pronto
    else:
        blocking.waiting = waitnum
        processwait[processo.pid] = blocking # colocando o blocking no dicionário de processos bloqueados
        return 1    # Indica que o processo foi adicionado na fila de bloqueio e não está pronto

def liberar_recursos(processo_id):
    # Função chamada quando um processo se encerra por completo
    # Retorna lista de ids dos processos prontos para serem escalonados
    
    rec_proc = processwait[processo_id] # Pegando a lista dos recursos bloqueantes
    processwait.pop(processo_id) # removendo desse dicionário, pois será retornado
    for recurso in rec_proc.bloqueios:
        chk = desalocar_recurso(recurso[0],recurso[1]) # Remove uso de recurso
        if chk == 1:
            print("ERRO: Tentou liberar recurso já liberto")
        elif chk == 2:
            print("ERRO: Tentou liberar recurso inexistente")
        informar_liberacao(recurso[0],recurso[1]) # Informa os outros processos que o recurso foi liberado, reduzindo seus valores de espera

    return conferir_alocacao(rec_proc.bloqueios)

def conferir_alocacao(bloqueio):    
    # Dada uma lista de recursos liberados (dada por liberear_recuros), checa se isso permite que um proesso seja desbloqueado
    proc_prontos = []   # Lista de processos liberadis para irem para a lista de prontos
    for recurso in bloqueio:
        for proc in waitlist[recurso[0]][recurso[1]]:
            pwait = processwait[proc]
            if pwait.waiting == 0:
                for bloqueio in pwait.bloqueios:
                    waitlist[bloqueio[0]][bloqueio[1]].remove(proc) # Removendo o processo das filas de espera
                aloca_avisa_recursos(proc) # Aloca o recurso para esse processo
                proc_prontos.append(proc)
                break
    return proc_prontos

def informar_liberacao(recurso,codigo):  # Reduz o contador de esperando de todo processo que espera por esse recurso
    for id in waitlist[recurso][codigo]:
        processwait[id].waiting -= 1    # Reduz o valor de esperando

def informar_alocacao(recurso,codigo):  # Aumenta o contador de esperando de todo processo que espera por esse recurso
    for id in waitlist[recurso][codigo]:
        processwait[id].waiting += 1    # Aumenta o valor de esperando
    
def aloca_avisa_recursos(pid):
    # Essa função aloca recursos a um processo e avisa aos outros que esperam por esse recurso que ele foi tomado

    bloqueios = processwait[pid].bloqueios
    for bloqueio in bloqueios:
        
        chk = alocar_recurso(pid,bloqueio[0],bloqueio[1])  # Alocando recursos para esse processo
        if chk == 1:
            print("ERRO: Tentou alocar recurso já alocado")
        elif chk == 2:
            print("ERRO: Tentou alocar recurso inexistente")
        else:
            informar_alocacao(bloqueio[0],bloqueio[1]) # Informa outros processos esperando por esse recurso que ele foi tomado

def checar_recurso(recurso,codigo): 
    return alocar_recurso(-1,recurso,codigo)

def alocar_recurso(processo_id,recurso,codigo):
    # retorna sucesso (0) se obteu o recurso, valor diferente caso contrário
    # recurso = 0 é scanner, = 1 é modem, = 2 impressoras = 3 sata

    if recurso >= 0 and recurso < 4:
        try:
            if recursos[recurso][codigo] == -1:
                recursos[recurso][codigo] = processo_id
                return 0
            else:
                return 1 # Erro recurso indisponível
        except:
            return 2    # Erro de código de recurso ou código desconhecido
    else:
        return 2    # Erro de código de recurso ou código desconhecido
    
def desalocar_recurso(recurso,codigo):
    # retorna sucesso (0) se obteu o recurso, valor diferente caso contrário
    # recurso = 0 é scanner, = 1 é modem, = 2 impressoras = 3 sata

    if recurso >= 0 and recurso < 4:
        try:
            if recursos[recurso][codigo] != -1:
                recursos[recurso][codigo] = -1
                return 0
            else:
                return 1 # Erro recurso já livre
        except:
            return 2    # Erro de código de recurso ou código desconhecido
    else:
        return 2    # Erro de código de recurso ou código desconhecido
    

"""
#  impressora, scanner, modem, disco
pro0 = Processo(0,0,1,1,1,1,0,0,0)
pro1 = Processo(1,0,1,1,1,0,1,0,2)
pro2 = Processo(2,0,1,1,1,0,1,1,1)
pro3 = Processo(3,0,1,1,1,2,0,0,1)

print(tentar_alocacoes(pro0))
print(tentar_alocacoes(pro1))
print(tentar_alocacoes(pro2))
print(tentar_alocacoes(pro3))

print(waitlist)

for pro in [pro1,pro2,pro3]:
    if processwait[pro.pid].waiting == 0:
        print("Processos prontos:",liberar_recursos(pro.pid))

print("Waitlist:",waitlist)

print("Scanner:",scanner)
print("Modem:",modem)
print("Impressoras:",impressora)
print("SATAS:",sata)"""
