

scanner = [-1]   # Todo recurso é tratado como array para padronizr, mesmo se 2 só tem 1 unidade
modem = [-1]
impressora = [-1,-1] 
sata = [-1,-1]

def alocar_recurso(processo_id,recurso,codigo):
    # retorna sucesso (0) se obteu o recurso, valor diferente caso contrário
    # recurso = 0 é scanner, = 1 é modem, = 2 impressoras = 3 sata
    # código - 1 (porque 0 no arquivo indica que não usará o recurso) é o índice no array, se está fora dos limites é um erro

    id = codigo - 1
    if recurso == 0:
        if codigo != 1:
            return 2 # número do dispositivo invalido
        
        if scanner[id] == -1:
            scanner[id] = processo_id
        else:
            return 3 # Dipositivo ocupado
    elif recurso == 1:
        if codigo != 1:
            return 2 # número do dispositivo invalido
        
        if modem[id] == -1:
            modem[id] = processo_id
        else:
            return 3 # Dipositivo ocupado
    elif recurso == 2:
        if codigo != 1 and codigo != 2:
            return 2 # número do dispositivo invalido
        
        if impressora[id] == -1:
            impressora[id] = processo_id
        else:
            return 3 # Dipositivo ocupado
    elif recurso == 3:
        if codigo != 1 and codigo != 2:
            return 2 # número do dispositivo invalido
        
        if sata[id] == -1:
            sata[id] = processo_id
        else:
            return 3 # Dipositivo ocupado
    else:
        return 1    # Erro de código de recurso indisónível
    
def desalocar_recurso(recurso,codigo):
    # retorna sucesso (0) se obteu o recurso, valor diferente caso contrário
    # recurso = 0 é scanner, = 1 é modem, = 2 impressoras = 3 sata
    # código - 1 é o índice no array, se está fora dos limites é um erro

    id = codigo - 1
    if recurso == 0:
        if codigo != 1:
            return 2 # número do dispositivo invalido
        
        if scanner[id] != -1:
            scanner[id] = -1
        else:
            return 3 # Dipositivo já está livre 
    elif recurso == 1:
        if codigo != 1:
            return 2 # número do dispositivo invalido
        
        if modem[id] != -1:
            modem[id] = -1
        else:
            return 3 # Dipositivo já está livre 
    elif recurso == 2:
        if codigo != 1 and codigo != 2:
            return 2 # número do dispositivo invalido
        
        if impressora[id] != -1:
            impressora[id] = -1
        else:
            return 3 # Dipositivo já está livre 
    elif recurso == 3:
        if codigo != 1 and codigo != 2:
            return 2 # número do dispositivo invalido
        
        if sata[id] != -1:
            sata[id] = -1
        else:
            return 3 # Dipositivo já está livre 
    else:
        return 1    # Erro de código de recurso indisónível
    
alocar_recurso(0,0,1)
alocar_recurso(2,3,2)

print(scanner)
print(modem)
print(impressora)
print(sata)