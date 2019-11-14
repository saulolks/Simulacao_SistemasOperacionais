import time
import threading
import random


class Disk:
    def __init__(self, size):
        self.cylinder = [i*random.randint(1,100) for i in range(size)]
        self.pointer = 0
        self.direction = True
        self.row = []
        self.found = [0] * size
        self.size = size

    def find(self, item):
        self.row.append(item)
        while not self.found[item]:
            time.sleep(4.5)
        aux = self.found[item]
        self.found[item] = 0
        return aux

    def run(self):
        print(" Rodando")
        while True:
            if self.row:
                try:
                    self.search2()
                except Exception as ex:
                    print(ex)
                time.sleep(2.5)
    
    def search(self):
        if self.direction:
            for i in range(self.pointer, self.size):
                if i in self.row:
                    self.found[i] = self.cylinder[i]
                    self.row.remove(i)
                self.direction = False if i+1 == self.size else True
        else:
            for i in range(self.size, self.pointer, -1):
                if i in self.row:
                    self.found[i] = self.cylinder[i]
                    self.row.remove(i)
                self.direction = True if i-1 == 0 else False
    
    def find_higher(self):
        self.row.sort(reverse=False)
        for index in self.row:
            if index >= self.pointer:
                return index
    
    def find_lower(self):
        self.row.sort(reverse=True)
        for index in self.row:
            if index <= self.pointer:
                return index
        return None

    def search2(self):
        print("     ",self.row)
        print(f"    Braço em {self.pointer}")
        if self.pointer in self.row:
            self.found[self.pointer] = self.cylinder[self.pointer]
            self.row.remove(self.pointer)
            if self.direction:
                print(f"    Cilindro {self.pointer} encontrado. Braço se deslocando para a direita...")
            else:
                print(f"    Cilindro {self.pointer} encontrado. Braço se deslocando para a esquerda...")
        if self.direction:
            index = self.find_higher()
            if index:
                self.pointer = index
                self.found[index] = self.cylinder[index]
                self.row.remove(index)
                print(f"    Cilindro {index} encontrado. Braço se deslocando para a direita...")
            else:
                self.direction = False
                print(f"    Braço em {self.pointer}. Nada encontrado. Braço se deslocando para esquerda...")
        else:
            index = self.find_lower()
            if index:
                self.pointer = index
                self.found[index] = self.cylinder[index]
                self.row.remove(index)
                print(f"    Cilindro {index} encontrado. Braço se deslocando para a esquerda...")
            else:
                self.direction = True
                print(f"    Braço em {self.pointer}. Nada encontrado. Braço se deslocando para direita...")

def finding(disk):
    index = random.randint(0, 9)
    print(f"\n======Buscando cilindro {index}======\n")
    item = disk.find(index)
    print(f"\n======Item {item} obtido do cilindro {index}======\n")

if __name__ == "__main__":
    disk = Disk(size=10)
    main_thread = threading.Thread(target=disk.run, args=())
    main_thread.start()
    while True:
        threading.Thread(target=finding, args=(disk,)).start()
        time.sleep(2.0)