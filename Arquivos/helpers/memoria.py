from helpers.i_node import I_node


class Memoria:
    def __init__(self, size):
        self.data = [False]*size
        self.size = size

        self.data[0] = I_node(None, 'r', 1, node_type='dir')

    """
        Verificará primeiramente se a memória (mesmo com fragmentação)
        conseguirá armazenar o `file`. Caso tenha espaço disponível, será
        realizado o `alocate`.
    """
    def add_file(self, index, file):
        if self.check_storage(file.size):
            self.allocate(file)
            return True
        return False

    def check_storage(self, filesize):
        if self.data.count(False) >= filesize:
            return True
        return False

    """
        Recebendo um `file` que pode ser um diretório ou arquivo, será
        realizado a alocação desse `file` na memória.

        Percorre-se todas as posições de memória em busca da primeira posição
        livre. Quando acha-se ela, é inserido uma parte do `file` nesa posição.

        Continuará percorrendo a memória, ate que todo o conteúdo do `file`
        tenha sido alocado na memória.

        As posições da memória que estão armazenando o `file`, serão salvas no
        vetor `file.indexes`.
    """
    def allocate(self, file):
        primary_alocate = False

        for i, value in enumerate(self.data):
            if not value:
                if not primary_alocate:
                    self.data[i] = file
                else:
                    self.data[i] = True

                file.indexes.append(i)
                if len(file.indexes) >= file.size:
                    break

    def deallocate(self, index, file):
        pass

    def find_node(self, node):
        for i, file in enumerate(self.data):
            if type(file) != bool and file.name == node:
                return i
        raise KeyError
