'''
Author: Saulo Lucas Ferreira
'''

import threading
import random
import time

buffer = [100, 350, 10, 6, 8, 18, 56, 72]
MAX = 10
sp = False
sc = False

def sleep_produtor():
    global sp
    sp = True
    # print("produtor dormiu")
    while sp:
        pass
    # print("produtor acordou")

def sleep_consumer():
    global sc
    sc = True
    # print("consumidor dormiu")
    while sc:
        pass
    # print("consumidor acordou")

def print_buffer():
    global buffer
    global sc
    global sp
    while True:
        print(f"\n=========== BUFFER | tamanho: {len(buffer)} | cons: {sc} | prod: {sp} ===========\n{buffer}\n=========================================\n")
        time.sleep(1)

def produtor(nome):
    global sc
    choice = [True, False]
    flag = random.choice(choice)

    while True and not sp:
        flag = random.choice(choice)
        time.sleep(1)
        item = random.randint(0,1000)
        
        if len(buffer) == MAX:
            print("Produtor dormindo........")
            sleep_produtor()

        # print(f"Produtor {nome} vai produzir? {flag}")
        
        if flag:
            print(f"Processo {nome} produzindo...")
            buffer.append(item)
        
        if len(buffer) == 1:  
            print("Consumidor acordando.....")
            sc = False

def consumidor(nome):
    global sp
    choice = [True, False]
    while True and not sc:
        time.sleep(1)
        flag = random.choice(choice)
        
        if len(buffer) == 0:
            print(f"Consumidor {nome} dormindo......")
            sleep_consumer()
        
        # print(f"Consumidor {nome} vai consumir? {flag}")
        if flag:
            print(f"Processo {nome} consumindo...")
            item = buffer.pop()
        
        if len(buffer) == MAX-1:
            print("Produtor acordando.......")
            sp = False
        
prod1 = threading.Thread(target=produtor, args=("1",))
prod2 = threading.Thread(target=produtor, args=("2",))
cons1 = threading.Thread(target=consumidor, args=("3",))
cons2 = threading.Thread(target=consumidor, args=("4",))
# cons3 = threading.Thread(target=consumidor, args=("5",))
buf = threading.Thread(target=print_buffer, args=())

prod1.start()
prod2.start()
cons1.start()
cons2.start()
# cons3.start()
buf.start()