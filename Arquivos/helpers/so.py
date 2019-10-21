from helpers.memoria import Memoria
from helpers.i_node import I_node
from datetime import datetime


class OS:
    def __init__(self, memory_size):
        self.root = {'r': {}}
        self.current = self.root['r']
        self.wayback = "/r/"
        self.index_wayback = [0]
        self.memory = Memoria(memory_size)
        self.pointer = 0

    def cd(self, node):
        if node == "..":
            print(self.wayback)
            nodes = self.wayback.split('/')[1:-2]
            new_wayback = "/"
            print(nodes)

            try:
                self.current = self.root

                for item in nodes:
                    new_wayback = new_wayback + str(item) + "/"
                    self.current = self.current[item]

                self.wayback = new_wayback
                self.index_wayback.pop()
                self.pointer = self.index_wayback[-1]
            except KeyError:
                print("O diretório não existe!")
        else:
            nodes = node.split('/')

            try:
                for item in nodes:
                    self.current = self.current[item]
                    self.pointer = self.memory.find_node(item, self.pointer)
                    self.wayback = self.wayback + str(item) + "/"
                    self.index_wayback.append(self.pointer)
            except KeyError:
                print("O diretório não existe!")

        return self.wayback

    def mkdir(self, node):
        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        inode = I_node(date=date, name=node, size=1, node_type="dir")

        if '/' not in node and node not in self.current:
            try:
                self.memory.add_file(self.pointer, inode)
                self.current[node] = {}
            except KeyError:
                print("Informe outro nome, já existe um arquivo ou diretório "
                      "com esse nome no SO")
            except MemoryError:
                print("Não há espaço no sistema para armazenar esse arquivo")
        else:
            print("O nome do diretório é inválido!")

    def ls(self):
        text = ""
        for a in self.current:
            text += a + " "
        print(text)

    def rm(self, node):
        if node in self.current:
            if self.memory.deallocate(self.pointer, node):
                del self.current[node]

    def info(self):
        text = f"""
        wayback: {self.wayback}
        indexes: {self.index_wayback}
        root: {self.root}
        current: {self.current}
        allocation: {self.memory.data}
        """
        return text
    
    def currinfo(self):
        text = f"""
        name: {self.memory.data[self.pointer].name}
        created: {self.memory.data[self.pointer].date}
        head: {self.memory.data[self.pointer].head}
        indexes: {self.memory.data[self.pointer].indexes}
        """
        return text
