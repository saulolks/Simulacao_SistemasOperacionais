from helpers.i_node import I_node
from helpers.disco import Disco
from datetime import datetime


class OS:
    def __init__(self, disc_size, qtd_disc):
        self.root = {'r': {}}
        self.current = self.root['r']
        self.wayback = "/r/"
        self.index_wayback = [0]
        self.disc = Disco(disc_size, qtd_disc)
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
                        print("Arquivos não podem ser acessados pelo comando"
                              " 'cd'.")
                        break
                    else:
                        self.current = self.current[item]
                        self.pointer = self.disc.find_node(item,
                                                           self.pointer)
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
                self.disc.add_file(self.pointer, inode)
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
            if self.disc.deallocate(self.pointer, node):
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
            self.disc.add_file(self.pointer, file)
            self.current[node] = True
        except MemoryError:
            print("Memória cheia!")
        except Exception as ex:
            print(ex)

    def info(self, node=None):
        if node:
            index = self.disc.find_node(node, self.pointer)
            text = f"""
        name: {self.disc.discos[0][index].name}
        created: {self.disc.discos[0][index].date}
        head: {self.disc.discos[0][index].head}
        indexes: {self.disc.discos[0][index].indexes}
            """
        else:
            text = f"""
        wayback: {self.wayback}
        indexes: {self.index_wayback}
        root: {self.root}
        current: {self.current}
        allocation: {self.disc.discos[0]}
            """
        return text

    def currinfo(self):
        text = f"""
        name: {self.disc.discos[0][self.pointer].name}
        created: {self.disc.discos[0][self.pointer].date}
        head: {self.disc.discos[0][self.pointer].head}
        indexes: {self.disc.discos[0][self.pointer].indexes}
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
