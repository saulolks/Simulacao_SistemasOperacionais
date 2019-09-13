'''
Author: Saulo Lucas Ferreira
'''

import threading
import time

var = 2
alive = [False]*5
turn = 1

def job1(message):
    while True:
        global turn
        while turn != 1:
            print('wait 1 ', end='')
            time.sleep(0.2)
        print(f'\n\n======\t\tregião crítica\t\t======\t\t{message}\n')
        time.sleep(1)
        #var += 1
        turn = 2
        print(f'\n\n======\t\tfinishing var: {var}\t\t======\t\t{message}\n')

def job2(message):
    while True:
        global turn
        while turn != 2:
            print('wait 2 ', end='')
            time.sleep(0.2)
        print(f'\n\n======\t\tregião crítica\t\t======\t\t{message}\n')
        #var -= 1
        time.sleep(1)
        turn = 3
        print(f'\n\n======\t\tfinishing var: {var}\t\t======\t\t{message}\n')

def job3(message):
    while True:
        global turn
        while turn != 3:
            print('wait 3 ', end='')
            time.sleep(0.2)
        print(f'\n\n======\t\tregião críticag\t\t======\t\t{message}\n')
        #var += 1
        time.sleep(1)
        turn = 4
        print(f'\n\n======\t\tfinishing var: {var}\t\t======\t\t{message}\n')

def job4(message):
    while True:
        global turn
        while turn != 4:
            print('wait 4 ', end='')
            time.sleep(0.2)
        print(f'\n\n======\t\tregião crítica\t\t======\t\t{message}\n')
        #var -= 1
        time.sleep(1)
        turn = 5
        print(f'\n\n======\t\tfinishing var: {var}\t\t======\t\t{message}\n')

def job5(message):
    while True:
        global turn
        while turn != 5:
            print('wait 5 ', end='')
            time.sleep(0.2)
        print(f'\n\n======\t\tregião crítica\t\t======\t\t{message}\n')
        #var += 1
        time.sleep(1)
        turn = 1
        print(f'\n\n======\t\tsaindo var: {var}\t\t======\t\t{message}\n')

t1 = threading.Thread(target=job1, args=('job 1',))
t2 = threading.Thread(target=job2, args=('job 2',))
t3 = threading.Thread(target=job3, args=('job 3',))
t4 = threading.Thread(target=job4, args=('job 4',))
t5 = threading.Thread(target=job5, args=('job 5',))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()