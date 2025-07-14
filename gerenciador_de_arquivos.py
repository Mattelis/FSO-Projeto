from pathlib import Path
from processo import Processo

disc_space   =  []  # Representa o espaço de memória ocupado
disc_size = 0
arquivos = {}  # Dicionário de identificadores usados
processos = {}  # PLACEHOLDER do dicionário de processos

class Arquivo:
    def __init__(self,nome,endereco,tamanho,criador):
        self.nome = nome    # Identificador do arquivo
        self.endereco = endereco    # Endereço base do arquivo
        self.tamanho = tamanho  # Tamanho do arquivo
        self.criador = criador  # Id do processo criador, -1 indica que foi criado na inicialização

# DEPRECISADO PELO PROCESSO NO MODULO PROCESSO.PY, vamos manter por enquanto em caso de incompatibilidade e teste
# class Processo:     # PLACEHOLDER enquanto o resto do grupo não faz a classe própria
#     def __init__(self,id,prioridade):
#         self.id = id
#         self.prio = prioridade
    

def criar_arquivo(processo,nome,tamanho):
    global disc_size

    if (arquivos.get(nome) != None):    # Checando se identificador já existe
        return 1
    base = 0
    while base < disc_size:
        if disc_space[base] == 0:
            iter = base
            vazio = 1   # Conta o espaço vazio contíguo
            check = 1
            while vazio  < tamanho and check == 1 and iter < disc_size:
                if disc_space[iter] != 0:
                    check = 0
                else:
                    vazio += 1    
                iter += 1
                if iter == disc_size:
                    check = 0
            if check == 1:
                base 
                arquivo = Arquivo(nome,base,tamanho,processo)
                arquivos[nome] = arquivo # Armazenando arquivo na lista

                for bloco in range(tamanho):
                    
                    disc_space[base+bloco] = nome  # Armazenando arquivo no disco
                return 0 # Indicando que colocou corretamente
            else:
                
                base = iter + 1    # Pulando para o próximo endereço não checado
        else:
            
            base += 1
    return 2 # Se chega no fim do loop, retorna que não tem espaço

def deletar_arquivo(processo,nome):
    prioridade = processo.prio
    arquivo = arquivos.get(nome)
    if arquivo == None:
        return 1    # Indica que não existe esse arquivo
    
    if prioridade == 0 or arquivo.criador==processo.id: # Só tem permissão se é prio 0 ou é o criador
        base = arquivo.endereco
        tamanho = arquivo.tamanho
        for bloco  in range(tamanho):
            disc_space[base+bloco] = 0  # liberando os blocos no disco
        arquivos.pop(nome)
        return 0 # Indica sucesso na deleção
    
    else:
        return 2    # indica que não tem permissão de deletar o arquivo

def ler_operacao(entrada):
    linha = entrada.readline()
    if not linha: # Se leu uma linha vazia
        return (10,0)    # Indica que terminou de ler
    else:
        instrucao = linha.replace(',','').split()  # Tenta ler uma próxima linha
        try:
            id = int(instrucao[0])
            operacao = int(instrucao[1])    # Tentando converter para string
            nome = instrucao[2]
        except:
            return (1,linha)    # Indica uma linha formatada incorretamente, seja por não serem ints, ou por ter poucos argumentos no geral
        
        if (operacao == 1):
            if len(instrucao) != 3:
                return (2,linha) # Indica quantidade de argumentos incorreta para a opercao
            processo = processos.get(id) # Pegando o ponteiro para o processo
            if processo == None:
                return (4,(id,operacao,nome)) # Processo inválido
            retorno = deletar_arquivo(processo,nome)
            if retorno == 1:
                return (5,(id,operacao,nome))    # retorna arquivo não existente
            elif retorno == 2:
                return (6,(id,operacao,nome))    # retorna sem permissão
            return (0,(id,operacao,nome))   # Retorna sucesso

        elif (operacao == 0):   # Operação de criar arquivo
            if len(instrucao)!= 4:
                return (2,linha) # Indica quantidade de argumentos incorreta para a opercao
            try:
                tamanho = int(instrucao[3])
            except:
                return (1,linha)    # Indica formatação errada
            
            processo = processos.get(id) # Pegando o ponteiro para o processo
            if processo == None:
                return (4,(id,operacao,nome)) # Processo inválido
            nome = instrucao[2]
            retorno = criar_arquivo(processo,nome,tamanho)

            if retorno == 1:
                return (5,(id,operacao,nome))    # retorna arquivo já existente
            elif retorno == 2:
                return (6,(id,operacao,nome))    # retorna falta de espaço
            return (0,(id,operacao,nome))   # Retorna sucesso
        else:
            return (3,linha)    # Indica uma linha com operacao inválida
    

