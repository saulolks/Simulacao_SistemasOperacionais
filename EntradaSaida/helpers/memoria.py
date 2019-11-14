from helpers.i_node import I_node


class Memoria:
    def __init__(self, size):
        self.size = size//3
        self.disk = [False] * self.size
        self.trash = []  # Lista de indices que ainda precisam ser removidos
        self.disk[0] = I_node(None, 'r', 1, node_type='dir', head=0)
        self.disk2 = self.disk
        self.disk3 = self.disk

    """
        Verificará primeiramente se a memória (mesmo com fragmentação)
        conseguirá armazenar o `file`. Caso tenha espaço disponível, será
        realizado o `alocate`.
    """
    def add_file(self, index, file):
        if self._check_storage(file.size):
            if self.find_node(file, index) is not None:
                raise KeyError
            self.allocate(file)
            """
                Adiciona ao diretório raiz o primeiro indíce que o
                arquivo/diretório novo está localizado.
            """
            self.disk[index].indexes.append(file.head)
        else:
            raise MemoryError

    def _check_storage(self, filesize):
        if self.disk.count(False) >= filesize:
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

        for i, value in enumerate(self.disk):
            if not value:
                if not primary_alocate:
                    self.disk[i] = file
                    file.head = i
                    primary_alocate = True
                else:
                    self.disk[i] = file.name
                    file.indexes.append(i)

                if len(file.indexes) >= file.size-1:
                    break
    
    # def set_file(self, i):
    
    def deallocate(self, index, file):
        node = self.disk[index]
        find = False

        for i in node.indexes:
            _file = self.disk[i]
            if _file.name == file:
                find = True
                # self._clean_memory(_file.indexes)
                self.delete_in_cascade(_file.indexes)
                self.disk[i] = False
                self.disk[index].indexes.remove(i)
                break
        print(self.trash)
        while len(self.trash) != 0:
            self._clean_trash()
            # if i in self.trash:
            #     self.disk[i] = False
            #     self.trash.remove(i)
            # self._clean_trash()

        return find

    def delete_in_cascade(self, indexes):
        for i in indexes:
            self.trash.append(i)
            if type(self.disk[i]) is not str and self.disk[i].indexes:
                self.delete_in_cascade(self.disk[i].indexes)

    """
        Inverte a ordem dos indices, para pegar o ultimo inserido e apartir
        dele verificar ir removendo da memória, dado que o primeiro indice é
        o nó inicial.
    """
    def _clean_memory(self, indexes):
        indexes.reverse()

        for i in indexes:
            _node = self.disk[i]

            """
                Caso esse node tenha mais de um indice em sua lista de
                indices, ele então tem sub pastas ou sub arquivos que
                precisam também ser removidos. Esses indices serão
                inseridos ao `trash`, que será percorrido em outro momento.
            """
            if len(_node.indexes) > 1:
                self.trash.append(i)
            elif type(self.disk[i]) is not bool:
                self.disk[i] = False

    def _clean_trash(self):
        for i in self.trash:
            # _node_indexes = self.disk[i].indexes
            # _node_indexes.remove(i)
            # self._clean_memory(_node_indexes)
            self.disk[i] = False
            self.trash.remove(i)
            print(self.trash)

    """
        A partir de um `pointer` que conterá o indice do diretório anterior,
        captura o node_root presente nesse ponto e a partir dos indices
        presentes no seu `indexes` procurará o `node` em questão.
    """
    def find_node(self, node, pointer):
        node_root = self.disk[pointer]

        if len(node_root.indexes) > 0:
            for i in node_root.indexes:
                file = self.disk[i]
                if type(file) != bool and file.name == node:
                    return i
        return None
