'''
Author: Saulo Lucas Ferreira
'''

import threading
import random
import time

n = 10
processos = [None]*n
print(processos)
terminados = [None]*n
start = False
turn = -1

def maior_prioridade(pos):
    for i in range(n):
        if terminados[i] == 0:
            if processos[i].prioridade > processos[pos].prioridade:
                return False
    return True

class Processo:
    
    def __init__(self, prioridade, id):
        self.prioridade = prioridade
        self.vez = False
        self.id = id

        self.thread = threading.Thread(target=self.processo, args=())
        self.thread.start()
    
    def processo(self):
        i = 0
        while i < 100:
            if self.vez:
                i += 1
                time.sleep(0.1)
            else:
                time.sleep(0.1)
        terminados[self.id] = 1
        print(f"Processo {self.id} terminado!\n===========================")

for i in range(n):
    processos[i] = Processo(prioridade=random.randint(1,2), id=i)
    print(f"Processo {i}, prioridade {processos[i].prioridade}.")
    terminados[i] = 0

print("Escalonamento iniciado...")
while True:
    if turn < 0:
        while True:
            vez = random.randint(0,n-1)
            if terminados[vez] != 1 and maior_prioridade(vez):
                turn = vez
                print(f"Processo {vez} iniciado.\nPrioridade: {processos[turn].prioridade}\n===========================")
                processos[turn].vez = True
                break
        time.sleep(5)
    else:
        print(f"Processo {turn} pausado.\nPrioridade: {processos[turn].prioridade}\n===========================")
        processos[turn].vez = False
        while True:
            vez = random.randint(0,n-1)
            if terminados[vez] != 1 and maior_prioridade(vez) and vez != turn:
                turn = vez
                print(f"Processo {vez} iniciado.\nPrioridade: {processos[turn].prioridade}\n===========================")
                processos[turn].vez = True
                break
        time.sleep(5)

    if 0 not in terminados:
        break
print("Escalonamento terminado...")
    
