from helpers.i_node import I_node


class Memoria:
    def __init__(self, size):
        self.data = [False]*size
        self.size = size
        self.trash = []  # Lista de indices que ainda precisam ser removidos
        self.data[0] = I_node(None, 'r', 1, node_type='dir')

    """
        Verificará primeiramente se a memória (mesmo com fragmentação)
        conseguirá armazenar o `file`. Caso tenha espaço disponível, será
        realizado o `alocate`.
    """
    def add_file(self, index, file):
        if self._check_storage(file.size):
            if self.find_node(file.name) is not None:
                raise KeyError
            self.allocate(file)
            """
                Adiciona ao diretório raiz o primeiro indíce que o
                arquivo/diretório novo está localizado.
            """
            self.data[index].indexes.append(file.indexes[0])
        else:
            raise MemoryError

    def _check_storage(self, filesize):
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
        node = self.data[index]
        find = False

        for i in node.indexes:
            _file = self.data[i]
            if _file.name == file:
                find = True
                self._clean_memory(_file.indexes)
                break

        while len(self.trash) != 0:
            if i in self.trash:
                self.data[i] = False
                self.trash.remove(i)
            self._clean_trash()

        return find

    """
        Inverte a ordem dos indices, para pegar o ultimo inserido e apartir
        dele verificar ir removendo da memória, dado que o primeiro indice é
        o nó inicial.
    """
    def _clean_memory(self, indexes):
        indexes.reverse()

        for i in indexes:
            _node = self.data[i]

            """
                Caso esse node tenha mais de um indice em sua lista de
                indices, ele então tem sub pastas ou sub arquivos que
                precisam também ser removidos. Esses indices serão
                inseridos ao `trash`, que será percorrido em outro momento.
            """
            if len(_node.indexes) > 1:
                self.trash.append(i)
            elif type(self.data[i]) is not bool:
                self.data[i] = False

    def _clean_trash(self):
        for i in self.trash:
            _node_indexes = self.data[i].indexes
            _node_indexes.remove(i)
            self._clean_memory(_node_indexes)
            self.data[i] = False
            self.trash.remove(i)

    def find_node(self, node):
        for i, file in enumerate(self.data):
            if type(file) != bool and file.name == node:
                return i
        return None