def ler_entrada_memoria(path):
    base_dir = Path(__file__).parent
    file_path = base_dir / path # Pegando o caminho completo para o arquivo passado

    try:
        entrada_f = open(file_path,'r') 
    except:
        return (1,path)    # Código de caminho inválido nessa operação
    try:
        espaco_de_disco = int(entrada_f.readline())  # Lendo o valor que indica o tamanho de segmentos de disco
        segmentos = int(entrada_f.readline())   # número de segmentos ocupados
    except:
        return (2,0)    # Erro de formatacao do documento
    vazio = 0  # Código de bloco vazio

    global disc_size
    disc_size= espaco_de_disco
    for bloco in range(espaco_de_disco):
        disc_space.append(vazio)    # Estende o espaco de disco até o número de blocos adequado com valor default vazio
    for segmento in range(segmentos):
        try:
            arquivo = entrada_f.readline().replace(',','')
            arq_nome,arq_base,arq_tamanho = arquivo.split()
            arq_base = int(arq_base)
            arq_tamanho = int(arq_tamanho)
            
            if (arquivos.get(arq_nome) != None):
                return (3,arq_nome) # Indica que já tem um arquivo com esse nome
            arquivo = Arquivo(arq_nome,arq_base,arq_tamanho,-1)
            arquivos[arq_nome] = arquivo
            for bloco in range(arq_tamanho):
                disc_space[arq_base+bloco] = arq_nome
        except:
            return (2,0)
    print(disc_space)

    # agora realizando as operações
    incompleta = 1 # Indica se ainda tem valores a ler no documento
    cont_operacao = 0   # Número da Operacao
    while incompleta == 1:
        cont_operacao += 1
        retorno = ler_operacao(entrada_f)
        resultado = retorno[0]
        instrucao = retorno[1]
        
        if resultado == 0:
            print("Operação",cont_operacao,"=> ",end='')
            print("Sucesso")
            nome = instrucao[2]
            if instrucao[1] == 0:
                print("O processo",instrucao[0],"criou o arquivo",nome,"(blocos",end='')
                arquivo = arquivos[nome]
                base = arquivo.endereco
                tamanho = arquivo.tamanho
                for bloco in range(tamanho):
                    print("",base+bloco,end='')
                    if bloco < tamanho -2:
                        print(',',end='')
                    elif bloco < tamanho -1:
                        print(' e',end='')
                    
                print(").")
            else:
                print("O processo",instrucao[0],"deletou o arquivo",nome,".")
        elif resultado == 10:
            incompleta = 0  # Indica que não leu nada
        else:
            print("Operação",cont_operacao,"=> ",end='')
            print("Fracasso")
            if resultado == 1:
                print("Instrução invalida.")
            elif resultado == 2:
                print("Número incorreto de argumentos.")
            elif resultado == 3:
                print("Operação não reconhecida.")
            elif resultado == 4:
                print("O processo",instrucao[0], "não existe.")
            elif resultado == 5:
                if instrucao[1] == 0:
                    print("O processo",instrucao[0],"não pode criar o arquivo", instrucao[2],"(arquivo já existe).")
                else:
                    print("O processo",instrucao[0],"não pode deletar o arquivo", instrucao[2], "(arquivo não existe)")
            elif resultado == 6:
                if instrucao[1] == 0:
                    print("O processo",instrucao[0],"não pode criar o arquivo", instrucao[2],"(falta de espaço).")
                else:
                    print("O processo",instrucao[0],"não pode deletar o arquivo", instrucao[2], "(sem permissão)")
    return (0,0)
    

    

processo = Processo(0,0)
processos[0] = processo
processo = Processo(1,1)
processos[1] = processo
arq_ret = ler_entrada_memoria('arquivo.txt')
print(disc_space)
ret_val = arq_ret[1]
arq_ret = arq_ret[0]
if (arq_ret == 1):
    print("ERRO: Caminho inválido para descritor do sistema de arquivos:",ret_val)
elif (arq_ret == 2):
    print("ERRO: Descritor do sistema de arquivos inválido")
elif (arq_ret == 3):
    print("ERRO: Reuso de identificador de arquivo:",ret_val)