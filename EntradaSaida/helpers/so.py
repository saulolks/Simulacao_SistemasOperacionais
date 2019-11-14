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
            nodes = self.wayback.split('/')[1:-2]
            new_wayback = "/"

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
                    if type(self.current[item]) is bool:
                        print("Arquivos não podem ser acessados pelo comando 'cd'.")
                        break
                    else:
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
    
    def touch(self, node, size):
        if size.isdigit:
            size = int(size)
        else:
            print("O tamanho do arquivo deve ser um inteiro.")
            return
        
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        file = I_node(date=date, name=node, size=size, node_type="file")
        try:
            self.memory.add_file(self.pointer, file)
            self.current[node] = True
        except MemoryError:
            print("Memória cheia!")
        except Exception as ex:
            print(ex)

    def info(self, node=None):
        if node:
            index = self.memory.find_node(node, self.pointer)
            text = f"""
        name: {self.memory.disk[index].name}
        created: {self.memory.disk[index].date}
        head: {self.memory.disk[index].head}
        indexes: {self.memory.disk[index].indexes}
            """
        else:
            text = f"""
        wayback: {self.wayback}
        indexes: {self.index_wayback}
        root: {self.root}
        current: {self.current}
        main disk 1: {self.memory.disk}
        alt disk 2: {self.memory.disk2}
        alt disk 3: {self.memory.disk3}
            """
        return text
    
    def currinfo(self):
        text = f"""
        name: {self.memory.disk[self.pointer].name}
        created: {self.memory.disk[self.pointer].date}
        head: {self.memory.disk[self.pointer].head}
        indexes: {self.memory.disk[self.pointer].indexes}
        """
        return text
    
    def help(self):
        text = """
        'cd sample':    navega ao diretorio 'sample'
        'ls':           lista todos os itens contidos no diretorio corrente
        'mkdir sample': cria o diretorio 'sample' dentro no diretorio corrente
        'rm sample':    remove o diretorio 'sample' e todos os seus itens
        'currinfo':     mostra os detalhes do diretorio corrente
        'info':         mostra os detalhes gerais do sistema
        'info sample':  mostra os detalhes do diretorio 'sample'
        """
        return text
